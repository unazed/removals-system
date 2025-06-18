-- +goose Up
-- +goose StatementBegin
CREATE FUNCTION item_update()
RETURNS trigger AS $$
BEGIN
  IF OLD.created_at IS DISTINCT FROM NEW.created_at THEN
    RAISE EXCEPTION 'Cannot modify created_at timestamp';
  END IF;
  
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRG_Items__update
BEFORE UPDATE ON Items
FOR EACH ROW
EXECUTE FUNCTION item_update();
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TRIGGER TRG_Items__update ON Items;
DROP FUNCTION item_update;
-- +goose StatementEnd
