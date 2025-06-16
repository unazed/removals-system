BEGIN;
  CREATE EXTENSION IF NOT EXISTS pgcrypto;
  CREATE EXTENSION IF NOT EXISTS pgjwt;

  \i 'schema/types.sql'
  \i 'schema/phone-numbers.sql'
  \i 'schema/addresses.sql'
  \i 'schema/businesses.sql'
  \i 'schema/users.sql'
  \i 'schema/items.sql'
  \i 'schema/orders.sql'
COMMIT;

BEGIN;
  \i 'schema/migrations/1-types.sql'
  \i 'schema/migrations/2-countries.sql'
COMMIT;

\i 'schema/migrations/3-envvars.sql'

BEGIN;
  \i 'schema/migrations/proc/get_envvars.sql'
  \i 'schema/migrations/proc/login.sql'
  \i 'schema/migrations/proc/register.sql'
  \i 'schema/migrations/proc/email.sql'
  \i 'schema/migrations/proc/addresses.sql'
  \i 'schema/migrations/proc/util.sql'
  \i 'schema/migrations/proc/forgot_password.sql'
  \i 'schema/migrations/proc/phone_numbers.sql'
  \i 'schema/migrations/proc/types.sql'
COMMIT;

BEGIN;
  \i 'schema/migrations/proc/triggers/bids.sql'
  \i 'schema/migrations/proc/triggers/items.sql'
  \i 'schema/migrations/proc/triggers/users.sql'
  \i 'schema/migrations/proc/triggers/orders.sql'
COMMIT;

BEGIN;
  \i 'schema/migrations/4-permissions.sql'
  \i 'schema/migrations/5-triggers.sql'
  \i 'schema/migrations/6-indexes.sql'
COMMIT;

BEGIN;
  \i 'schema/migrations/mock/create_users.sql'
COMMIT;