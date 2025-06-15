CREATE OR REPLACE FUNCTION get_jwt_secret()
RETURNS TEXT AS $$
BEGIN
  RETURN current_setting('app.jwt_secret', true);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;