#!/bin/bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo "Creating database role: ${DB_DEFAULT_USER}"

$POSTGRES <<-EOSQL
CREATE USER ${DB_DEFAULT_USER} WITH CREATEDB PASSWORD '${DB_DEFAULT_PASS}';
EOSQL


