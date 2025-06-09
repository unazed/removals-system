CREATE TABLE AddressTypes (
  address_type      TEXT NOT NULL,

  CONSTRAINT PK_AddressTypes
    PRIMARY KEY (address_type),

  CONSTRAINT CHK_AddressTypes__length
    CHECK (LENGTH(address_type) <= 15),
  CONSTRAINT CHK_AddressTypes__valid
    CHECK (address_type IN (
      'home', 'office', 'mailing'
    ))
);

CREATE TABLE OrderStaffRoles (
  staff_role        TEXT NOT NULL,

  CONSTRAINT PK_OrderStaffRoles
    PRIMARY KEY (staff_role),

  CONSTRAINT CHK_OrderStaffRoles__length
    CHECK (LENGTH(staff_role) <= 50),
  CONSTRAINT CHK_OrderStaffRoles__valid
    CHECK (staff_role IN (
      'driver', 'helper'
    ))
);

CREATE TABLE PhoneNumberTypes (
  phone_number_type TEXT NOT NULL,

  CONSTRAINT PK_PhoneNumberTypes
    PRIMARY KEY (phone_number_type),
  
  CONSTRAINT CHK_PhoneNumberTypes__length
    CHECK (LENGTH(phone_number_type) <= 20),
  CONSTRAINT CHK_PhoneNumberTypes__valid
    CHECK (phone_number_type IN (
      'home', 'work'
    ))
);

CREATE TABLE BidActionType (
  action_name     TEXT NOT NULL,

  CONSTRAINT PK_BidActionType
    PRIMARY KEY (action_name),

  CONSTRAINT CHK_BidActionType__length
    CHECK (LENGTH(action_name) <= 20),
  CONSTRAINT CHK_BidActionType__valid
    CHECK (action_name IN (
      'bid', 'accept', 'withdraw'
    ))
);

CREATE TABLE BusinessResourceTypes (
  resource_name   TEXT NOT NULL,

  CONSTRAINT PK_BusinessResourceTypes
    PRIMARY KEY (resource_name),

  CONSTRAINT CHK_BusinessResourceTypes__length
    CHECK (LENGTH(resource_name) <= 50),
  CONSTRAINT CHK_BusinessResourceTypes__valid
    CHECK (resource_name IN (
      'large van', 'medium van', 'small van',
      'storage unit'
    ))
);

CREATE TABLE UserRoles (
  user_role       TEXT NOT NULL,

  CONSTRAINT PK_UserRoles
    PRIMARY KEY (user_role),

  CONSTRAINT CHK_UserRoles__length
    CHECK (LENGTH(user_role) <= 25),
  CONSTRAINT CHK_UserRoles__valid
    CHECK (user_role IN (
      'customer', 'service-provider'
    ))
);

CREATE TABLE UserStatus (
  user_status     TEXT NOT NULL,

  CONSTRAINT PK_UserStatus
    PRIMARY KEY (user_status),

  CONSTRAINT CHK_UserStatus__length
    CHECK (LENGTH(user_status) <= 25),
  CONSTRAINT CHK_UserStatus__valid
    CHECK (user_status IN (
      'pending-approval', 'active', 'deleted',
      'banned'
    ))
);