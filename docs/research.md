# Design Rationale: Research Notes and Current Choices

Current design updated 2026-10-28. Source notes in sections 1–6 and the reference list are retained from the 2026-10-13 document; bibliographic details, numbers, and publication status were not reverified during this simplification. Their historical design notes describe earlier reasoning, not the current runtime instructions. Consult the primary sources before citing those claims.

This document is optional background, not a runtime checklist. The current behavior is defined in [SKILL.md](../skills/prompt-calibrator/SKILL.md). No end-to-end evaluation results for Prompt Calibrator are reported here.

## Current design summary

- Read the available context before asking. Check goal/deliverable, target/scope, constraints/authorization, and completion/verification.
- Ask about unresolved gaps that materially change correctness, scope, or the intended result. Usually collect 0–3 necessary questions together; never fill a quota. Complexity alone does not require a question or approval.
- Continue with explicit low-risk assumptions within existing authorization. Do not guess a high-impact missing fact or treat silence as approval. Respect user-defined checkpoints and pause only dependent work.
- Record a short brief only when useful; reuse existing project records. Delegate with the necessary context, decisions, boundaries, interfaces, and acceptance checks. A scout may gather evidence, but does not duplicate the main agent's brief.
- The keyword hook is an optional reminder. Its scoring algorithm is unchanged by this simplification and is separate from the agent's decision to ask.

These are design choices to be evaluated, not effects established by the studies below. The earlier numerical question score, mandatory full brief approval, repeated constraints, and fixed failure-count pause are no longer runtime rules.

## Historical source notes

The following study summaries and their original design implications are preserved for traceability. They neither validate this implementation nor prescribe its current workflow.

## 1. The problem: underspecification makes agents guess

| Study | Recorded finding | Historical design note |
|---|---|---|
| Laban et al. 2025, *LLMs Get Lost in Multi-Turn Conversation* | Across 200,000+ simulated conversations, top LLMs average a 39% drop when requirements arrive over several turns instead of one. The drop comes mostly from a large rise in unreliability, not lost aptitude: models commit to early assumptions and don't recover. | Collect the spec before the first action, in one round. |
| Ji et al. 2026, *Coding Agents Are Guessing* (UnderSpecBench) | 2,208 DevOps instruction variants run on Claude Code, Codex, and OpenCode. Between 55.8% and 67.8% of runs cross at least one action boundary. Underspecification mainly makes agents guess rather than fail. An uncertain target sharply degrades action quality, and blast-radius cues barely reduce the urge to act. | Require confirmation for irreversible actions with uncertain targets; don't count on the model to hold back. |
| Zhou et al. 2026, SWE-RPG | On 163 repository-level tasks, popular coding agents resolve 31.5% on average. Recovering implicit requirements is the main bottleneck, in 24.5–46.0% of runs. | Make implicit requirements their own checklist dimension. |
| Yang et al. 2025, *What Prompts Don't Say* | Models infer unstated requirements 41.1% of the time, but fragilely: underspecified prompts are twice as likely to regress when the model or prompt changes, sometimes losing more than 20% accuracy. Requirements-aware prompt optimization adds 4.8% on average. | Specify the requirements that matter and record assumptions so they can be corrected. |
| Cemri et al. 2025, *Why Do Multi-Agent LLM Systems Fail?* (MAST) | 1,600+ traces from 7 frameworks yield 14 failure modes in three groups: system design, inter-agent misalignment, and task verification. The groups include disobeying the task specification and failing to ask for clarification. | Check specs and role definitions before delegating. |
| Lyu et al. 2025, *Planner-Coder Gap* | Semantically equivalent inputs make multi-agent coding systems fail on 7.9–83.3% of problems they had already solved. The planner-coder gap, where the planner hands over an underspecified plan, accounts for 75.3% of failures. | Sub-briefs go through the same checklist. |
| Kwa et al. 2025 (METR) | The length of task that agents complete with 50% success has doubled roughly every 7 months. | The longer the autonomous run, the more an early spec error costs. |
| Baumann et al. 2026, SWE-chat | In ~18,000 real coding-agent sessions, only 59% of agent-written code survives into commits, and users push back in 50% of turns. | Intent misalignment drives much of the rework, so up-front calibration has a lot to gain. |

## 2. Asking pays off

| Study | Recorded finding | Historical design note |
|---|---|---|
| Vijayvargiya et al., Ambig-SWE (ICLR 2026) | On underspecified SWE-bench Verified, interaction improves results by up to 74%. Models struggle to tell underspecified instructions from well-specified ones. | Add an explicit "is this underspecified?" step. |
| Edwards & Schuster 2026, *Ask or Assume?* (EMNLP 2026) | A scaffold that separates underspecification detection from code execution resolves 69.40% of underspecified SWE-bench tasks, closing the gap to fully specified instructions. Its questioning is well calibrated: few questions on simple tasks, more on complex ones. | Use a dedicated calibrator (this skill or the scout subagent), not the executor in passing. |
| Wu & Fard, HumanEvalComm (TOSEM) | On problems made inconsistent, ambiguous, or incomplete, code LLMs mostly generate code without asking clarifying questions. | Models default to acting, so asking has to be built into the workflow. |
| Mu et al. 2023, ClarifyGPT | Detects ambiguity by checking whether sampled solutions agree; raises GPT-4's average across four benchmarks from 68.02% to 75.75%. | "Do different readings lead to different results?" works as a trigger (the divergence test). |
| Stoisser et al. 2026, Ambig-DS | Data-science agents silently commit to a plausible but wrong target or metric. One clarifying question recovers much of the loss, but agents can't tell when to ask: permissive prompts over-ask on clear tasks, and conservative prompts silently default on ambiguous ones. | Calibrate the asking threshold in both directions. |
| Zhou et al. 2025, SWEET-RL / ColBench | Multi-turn collaborative RL lets an 8B model match or exceed GPT-4o on collaborative tasks. | Collaboration can be trained, but prompting alone also helps. |

## 3. What to ask, and how much

| Study | Recorded finding | Historical design note |
|---|---|---|
| Kuhn et al. 2022, CLAM | Asking only on ambiguous inputs improves accuracy on mixed datasets. | Ask selectively, not always. |
| Ren et al. 2023, KnowNo | Conformal prediction asks for help only when more than one candidate plan remains, minimizing help requests while guaranteeing success rates. | Ask only when the reasonable readings aren't unique. |
| Hu et al. 2024, *Uncertainty of Thoughts* | Picking questions by expected information gain raises success by 38.1% on average while needing fewer questions. | Rank questions by value. |
| Suri et al. 2025, SAGE-Agent | Structured-uncertainty question selection gives 7–39% higher coverage on ambiguous tasks with 1.5–2.7× fewer questions. | Tie each question to a specific parameter (a brief field) and treat asking as a cost. |
| Berant et al. 2025, *Steerable Clarification Policies* (COLM 2026) | A cost-conditioned policy switches between guessing, enumerating readings, and asking, and generalizes to unseen costs. | Offer an interaction-level setting. |
| Kim et al. 2023, *Tree of Clarifications* | Recursively enumerates interpretations to cover an ambiguous question. | When asking is expensive, list the readings and pick a default. |
| Aliannejadi et al. 2019 | One good clarifying question improves P@1 by over 170% (oracle setting). | A few good questions have high marginal value. |
| Zhang et al. 2024; Chen et al. 2024 (ACT) | Training on simulated future turns teaches when to ask versus answer; LLMs tend to hedge or guess intent. | Ask "would the plan differ if the answer were A or B?" |

## 4. Eliciting intent with little user effort

| Study | Recorded finding | Historical design note |
|---|---|---|
| Li et al. 2023, GATE | Model-generated questions elicit more information with less user effort than users writing prompts themselves, and surface considerations users hadn't thought of. | The agent asks; the user doesn't have to write a long prompt. |
| Qian et al. 2024, IN3 | An upstream model judges task vagueness, asks about intent, and turns the answers into actionable goals before execution starts, which improves understanding and cuts redundant tool use. | Produce a goal summary the user can confirm (the brief). |
| Wu et al. 2025, CollabLLM | Multi-turn-aware rewards give 18.5% higher task performance; in a 201-person user study, satisfaction rose 17.6% and time spent fell 10.4%. | Up-front clarification can raise satisfaction and efficiency together. |
| Qian et al. 2025, UserBench | Answers fully match user intent only 20% of the time; the best models uncover under 30% of user preferences. | Preferences don't surface on their own; elicit them. |
| Andukuri et al. 2024, STaR-GATE | After two self-improvement rounds, responses are preferred over the base model's on 72% of tasks. | Question-asking is a trainable skill. |
| Deng et al. 2023, *Rephrase and Respond* | Restating the question before answering improves results across tasks and complements chain-of-thought. | Restate the task before executing (the L1 short form). |

## 5. Context and multi-agent engineering

**Context degrades.** Liu et al. (*Lost in the Middle*) show that information in the middle of a long context gets overlooked. Chroma's *Context Rot* report found performance becomes less reliable as input grows, across 18 models. Hence the short brief, with red lines at both the top and the end.

**Delegation needs full specs.** Anthropic's multi-agent research post reports that vague delegation, such as a one-line task, leads subagents to duplicate work or misread the task. Each subagent needs an objective, an output format, guidance on tools and sources, and clear boundaries. Effort should scale with complexity: 1 agent for simple tasks, 2–4 subagents for comparisons, 10 or more for complex research. Cognition's *Don't Build Multi-Agents* argues that actions carry implicit decisions and conflicting decisions produce bad results, so full context must be shared. Manus recites goals by rewriting a todo file so they stay in recent attention, and keeps errors in context. These map to the sub-brief's Decisions and Interface contracts fields and to the practice of saving the brief and re-reading it.

**Clarification is an attack window.** Sehwag et al. 2026 (ASPI) found that agents waiting for clarification are far more vulnerable to prompt injection: attack success rose from 1.8% to 34.0% for o3. Only the user's own replies count as answers.

## 6. Prior art

| Project or guide | Recorded mechanism | Historical design note |
|---|---|---|
| GitHub Spec Kit | Specs mark high-impact items that lack a reasonable default as `[NEEDS CLARIFICATION]`, at most 3. The clarify step scans coverage by category (Clear/Partial/Missing), picks questions by impact × uncertainty, asks at most 5 per session as multiple choice with a recommendation, and writes answers back into the spec. | Coverage scan, multiple choice with a recommendation, answers written back into the brief. |
| Kiro Specs | Requirements use EARS syntax (WHEN … THE SYSTEM SHALL …). "Analyze requirements" flags vague terms, conflicting constraints, unstated assumptions, and missing edge cases. | Vague-term table, contradiction check. |
| obra/superpowers | Tasks are classed as spike, bounded, or architectural. Hard gate: nothing is implemented without approval. One question at a time, multiple choice preferred. Plans must be executable by an engineer who has never seen the codebase. | L0/L1/L2 triage, escalate when unsure, confirm before executing at L2. |
| BMAD-METHOD, claude-task-master, Agent OS | Planning depth matches change size; PRD first, then tasks with complexity scores; project standards injected into specs. | Size-based triage, reading AGENTS.md/CLAUDE.md first. |
| severity1/claude-code-prompt-improver | A `UserPromptSubmit` hook cheaply judges vagueness, passes clear prompts through, and loads a skill for vague ones, which then researches and asks 1–6 questions. A `*` prefix bypasses it. | The cheap gate plus on-demand skill design of `calibrate_gate.py`, and the bypass prefix. |
| Claude Code best practices | Explore, plan, code, commit. A diff you can describe in one sentence can skip planning. Have Claude interview you with AskUserQuestion, write SPEC.md, then execute in a fresh session. | L0 criterion, saved brief, fresh-session execution. |
| OpenAI Codex prompting guide | Codex is biased to action: implement with reasonable assumptions and don't end a turn on a clarifying question unless truly blocked. Uncertainty thresholds can differ per tool (low for destructive tools, high for search). Contradictory instructions waste reasoning. | Codex guidance: calibrate fully up front, then don't interrupt; a separate bar for irreversible actions; contradiction check. |
| Cursor Plan Mode, Cline Plan/Act, Roo Code `ask_followup_question`, Aider architect mode | Planning separated from execution; question tools offer 2–4 suggested answers. | Question format, read-only grounding phase. |
| DSPy/GEPA, TextGrad, promptfoo | Offline, metric-driven prompt optimization and evaluation. | Regression-testing and tuning the skill itself (section 8), not runtime calibration. |

## 7. Current design choices and rationale

The source connections below explain where ideas came from. They do not establish that these exact rules, limits, or templates improve task performance.

| Current choice | Rationale and source connection | What remains unverified |
|---|---|---|
| Read context before asking | Earlier notes connect this to Ambig-SWE, HumanEvalComm, and project-guidance conventions. | Whether this implementation avoids redundant questions in realistic projects. |
| Four concise checks, without numerical gap scoring | Consolidates goal, target, constraints, authorization, and verification while retaining relevant implicit requirements and conflicts. | Whether the shorter checklist misses consequential requirements. |
| Ask when reasonable interpretations lead to materially different outcomes | Related to the ambiguity checks discussed in ClarifyGPT and KnowNo. | The model's ability to recognize those differences reliably. |
| Usually 0–3 necessary questions together; follow up on new consequential gaps or answers that leave one unresolved | Treats user effort as a cost, as discussed in the clarification work above; the usual batch size is a product choice, not a reason to omit an essential gap. | The best question budget. The cited multi-turn studies do not prove one round is always optimal. |
| Preserve existing authorization; obtain missing authorization or correctness-critical answers | Separates work size from permission and uncertainty. Target/scope concerns appear in the UnderSpecBench notes. | Prompt-level compliance; the skill and hook are not enforcement controls. |
| Use short records only when useful | Keeps consequential decisions and assumptions available without requiring a fixed length or duplicated constraints. Related context concerns appear in the notes above. | Whether the brief improves recovery or reduces errors. |
| Delegate with sufficient context and clear boundaries; scout is optional | Related to Anthropic's delegation guidance, MAST, and Planner-Coder Gap. | Whether a separate scout adds value over direct grounding at comparable cost. |
| Resolve routine failures within scope; pause dependent work for material changes or missing approval | Avoids turning an arbitrary retry count into a user question. | Whether the agent correctly distinguishes routine recovery from scope or correctness changes. |
| Only direct user authorization counts | Preserves the trust boundary discussed in the ASPI notes. | Resistance to injection in actual agent runs. |

## 8. Evaluating the skill

Start with a static consistency review: check that the skill, adapter, scout, hook message, templates, and examples agree. Representative cases should include:

- A clear, authorized long or parallel task proceeds without extra approval.
- A question answered by project files is resolved from those files.
- A missing fact that changes correctness or the intended result is asked, not guessed.
- Existing authorization is reused within scope; missing authorization and explicit review checkpoints are respected.
- A blocked step does not stop independent, authorized work; unanswered questions are not treated as approval.
- A prompt-writing request produces a prompt without executing it.

These are rule-review cases, not measurements of model behavior. Hook unit tests check keyword scoring and output plumbing only.

For an empirical evaluation, first define an authorized run budget and a task set covering clear requests, material ambiguities, low-risk assumptions, and approval boundaries. Compare the previous skill, the simplified skill, and no skill under the same model/version, tools, task inputs, and resource budgets. Record prompts, expected decisions, model settings, repetitions, traces, and costs so results are reproducible. Compare:

- **Effectiveness:** task acceptance, wrong-target or out-of-scope actions, missed requirements, and explicit-checkpoint violations.
- **Efficiency:** questions, user answer time, total time/tokens, and rework. Fewer questions alone is not success.
- **Calibration:** unnecessary questions on clear tasks, consequential unasked gaps, and assumptions later overturned.

Define task-specific success and failure conditions before running. Inspect failures and report uncertainty; a small scenario review cannot establish general performance. Evaluate the optional scout with a comparable resource budget. If hook thresholds are tuned later, retain misclassified prompts as regression cases and separate trigger accuracy from the downstream decision to ask. No such evaluation was run for this documentation change.

## 9. Limitations

- The retained source notes have not been independently reverified in this revision. Verify titles, authors, venue status, numerical results, and their experimental conditions against the linked primary sources before reuse.
- The simplified workflow has no measured task-level advantage in this repository. Shorter instructions may omit useful detail; the review cases and empirical comparisons above should check that risk.
- The hook remains a keyword heuristic with false positives and negatives. A reminder is not evidence that the task needs questions, and bypassing it does not authorize an action.
- Asking quality and instruction compliance can vary by model and host tool. No current platform comparison is established here.

## References

**Research**

- Laban et al. 2025. LLMs Get Lost In Multi-Turn Conversation. https://arxiv.org/abs/2505.06120
- Ji et al. 2026. Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions. https://arxiv.org/abs/2607.02294
- Zhou et al. 2026. A Unified Issue Resolution Benchmark for Requirement Clarification, Planning, and Code Generation for Coding Agents (SWE-RPG). https://arxiv.org/abs/2608.09072
- Yang et al. 2025. What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts. https://arxiv.org/abs/2505.13360
- Cemri et al. 2025. Why Do Multi-Agent LLM Systems Fail? https://arxiv.org/abs/2503.13657
- Lyu et al. 2025. Understanding and Bridging the Planner-Coder Gap. https://arxiv.org/abs/2510.10460
- Kwa et al. 2025. Measuring AI Ability to Complete Long Software Tasks. https://arxiv.org/abs/2503.14499
- Baumann et al. 2026. SWE-chat: Coding Agent Interactions From Real Users in the Wild. https://arxiv.org/abs/2604.20779
- Vijayvargiya et al. Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering. https://arxiv.org/abs/2502.13069
- Edwards & Schuster 2026. Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents. https://arxiv.org/abs/2603.26233
- Wu & Fard. HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent. https://arxiv.org/abs/2406.00215
- Mu et al. 2023. ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification. https://arxiv.org/abs/2310.10996
- Stoisser et al. 2026. Ambig-DS: A Benchmark for Task-Framing Ambiguity in Data-Science Agents. https://arxiv.org/abs/2605.09698
- Zhou et al. 2025. SWEET-RL: Training Multi-Turn LLM Agents on Collaborative Reasoning Tasks. https://arxiv.org/abs/2503.15478
- Kuhn et al. 2022. CLAM: Selective Clarification for Ambiguous Questions with Generative Language Models. https://arxiv.org/abs/2212.07769
- Ren et al. 2023. Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners (KnowNo). https://arxiv.org/abs/2307.01928
- Hu et al. 2024. Uncertainty of Thoughts: Uncertainty-Aware Planning Enhances Information Seeking in Large Language Models. https://arxiv.org/abs/2402.03271
- Suri et al. 2025. Structured Uncertainty guided Clarification for LLM Agents (SAGE-Agent). https://arxiv.org/abs/2511.08798
- Berant et al. 2025. Learning Steerable Clarification Policies with Collaborative Self-play. https://arxiv.org/abs/2512.04068
- Kim et al. 2023. Tree of Clarifications: Answering Ambiguous Questions with Retrieval-Augmented Large Language Models. https://arxiv.org/abs/2310.14696
- Aliannejadi et al. 2019. Asking Clarifying Questions in Open-Domain Information-Seeking Conversations. https://arxiv.org/abs/1907.06554
- Zhang et al. 2024. Modeling Future Conversation Turns to Teach LLMs to Ask Clarifying Questions. https://arxiv.org/abs/2410.13788
- Chen et al. 2024. Learning to Clarify: Multi-turn Conversations with Action-Based Contrastive Self-Training (ACT). https://arxiv.org/abs/2406.00222
- Li et al. 2023. Eliciting Human Preferences with Language Models (GATE). https://arxiv.org/abs/2310.11589
- Qian et al. 2024. Tell Me More! Towards Implicit User Intention Understanding of Language Model Driven Agents (IN3). https://arxiv.org/abs/2402.09205
- Wu et al. 2025. CollabLLM: From Passive Responders to Active Collaborators. https://arxiv.org/abs/2502.00640
- Qian et al. 2025. UserBench: An Interactive Gym Environment for User-Centric Agents. https://arxiv.org/abs/2507.22034
- Andukuri et al. 2024. STaR-GATE: Teaching Language Models to Ask Clarifying Questions. https://arxiv.org/abs/2403.19154
- Deng et al. 2023. Rephrase and Respond: Let Large Language Models Ask Better Questions for Themselves. https://arxiv.org/abs/2311.04205
- Liu et al. 2023. Lost in the Middle: How Language Models Use Long Contexts. https://arxiv.org/abs/2307.03172
- Hong et al. 2025. Context Rot (Chroma). https://research.trychroma.com/context-rot
- Sehwag et al. 2026. ASPI: Seeking Ambiguity Clarification Amplifies Prompt Injection Vulnerability in LLM Agents. https://arxiv.org/abs/2605.17324

**Engineering**

- GitHub Spec Kit: https://github.com/github/spec-kit
- Kiro Specs: https://kiro.dev/docs/specs/
- obra/superpowers: https://github.com/obra/superpowers
- BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD
- claude-task-master: https://github.com/eyaltoledano/claude-task-master
- Agent OS: https://github.com/buildermethods/agent-os
- severity1/claude-code-prompt-improver: https://github.com/severity1/claude-code-prompt-improver
- Claude Code best practices: https://code.claude.com/docs/en/best-practices
- Claude Code skills, hooks, and plugins: https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/plugins-reference
- Agent Skills specification: https://agentskills.io/specification
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Codex skills: https://learn.chatgpt.com/docs/build-skills
- OpenAI Codex prompting guide: https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- Cognition, Don't Build Multi-Agents: https://cognition.ai/blog/dont-build-multi-agents
- Manus, Context Engineering for AI Agents: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
