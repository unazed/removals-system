CREATE OR REPLACE FUNCTION login_user(p_email TEXT, p_password TEXT)
RETURNS TABLE(msg TEXT, token TEXT, role TEXT) AS $$
DECLARE
  stored_user_id INTEGER;
  stored_hash TEXT;
  stored_user_role TEXT;
  normalized_email TEXT;
  token TEXT;
BEGIN
  normalized_email = normalize_email(p_email);

  SELECT user_id, password_hash, user_role
  INTO stored_user_id, stored_hash, stored_user_role
  FROM Users
  WHERE email = normalized_email;

  IF NOT FOUND THEN
    RETURN QUERY
    SELECT 'Invalid email or password', NULL, NULL;
  END IF;

  IF crypt(p_password, stored_hash) = stored_hash THEN
    RETURN QUERY SELECT
      '',
      sign(
        json_build_object(
          'user_id', stored_user_id,
          'email', p_email,
          'role', stored_user_role
        ),
        get_jwt_secret(),
        'HS256'
      ),
      stored_user_role;
  END IF;
  
  RETURN QUERY
  SELECT 'Invalid email or password', NULL, NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
