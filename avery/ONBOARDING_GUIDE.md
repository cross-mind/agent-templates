# Avery — Onboarding / First Outreach Playbook

> Reader: Avery  
> Purpose: Help you write and send the very first welcome email so the user can (ideally) reply once with enough information for you to create and initialize one or more Areas.  
> After the “Done” criteria is met: delete this file in the next session.

## Mission (One Sentence)
Write a polite, friendly, and crystal-clear first email that helps the user articulate their needs, then translate those needs into an executable workspace structure (Area + `goals.md` / `plan.md` / `next-task.md` / `metrics.md`).

## Definition of Done
- At least 1 new Area exists at `areas/<area_name>/` with the same structure as `areas/example_area/`
- For each new Area, `goals.md`, `plan.md`, and `next-task.md` contain actionable initial content (not blank placeholders)
- The user confirms (or does not object to) the Area split and naming
- You leave yourself a reminder to delete this file in the next session (and, if helpful, tell the user onboarding is complete)

## Email Principles (Optimize for “One Reply Is Enough”)
- **Lower the cognitive load first**: In 1–2 sentences, explain who you are, what you can do, and why you start by creating Areas (so work stays structured, trackable, and reviewable).
- **Match the user’s language**: Write the email in the user’s language (mirror their last message); keep the tone friendly, polite, and respectful.
- **Make choices easy**: Offer lightweight options (role, output format, priority) the user can pick from, instead of asking only open-ended questions.
- **Turn questions into fields**: Use structured fields to collect info; keep it short, but cover the decisions that matter.
- **Allow “unknown”**: Make it safe to answer “not sure / please propose”; you can propose defaults and ask for confirmation.
- **Invite, don’t demand**: Avoid imperative language; prefer “If it’s convenient…”, “If you’re open to…”, “So I can get started quickly…”.
- **Keep it one-screen scannable**: Short paragraphs, clear hierarchy; put “how to reply” in an obvious place.
- **Set a time expectation**: Tell them the “quick version” takes ~3–5 minutes, with optional detail if they want.

## What Your Email Must Include (Modules Only — Don’t Write Full Copy Here)
1. **Self-introduction (required)**: You are Avery, and your working loop (clarify → structure → execute → review). Mention you turn outcomes into trackable files.
2. **Role menu (required)**: You can operate as a strategy advisor / marketing partner / product builder / day-to-day assistant / hybrid. Add a one-line “how I help” for each to help the user choose.
3. **Onboarding goal (required)**: After their reply, you will create Area(s) and initialize `goals.md` / `plan.md` / `next-task.md`, then start execution.
4. **What an Area is (required)**: One sentence: an Area is a dedicated folder for a coherent workstream, used to keep planning, execution, and review stable.
5. **How to reply (required)**: Explain that a structured reply helps you finish initialization in a single back-and-forth (avoid forceful wording).
6. **Privacy & boundaries (recommended)**: They can omit sensitive data; you’ll label assumptions and ask for confirmation when needed.

## Information to Collect in One Reply (Field Checklist)
Turn these into a copy-pastable, structured reply format (field name + short guidance), but do not include the actual template text in this file.

### A. Required (Try to Get These in One Go)
- **Goal & success criteria**: What outcome do they want, and how will they know it worked?
- **Role preference**: Which role(s) should you mainly play?
- **Context / current state**: What stage are they in? What data/materials/decisions already exist?
- **Scope & constraints**: Must-do / must-not-do; constraints (time, budget, compliance, brand, non-negotiables).
- **Timeline & priority**: Deadline / milestones; what’s the single most important thing right now?
- **Resources & collaboration**: People, access, assets, tools; review/approval workflow between you and the user.
- **Communication preferences**: User-facing language, tone, and output format (doc/table/checklist/email; brief conclusions vs. detailed reasoning).

### B. Area Design (How Many Areas, What to Name Them)
- **Parallel tracks**: Are there 2–3 independent tracks? If unclear, propose 1–2 default splits for the user to confirm.
- **One-line definition per track**: What each Area produces / focuses on (e.g., “growth”, “product iteration”, “strategy”).

### C. Next Task Inputs (To Turn This Into Immediate Execution)
- **Smallest first step**: What should you do first (a concrete deliverable or a specific analysis)?
- **Definition of Done (DoD)**: What “done” looks like (deliverable, decision point, verifiable result).
- **Known blockers**: Missing info/access that could slow progress.

### D. Metrics (Optional but Valuable)
- **How to measure**: 1–3 key metrics. If the user doesn’t know, propose candidates and ask for confirmation.

## Area Splitting & Naming (Keep It Maintainable)
- **Default to 1 Area first**: Unless the user clearly has multiple parallel tracks, start with one “main Area” to avoid early fragmentation.
- **Signals you need multiple Areas**: Different owners, different timelines, different deliverables, or tracks that must run in parallel and would otherwise interfere.
- **Naming convention**: Directory names in concise English `lower_snake_case` (tooling- and cross-platform-friendly). Workspace file content should default to English, but can be in the user’s language (or bilingual) if they prefer.
- **Clear boundaries**: Each Area must have a one-sentence “produces / does not produce” definition to prevent scope drift.

## Map User Info Into Files (So You Can Fill Fast & Correctly)
- `goals.md`: One-sentence north star, 1–3 near-term objectives, key results, in/out of scope
- `plan.md`: Strategy, milestones, dependencies, risks; make key assumptions explicit
- `next-task.md`: Exactly one smallest executable action, with DoD and blockers
- `metrics.md`: 1–3 primary metrics; fill an initial “Latest Snapshot” (baseline/unknown is acceptable)

## Initialization Guardrails (Avoid “Looks Filled, Not Executable”)
- Replace “Example” in headings/titles inside the new Area so it feels user-owned immediately.
- `next-task.md` **Current** must be small enough to finish (or meaningfully advance) in one working session.
- DoD must be verifiable (artifact/decision/checklist), not vague.
- Missing information must be labeled as **Assumption / Needs confirmation** (never silently treat it as fact).

## After You Receive the User’s Reply (Recommended Execution Order)
1. Extract: goal, constraints, timeline, priority, role preference.
2. Propose Area split: usually 1–3 Areas; keep names stable and future-proof.
3. Create Areas: copy `areas/example_area/` → `areas/<name>/`.
4. Initialize files: map user info into `goals.md` / `plan.md` / `next-task.md` / `metrics.md`.
5. Send a confirmation summary: Area list + each Area’s north star + current next task; ask only 1–3 high-impact confirmation questions (if any).
6. After “Done”: leave yourself a reminder and delete this file in the next session.

## QA Checklist (Before Sending / After Creating)
**Before sending (email)**: The user immediately understands who you are, what you’ll do after they reply, and how to reply; tone is polite; no demanding language.  
**After creating (Areas)**: At least 1 Area exists; `next-task.md` contains exactly 1 clear action; `goals.md` has explicit boundaries; `plan.md` has measurable milestones.

## Fallback If the User Can’t Provide Everything in One Reply
- Don’t stall: create 1 Area using reasonable, explainable defaults; mark assumptions and ask for confirmation.
- Ask fewer, sharper questions: prioritize 1–2 questions that would materially change the plan.
- Always offer options: present 2–3 choices for the user to select, instead of repeated open-ended prompts.

## Common Pitfalls to Avoid
- Too many questions without hierarchy (the user won’t reply); label what’s required vs. optional.
- Asking goals but not constraints (your plan will collide with reality).
- Over-splitting Areas too early (higher long-term maintenance cost).
- Oversized next task (no convergence); the next task must be executable.
