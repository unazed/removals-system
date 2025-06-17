CREATE OR REPLACE FUNCTION user_update()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.created_at IS DISTINCT FROM NEW.created_at THEN
    RAISE EXCEPTION 'Cannot modify created_at timestamp';
  END IF;

  IF OLD.email IS DISTINCT FROM NEW.email
      AND NOT is_valid_email(NEW.EMAIL) THEN
    RAISE EXCEPTION 'Newly updated email is invalid';
  END IF;

  IF OLD.user_status = 'deleted' THEN
    RAISE EXCEPTION 'Cannot modify a deleted user';
  END IF;
  
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
  
CREATE OR REPLACE FUNCTION user_before_insert()
RETURNS TRIGGER AS $$
DECLARE
  normalized_email TEXT;
BEGIN
  normalized_email := normalize_email(NEW.email);

  IF LENGTH(normalized_email) = 0 THEN
    RAISE EXCEPTION 'Invalid email address: %', NEW.email;
  END IF;

  IF EXISTS (
    SELECT 1 FROM Users WHERE email = normalized_email
  ) THEN
    RAISE EXCEPTION 'Email address already exists: %', NEW.email;
  END IF;

  NEW.email := normalized_email;

  IF NEW.user_role = 'service-provider' THEN
    NEW.user_status = 'pending-approval';
  ELSIF NEW.user_role = 'customer' THEN
    NEW.user_status = 'active';
  ELSE
    RAISE EXCEPTION 'Unhandled user role';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;