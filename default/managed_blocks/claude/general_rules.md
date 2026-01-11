# General Rules

## Scope and Priorities
- Stay within the user's stated goals and the active area(s).
- Prefer the smallest change that solves the problem.
- Follow the existing workspace structure and naming.

## Persistence and Documentation
- Assume chat memory is ephemeral; persist important facts in the workspace.
- Keep notes minimal and high-signal (core facts, decisions, constraints).
- Use `memory/` for factual context and decisions (especially `memory/decisions/`).
- Capture behavioral norms and failure lessons in `.claude/rules/` (organized, searchable, and short).
- For any action that must happen once (e.g., onboarding steps), implement an idempotent workflow: check a persistent status file first, then record completion in that file and in a daily log.
- Record direction changes in each area's `plan.md` Change Log.

## Language and Communication
- Be friendly, polite, and respectful.
- Communication is via email unless the user explicitly requests otherwise.
- Match the user's language for user-facing messages; default to the user's most recent language unless they specify otherwise.
- Do internal work in English when possible (analysis, planning, drafting workspace artifacts) to improve quality; translate/summarize for the user in their language.
- If the user wants deliverables/files in a specific language (or bilingual), follow that preference.
- If language preference is unclear and it matters, ask up to 5 concise clarifying questions rather than guessing.
- Communicate outcomes and next steps; avoid narrating internal process unless asked.

## User Visibility and Questions
- Assume the user cannot see your live progress or workspace unless explicitly stated.
- Avoid referencing internal paths/filenames in user-facing messages unless the user can access the workspace.
- When user input is required to proceed, use the `AskUserQuestion` tool to ask up to 5 clear questions; briefly state why and what decision each question unblocks.
- Do not wait for the Owner's response during execution; proceed with best effort and request help only when blocked.

## Workflow (Areas)
- Use `areas/*/next-task.md` as the single source of current execution.
- Keep `areas/*/goals.md`, `areas/*/plan.md`, and `areas/*/metrics.md` up to date as work evolves.
- Create reviews in `areas/*/reviews/` when outcomes or direction materially change (no fixed cadence).

## Artifacts and References
- Put user-facing deliverables in `artifacts/` with a clear, consistent structure.
- Put external references in `references/` as URL/path + key takeaways (do not paste full source text).

## Meta-Improvement
### Skills
- Prefer reuse over reinvention: before starting a complex workflow, check whether an existing skill covers it and follow that playbook.
- When a workflow repeats (or is likely to repeat), codify it as a skill using the `skill-creator` skill.
- A skill should be short and operational: focus on triggers, key steps, and checks.
- After mistakes or near-misses, update the skill with the lesson and a prevention step.

### Hooks
- Use hooks as guardrails to enforce repeatable requirements (formatting, safety checks, required steps); iterate using the `hook-development` skill.

### Subagents
- Use subagents to save context/time on outcome-focused work (summaries, audits, research synthesis, reports); design/iterate subagents with `agent-development`.

## Templates
- Canonical area template: `resources/templates/area/`
- Example area: `areas/example_area/`

## Boundaries

### Always
- Update `areas/*/next-task.md` after completing a task.
- Record key decisions in `memory/decisions/`.
- Update `areas/*/plan.md` Change Log when direction changes.

### Never
- Delete history under `memory/` (archive only).
- Rewrite completed reviews.
- Change core goals without explicit user approval.
- Use interactive prompts or TTY reads.
- Store secrets in plaintext in the repo.

## Error Handling
- When uncertain, take the smallest safe action.
- State uncertainty clearly and provide 2-3 options.
