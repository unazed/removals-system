-- +goose Up
-- +goose StatementBegin
DO $$
DECLARE
  r RECORD;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE FORMAT('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', r.tablename);
    END LOOP;

    CREATE ROLE app_guest LOGIN PASSWORD 'app_guest' NOINHERIT;
    REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_guest;

    GRANT USAGE ON SCHEMA public TO app_guest;
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_guest;
END;
$$;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DO $$
DECLARE
  r RECORD;
BEGIN
    -- Disable Row Level Security on all public tables
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE FORMAT('ALTER TABLE public.%I DISABLE ROW LEVEL SECURITY;', r.tablename);
    END LOOP;

    -- Revoke permissions from app_guest role
    REVOKE USAGE ON SCHEMA public FROM app_guest;
    REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM app_guest;
    
    -- Drop the app_guest role
    DROP ROLE IF EXISTS app_guest;
END;
$$;
-- +goose StatementEnd
