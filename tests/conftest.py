import pytest
import psycopg2
import psycopg2.extensions
import psycopg2.extras

from datetime import datetime
import subprocess
import logging
import os

g_logger = logging.getLogger(__name__)
g_logger.setLevel(logging.INFO)

TEST_DB_NAME = "test_db"
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"


def connect_db_if_exists(db_name: str):
    try:
        with psycopg2.connect(
            database = db_name,
            user = DB_USERNAME,
            password = DB_PASSWORD,
        ) as conn:
            cur = conn.cursor()
            try:
                cur.execute("create schema goose;")
                g_logger.debug("created database schema for migrations")
            except psycopg2.errors.DuplicateSchema:
                g_logger.debug("database migration schema already exists")
            finally:
                cur.close()
            return conn
    except psycopg2.OperationalError:
        pass


def create_db(db_name: str):
    conn = psycopg2.connect(
        database="postgres",
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
    try:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            cur.execute(f"create database {db_name};")
            g_logger.debug(f"created database: {db_name!r}")
        except psycopg2.errors.DuplicateDatabase:
            g_logger.debug(f"database already exists: {db_name!r}")
        cur.close()
    finally:
        conn.close()

    new_conn = connect_db_if_exists(db_name)
    if new_conn is None:
        raise ConnectionError("Created database, but can't connect to it")
    return new_conn


def call_goose(*args: str) -> None:
    env = os.environ.copy()
    env.update({
        'GOOSE_DRIVER': 'postgres',
        'GOOSE_DBSTRING': f'postgres://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{TEST_DB_NAME}',
        'GOOSE_MIGRATION_DIR': './migrations'
    })
    
    try:
        g_logger.debug(f"running: `goose {' '.join(args)}`")
        
        proc = subprocess.Popen([
            "goose",
            "-table", "goose.migrations",
            *args
        ], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        stdout, _ = proc.communicate()
        g_logger.debug(f"goose output: {stdout}")

        proc.wait()
    except subprocess.CalledProcessError as e:
        g_logger.debug(f"goose command failed: {e}")
        g_logger.debug(f"goose output: {e.output}")
        raise
    finally:
        g_logger.debug("finished schema operation.")


@pytest.fixture(scope="session")
def db_setup():
    conn = create_db(TEST_DB_NAME)
    call_goose("up")
    psycopg2.extras.register_composite("error_t", conn)
    psycopg2.extras.register_composite("result_t", conn)
    yield conn
    conn.close()
    call_goose("reset")


@pytest.fixture(scope="function")
def db_cursor(db_setup):
    yield db_setup.cursor()
    db_setup.rollback()


@pytest.fixture
def with_valid_user(db_cursor):
    def inner(role):
        email, password = "a@a.com", "password"
        db_cursor.callproc("register_user", (
            "first_name",
            "last_name",
            email,
            datetime(2000, 1, 1).date(),
            password,
            role,
        ))
        return email, password, db_cursor.fetchone()
    return inner