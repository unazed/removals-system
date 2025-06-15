CREATE INDEX IDX_Countries__name ON Countries(country_name);
CREATE INDEX IDX_Counties__country_name ON Counties(country_id, county_name);
CREATE INDEX IDX_Cities__county ON Cities(county_id);