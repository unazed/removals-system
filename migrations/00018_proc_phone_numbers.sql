-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION create_user_phone_number(
    p_token TEXT,
    p_extension TEXT,
    p_number TEXT,
    p_phone_type TEXT DEFAULT 'home'
)
RETURNS result_t AS $$
DECLARE
  user_session JSON;
  new_phone_id INTEGER;
BEGIN
  user_session := decode_token(p_token);

  IF user_session IS NULL THEN
    RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
  END IF;

  INSERT INTO PhoneNumbers(phone_extension, phone_number)
  VALUES (p_extension, p_number)
  RETURNING phone_number_id INTO new_phone_id;

  INSERT INTO UserPhoneNumbers(user_id, phone_number_id, phone_number_type)
  VALUES ((user_session->>'user_id')::INTEGER, new_phone_id, p_phone_type);

  RETURN make_success_result();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION get_user_phone_numbers(p_token TEXT)
RETURNS result_t AS $$
DECLARE
    user_session JSON;
    phone_data JSONB;
BEGIN
    user_session := decode_token(p_token);
    IF user_session IS NULL THEN
        RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
    END IF;

    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'phone_number_id', pn.phone_number_id,
                'phone_extension', pn.phone_extension,
                'phone_number', pn.phone_number,
                'phone_number_type', upn.phone_number_type
            )
        ),
        '[]'::jsonb
    ) INTO phone_data
    FROM UserPhoneNumbers upn
    JOIN PhoneNumbers pn ON upn.phone_number_id = pn.phone_number_id
    WHERE upn.user_id = (user_session->>'user_id')::INTEGER;

    RETURN make_success_result(phone_data);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION get_user_phone_numbers;
DROP FUNCTION create_user_phone_number;
-- +goose StatementEnd
