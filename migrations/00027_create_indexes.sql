-- +goose Up
-- +goose StatementBegin
CREATE INDEX IDX_Countries__name ON Countries(country_name);
CREATE INDEX IDX_Counties__country_name ON Counties(country_id, county_name);
CREATE INDEX IDX_Cities__county ON Cities(county_id);
CREATE INDEX IDX_Businesses__crn on Businesses(crn_no);
CREATE UNIQUE INDEX UDX_BusinessStaff__single_executive
ON BusinessStaff (business_id)
WHERE user_role = 'executive';
CREATE INDEX IDX_BusinessResources__business_resource
ON BusinessResources(business_id, resource_name);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP INDEX IDX_BusinessResources__business_resource;
DROP INDEX UDX_BusinessStaff__single_executive;
DROP INDEX IDX_Businesses__crn;
DROP INDEX IDX_Cities__county;
DROP INDEX IDX_Counties__country_name;
DROP INDEX IDX_Countries__name;
-- +goose StatementEnd