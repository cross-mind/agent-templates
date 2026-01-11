#!/bin/sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "Usage (must be sourced): . resources/scripts/load-credential.sh <CREDENTIAL_NAME> [ENV_VAR]" >&2
  return 2 2>/dev/null || exit 2
fi

credential_name="$1"
env_var="${2:-$credential_name}"
key_file="${CREDENTIALS_KEY_FILE:-resources/credentials/private_key}"
enc_file="resources/credentials/$credential_name"

first_char="$(printf %s "$env_var" | cut -c1)"
case "$first_char" in
  [A-Za-z_]) ;;
  *)
    echo "Invalid env var name (must start with [A-Za-z_]): $env_var" >&2
    return 2 2>/dev/null || exit 2
    ;;
esac

case "$env_var" in
  *[!A-Za-z0-9_]*)
    echo "Invalid env var name (must match [A-Za-z_][A-Za-z0-9_]*): $env_var" >&2
    return 2 2>/dev/null || exit 2
    ;;
esac

if [ ! -f "$key_file" ]; then
  echo "Missing credentials key file: $key_file" >&2
  echo "Run: resources/scripts/create-credentials-key.sh" >&2
  return 1 2>/dev/null || exit 1
fi

if [ ! -f "$enc_file" ]; then
  echo "Missing encrypted credential file: $enc_file" >&2
  return 1 2>/dev/null || exit 1
fi

value="$(
  openssl enc -d -aes-256-cbc -pbkdf2 \
    -pass "file:$key_file" \
    -in "$enc_file"
)"

eval "export $env_var=\$value"

prefix="$(printf %s "$value" | cut -c1-4)"
echo "$env_var=cr_${prefix}***" >&2

unset value
