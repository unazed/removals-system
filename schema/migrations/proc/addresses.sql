CREATE OR REPLACE FUNCTION get_countries()
RETURNS TABLE(code TEXT, name TEXT) AS $$
  SELECT country_code, country_name
  FROM Countries;
$$ LANGUAGE sql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_counties(p_country_name TEXT)
RETURNS TABLE(name TEXT) AS $$
  SELECT county_name
  FROM Counties Cty
  JOIN Countries Ctry ON Cty.country_id = Ctry.country_id
  WHERE Ctry.country_name = p_country_name;
$$ LANGUAGE sql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_cities(p_country_name TEXT, p_county_name TEXT)
RETURNS TABLE(name TEXT) as $$
    SELECT city_name
    FROM Cities City
    JOIN Counties Cty ON City.county_id = Cty.county_id
    JOIN Countries Ctry ON Cty.country_id = Ctry.country_id
    WHERE Ctry.country_name = p_country_name
    AND Cty.county_name = p_county_name;
$$ LANGUAGE sql SECURITY DEFINER;