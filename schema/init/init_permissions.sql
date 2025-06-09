CREATE OR REPLACE FUNCTION get_jwt_secret()
RETURNS TEXT AS $$
BEGIN
  RETURN current_setting('app.jwt_secret', true);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION login_user(p_email TEXT, p_password TEXT)
RETURNS TEXT AS $$
DECLARE
  stored_user_id INTEGER;
  stored_hash TEXT;
  stored_user_role TEXT;
  token TEXT;
BEGIN
  SELECT user_id, password_hash, user_role
  INTO stored_user_id, stored_hash, stored_user_role
  FROM Users
  WHERE email = p_email;

  IF NOT FOUND THEN
    RETURN NULL;
  END IF;

  IF crypt(p_password, stored_hash) = stored_hash THEN
    token := sign(
      json_build_object(
        'user_id', stored_user_id,
        'email', p_email,
        'role', stored_user_role
      ),
      get_jwt_secret(),
      'HS256'
    );

    RETURN token;
  ELSE
    RETURN NULL;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION register_user(
  p_first_name TEXT,
  p_last_name TEXT,
  p_email TEXT,
  p_dob DATE,
  p_password TEXT,
  p_user_role TEXT DEFAULT 'customer',
  p_user_status TEXT DEFAULT 'pending-approval',
  p_business_id INTEGER DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
  new_user_id INTEGER;
  hashed_password TEXT;
  token TEXT;
BEGIN
  IF EXISTS (SELECT 1 FROM Users WHERE email = p_email) THEN
    RETURN NULL;
  END IF;

  hashed_password := crypt(p_password, gen_salt('bf', 8));

  INSERT INTO Users (
    first_name,
    last_name,
    email,
    dob,
    password_hash,
    user_role,
    user_status,
    business_id
  ) VALUES (
    p_first_name,
    p_last_name,
    p_email,
    p_dob,
    hashed_password,
    p_user_role,
    p_user_status,
    p_business_id
  )
  RETURNING user_id INTO new_user_id;

  token := sign(
    json_build_object(
      'user_id', new_user_id,
      'email', p_email,
      'role', p_user_role
    ),
    get_jwt_secret(),
    'HS256'
  );

  RETURN token;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

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

  reg_token := register_user(
    'Alice',
    'Smith',
    'alice@example.com',
    DATE '1995-04-15',
    'supersecret123'
  );
  RAISE NOTICE 'Registration JWT: %', reg_token;

  log_token := login_user('alice@example.com', 'supersecret123');
  RAISE NOTICE 'Login JWT: %', log_token;
END;
$$;