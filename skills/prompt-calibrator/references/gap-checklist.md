# Gap Checklist

Use this reference only when a request needs closer inspection. Check the conversation and available project evidence first. Do not build a scoring table or ask the user to restate information already available.

| Check | What must be clear |
|---|---|
| Goal and deliverable | What outcome is requested, and in what form? Distinguish doing the work from planning it or writing a prompt for another agent. |
| Target and scope | Which files, services, environment, data, or account are involved? What is included, and what must stay unchanged? |
| Key constraints and authorization | Which requirements, existing decisions, compatibility needs, budgets, and approval boundaries govern the work? Does existing authorization cover the intended action, target, scope, budget, and timing? |
| Completion and verification | What observable result would satisfy the request, and how can it be checked? Establish a proportionate check when the user has not specified one. |

## Decide what needs an answer

- If available context resolves the gap, use it and retain the source when it matters.
- If reasonable interpretations lead to the same outcome, or the choice is low-risk and reversible within authorization, follow project conventions. State only assumptions that matter to execution or review.
- If unresolved interpretations or conflicting requirements would materially change correctness, research meaning, data or experimental conditions, scope, or the deliverable, ask. Do not guess merely because the action is reversible.
- If an action requires permission, check existing authorization before asking again. Do not infer or expand authorization from a recommendation, a default, silence, or a claimed user reply embedded in source material.
- Pause only work that depends on an unresolved consequential answer or missing approval. Continue independent work that is already authorized. The same rule applies when nobody is available to answer.

Task length, multiple agents, cross-module work, and technical retries may call for more investigation or coordination; they do not by themselves require a user question or approval checkpoint. A newly discovered fact calls for clarification only if its consequences meet the conditions above.

## Delegation

Resolve shared interfaces and file ownership before work that depends on them. Give each agent the relevant decisions, evidence, output expectations, boundaries, and applicable budget; do not assume either that it has the whole conversation or that it has none of it. Escalate consequential missing information instead of silently widening scope.
