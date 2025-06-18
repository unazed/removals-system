-- +goose Up
-- +goose StatementBegin
INSERT INTO types.ItemCategories (category_name) VALUES
  ('living room'),
  ('bathroom'),
  ('bedroom'),
  ('kitchen'),
  ('garden')
ON CONFLICT DO NOTHING;

INSERT INTO types.BusinessStaffRoles (staff_role) VALUES
  ('executive'),
  ('employee')
ON CONFLICT DO NOTHING;

INSERT INTO types.AddressTypes (address_type) VALUES
  ('home'),
  ('office'),
  ('mailing')
ON CONFLICT DO NOTHING;

INSERT INTO types.OrderStaffRoles (staff_role) VALUES
  ('driver'),
  ('helper')
ON CONFLICT DO NOTHING;

INSERT INTO types.PhoneNumberTypes (phone_number_type) VALUES
  ('home'),
  ('work')
ON CONFLICT DO NOTHING;

INSERT INTO types.BidActionType (action_name) VALUES
  ('bid'),
  ('accept'),
  ('withdraw')
ON CONFLICT DO NOTHING;

INSERT INTO types.BusinessResourceTypes (resource_name) VALUES
  ('large van'),
  ('medium van'),
  ('small van'),
  ('storage unit')
ON CONFLICT DO NOTHING;

INSERT INTO types.UserRoles (user_role) VALUES
  ('customer'),
  ('service-provider')
ON CONFLICT DO NOTHING;

INSERT INTO types.UserStatus (user_status) VALUES
  ('pending-approval'),
  ('active'),
  ('deleted'),
  ('banned')
ON CONFLICT DO NOTHING;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
TRUNCATE TABLE types.UserStatus CASCADE;
TRUNCATE TABLE types.UserRoles CASCADE;
TRUNCATE TABLE types.BusinessResourceTypes CASCADE;
TRUNCATE TABLE types.BidActionType CASCADE;
TRUNCATE TABLE types.PhoneNumberTypes CASCADE;
TRUNCATE TABLE types.OrderStaffRoles CASCADE;
TRUNCATE TABLE types.AddressTypes CASCADE;
TRUNCATE TABLE types.BusinessStaffRoles CASCADE;
TRUNCATE TABLE types.ItemCategories CASCADE;
-- +goose StatementEnd
