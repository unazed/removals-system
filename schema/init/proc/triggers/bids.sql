CREATE OR REPLACE FUNCTION bid_modify()
RETURNS trigger AS $$
DECLARE
  order_creator               INTEGER;
  order_customer              INTEGER;
  recent_active_bid_amount    DECIMAL(10, 2);
  recent_active_bid_user      INTEGER;
  accepted_bid_action         INTEGER;
BEGIN
  SELECT created_by, created_for INTO order_creator, order_customer
  FROM Orders
  WHERE order_id = NEW.order_id;

  IF order_creator IS NULL THEN
    RAISE EXCEPTION 'Order % does not exist', NEW.order_id;
  ELSIF EXISTS (SELECT 1 FROM BidActions WHERE order_id = NEW.order_id AND bid_status = 'accepted') THEN
    RAISE EXCEPTION 'Cannot create a bid for an order which is finalised';
  END IF;

  SELECT bid_amount, bidder_id INTO recent_active_bid_amount, recent_active_bid_user
  FROM BidActions
  WHERE bid_status = 'active'
  AND order_id = NEW.order_id
  AND bidder_id <> order_customer
  ORDER BY bid_timestamp DESC
  LIMIT 1; 

  IF NEW.action_type = 'bid' THEN
    IF recent_active_bid_amount IS NOT NULL AND NEW.bidder_id = order_customer THEN
      IF NEW.bid_amount >= recent_active_bid_amount THEN
        RAISE EXCEPTION 'Customer bids must be lower than the last bid (%.%)', recent_active_bid_amount, NEW.bid_amount;
      END IF;
    ELSIF recent_active_bid_amount IS NOT NULL AND NEW.bid_amount <= recent_active_bid_amount THEN
      RAISE EXCEPTION 'Service provider bids must be higher than the last bid (%.%)', recent_active_bid_amount, NEW.bid_amount;
    END IF;
  ELSIF NEW.action_type = 'accept' THEN
    IF NEW.bidder_id <> order_customer THEN
      RAISE EXCEPTION 'Non-customer attempted to accept bid';
    END IF;

    SELECT bid_action_id INTO accepted_bid_action
    FROM BidActions
    WHERE bid_amount = NEW.bid_amount
    AND order_id = NEW.order_id
    AND bid_status = 'active';

    IF accepted_bid_action IS NULL THEN
      RAISE EXCEPTION 'No active bid matching the acceptance criteria (amt.: %, order ID: %)', NEW.bid_amount, NEW.order_id;
    END IF;

    UPDATE BidActions
    SET bid_status = 'accepted'
    WHERE bid_action_id = accepted_bid_action;

    RETURN NULL;
  ELSIF NEW.action_type = 'withdraw' THEN
    UPDATE BidActions 
      SET bid_status = 'withdrawn'
      WHERE order_id = NEW.order_id 
      AND bidder_id = NEW.bidder_id 
      AND bid_amount = NEW.bid_amount 
      AND bid_status = 'active';
        
    IF NOT FOUND THEN
      RAISE EXCEPTION 'No active bid found to withdraw for amount %', NEW.bid_amount;
    END IF;

    RETURN NULL;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

