-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION get_length_constraint(p_table TEXT, p_column TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT character_maximum_length 
        FROM information_schema.columns 
        WHERE table_name = p_table 
        AND column_name = p_column
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER IMMUTABLE STRICT;

CREATE FUNCTION decode_token(p_token TEXT)
RETURNS JSON AS $$
DECLARE
    v_header JSON;
    v_payload JSON;
    v_valid BOOLEAN;
BEGIN
    SELECT header, payload, valid
    INTO v_header, v_payload, v_valid
    FROM verify(p_token, utils.get_app_config_value('jwt_secret'));

    IF NOT v_valid THEN
        RETURN NULL;
    END IF;

    RETURN v_payload;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STRICT;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION decode_token;
DROP FUNCTION get_length_constraint;
-- +goose StatementEnd
