DROP FUNCTION IF EXISTS get_length_constraint;
CREATE OR REPLACE FUNCTION get_length_constraint(p_table TEXT, p_column TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT character_maximum_length 
        FROM information_schema.columns 
        WHERE table_name = p_table 
        AND column_name = p_column
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER IMMUTABLE STRICT;