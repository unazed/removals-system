CREATE OR REPLACE FUNCTION order_insert()
RETURNS trigger AS $$
BEGIN
  IF NEW.pickup_date < CURRENT_DATE + INTERVAL '1 day' THEN
    RAISE EXCEPTION 'Pickup date must be at least one day in the future';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION order_update()
RETURNS trigger AS $$
BEGIN
  IF OLD.created_at IS DISTINCT FROM NEW.created_at THEN
    RAISE EXCEPTION 'Cannot modify created_at timestamp';
  END IF;

  IF NEW.pickup_date < CURRENT_DATE + INTERVAL '1 day' THEN
    RAISE EXCEPTION 'Pickup date must be at least one day in the future';
  END IF;
  
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;