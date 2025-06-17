CREATE OR REPLACE FUNCTION create_business(
    p_token TEXT,
    p_business_name TEXT,
    p_crn_no TEXT,
    p_vat_no TEXT,
    p_utr_no TEXT,
    p_num_employees INTEGER
)
RETURNS TEXT AS $$
DECLARE
    user_session JSON;
    stored_business_id INTEGER;
BEGIN
    user_session := decode_token(p_token);

    IF user_session IS NULL THEN
        RETURN 'Invalid session token';
    END IF;

    INSERT INTO Businesses(business_name, crn_no, vat_no, utr_no, num_employees)
    VALUES (p_business_name, p_crn_no, p_vat_no, p_utr_no, p_num_employees)
    RETURNING business_id INTO stored_business_id;

    INSERT INTO BusinessStaff(business_id, user_id, user_role)
    VALUES (stored_business_id, user_session->>'user_id', 'executive');

    RETURN '';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION utils.get_business_id_by_crn(p_crn_no TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT business_id FROM Businesses WHERE crn_no = p_crn_no);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION utils.get_business_staff_role(
    p_user_id INTEGER,
    p_business_id INTEGER
)
RETURNS StaffValidationResultT AS $$
DECLARE
    result StaffValidationResultT;
    found_role TEXT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Users WHERE user_id = p_user_id) THEN
        result.is_valid := FALSE;
        result.error_message := 'User does not exist';
        RETURN result;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM Businesses
        WHERE business_id = p_business_id
    ) THEN
        result.is_valid := FALSE;
        result.error_message := 'Invalid business identifier';
        RETURN result;
    END IF;

    SELECT user_role INTO found_role
    FROM BusinessStaff
    WHERE user_id = p_user_id
    AND business_id = p_business_id;

    IF NOT FOUND THEN
        result.is_valid := FALSE;
        result.error_message := 'User is not staff of this business';
        RETURN result;
    END IF;

    result.is_valid := TRUE;
    result.user_role := found_role;
    result.error_message := NULL;
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_business_staff_role(
    p_token TEXT,
    p_crn_no TEXT
)
RETURNS RECORD AS $$
DECLARE
    user_session JSON;
    stored_business_id INTEGER;
    stored_staff_role StaffValidationResultT;
    result RECORD;
BEGIN
    user_session := decode_token(p_token);
    IF user_session IS NULL THEN
        SELECT 'Invalid session token', NULL::TEXT INTO result;
        RETURN result;
    END IF;

    stored_business_id := utils.get_business_id_by_crn(p_crn_no);
    IF stored_business_id IS NULL THEN
        SELECT 'Invalid business identifier', NULL::TEXT INTO result;
        RETURN result;
    END IF;

    stored_staff_role := utils.get_business_staff_role(
        (user_session->>'user_id')::INTEGER,
        stored_business_id
    );

    IF NOT stored_staff_role.is_valid THEN
        SELECT stored_staff_role.error_message, NULL::TEXT INTO result;
        RETURN result;
    END IF;

    SELECT ''::TEXT, stored_staff_role.user_role INTO result;
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION add_business_resource(
    p_token TEXT,
    p_crn_no TEXT,
    p_resource_name TEXT,
    p_quantity INTEGER
)
RETURNS TEXT AS $$
DECLARE
    staff_check RECORD;
    stored_business_id INTEGER;
BEGIN
    staff_check := get_business_staff_role(p_token, p_crn_no);
    
    IF staff_check.f1 = '' THEN
        RETURN staff_check.f1;
    END IF;
    
    IF staff_check.f2 <> 'executive' THEN
        RETURN 'Insufficient permissions';
    END IF;

    stored_business_id := utils.get_business_id_by_crn(p_crn_no);
    
    INSERT INTO BusinessResources(business_id, resource_name, quantity)
    VALUES (stored_business_id, p_resource_name, p_quantity)
    ON CONFLICT (business_id, resource_name) 
    DO UPDATE SET quantity = BusinessResources.quantity + EXCLUDED.quantity;

    RETURN '';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;