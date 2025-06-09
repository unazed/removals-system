CREATE TABLE Businesses (
  business_id     INTEGER GENERATED ALWAYS AS IDENTITY,

  business_name   TEXT NOT NULL,
  vat_no          TEXT UNIQUE NOT NULL,
  utr_no          TEXT UNIQUE,
  num_employees   INTEGER NOT NULL,

  CONSTRAINT PK_Businesses
    PRIMARY KEY (business_id),

  CONSTRAINT CHK_Businesses__name_length
    CHECK (LENGTH(business_name) <= 120),
  CONSTRAINT CHK_Businesses__vat_length
    CHECK (LENGTH(vat_no) = 11),
  CONSTRAINT CHK_Businesses__utr_no
    CHECK (LENGTH(utr_no) = 10)
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
  
  CONSTRAINT FK_BusinessResources__business
    FOREIGN KEY (business_id)
    REFERENCES Businesses(business_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_BusinessResources__resource_name
    FOREIGN KEY (resource_name)
    REFERENCES BusinessResourceTypes(resource_name)
    ON DELETE RESTRICT
);