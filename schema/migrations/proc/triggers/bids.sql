CREATE OR REPLACE FUNCTION bid_insert_update()
RETURNS TRIGGER AS $$
DECLARE
  v_low_bid INTEGER;
  v_is_bidder_owner BOOLEAN;
  v_min_price INTEGER;
  v_winning_bidder INTEGER;
  v_winning_bid_amt INTEGER;
  v_withdraw_bid_id INTEGER;
BEGIN
  IF (SELECT is_closed FROM Auctions WHERE auction_id = NEW.auction_id) THEN
    RAISE EXCEPTION 'Cannot create/alter bids on closed auction';
  END IF;

  SELECT MIN(bid_amount) INTO v_low_bid
  FROM BidActions
  WHERE auction_id = NEW.auction_id
  AND action_type = 'bid';

  SELECT min_bid INTO v_min_price
  FROM Auctions
  WHERE auction_id = NEW.auction_id;

  v_is_bidder_owner := (
    NEW.bidder_id = (
      SELECT created_by
      FROM Orders
      WHERE order_id = utils.get_order_by_auction(NEW.auction_id)
    )
  );

  IF NEW.action_type = 'bid' THEN
    IF v_is_bidder_owner THEN
      RAISE EXCEPTION 'Order creator cannot place bids';
    ELSIF NEW.bid_amount < v_min_price THEN
      RAISE EXCEPTION 'Cannot place a bid for less than the minimum price';
    ELSIF v_low_bid IS NOT NULL AND NEW.bid_amount >= v_low_bid THEN
      RAISE EXCEPTION 'Cannot place a bid for higher than the least bid';
    END IF;
  ELSIF NEW.action_type = 'accept' THEN
    IF NOT v_is_bidder_owner THEN
      RAISE EXCEPTION 'Order bidders cannot accept bids';
    ELSIF NEW.bid_amount < v_low_bid THEN
      RAISE EXCEPTION 'Cannot accept bid for less than the least bid';
    END IF;

    SELECT bidder_id, bid_amount
    INTO v_winning_bidder, v_winning_bid_amt
    FROM BidActions
    WHERE auction_id = NEW.auction_id
      AND action_type = 'bid'
      AND bid_amount <= NEW.bid_amount
    ORDER BY bid_amount DESC
    LIMIT 1;

    IF NOT FOUND THEN
      RAISE EXCEPTION 'No qualifying bids found for acceptance';
    END IF;

    UPDATE Auctions
    SET
      winning_bidder_id = v_winning_bidder,
      winning_bid_amt = v_winning_bid_amt,
      is_closed = TRUE
    WHERE auction_id = NEW.auction_id;
  ELSIF NEW.action_type = 'withdraw' THEN
    IF v_is_bidder_owner THEN
      RAISE EXCEPTION 'Order creator cannot withdraw bids';
    END IF;

    UPDATE BidActions
       SET action_type = 'withdraw'
     WHERE auction_id = NEW.auction_id
       AND action_type = 'bid'
       AND bidder_id = NEW.bidder_id
       AND bid_amount = NEW.bid_amount;

    IF NOT FOUND THEN
      RAISE EXCEPTION 'No matching bid found to withdraw';
    END IF;

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

