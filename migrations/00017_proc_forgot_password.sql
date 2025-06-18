-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION forgot_password(
    p_code TEXT,
    p_email TEXT,
    p_password TEXT
)
RETURNS result_t AS $$
DECLARE
    stored_user_id INTEGER;
    stored_user_role TEXT;
    normalized_email TEXT;
BEGIN
    normalized_email := normalize_email(p_email);
    
    SELECT user_id, user_role
    INTO stored_user_id, stored_user_role
    FROM Users
    WHERE email = normalized_email;

    IF NOT FOUND THEN
        RETURN make_error_result('INVALID_CREDENTIALS', 'Invalid email');
    END IF;

    RAISE NOTICE 'Pretending to verify code: %', p_code;

    IF p_code IS DISTINCT FROM '1234' THEN
        RETURN make_error_result('INVALID_CODE', 'Invalid authentication code');
    END IF;

    UPDATE Users
    SET password_hash = crypt(p_password, gen_salt('bf', 8))
    WHERE email = normalized_email;

    RETURN login_user(normalized_email, p_password);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION forgot_password;
-- +goose StatementEnd
