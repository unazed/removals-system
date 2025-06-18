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

    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = 'app_guest'
    ) THEN
        CREATE ROLE app_guest LOGIN PASSWORD 'app_guest';

        REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_guest;
        GRANT USAGE ON SCHEMA public TO app_guest;
        GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_guest;
    END IF;
END;
$$;
-- +goose StatementEnd

-- +goose Down
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
        EXECUTE FORMAT('ALTER TABLE public.%I DISABLE ROW LEVEL SECURITY;', r.tablename);
    END LOOP;
END;
$$
-- +goose StatementEnd