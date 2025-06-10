CREATE TABLE Countries (
  country_id    INTEGER GENERATED ALWAYS AS IDENTITY,
  country_code  CHAR(2) UNIQUE NOT NULL,
  country_name  TEXT NOT NULL,
  
  CONSTRAINT PK_Countries
    PRIMARY KEY (country_id),

  CONSTRAINT CHK_Countries__length
    CHECK (LENGTH(country_name) <= 120)
);

CREATE TABLE Counties (
  county_id     INTEGER GENERATED ALWAYS AS IDENTITY,
  country_id    INTEGER NOT NULL,
  county_name   TEXT NOT NULL,

  CONSTRAINT PK_Counties
    PRIMARY KEY (county_id),

  CONSTRAINT CHK_Counties__length
    CHECK (LENGTH(county_name) <= 120),

  CONSTRAINT FK_Counties__city
    FOREIGN KEY (country_id)
    REFERENCES Countries(country_id)
);

CREATE TABLE Cities (
  city_id       INTEGER GENERATED ALWAYS AS IDENTITY,
  county_id     INTEGER NOT NULL,
  city_name     TEXT NOT NULL,

  CONSTRAINT PK_Cities
    PRIMARY KEY (city_id),
  
  CONSTRAINT CHK_Cities__length
    CHECK (LENGTH(city_name) <= 120),

  CONSTRAINT FK_Cities__county
    FOREIGN KEY (county_id)
    REFERENCES Counties(county_id)
);

CREATE TABLE Addresses (
  address_id    INTEGER GENERATED ALWAYS AS IDENTITY,
  line_1        TEXT NOT NULL,
  line_2        TEXT,
  line_3        TEXT,
  city_id       INTEGER NOT NULL,
  county_id     INTEGER NOT NULL,
  country_id    INTEGER NOT NULL,
  post_code     CHAR(16) NOT NULL,

  CONSTRAINT PK_Addresses
    PRIMARY KEY (address_id),

  CONSTRAINT CHK_Addresses__line_length_1
    CHECK (LENGTH(line_1) <= 120),
  CONSTRAINT CHK_Addresses__line_length_2
    CHECK (COALESCE(LENGTH(line_2) <= 120, TRUE)),
  CONSTRAINT CHK_Addresses__line_length_3
    CHECK (COALESCE(LENGTH(line_3) <= 120, TRUE)),

  CONSTRAINT FK_Addresses_county
    FOREIGN KEY (county_id)
    REFERENCES Counties(county_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_Addresses_city
    FOREIGN KEY (city_id)
    REFERENCES Cities(city_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_Addresses_country
    FOREIGN KEY (country_id)
    REFERENCES Countries(country_id)
    ON DELETE RESTRICT
);