# Examples

## 1. L1: fill gaps silently, ask nothing

**User:** "Add pagination to the /users endpoint."

**Grounding:** `src/orders/list.ts` already paginates with `page`/`pageSize` and returns `meta.total`; its tests are in `tests/orders.test.ts`.

**Reply opens with:**

```
L1.
Understanding: add pagination to GET /users, following the /orders pattern.
Assumptions: (1) page starts at 1, pageSize defaults to 20 with a max of 100, matching orders (2) response gains meta.total (3) 3 new tests: defaults, out of range, max size
Verification: pnpm test
Starting now. Correct anything above that's wrong.
```

Then it executes. It doesn't ask "offset or cursor?" because the repo has a precedent and the change is reversible.

## 2. L2: full calibration

**User:** "Switch auth from sessions to JWT, frontend and backend. Feel free to run several agents in parallel."

**Grounding:** Express with Redis sessions; `web/` is React and `mobile/` is React Native, and both call the same API; 23 call sites read `req.session.user`.

**Gap scan (excerpt):** done criteria partial; migration strategy missing, high impact; token storage missing, high impact; whether `mobile/` is in scope partial, high impact; naming conventions clear.

**Questions (one round):**

```
Q1. How should signed-in users transition? (affects: whether a dual-stack period is needed, roughly 2x the work)
  A. Accept both session and JWT for 2 weeks (recommended: no forced logout)
  B. Force everyone to sign in again at launch
  Default if unanswered: A
Q2. Where should the frontend keep the token? (affects: XSS/CSRF defenses)
  A. httpOnly cookie + CSRF token (recommended: matches the existing cookie setup)
  B. In memory, with the refresh token in an httpOnly cookie
  C. localStorage
  Default if unanswered: A
Q3. Is mobile/ in scope? (affects: number of subagents and the interface contract)
  A. Yes, update it in the same change (recommended: it uses the same API)
  B. No, just keep the API backward compatible
  Default if unanswered: B
Reply like "1A 2C 3B", or "go with the recommendations".
```

After the answers, it writes the full brief (template §1) and splits the work: token issuing and validation (backend), web, mobile, and migration and rollback scripts. The main agent first fixes the shared contract serially (token format, refresh endpoint signature, error codes), then fans out. Every sub-brief carries "Decided: 2-week dual stack, httpOnly cookie". The user confirms the brief before execution starts.

## 3. Irreversible operation: confirmation is mandatory

**User:** "Clean up the unused stuff on staging."

"Unused" and "clean up" are vague terms, and the action is irreversible with an uncertain target, so confirmation is required.

**Grounding (read-only):** 7 staging resources have had no traffic for 30 days and no owner tag.

```
Q1. These 7 resources look unused (no traffic for 30 days, no owner tag). What should happen to them?
  [table: name / type / last active / monthly cost]
  A. Snapshot or back up, then delete all 7 (recommended)
  B. Delete only the first 4 (stateless compute) and keep the databases
  C. Produce a dry-run report only; delete nothing
  Default if unanswered: C
```

The default is C, the safest option, not the recommended A. For irreversible actions the default is always the most conservative choice.

## 4. Multi-agent research with budgeted delegation

**User:** "Research the main vector databases and recommend one for us."

**Grounding:** a Python service deployed on Kubernetes; data volume not stated.

```
Q1. What scale do you expect? (affects: the candidate list and what to benchmark)
  A. Up to tens of millions of vectors (recommended: typical starting scale)
  B. Hundreds of millions or more
  Default if unanswered: A
Q2. Deployment preference? (affects: whether fully managed services are included)
  A. Compare self-hosted and managed (recommended)
  B. Self-hostable only
  Default if unanswered: A
```

**Done when:** a comparison of at most 2 pages covering latency, filtering, operating cost, license, and Kubernetes support, ending in a recommendation with reasons, and every claim linked to a source.

**Delegation:** 2–4 subagents, since this is a comparison task. Each covers 1–2 candidates and returns the same JSON shape so the results merge cleanly. Boundary in every sub-brief: "Official docs and published benchmarks only; record the date of each source."

## 5. Brief only: a refined prompt for another agent

**User:** "Write me a prompt for Codex: add dark mode to the app."

**Grounding:** React with Tailwind; `tailwind.config.js` has no `darkMode` setting; colors are hard-coded in about 40 components; no theme toggle exists.

```
Q1. What scope? (affects: number of files touched and whether colors become design tokens)
  A. App-wide theme, with hard-coded colors replaced by tokens (recommended: avoids patching each component twice)
  B. Dark styles only for the pages users see most, colors left as they are
  Default if unanswered: A
Q2. How is the theme chosen? (affects: the toggle UI and persistence)
  A. Follow the system setting, with a manual override saved in localStorage (recommended)
  B. Manual toggle only
  Default if unanswered: A
```

**Output:** the pasteable prompt (template §3) wrapping a brief whose Done-when list includes "every page passes WCAG AA contrast in both themes" and "no hard-coded hex colors remain in src/components". Its Red lines include "no visual change in light mode". Nothing is executed.
