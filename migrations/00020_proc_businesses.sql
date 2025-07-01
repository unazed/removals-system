-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION create_business(
    p_token TEXT,
    p_business_name TEXT,
    p_crn_no TEXT,
    p_vat_no TEXT,
    p_utr_no TEXT,
    p_num_employees INTEGER
)
RETURNS result_t AS $$
DECLARE
    user_session JSON;
    stored_business_id INTEGER;
BEGIN
    user_session := decode_token(p_token);

    IF user_session IS NULL THEN
        RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
    ELSIF user_session->>'role' <> 'service-provider' THEN
        RETURN make_error_result(
            'INSUFFICIENT_PERMISSIONS',
            'Invalid role for creating business'
        );
    END IF;

    INSERT INTO Businesses(business_name, crn_no, vat_no, utr_no, num_employees)
    VALUES (p_business_name, p_crn_no, p_vat_no, p_utr_no, p_num_employees)
    RETURNING business_id INTO stored_business_id;

    INSERT INTO BusinessStaff(business_id, user_id, user_role)
    VALUES (
        stored_business_id,
        (user_session->>'user_id')::INTEGER,
        'executive'
    );

    RETURN make_success_result();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION utils.get_business_id_by_crn(p_crn_no TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT business_id FROM Businesses WHERE crn_no = p_crn_no);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION utils.get_business_staff_role(
    p_user_id INTEGER,
    p_business_id INTEGER
)
RETURNS result_t AS $$
DECLARE
    found_role TEXT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Users WHERE user_id = p_user_id) THEN
        RAISE EXCEPTION 'Invalid user ID';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM Businesses
        WHERE business_id = p_business_id
    ) THEN
        RAISE EXCEPTION 'Invalid business ID';
    END IF;

    SELECT user_role INTO found_role
    FROM BusinessStaff
    WHERE user_id = p_user_id
    AND business_id = p_business_id;

    IF NOT FOUND THEN
        RETURN make_error_result(
            'INSUFFICIENT_PERMISSIONS',
            'User is not staff of this business'
        );
    END IF;

    RETURN make_success_result(jsonb_build_object(
        'role', found_role
    ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION get_business_staff_role(
    p_token TEXT,
    p_crn_no TEXT
)
RETURNS result_t AS $$
DECLARE
    user_session JSON;
    stored_business_id INTEGER;
    stored_staff_role result_t;
BEGIN
    user_session := decode_token(p_token);
    IF user_session IS NULL THEN
        RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
    END IF;

    stored_business_id := utils.get_business_id_by_crn(p_crn_no);
    IF stored_business_id IS NULL THEN
        RETURN make_error_result(
            'INVALID_BUSINESS',
            'Invalid business identifier'
        );
    END IF;

    stored_staff_role := utils.get_business_staff_role(
        (user_session->>'user_id')::INTEGER,
        stored_business_id
    );

    IF NOT stored_staff_role.success THEN
        RETURN stored_staff_role;
    END IF;

    RETURN make_success_result(jsonb_build_object(
        'role', stored_staff_role.data->>'role'
    ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION add_business_resource(
    p_token TEXT,
    p_crn_no TEXT,
    p_resource_name TEXT,
    p_quantity INTEGER
)
RETURNS result_t AS $$
DECLARE
    stored_staff_role result_t;
    stored_business_id INTEGER;
BEGIN
    stored_staff_role := get_business_staff_role(p_token, p_crn_no);
    
    IF NOT stored_staff_role.success THEN
        RETURN stored_staff_role;
    END IF;
    
    IF stored_staff_role.data->>'role' <> 'executive' THEN
        RETURN make_error_result(
            'INSUFFICIENT_PERMISSIONS',
            'Non-executive staff cannot create business resources'
        );
    END IF;

    stored_business_id := utils.get_business_id_by_crn(p_crn_no);
    
    INSERT INTO BusinessResources(business_id, resource_name, quantity)
    VALUES (stored_business_id, p_resource_name, p_quantity)
    ON CONFLICT (business_id, resource_name) 
    DO UPDATE SET quantity = BusinessResources.quantity + EXCLUDED.quantity;

    RETURN make_success_result();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE FUNCTION exists_business_crn(p_crn TEXT)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM Businesses WHERE crn_no = p_crn
  );
$$ LANGUAGE sql SECURITY DEFINER;

CREATE FUNCTION exists_business_utr(p_utr TEXT)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM Businesses WHERE utr_no = p_utr
  );
$$ LANGUAGE sql SECURITY DEFINER;

CREATE FUNCTION exists_business_vat(p_vat TEXT)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM Businesses WHERE vat_no = p_vat
  );
$$ LANGUAGE sql SECURITY DEFINER;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP FUNCTION exists_business_vat;
DROP FUNCTION exists_business_utr;
DROP FUNCTION exists_business_crn;
DROP FUNCTION add_business_resource;
DROP FUNCTION get_business_staff_role;
DROP FUNCTION utils.get_business_staff_role;
DROP FUNCTION utils.get_business_id_by_crn;
DROP FUNCTION create_business;
-- +goose StatementEnd
