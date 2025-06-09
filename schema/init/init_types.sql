  INSERT INTO AddressTypes (address_type) VALUES
    ('home'),
    ('office'),
    ('mailing')
  ON CONFLICT DO NOTHING;

  INSERT INTO OrderStaffRoles (staff_role) VALUES
    ('driver'),
    ('helper')
  ON CONFLICT DO NOTHING;

  INSERT INTO PhoneNumberTypes (phone_number_type) VALUES
    ('home'),
    ('work')
  ON CONFLICT DO NOTHING;

  INSERT INTO BidActionType (action_name) VALUES
    ('bid'),
    ('accept'),
    ('withdraw')
  ON CONFLICT DO NOTHING;

  INSERT INTO BusinessResourceTypes (resource_name) VALUES
    ('large van'),
    ('medium van'),
    ('small van'),
    ('storage unit')
  ON CONFLICT DO NOTHING;

  INSERT INTO UserRoles (user_role) VALUES
    ('customer'),
    ('service-provider')
  ON CONFLICT DO NOTHING;

  INSERT INTO UserStatus (user_status) VALUES
    ('pending-approval'),
    ('active'),
    ('deleted'),
    ('banned')
  ON CONFLICT DO NOTHING;