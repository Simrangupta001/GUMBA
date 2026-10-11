#!/bin/sh
set -e

echo "[entrypoint] Initialising database (tables + roles)..."
python -m app.init_db

echo "[entrypoint] Starting: $*"
exec "$@"