CREATE OR REPLACE FUNCTION get_type_values(p_table TEXT)
RETURNS TABLE(value TEXT) AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'types' AND table_name = p_table
  ) THEN
    RAISE EXCEPTION 'Invalid table name: %. Only tables from "types" schema are allowed.', p_table;
  END IF;

  RETURN QUERY
  EXECUTE format('SELECT * FROM %I', p_table);
END;
$$
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = types;

CREATE OR REPLACE FUNCTION get_type_table_names()
RETURNS TABLE(name TEXT) AS $$
  SELECT table_name
  FROM information_schema.tables
  WHERE table_schema = 'types'
  AND table_type = 'BASE TABLE'
  ORDER BY table_name;
$$
LANGUAGE sql SECURITY DEFINER
SET search_path = public;