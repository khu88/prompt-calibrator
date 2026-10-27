# Examples

These are illustrative scenarios, not results from evaluated runs.

## 1. Clear complex work: proceed without questions

**User:** "Update pagination in the API and web client to the existing cursor format. Keep response fields compatible, use parallel agents if helpful, and run the relevant tests. Make local changes only."

**Available context:** Project documentation defines the cursor format; the affected endpoints and client callers are identifiable; existing tests cover compatibility.

**Response:** "I'll apply the documented cursor format to the API and its web callers, preserve the response fields, and verify compatibility with the relevant tests."

The agent reads the implementation, settles shared interfaces and file ownership, then proceeds within the local-change scope. Task size and parallel agents do not create a need for confirmation. A separate brief is unnecessary unless it helps the actual coordination.

## 2. A consequential correctness gap: ask and pause dependent work

**User:** "Compare the two models on our dataset and report which one is better."

**Available context:** The project contains two evaluation splits, but neither the conversation nor the evaluation configuration identifies which split is authoritative for this comparison. The evaluation code is available.

**Question:** "Which evaluation split should define this comparison: A. the standard test split, or B. the out-of-domain split? They measure different generalization settings."

The agent does not choose a split or report a winner without an answer. It can inspect preprocessing and metric code while waiting. Any execution also remains subject to the user's resource and cost authorization. Once the missing conditions are resolved, it records the decision and continues without asking the user to reconfirm an identical brief.

## 3. The user requests review before changes: respect the checkpoint

**User:** "Simplify this skill. First show me the plan; make changes only after I confirm."

**Response:** The agent reads the current files and presents concrete proposed edits, preserved behaviors, and verification steps. It identifies trade-offs and unresolved questions, if any.

The agent stops before editing, even if the edits would be reversible. After the user approves, it implements and verifies within the approved scope. Approval for local edits does not also authorize publication or a Git push.

## 4. Missing authorization: prepare what is allowed, pause the external action

**User:** "Prepare this project for open source: fix the installation instructions and check the files for private information. Keep everything local until I approve publication."

The agent makes the requested local edits, runs appropriate authorized checks, and presents the exact files and proposed publication destination for review. It does not create a public repository or push. If the user does not reply, publication remains paused; silence does not select a recommended option.

If the user later explicitly authorizes publication to that destination within the reviewed scope, the agent proceeds without requesting the same permission again. A different destination, additional sensitive content, or a materially expanded scope requires resolving that new gap first.
