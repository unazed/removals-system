CREATE TABLE Users (
  user_id       INTEGER GENERATED ALWAYS AS IDENTITY,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  dob           DATE NOT NULL,

  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  password_hash TEXT NOT NULL,

  user_role     TEXT,
  user_status   TEXT,
  is_disabled   BOOLEAN DEFAULT FALSE,

  business_id   INTEGER,

  CONSTRAINT PK_Users
    PRIMARY KEY (user_id),
  
  CONSTRAINT CHK_Users__min_age
    CHECK (DATE_PART('year', AGE(CURRENT_TIMESTAMP, dob)) >= 18),
  CONSTRAINT CHK_Users__email_validate
    CHECK (email LIKE '%@%'),

  CONSTRAINT FK_Users__user_role
    FOREIGN KEY (user_role)
    REFERENCES UserRoles(user_role)
    ON DELETE SET NULL,
  CONSTRAINT FK_Users__user_status
    FOREIGN KEY (user_status)
    REFERENCES UserStatus(user_status)
    ON DELETE SET NULL,
  CONSTRAINT FK_Users__business
    FOREIGN KEY (business_id)
    REFERENCES Businesses(business_id)
    ON DELETE SET NULL
);

CREATE TABLE UserPhoneNumbers (
  user_id           INTEGER NOT NULL,
  phone_number_id   INTEGER NOT NULL,
  phone_number_type TEXT NOT NULL,

  CONSTRAINT PK_UserPhoneNumbers
    PRIMARY KEY (user_id, phone_number_id),

  CONSTRAINT FK_UserPhoneNumbers__user
    FOREIGN KEY (user_id)
    REFERENCES Users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_UserPhoneNumbers__phone_number
    FOREIGN KEY (phone_number_id)
    REFERENCES PhoneNumbers(phone_number_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_UserPhoneNumbers__phone_type
    FOREIGN KEY (phone_number_type)
    REFERENCES PhoneNumberTypes(phone_number_type)
    ON DELETE RESTRICT
);

CREATE TABLE UserAddresses (
  user_id       INTEGER NOT NULL,
  address_id    INTEGER NOT NULL,
  address_type  TEXT NOT NULL,

  CONSTRAINT PK_UserAddresses
    PRIMARY KEY (user_id, address_id),

  CONSTRAINT FK_UserAddresses__user
    FOREIGN KEY (user_id)
    REFERENCES Users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_UserAddresses__address
    FOREIGN KEY (address_id)
    REFERENCES Addresses(address_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_UserAddresses__address_type
    FOREIGN KEY (address_type)
    REFERENCES AddressTypes(address_type)
    ON DELETE RESTRICT
);