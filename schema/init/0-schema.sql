BEGIN;
  CREATE EXTENSION IF NOT EXISTS pgcrypto;
  CREATE EXTENSION IF NOT EXISTS pgjwt;

  \i 'types.sql'
  \i 'phone-numbers.sql'
  \i 'addresses.sql'
  \i 'businesses.sql'
  \i 'users.sql'
  \i 'items.sql'
  \i 'orders.sql'
COMMIT;

BEGIN;
  \i 'triggers/bids.sql'
  \i 'triggers/items.sql'
  \i 'triggers/users.sql'
  \i 'triggers/orders.sql'
COMMIT;

BEGIN;
  \i 'init/1-types.sql'
  \i 'init/2-countries.sql'
COMMIT;

\i 'init/3-envvars.sql'

BEGIN;
  \i 'init/proc/get_envvars.sql'
  \i 'init/proc/login.sql'
  \i 'init/proc/register.sql'
COMMIT;

BEGIN;
  \i 'init/4-permissions.sql'
COMMIT;