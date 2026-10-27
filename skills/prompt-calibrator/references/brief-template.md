# Brief Templates

A brief is optional. Use one when it helps coordinate consequential decisions, support a handoff, satisfy a user-requested planning checkpoint, or deliver a prompt for another agent. Ordinary work does not need a separate document or fixed response format.

Use the user's language. Keep only useful information, omit empty fields, and reuse existing project status documents instead of creating a parallel record. Do not require a confirmation merely because a brief was written.

## Compact brief

```markdown
# Task brief: {task name}

## Goal and scope
{Requested result and deliverable; exact target, included work, and important exclusions.}

## Key decisions and assumptions
- {Confirmed decision and its source, or a consequential assumption and its basis.}
- {Applicable constraints and existing authorization.}

## Acceptance
- {Observable completion condition and the check that will verify it.}

## Pending confirmation
- {Unresolved consequential question or missing approval; the work that depends on it.}
```

Do not fill a pending item with a guessed answer. State which independent authorized work can continue. If the user asks to review a plan before changes, present the concrete proposed changes and checks, then wait at that checkpoint.

## Handoff or delegated task

Add only what the recipient needs beyond the compact brief:

```text
Context: {relevant evidence, prior decisions, and where to find them}
Output: {expected artifact or response format}
Interfaces and ownership: {shared contracts, files, and coordination dependencies}
Boundaries and budget: {allowed work, applicable limits, and approvals still required}
If blocked: {return the consequential missing information; continue only independent authorized work}
```

Pass the information the recipient needs without assuming how much conversation history it inherits. A subtask cannot grant permissions beyond those available to the parent task. Reuse the acceptance conditions above, adding a task-specific check only when needed.

## A prompt for another agent

When the user requests only a refined prompt, produce the requested prompt and do not execute its task. Include the compact brief and any necessary context, plus these working rules when useful:

```text
Read the available context before asking. Follow the stated scope, constraints, and authorization boundaries. Resolve low-risk implementation details from project conventions; do not guess consequential missing facts or treat silence as permission. Pause only dependent work when an answer or approval is required. Finish by reporting the result, actual verification, and unresolved items.
```
