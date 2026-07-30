#!/bin/bash
set -e
set -u

function create_user_and_database() {
    local database=$1
    echo "  Creating database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        SELECT 'CREATE DATABASE $database' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$database')\gexec
EOSQL
}

if [ -n "$POSTGRES_DB" ]; then
    # Если в будущем понадобятся еще базы данных, можно перечислить их через запятую
    for db in $(echo "wallet_db_test" | tr ',' ' '); do
        create_user_and_database $db
    done
    echo "Multiple databases created"
fi
