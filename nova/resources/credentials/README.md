# Credentials (Identity & Secrets)

This directory is for managing identity information and sensitive credentials (tokens / passwords / keys / secrets) collected during user communication.

## 1) Registry: `resources/credentials/credentials.json`
- Record user-provided identity information in `resources/credentials/credentials.json`.
- Minimum fields per entry:
  - `description`: what it is and why it exists
  - `updated_at`: ISO 8601 timestamp
  - `value`: the value
- For sensitive items (password/key/secret/token): do not store the real value in `credentials.json`. Store a variable reference instead (e.g. `IVAN_GITHUB_PERSONAL_TOKEN` or `${IVAN_GITHUB_PERSONAL_TOKEN}`).

Example structure:
```json
[
  {
    "key": "IVAN_GITHUB_PERSONAL_TOKEN",
    "description": "GitHub personal token (scopes: ...)",
    "updated_at": "2026-01-11T00:00:00Z",
    "value": "${IVAN_GITHUB_PERSONAL_TOKEN}"
  }
]
```

## 2) Local encrypted storage: `resources/credentials/<NAME>`
- Keep a local encryption key at `resources/credentials/private_key` (local only; never commit).
- Store each secret as an encrypted file at `resources/credentials/<NAME>` (e.g. `resources/credentials/IVAN_GITHUB_PERSONAL_TOKEN`).

Create the local encryption key (optional script):
```sh
resources/scripts/create-credentials-key.sh
```

Encrypt a secret (script):
```sh
# Automatically creates `resources/credentials/private_key` if missing.
printf %s "YOUR_TOKEN_HERE" | resources/scripts/encrypt-credential.sh IVAN_GITHUB_PERSONAL_TOKEN
```

## 3) Use via env vars only + masked verification
- Never print or paste the real secret value into user-facing messages/logs.
- Decrypt and inject into an environment variable, then verify with a masked output, and use the env var in commands.

Load a credential into the current shell (script; must be sourced):
```sh
. resources/scripts/load-credential.sh IVAN_GITHUB_PERSONAL_TOKEN
# or map to a different env var name:
. resources/scripts/load-credential.sh IVAN_GITHUB_PERSONAL_TOKEN GITHUB_TOKEN
```

The script prints a masked value (e.g. `GITHUB_TOKEN=cr_xxx***`) and exports the env var for subsequent commands.
