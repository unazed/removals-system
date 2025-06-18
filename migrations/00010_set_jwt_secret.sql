-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS app_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- +goose ENVSUB ON
INSERT INTO app_config (key, value) 
VALUES ('jwt_secret', '${JWT_SECRET}')
ON CONFLICT (key) DO UPDATE SET 
    value = EXCLUDED.value,
    created_at = CURRENT_TIMESTAMP;
-- +goose ENVSUB OFF
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DELETE FROM app_config WHERE key = 'jwt_secret';
DROP TABLE app_config;
-- +goose StatementEnd