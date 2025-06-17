CREATE OR REPLACE FUNCTION login_user(p_email TEXT, p_password TEXT)
RETURNS result_t AS $$
DECLARE
  stored_user_id INTEGER;
  stored_hash TEXT;
  stored_user_role TEXT;
  stored_user_status TEXT;
  normalized_email TEXT;
  token TEXT;
BEGIN
  normalized_email = normalize_email(p_email);

  SELECT user_id, password_hash, user_role, user_status
  INTO stored_user_id, stored_hash, stored_user_role, stored_user_status
  FROM Users
  WHERE email = normalized_email;

  IF NOT FOUND THEN
    RETURN make_error_result('INVALID_CREDENTIALS', 'Invalid email or password');
  END IF;

  IF crypt(p_password, stored_hash) <> stored_hash THEN
    RETURN make_error_result('INVALID_CREDENTIALS', 'Invalid email or password');
  END IF;

  IF stored_user_status = 'pending-approval' THEN
    RETURN make_error_result('PENDING_APPROVAL', 'Account pending approval');
  END IF;

  token := sign(
    json_build_object(
      'user_id', stored_user_id,
      'email', p_email,
      'role', stored_user_role
    ),
    get_jwt_secret(),
    'HS256'
  );

  RETURN make_success_result(jsonb_build_object(
    'token', token,
    'user_role', stored_user_role
  ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;