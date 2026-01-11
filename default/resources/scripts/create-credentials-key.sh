#!/bin/sh
set -eu

key_file="${1:-resources/credentials/private_key}"

if [ -f "$key_file" ]; then
  echo "Credentials key already exists: $key_file" >&2
  exit 0
fi

umask 077
mkdir -p "$(dirname "$key_file")"

openssl rand -base64 32 >"$key_file"
chmod 600 "$key_file" 2>/dev/null || true

echo "Created credentials key: $key_file" >&2
