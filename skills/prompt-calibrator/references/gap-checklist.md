# Gap Checklist

Rate each dimension **clear / partial / missing** and estimate impact **high / medium / low**. "Check" is the self-test. "Default" is what to assume at L1 when nothing is specified; record every default you use under Assumptions in the brief.

| # | Dimension | Check | Default when unspecified |
|---|---|---|---|
| 1 | Goal and motivation | Do you know *why*? Motivation changes trade-offs, such as speed versus readability. | Infer it from context and restate it in the brief. |
| 2 | Definition of done | Can you write a checkable done condition: tests, command output, a metric threshold, UI behavior? | Existing tests pass, plus tests that cover the new behavior. |
| 3 | Scope | What is in, and what is explicitly out? What do "all" and "related" cover? | Minimal change; no drive-by refactors; public API unchanged. |
| 4 | Target certainty | Exactly which file, module, service, environment, branch, dataset, or account? Do several share the name? | **No default.** Ask if impact is high. If low, pick the obvious one and say so. |
| 5 | Inputs and context | Where are the docs, examples, logs, specs, or credentials this needs? | Search the repo first; ask only if you can't find them. |
| 6 | Constraints | Stack and versions, whether new dependencies are allowed, performance and time budgets, compliance. | Follow the existing stack; add no dependencies; keep versions pinned. |
| 7 | Implicit requirements | Conventions, backward compatibility with old clients and data, logging and monitoring, i18n, accessibility, migrations. | Follow existing patterns; stay backward compatible. |
| 8 | Edge cases and errors | Empty input, concurrency, timeouts, retries, permission denied, partial failure. | Match how the same module already handles them. |
| 9 | Risk and irreversibility | Any delete, overwrite, migration, production change, outbound message, spending, or permission or secret change? | **No default.** Confirm the target list and offer a dry-run or backup. |
| 10 | Verification | How is correctness shown: commands, tests, manual checks, a reviewer? | Run the project's build, lint, and test commands. |
| 11 | Deliverable | Form (PR, patch, report, file), location, naming, language, length. | Leave changes uncommitted in the working tree; write reports in the user's language. |
| 12 | Autonomy and checkpoints | When to stop and report? How much may the agent decide alone? Commit or push? | Stop before confirm-before actions; never commit or push unless asked. |

Two cross-cutting checks:

- **Contradictions**: between requirements, between the request and the repo, or between a new instruction and AGENTS.md/CLAUDE.md. Raise each as a candidate question; never pick a side silently.
- **Multi-agent split**: do subtasks share state, interfaces, or files? Decide which contracts must be settled, or which parts must run serially, before fanning out.

## Vague terms

When one of these (or its equivalent in any language) appears, it must be quantified or pinned to a target. Until it is, rate that dimension as partial.

| Vague term | Must become |
|---|---|
| optimize, speed up, improve performance | The metric (p95 latency, throughput, memory, bundle size), its baseline, and the target. |
| clean up, tidy, remove what's unused | The rule for "unused" and the final list of objects. |
| refactor, improve, polish | The motivation (testability, readability, decoupling) and the behavior that must not change. |
| fix it, it's broken | Reproduction steps, plus expected versus actual behavior. |
| support X, compatible with X | The version range, which features, and the fallback. |
| like X, similar to X | Which aspects to copy: interaction, structure, or style. |
| all, every, related | An enumerated list, or the query that produces it. |
| as much as possible, appropriate, reasonable | Hard constraint or soft preference, and which wins in a conflict. |
| large, many, high traffic | The actual magnitude. |
| ship, deploy, release, go live | The environment, the rollout method, and whether it can be rolled back. |

## Impact levels

- **High**: a wrong answer costs more than ~30 minutes of rework, triggers an irreversible action, or affects other subtasks or people.
- **Medium**: one design decision has to be redone, but locally.
- **Low**: style or naming that is cheap to change later.

Whether a gap becomes a question is decided by the scoring in `question-design.md`.
