#!/bin/sh
set -eu

FRONTEND_DIR=${FRONTEND_DIR:-/app/frontend_dist}
API_URL=${API_URL:-}
PORT=${PORT:-8000}

echo "ENTRYPOINT: FRONTEND_DIR=$FRONTEND_DIR"
echo "ENTRYPOINT: API_URL=${API_URL:+***set***}"
echo "ENTRYPOINT: PORT=$PORT"

if [ -n "$API_URL" ] && [ -d "$FRONTEND_DIR" ]; then
  echo "Injecting API_URL into frontend assets (POSIX safe)..."

  find "$FRONTEND_DIR" -type f | while IFS= read -r file; do
    sed -i "s|http://localhost:8000|$API_URL|g" "$file" || true
  done

  echo "Injection done."
else
  echo "No injection performed (missing API_URL or folder)."
fi

# start the server
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
