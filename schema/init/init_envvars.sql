ALTER SYSTEM SET app.jwt_secret = 'my-jwt-secret';
SELECT pg_reload_conf();