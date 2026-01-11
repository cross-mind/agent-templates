# Working Notes (templates submodule)

## Repo Boundary (Important)
- This directory is a **git submodule**. Do **not** change files in the parent repo while working here.
- Before/after any work, run `git status` in this directory and confirm only submodule files changed.

## Dependency & Commands (uv)
- Use `uv` **inside this submodule**:
  - Install/sync: `uv sync` (tests: `uv sync --extra test`)
  - Run tests: `uv run pytest`
- Known gotcha: `uv run lumina-templates ...` / `uv run -m template_sync.cli ...` may fail due to sandbox access to the global uv cache or may panic on macOS.
  - Preferred workaround: run the entrypoint directly: `.venv/bin/lumina-templates ...`

## Documentation & Non-Interactive Policy
- Documentation in this repo should be written in **English**.
- Never use interactive prompts/commands (no TTY reads, no `--prompt`, no password prompts). Prefer piping via stdin and non-interactive flags.

## `CLAUDE.md` Managed Block Markers
- Each target template `CLAUDE.md` must include **exactly one** managed block:
  - `<general_rules>` (on its own line) … `</general_rules>` (on its own line)
- Avoid writing raw `<general_rules>` / `</general_rules>` / `<general_rules>...</general_rules>` text elsewhere in `CLAUDE.md` (even in code fences), or the sync parser may mis-detect it.
  - If you need to mention it, use escaped text like `&lt;general_rules&gt;...`.
- Put template-specific rules **outside** the managed block.

## Daily Logs
- Daily logs live under `daily_logs/` (not under `resources/templates/`).
- The default example filename is `daily_logs/YYYY-MM-DD.md`.

## Credentials (Identity & Secrets)
- Store the credential registry at `resources/credentials/credentials.json` (sensitive values referenced by variable name, not stored in plaintext there).
- Store encrypted credential payloads at `resources/credentials/<NAME>` and keep the local encryption key at `resources/credentials/private_key` (local only; never commit).
- Use scripts under `resources/scripts/`:
  - `create-credentials-key.sh` (create local key file)
  - `encrypt-credential.sh` (encrypt from stdin; auto-creates key if missing)
  - `load-credential.sh` (decrypt and export env var; prints masked value)

## Workspace Conventions
- Store meaningful external references in `references/` as URL/path + key points/value (avoid copying full original text).
- Store user-facing deliverables produced during work in `artifacts/` with a clear folder/file structure.
- When recurring behavior patterns are identified, create a skill and iterate its description based on mistakes/lessons learned.
- If a task cannot proceed due to identity/permissions constraints, proactively ask the Owner for help.

## Sync Policy Reminders
- `ONBOARDING_GUIDE.md` and `IDENTITY.md` are `never_update` (do not auto-overwrite).
- Keep `default/memory/memory.jsonl` empty (0 bytes) to avoid noisy diffs.
- Skills sync rule: only update skills when the target already has a same-named skill directory.
