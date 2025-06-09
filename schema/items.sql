CREATE TABLE ItemCategories (
  category_id   INTEGER GENERATED ALWAYS AS IDENTITY,
  category_name TEXT NOT NULL,

  CONSTRAINT PK_ItemCategories
    PRIMARY KEY (category_id),

  CONSTRAINT CHK_ItemCategories__length
    CHECK (LENGTH(category_name) <= 60)
);

CREATE TABLE Items (
  item_id       INTEGER GENERATED ALWAYS AS IDENTITY,
  category_id   INTEGER NOT NULL,
  
  item_name     TEXT NOT NULL,
  item_description TEXT,
  
  length_cm     DECIMAL(10,2),
  width_cm      DECIMAL(10,2),
  height_cm     DECIMAL(10,2),
  weight_kg     DECIMAL(10,2),

  is_fragile    BOOLEAN DEFAULT FALSE,
  is_hazardous  BOOLEAN DEFAULT FALSE,
  requires_upright BOOLEAN DEFAULT FALSE,
  
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT PK_Items
    PRIMARY KEY (item_id),

  CONSTRAINT CHK_Items__valid_weight
    CHECK (weight_kg > 0),
  CONSTRAINT CHK_Items__valid_dimensions
    CHECK (length_cm > 0 AND width_cm > 0 AND height_cm > 0),
  CONSTRAINT CHK_Items__name_length
    CHECK (LENGTH(item_name) <= 120),
  CONSTRAINT CHK_Items__description_length
    CHECK (COALESCE(LENGTH(item_description) <= 240, TRUE)),

  CONSTRAINT FK_Items__category
    FOREIGN KEY (category_id)
    REFERENCES ItemCategories(category_id)
);