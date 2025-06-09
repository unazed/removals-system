CREATE TABLE PhoneNumbers (
  phone_number_id     INTEGER GENERATED ALWAYS AS IDENTITY,
  phone_extension     CHAR(5) NOT NULL,
  phone_number        TEXT NOT NULL,

  CONSTRAINT PK_PhoneNumbers
    PRIMARY KEY (phone_number_id),

  CONSTRAINT CHK_PhoneNumbers__length
    CHECK (LENGTH(phone_number) <= 20)
);