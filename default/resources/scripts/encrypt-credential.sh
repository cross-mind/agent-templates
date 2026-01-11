#!/bin/sh
set -eu

usage() {
  cat >&2 <<'EOF'
Encrypt a credential and store it under resources/credentials/<NAME>.

Usage:
  resources/scripts/encrypt-credential.sh <CREDENTIAL_NAME>

By default, reads the secret from stdin (recommended):
  printf %s "$MY_SECRET" | resources/scripts/encrypt-credential.sh MY_SECRET_NAME

Key file can be overridden with CREDENTIALS_KEY_FILE (default: resources/credentials/private_key).
EOF
}

if [ "${1:-}" = "" ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 2
fi

credential_name="$1"

key_file="${CREDENTIALS_KEY_FILE:-resources/credentials/private_key}"
enc_file="resources/credentials/$credential_name"

if [ ! -f "$key_file" ]; then
  resources/scripts/create-credentials-key.sh "$key_file"
fi

mkdir -p "$(dirname "$enc_file")"
umask 077

if [ -t 0 ]; then
  echo "Refusing to read from terminal; pipe the value via stdin." >&2
  echo "Example: printf %s \"\$SECRET\" | $0 $credential_name" >&2
  exit 2
fi

openssl enc -aes-256-cbc -pbkdf2 -salt \
  -pass "file:$key_file" \
  -out "$enc_file"

chmod 600 "$enc_file" 2>/dev/null || true
echo "Wrote encrypted credential: $enc_file" >&2
