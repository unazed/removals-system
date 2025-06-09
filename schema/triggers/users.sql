CREATE OR REPLACE FUNCTION user_update()
RETURNS trigger AS $$
BEGIN
  IF OLD.created_at IS DISTINCT FROM NEW.created_at THEN
    RAISE EXCEPTION 'Cannot modify created_at timestamp';
  END IF;
  
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
  
CREATE TRIGGER user_update BEFORE UPDATE ON Users
  FOR EACH ROW EXECUTE FUNCTION user_update();