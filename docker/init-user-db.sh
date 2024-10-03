-- docker blog_db script

-- /docker-entrypoint-initdb.d/init-user-db.sh

#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE $POSTGRES_USER WITH SUPERUSER LOGIN PASSWORD '$POSTGRES_PASSWORD';
    CREATE DATABASE $POSTGRES_DB;
EOSQL