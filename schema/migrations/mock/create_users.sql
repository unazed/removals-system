DO $$
DECLARE
    reg_token TEXT;
BEGIN
    SET ROLE app_guest;

    reg_token := register_user(
        'Alice',
        'Smith',
        'alice@example.com',
        DATE '1995-04-15',
        'supersecret123',
        'customer'
    );

    IF reg_token IS NULL THEN
        RAISE NOTICE 'User exists: alice@example.com';
    ELSE
        RAISE NOTICE 'User created: alice@example.com, token: %', reg_token;
    END IF;

    reg_token := register_user(
        'John',
        'Doe',
        'john.doe@example.com',
        DATE '1970-01-01',
        'supersecret123',
        'service-provider'
    );
    IF reg_token IS NULL THEN
        RAISE NOTICE 'User exists: john.doe@example.com';
    ELSE
        RAISE NOTICE 'User created: john.doe@example.com, token: %', reg_token;
    END IF;
END;
$$;