#!/usr/bin/env sh
set -eu

if [ "${1:-}" = "postgres" ] && [ ! -s "${PGDATA}/PG_VERSION" ] && [ -z "${MIRROR_DEMO_PASSWORD:-}" ]; then
    echo "MIRROR_DEMO_PASSWORD must be set before initializing an empty database volume." >&2
    exit 1
fi

exec /usr/local/bin/docker-entrypoint.sh "$@"
