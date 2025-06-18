-- +goose Up
-- +goose StatementBegin
CREATE TYPE error_t AS (
    code TEXT,
    message TEXT
);

CREATE TYPE result_t AS (
    success BOOLEAN,
    error error_t,
    data JSONB
);

CREATE FUNCTION make_success_result(data JSONB DEFAULT NULL)
RETURNS result_t AS $$
BEGIN
    RETURN ROW(TRUE, NULL, data)::result_t;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION make_error_result(
    error_code TEXT,
    error_message TEXT
)
RETURNS result_t AS $$
DECLARE
    error_obj error_t;
BEGIN
    error_obj := ROW(error_code, error_message)::error_t;
    RETURN ROW(FALSE, error_obj, NULL)::result_t;
END;
$$ LANGUAGE plpgsql;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION make_error_result;
DROP FUNCTION make_success_result;
DROP TYPE result_t;
DROP TYPE error_t;
-- +goose StatementEnd
