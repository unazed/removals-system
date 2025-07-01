-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION get_business_resources(
    p_token TEXT,
    p_crn_no TEXT
)
RETURNS result_t AS $$
DECLARE
    v_user_session JSON;
    v_business_id INTEGER;
    v_resources JSONB;
BEGIN
    v_user_session := decode_token(p_token);
    IF v_user_session IS NULL THEN
        RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
    END IF;

    v_business_id := utils.get_business_id_by_crn(p_crn_no);
    IF v_business_id IS NULL THEN
        RETURN make_error_result(
            'INVALID_BUSINESS',
            'Invalid business identifier'
        );
    END IF;

    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'resource_name', BR.resource_name,
                'quantity', BR.quantity
            )
        ),
        '[]'::jsonb
    ) INTO v_resources
    FROM BusinessResources BR
    JOIN Businesses B ON B.business_id = BR.business_id
    WHERE B.crn_no = p_crn_no;

    RETURN make_success_result(v_resources);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION get_business_resources;
-- +goose StatementEnd
