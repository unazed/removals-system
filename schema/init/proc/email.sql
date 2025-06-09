CREATE OR REPLACE FUNCTION is_valid_email(p_email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  IF LENGTH(p_email) - LENGTH(REPLACE(p_email, '@', '')) != 1 THEN
    RETURN FALSE;
  END IF;

  IF p_email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
    RETURN FALSE;
  END IF;

  RETURN TRUE;
END;
$$ LANGUAGE plpgsql IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION normalize_email(p_email TEXT)
RETURNS TEXT AS $$
DECLARE
  local_part TEXT;
  domain_part TEXT;
  plus_pos INT;
BEGIN
  IF NOT is_valid_email(p_email) THEN
    RETURN '';
  END IF;

  local_part := LOWER(SPLIT_PART(p_email, '@', 1));
  domain_part := LOWER(SPLIT_PART(p_email, '@', 2));

  plus_pos := POSITION('+' IN local_part);
  IF plus_pos > 0 THEN
    local_part := left(local_part, plus_pos - 1);
  END IF;

  RETURN local_part || '@' || domain_part;
END;
$$ LANGUAGE plpgsql IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION exists_email(
  p_email TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
  exists_flag BOOLEAN;
  normalized_email TEXT;
BEGIN
  SELECT EXISTS (
    SELECT 1 FROM Users WHERE email = normalize_email(p_email)
  ) INTO exists_flag;

  RETURN exists_flag;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;