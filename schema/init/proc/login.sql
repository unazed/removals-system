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
