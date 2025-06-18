-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION order_insert()
RETURNS trigger AS $$
BEGIN
  IF NEW.pickup_date < CURRENT_DATE + INTERVAL '1 day' THEN
    RAISE EXCEPTION 'Pickup date must be at least one day in the future';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION order_update()
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

CREATE TRIGGER TRG_Orders__update
BEFORE UPDATE ON Orders
FOR EACH ROW
EXECUTE FUNCTION order_update();

CREATE TRIGGER TRG_Orders__insert
BEFORE INSERT ON Orders
FOR EACH ROW
EXECUTE FUNCTION order_insert();
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TRIGGER TRG_Orders__insert ON Orders;
DROP TRIGGER TRG_Orders__update ON Orders;
DROP FUNCTION order_update;
DROP FUNCTION order_insert;
-- +goose StatementEnd
