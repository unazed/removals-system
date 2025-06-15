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
  \i 'migrations/1-types.sql'
  \i 'migrations/2-countries.sql'
COMMIT;

\i 'migrations/3-envvars.sql'

BEGIN;
  \i 'migrations/proc/get_envvars.sql'
  \i 'migrations/proc/login.sql'
  \i 'migrations/proc/register.sql'
  \i 'migrations/proc/email.sql'
  \i 'migrations/proc/addresses.sql'
  \i 'migrations/proc/util.sql'
COMMIT;

BEGIN;
  \i 'migrations/proc/triggers/bids.sql'
  \i 'migrations/proc/triggers/items.sql'
  \i 'migrations/proc/triggers/users.sql'
  \i 'migrations/proc/triggers/orders.sql'
COMMIT;

BEGIN;
  \i 'migrations/4-permissions.sql'
  \i 'migrations/5-triggers.sql'
  \i 'migrations/6-indexes.sql'
COMMIT;