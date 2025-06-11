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
  \i 'init/1-types.sql'
  \i 'init/2-countries.sql'
COMMIT;

\i 'init/3-envvars.sql'

BEGIN;
  \i 'init/proc/get_envvars.sql'
  \i 'init/proc/login.sql'
  \i 'init/proc/register.sql'
  \i 'init/proc/email.sql'
  \i 'init/proc/addresses.sql'
COMMIT;

BEGIN;
  \i 'init/proc/triggers/bids.sql'
  \i 'init/proc/triggers/items.sql'
  \i 'init/proc/triggers/users.sql'
  \i 'init/proc/triggers/orders.sql'
COMMIT;

BEGIN;
  \i 'init/4-permissions.sql'
  \i 'init/5-triggers.sql'
  \i 'init/6-indexes.sql'
COMMIT;