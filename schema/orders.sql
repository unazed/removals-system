CREATE TABLE Orders (
  order_id          INTEGER GENERATED ALWAYS AS IDENTITY,
  created_by        INTEGER NOT NULL,
  created_for       INTEGER NOT NULL,

  pickup_address    INTEGER NOT NULL,
  pickup_date       TIMESTAMP NOT NULL,
  delivery_address  INTEGER NOT NULL,

  created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT PK_Orders
    PRIMARY KEY (order_id),

  CONSTRAINT CHK_Orders__unique_addresses
    CHECK (pickup_address <> delivery_address),

  CONSTRAINT FK_Orders__created_by
    FOREIGN KEY (created_by)
    REFERENCES Users(user_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_Orders__pickup_address
    FOREIGN KEY (pickup_address)
    REFERENCES Addresses(address_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_Orders__delivery_address
    FOREIGN KEY (delivery_address)
    REFERENCES Addresses(address_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_Orders__created_for
    FOREIGN KEY (created_for)
    REFERENCES Users(user_id)
    ON DELETE RESTRICT
);

CREATE TABLE BidActions (
  bid_action_id     INTEGER GENERATED ALWAYS AS IDENTITY,
  order_id          INTEGER NOT NULL,
  bidder_id         INTEGER NOT NULL,
  bid_amount        DECIMAL(10, 2) NOT NULL,
  bid_timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  action_type       TEXT NOT NULL,

  CONSTRAINT PK_BidActions
    PRIMARY KEY (bid_action_id),

  CONSTRAINT CHK_BidActions__valid_bid
    CHECK (bid_amount > 0),

  CONSTRAINT FK_BidActions__order
    FOREIGN KEY (order_id)
    REFERENCES Orders(order_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_BidActions__bidder
    FOREIGN KEY (bidder_id)
    REFERENCES Users(user_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_BidActions__action_type
    FOREIGN KEY (action_type)
    REFERENCES BidActionType(action_name)
    ON DELETE RESTRICT
);

CREATE TABLE OrderStaff (
  order_id          INTEGER NOT NULL,
  staff_id          INTEGER NOT NULL,
  staff_role        TEXT NOT NULL,

  CONSTRAINT PK_OrderStaff
    PRIMARY KEY (order_id, staff_id),

  CONSTRAINT FK_OrderStaff__order
    FOREIGN KEY (order_id)
    REFERENCES Orders(order_id)
    ON DELETE CASCADE,
  CONSTRAINT FK_OrderStaff__staff
    FOREIGN KEY (staff_id)
    REFERENCES Users(user_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_OrderStaff__role
    FOREIGN KEY (staff_role)
    REFERENCES OrderStaffRoles(staff_role)
    ON DELETE RESTRICT
);

CREATE TABLE OrderItems (
  item_id           INTEGER NOT NULL,
  order_id          INTEGER NOT NULL,

  quantity          INTEGER NOT NULL DEFAULT 1,
  actual_weight_kg  DECIMAL(8,2),
  special_notes     TEXT,

  CONSTRAINT PK_OrderItems
    PRIMARY KEY (item_id, order_id),

  CONSTRAINT CHK_OrderItems__valid_weight
    CHECK (actual_weight_kg > 0),
  CONSTRAINT CHK_OrderItems__valid_quantity
    CHECK (quantity > 0),

  CONSTRAINT FK_OrderItems__item
    FOREIGN KEY (item_id)
    REFERENCES Items(item_id)
    ON DELETE RESTRICT,
  CONSTRAINT FK_OrderItems__order
    FOREIGN KEY (order_id)
    REFERENCES Orders(order_id)
    ON DELETE CASCADE
);