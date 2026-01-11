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

## `CLAUDE.md` Managed Block Markers
- Each target template `CLAUDE.md` must include **exactly one** managed block:
  - `<general_rules>` (on its own line) … `</general_rules>` (on its own line)
- Avoid writing raw `<general_rules>` / `</general_rules>` / `<general_rules>...</general_rules>` text elsewhere in `CLAUDE.md` (even in code fences), or the sync parser may mis-detect it.
  - If you need to mention it, use escaped text like `&lt;general_rules&gt;...`.
- Put template-specific rules **outside** the managed block.

## Sync Policy Reminders
- `ONBOARDING_GUIDE.md` and `IDENTITY.md` are `never_update` (do not auto-overwrite).
- Keep `default/memory/memory.jsonl` empty (0 bytes) to avoid noisy diffs.
- Skills sync rule: only update skills when the target already has a same-named skill directory.
