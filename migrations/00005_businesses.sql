-- +goose Up
-- +goose StatementBegin
CREATE TABLE Businesses (
  business_id     INTEGER GENERATED ALWAYS AS IDENTITY,

  business_name   TEXT NOT NULL,
  crn_no          TEXT UNIQUE NOT NULL,
  vat_no          TEXT,
  utr_no          TEXT,
  num_employees   INTEGER NOT NULL,

  CONSTRAINT PK_Businesses
    PRIMARY KEY (business_id),

  CONSTRAINT CHK_Businesses__name_length
    CHECK (LENGTH(business_name) <= 120),
  CONSTRAINT CHK_Businesses__nr_employees
    CHECK (num_employees > 0),
  CONSTRAINT CHK_Businesses__crn_length
    CHECK (LENGTH(crn_no) = 8),
  CONSTRAINT CHK_Businesses__vat_length
    CHECK (COALESCE(LENGTH(vat_no) = 11, TRUE)),
  CONSTRAINT CHK_Businesses__utr_no
    CHECK (COALESCE(LENGTH(utr_no) = 10, TRUE))
);

CREATE TABLE BusinessStaff (
  business_id     INTEGER NOT NULL,
  user_id         INTEGER UNIQUE NOT NULL,
  user_role       TEXT NOT NULL,

  CONSTRAINT PK_BusinessStaff
    PRIMARY KEY (business_id, user_id),
  
  CONSTRAINT FK_BusinessStaff__business
    FOREIGN KEY (business_id)
    REFERENCES Businesses(business_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_BusinessStaff__user
    FOREIGN KEY (user_id)
    REFERENCES Users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_BusinessStaff__user_role
    FOREIGN KEY (user_role)
    REFERENCES types.BusinessStaffRoles(staff_role)
    ON DELETE RESTRICT
);

CREATE TABLE BusinessResources (
  resource_id     INTEGER GENERATED ALWAYS AS IDENTITY,
  business_id     INTEGER NOT NULL,

  resource_name   TEXT NOT NULL,
  quantity        INTEGER NOT NULL,

  CONSTRAINT PK_BusinessResources
    PRIMARY KEY (resource_id),

  CONSTRAINT CHK_BusinessResources__valid_quantity
    CHECK (quantity > 0),

  CONSTRAINT UK_BusinessResources
    UNIQUE (business_id, resource_name),
  
  CONSTRAINT FK_BusinessResources__business
    FOREIGN KEY (business_id)
    REFERENCES Businesses(business_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_BusinessResources__resource_name
    FOREIGN KEY (resource_name)
    REFERENCES types.BusinessResourceTypes(resource_name)
    ON DELETE RESTRICT
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE BusinessResources;
DROP TABLE BusinessStaff;
DROP TABLE Businesses;
-- +goose StatementEnd
