CREATE OR REPLACE FUNCTION create_user_phone_number(
    p_token TEXT, p_extension TEXT, p_number TEXT,
    p_phone_type TEXT DEFAULT 'home'
)
RETURNS TEXT AS $$
DECLARE
  user_session JSON;
  new_phone_id INTEGER;
BEGIN
  user_session := decode_token(p_token);

  IF user_session IS NULL THEN
    RETURN 'Invalid session token';
  END IF;

  INSERT INTO PhoneNumbers(phone_extension, phone_number)
  VALUES (p_extension, p_number)
  RETURNING phone_number_id INTO new_phone_id;

  INSERT INTO UserPhoneNumbers(user_id, phone_number_id, phone_number_type)
  VALUES ((user_session->>'user_id')::INTEGER, new_phone_id, p_phone_type);

  RETURN '';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_user_phone_numbers(p_token TEXT)
RETURNS TABLE (
    phone_number_id   INTEGER,
    phone_extension   TEXT,
    phone_number      TEXT,
    phone_number_type TEXT
) AS $$
DECLARE
    user_session JSON;
    uid INTEGER;
BEGIN
    user_session := decode_token(p_token);
    IF user_session IS NULL THEN
        RETURN;
    END IF;

    uid := (user_session->>'user_id')::INTEGER;

    RETURN QUERY
    SELECT
        pn.phone_number_id,
        pn.phone_extension,
        pn.phone_number,
        upn.phone_number_type
    FROM UserPhoneNumbers upn
    JOIN PhoneNumbers pn ON upn.phone_number_id = pn.phone_number_id
    WHERE upn.user_id = uid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
