# Brief Templates

Write every brief in the user's language. Omit sections that don't apply; never pad them.

## 1. Calibrated Brief

Aim for about 400 words. State red lines under the goal and repeat them at the end, because constraints in the middle of a long context get lost.

```markdown
# Calibrated Brief: {task name}
Level: L{1|2} · Interaction: {minimal|normal|thorough} · Date: {YYYY-MM-DD}

## Goal
{One sentence: what and why.}
Red lines: {1–3 constraints that must never be broken, e.g. "public API unchanged", "never touch prod"}

## Done when
- [ ] {e.g. `pnpm test` passes; new tests/foo.test.ts covers 3 branches}
- [ ] {e.g. GET /users?page=2&pageSize=20 returns meta.total}

## Scope
- In: {files, modules, services}
- Out: {what is explicitly left alone}

## Context
- {path or link}: {why it matters}
- Existing pattern: {e.g. pagination follows src/orders/list.ts}

## Constraints
{Stack, versions, dependencies, performance, time, compliance}

## Decisions
- Q: {question} → A: {answer} (user)
- Q: {question} → A: {recommended option} (delegated to agent)

## Assumptions (not asked; correct any time)
- {assumption}, based on {file or convention}

## Confirm before
- {action}: stop and show {target list / diff / dry-run output} first

## Plan
1. {milestone} → check: {output or verification}
2. {milestone} → check: {…}

## Verification
{Commands to run; manual checks}

## Delivery
{Form, location, commit or not, report format}

## Escalate when
An assumption proves false · scope must grow · the same approach fails twice · a "Confirm before" action is next.

Red lines (repeated): {same as above}
```

## 2. Sub-brief (one per delegated task)

The subagent cannot see the main conversation, so carry the decisions over explicitly; a task name alone is not enough. Check each sub-brief against the gap checklist before sending it.

```markdown
## Subtask {id}: {name}
Goal: {one sentence}
Output format: {e.g. JSON {file, change_summary, tests_run, open_issues[]}, or a markdown report under 300 words}
Tools and sources: {e.g. read-only search; may run `pytest tests/unit`; no network}
Boundaries: {e.g. don't modify src/shared/**; add no dependencies}
Decisions and shared context: {the decisions and assumptions from the main brief that apply here}
Interface contracts: {agreements with sibling subtasks: signatures, file ownership, data formats}
Acceptance: {e.g. the named tests pass and the output matches the format}
If blocked: {return open_issues; don't widen scope or guess the target}
Budget: {e.g. at most 15 tool calls}
```

## 3. Pasteable prompt (brief-only mode)

When the user only wants a refined prompt for another agent or a new session, output this block and stop:

```text
Execute the calibrated task below. Read the whole brief first. If anything in it conflicts, stop and report instead of choosing.

<brief>
{full brief from section 1}
</brief>

Working rules:
- Follow the Plan; tick each "Done when" box as you complete it.
- New ambiguity not covered by Decisions or Assumptions: if low-impact, follow repo convention and note it; if high-impact, stop and ask.
- Finish with a report in the Delivery format: what was done, how it was verified, what is still open.
```

## 4. Short form (top of an L1 reply)

```
Understanding: {one sentence}
Assumptions: (1) {…} (2) {…} (3) {…}
Verification: {command}
Starting now. Correct anything above that's wrong.
```
