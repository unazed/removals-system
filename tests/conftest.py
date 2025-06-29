import pytest
import psycopg2
import psycopg2.extensions

from removals_system.config import settings
from removals_system.models.db import proc_register_user

from typing import Generator
from datetime import datetime
import subprocess
import logging
import os
import uuid

g_logger = logging.getLogger(__name__)
g_logger.setLevel(logging.INFO)

TEST_DB_NAME = "test_db"
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"
GOOSE_PATH = r"D:\Programming\removals-system\ext\goose.exe"


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


def create_db(db_name: str, username: str = DB_USERNAME, password: str = DB_PASSWORD):
    try:
        conn = psycopg2.connect(
            database="postgres",
            user=username,
            password=password
        )
    except psycopg2.errors.OperationalError:
        g_logger.debug("failed to connect to database")
        raise
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
            GOOSE_PATH,
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


@pytest.fixture(scope="session", autouse=True)
def override_db_config_for_tests():
    settings.update_config(
        dbname=TEST_DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host="localhost",
        port=5432,
    )


@pytest.fixture(scope="session")
def db_setup() -> Generator[psycopg2.extensions.connection, None, None]:
    conn = create_db(TEST_DB_NAME)
    call_goose("up")
    yield conn
    conn.close()
    call_goose("reset")


@pytest.fixture(scope="function")
def db_cursor(db_setup) -> Generator[psycopg2.extensions.cursor, None, None]:
    yield db_setup.cursor()
    db_setup.rollback()


@pytest.fixture(scope="function")
def db_guest_cursor(db_setup) -> Generator[psycopg2.extensions.cursor, None, None]:
    cur = db_setup.cursor()
    cur.execute("set role app_guest;")
    yield cur
    db_setup.rollback()


@pytest.fixture
def with_valid_user(db_guest_cursor):
    def inner(role):
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        password = "password"
        result = proc_register_user(
            "first_name", "last_name",
            email, password,
            datetime(2000, 1, 1).date(),
            role,
        )
        assert result.success, "Registration should've been successful"
        return email, password, result
    return inner