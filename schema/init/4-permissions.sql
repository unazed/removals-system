DO $$
DECLARE
  r RECORD;
  reg_token TEXT;
  log_token TEXT;
BEGIN
  FOR r IN
    SELECT tablename
    FROM pg_tables
    WHERE schemaname = 'public'
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', r.tablename);
  END LOOP;

  DROP ROLE IF EXISTS app_guest;
  CREATE ROLE app_guest LOGIN NOINHERIT;
  REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_guest;
  GRANT USAGE ON SCHEMA public TO app_guest;
  GRANT EXECUTE ON FUNCTION login_user(TEXT, TEXT)
    TO app_guest;
  GRANT EXECUTE ON FUNCTION register_user(TEXT, TEXT, TEXT, DATE, TEXT, TEXT, TEXT, INTEGER)
    TO app_guest;
END;
$$;