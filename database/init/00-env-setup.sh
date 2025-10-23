#!/usr/bin/env bash
set -euo pipefail

: "${POSTGRES_DB:?POSTGRES_DB missing}"
: "${POSTGRES_USER:?POSTGRES_USER missing}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD missing}"

envsubst < /docker-entrypoint-initdb.d/01-db-setup.sql.tmpl > /docker-entrypoint-initdb.d/01-db-setup.sql
