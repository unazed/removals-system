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

CREATE OR REPLACE FUNCTION create_user_address(
  p_token TEXT,
  p_line_1 TEXT, p_line_2 TEXT, p_line_3 TEXT,
  p_city TEXT, p_county TEXT, p_country TEXT, p_post_code TEXT,
  p_address_type TEXT DEFAULT 'home'
)
RETURNS result_t AS $$
DECLARE
  user_session JSON;
  new_address_id INTEGER;
  stored_county_id INTEGER;
  stored_city_id INTEGER;
  stored_country_id INTEGER;
BEGIN
  user_session := decode_token(p_token);

  IF user_session IS NULL THEN
    RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
  END IF;

  SELECT country_id INTO stored_country_id
  FROM Countries
  WHERE country_name = p_country;

  IF NOT FOUND THEN
    RETURN make_error_result(
      'INVALID_COUNTRY',
      FORMAT('Invalid country: %', p_country)
    );
  END IF;

  SELECT county_id INTO stored_county_id
  FROM Counties
  WHERE county_name = p_county;

  IF NOT FOUND THEN
    RETURN make_error_result(
      'INVALID_COUNTY',
      FORMAT('Invalid county: %', p_county)
    );
  END IF;

  SELECT city_id INTO stored_city_id
  FROM Cities
  WHERE city_name = p_city;

  IF NOT FOUND THEN
    RETURN make_error_result(
      'INVALID_CITY',
      FORMAT('Invalid city: %', p_city)
    );
  END IF;

  INSERT INTO Addresses(
    line_1, line_2, line_3,
    city_id, county_id, country_id,
    post_code
  )
  VALUES (
    p_line_1, p_line_2, p_line_3,
    stored_city_id, stored_county_id, stored_country_id,
    p_post_code
  )
  RETURNING address_id INTO new_address_id;

  INSERT INTO UserAddresses(user_id, address_id, address_type)
  VALUES ((user_session->>'user_id')::INTEGER, new_address_id, p_address_type);

  RETURN make_success_result();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_user_addresses(p_token TEXT)
RETURNS result_t AS $$
DECLARE
    user_session JSON;
    address_data JSONB;
BEGIN
    user_session := decode_token(p_token);

    IF user_session IS NULL THEN
        RETURN make_error_result('INVALID_SESSION', 'Invalid session token');
    END IF;

    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'address_id', Addr.address_id,
                'line_1', Addr.line_1,
                'line_2', Addr.line_2,
                'line_3', Addr.line_3,
                'post_code', Addr.post_code,
                'address_type', UA.address_type,
                'city_name', C.city_name,
                'county_name', Cty.county_name,
                'country_name', Cntry.country_name
            )
        ),
        '[]'::jsonb
    ) INTO address_data
    FROM UserAddresses UA
    JOIN Addresses Addr  ON UA.address_id = Addr.address_id
    JOIN Cities C        ON Addr.city_id = C.city_id
    JOIN Counties Cty    ON Addr.county_id = Cty.county_id
    JOIN Countries Cntry ON Addr.country_id = Cntry.country_id
    WHERE UA.user_id = (user_session->>'user_id')::INTEGER;

    RETURN make_success_result(address_data);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;