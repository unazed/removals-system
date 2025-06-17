CREATE OR REPLACE FUNCTION utils.get_order_by_auction(p_auction_id INTEGER)
RETURNS INTEGER AS $$
  SELECT order_id
  FROM Orders
  WHERE auction_id = p_auction_id;
$$ LANGUAGE sql;