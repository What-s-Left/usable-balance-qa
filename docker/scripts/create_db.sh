#!/bin/bash
set -e

POSTGRES="psql --username ${POSTGRES_USER}"

echo "Creating database: ${DB_DEFAULT_NAME}"

$POSTGRES <<EOSQL
CREATE DATABASE ${DB_DEFAULT_NAME} OWNER ${DB_DEFAULT_USER};
EOSQL

