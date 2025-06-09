CREATE OR REPLACE FUNCTION register_user(
  p_first_name TEXT,
  p_last_name TEXT,
  p_email TEXT,
  p_dob DATE,
  p_password TEXT,
  p_user_role TEXT DEFAULT 'customer',
  p_user_status TEXT DEFAULT 'pending-approval',
  p_business_id INTEGER DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
  new_user_id INTEGER;
  hashed_password TEXT;
  token TEXT;
BEGIN
  IF EXISTS (SELECT 1 FROM Users WHERE email = p_email) THEN
    RETURN NULL;
  END IF;

  hashed_password := crypt(p_password, gen_salt('bf', 8));

  INSERT INTO Users (
    first_name,
    last_name,
    email,
    dob,
    password_hash,
    user_role,
    user_status,
    business_id
  ) VALUES (
    p_first_name,
    p_last_name,
    p_email,
    p_dob,
    hashed_password,
    p_user_role,
    p_user_status,
    p_business_id
  )
  RETURNING user_id INTO new_user_id;

  token := sign(
    json_build_object(
      'user_id', new_user_id,
      'email', p_email,
      'role', p_user_role
    ),
    get_jwt_secret(),
    'HS256'
  );

  RETURN token;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;