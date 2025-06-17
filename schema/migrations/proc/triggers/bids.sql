CREATE OR REPLACE FUNCTION utils.get_order_by_auction(p_auction_id INTEGER)
RETURNS INTEGER AS $$
  SELECT order_id
  FROM Orders
  WHERE auction_id = p_auction_id;
END;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION bid_insert_update()
RETURNS TRIGGER AS $$
DECLARE
  v_low_bid INTEGER;
  v_high_bid INTEGER;
  v_is_bidder_owner BOOLEAN;
BEGIN
  SELECT MIN(bid_amount), MAX(bid_amount)
  INTO v_low_bid, v_high_bid
  FROM BidActions
  WHERE auction_id = NEW.auction_id;
  AND action_type = 'bid';

  v_is_bidder_owner := (
    NEW.bidder_id = (
      SELECT created_by
      FROM Orders
      WHERE order_id = utils.get_order_by_auction(NEW.auction_id)
    )
  );
END;
$$ LANGUAGE plpgsql;

