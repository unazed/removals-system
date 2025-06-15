CREATE OR REPLACE FUNCTION forgot_password(p_code TEXT, p_email TEXT, p_password TEXT)
RETURNS TABLE(msg TEXT, token TEXT, role TEXT) AS $$
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
        RETURN QUERY
        SELECT 'Email does not exist', NULL, NULL;
    END IF;

    RAISE NOTICE 'Pretending to verify code: %', p_code;

    IF p_code IS DISTINCT FROM '1234' THEN
        RETURN QUERY
        SELECT 'Invalid code', NULL, NULL;
    END IF;

    UPDATE Users
    SET password_hash = crypt(p_password, gen_salt('bf', 8))
    WHERE email = normalized_email;

    RETURN QUERY
    SELECT L.msg, L.token, L.role
    FROM login_user(normalized_email, p_password) AS L;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
