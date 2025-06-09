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

  \i 'triggers/bids.sql'
  \i 'triggers/items.sql'
  \i 'triggers/users.sql'
  \i 'triggers/orders.sql'

  \i 'init/init_types.sql'
  \i 'init/init_countries.sql'

  \i 'init/init_envvars.sql'
  \i 'init/init_permissions.sql'
COMMIT;