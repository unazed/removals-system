-- +goose Up
-- +goose StatementBegin
CREATE EXTENSION pgcrypto;
CREATE EXTENSION pgjwt;

CREATE FUNCTION utils.get_app_config_value(p_key TEXT)
RETURNS TEXT
AS $$
    SELECT value FROM app_config WHERE key = p_key;
$$ LANGUAGE sql SECURITY DEFINER IMMUTABLE STRICT;

CREATE FUNCTION login_user(p_email TEXT, p_password TEXT)
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
    utils.get_app_config_value('jwt_secret'),
    'HS256'
  );

  RETURN make_success_result(jsonb_build_object(
    'token', token,
    'user_role', stored_user_role
  ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION login_user;
DROP FUNCTION utils.get_app_config_value;
DROP EXTENSION pgjwt;
DROP EXTENSION pgcrypto;
-- +goose StatementEnd
