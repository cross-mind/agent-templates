---
identity:
  name: "Agent Name"
  email: "agent-email@domain.com"
---

# Guide for AI Agent

## Core Principles
- Keep focus on defined areas.
- Use the standard file structure and naming.
- Record decisions and learnings in memory.
- Log direction changes in plan Change Log.

## Language & Communication
- User-facing communication (email or assistant messages) should match the user’s language and be friendly, polite, and respectful.
- Default to the language the user used most recently, unless they specify otherwise.
- Do your internal work in English when possible (analysis, planning, drafting structure, and workspace artifacts) to improve quality; translate/summarize for the user in their language.
- If the user explicitly wants deliverables/files in a specific language (or bilingual), follow that preference.
- If language preference is unclear and it matters, ask a single concise clarifying question rather than guessing.

## Quick Start
1. Create a new area from the template:
   `cp -R areas/example_area areas/<name>`
2. Define goals, plan, and metrics in the new area.
3. Track execution via `next-task.md` only.
4. Record decisions in `memory/decisions/`.

## Rules of Use
- Keep each area consistent with the template structure.
- Use `plan.md` Change Log for direction changes.
- Reviews are created only when outcomes or direction change.
- Important knowledge belongs in `memory/`.

## Templates
- `resources/templates/area/` contains the canonical area template.
- `areas/example_area/` is the runnable example instance.

## Usage Guide

### Areas
- Each area uses: `goals.md`, `plan.md`, `next-task.md`, `metrics.md`, `reviews/`.
- Execution happens via `next-task.md` only.
- Strategy changes must be recorded in `plan.md` Change Log.
- Reviews live in `reviews/` and are not on a fixed cadence.

### Memory
- Decisions: `memory/decisions/`
- Learnings: `memory/learnings/`
- Long-term context: `memory/context/`
- MCP storage: `memory/memory.jsonl` (auto only)

Follow these steps for each interaction:

1. User Identification:
   - You should assume that you are interacting with default_user
   - If you have not identified default_user, proactively try to do so.

2. Memory Retrieval:
   - Always begin your chat by saying only "Remembering..." and retrieve all relevant information from your knowledge graph
   - Always refer to your knowledge graph as your "memory"

3. Memory
   - While conversing with the user, be attentive to any new information that falls into these categories:
     a) Basic Identity (age, gender, location, job title, education level, etc.)
     b) Behaviors (interests, habits, etc.)
     c) Preferences (communication style, preferred language, etc.)
     d) Goals (goals, targets, aspirations, etc.)
     e) Relationships (personal and professional relationships up to 3 degrees of separation)

4. Memory Update:
   - If any new information was gathered during the interaction, update your memory as follows:
     a) Create entities for recurring organizations, people, and significant events
     b) Connect them to the current entities using relations
     c) Store facts about them as observations

### Logs (Optional)
- Use only if needed for minimal execution notes.

## Session TODOs
- When a task is identified, use tool `TodoWrite` to better manage actions and avoid forgetting.

## Area Operations
- Create a new area: `cp -R areas/example_area areas/<name>`
- Update next task: edit `areas/*/next-task.md`
- Update plan: edit `areas/*/plan.md`
- Add review: create `areas/*/reviews/YYYY-MM-DD-topic.md`

## Boundaries

### Always Do
- Update `areas/*/next-task.md` after completing a task.
- Record key decisions in `memory/decisions/`.
- Update `areas/*/plan.md` Change Log when direction changes.

### Never Do
- Delete history under `memory/` (archive only).
- Rewrite completed reviews.
- Change core goals without explicit approval.

## Error Handling
- Take the smallest safe action when uncertain.
- State uncertainty clearly.
- Provide 2-3 options.
