CREATE OR REPLACE FUNCTION register_user(
  p_first_name TEXT,
  p_last_name TEXT,
  p_email TEXT,
  p_dob DATE,
  p_password TEXT,
  p_user_role TEXT
)
RETURNS TABLE(token TEXT, role TEXT) AS $$
DECLARE
  new_user_id INTEGER;
  hashed_password TEXT;
  user_status TEXT;
BEGIN
  IF exists_email(p_email) THEN
    RETURN;
  END IF;

  hashed_password := crypt(p_password, gen_salt('bf', 8));

  INSERT INTO Users (
    first_name,
    last_name,
    email,
    dob,
    password_hash,
    user_role
  ) VALUES (
    p_first_name,
    p_last_name,
    p_email,
    p_dob,
    hashed_password,
    p_user_role
  )
  RETURNING user_id INTO new_user_id;

  RETURN QUERY SELECT
    sign(
      json_build_object(
        'user_id', new_user_id,
        'email', p_email,
        'role', p_user_role
      ),
      get_jwt_secret(),
      'HS256'
    ),
    p_user_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;