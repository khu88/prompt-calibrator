# Design Rationale: Research and Prior Art

Updated 2026-10-13. Covers Claude Code, Codex, and other agent harnesses.

This document records the evidence behind each design decision in `prompt-calibrator`. Use it when you change the skill. The agent never needs it at runtime.

## Summary

1. **Underspecified instructions are a major cause of failure in long agent runs, and the cost grows with run length.** Given a vague instruction, agents guess rather than ask.
2. **What works is separating underspecification detection from execution and doing it once, up front.** The agent answers what it can from context, asks a few high-value questions with recommended answers, fills the rest with explicit assumptions, and produces a verifiable spec (the brief).
3. **Asking too much and asking too little both cost something.** The amount of questioning should adapt to impact × uncertainty × irreversibility. An irreversible action with an uncertain target always needs confirmation.
4. **Multi-agent work also has to be calibrated between agents.** A sub-brief must carry the decisions already made and the interface contracts. Underspecified plans from the planner are otherwise a leading cause of failure.

## 1. The problem: underspecification makes agents guess

| Study | Finding | Design implication |
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

| Study | Finding | Design implication |
|---|---|---|
| Vijayvargiya et al., Ambig-SWE (ICLR 2026) | On underspecified SWE-bench Verified, interaction improves results by up to 74%. Models struggle to tell underspecified instructions from well-specified ones. | Add an explicit "is this underspecified?" step. |
| Edwards & Schuster 2026, *Ask or Assume?* (EMNLP 2026) | A scaffold that separates underspecification detection from code execution resolves 69.40% of underspecified SWE-bench tasks, closing the gap to fully specified instructions. Its questioning is well calibrated: few questions on simple tasks, more on complex ones. | Use a dedicated calibrator (this skill or the scout subagent), not the executor in passing. |
| Wu & Fard, HumanEvalComm (TOSEM) | On problems made inconsistent, ambiguous, or incomplete, code LLMs mostly generate code without asking clarifying questions. | Models default to acting, so asking has to be built into the workflow. |
| Mu et al. 2023, ClarifyGPT | Detects ambiguity by checking whether sampled solutions agree; raises GPT-4's average across four benchmarks from 68.02% to 75.75%. | "Do different readings lead to different results?" works as a trigger (the divergence test). |
| Stoisser et al. 2026, Ambig-DS | Data-science agents silently commit to a plausible but wrong target or metric. One clarifying question recovers much of the loss, but agents can't tell when to ask: permissive prompts over-ask on clear tasks, and conservative prompts silently default on ambiguous ones. | Calibrate the asking threshold in both directions. |
| Zhou et al. 2025, SWEET-RL / ColBench | Multi-turn collaborative RL lets an 8B model match or exceed GPT-4o on collaborative tasks. | Collaboration can be trained, but prompting alone also helps. |

## 3. What to ask, and how much

| Study | Finding | Design implication |
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

| Study | Finding | Design implication |
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

| Project or guide | Mechanism | What this skill adopted |
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

## 7. Design decisions and their evidence

| Decision in the skill | Evidence |
|---|---|
| L0/L1/L2 triage; escalate when unsure | superpowers task classes; Claude Code's one-sentence-diff rule; BMAD's size-based planning |
| Ground before asking | Ambig-SWE, HumanEvalComm (models neither ask nor look); "answerable from the code" listed as a bad question |
| 12-dimension checklist, with focus on done criteria, target certainty, implicit requirements, and contradictions | Spec Kit categories; UnderSpecBench (target certainty); SWE-RPG (implicit requirements); Codex guide (contradictions) |
| Divergence test decides ask or assume | ClarifyGPT consistency check; KnowNo's ask-only-when-several-plans rule |
| Rank by impact × uncertainty × irreversibility; at most 3 questions | Uncertainty of Thoughts, SAGE-Agent (value of information); Spec Kit (impact × uncertainty, 3–5 cap) |
| Multiple choice with a recommendation and a default | Spec Kit; Roo Code; GATE (less user effort) |
| One round of questions | Laban et al. (39% drop from piecemeal requirements) |
| Explicit Assumptions list | *What Prompts Don't Say* (inferred requirements are fragile and need to be correctable) |
| Mandatory confirmation for irreversible actions with uncertain targets; most conservative default | UnderSpecBench; Codex guide's per-tool thresholds |
| Calibrate in both directions; never invent questions | Ambig-DS; CLAM; *Ask or Assume?* (few questions on simple tasks) |
| Brief of about 400 words, red lines at top and end | *Lost in the Middle*; *Context Rot*; *What Prompts Don't Say* (longer requirement lists aren't better) |
| Restate before executing; L2 confirmation | *Rephrase and Respond*; IN3; Claude Code's SPEC.md workflow |
| Sub-briefs carry decisions and interface contracts | Anthropic multi-agent post; Cognition; MAST; Planner-Coder Gap |
| Re-calibration triggers during execution | Manus (recitation, keeping errors); Spec Kit's deferred items |
| Non-interactive mode: defaults, no irreversible actions, questions in the report | Codex guide (don't stop unless blocked); UnderSpecBench (agents act on guesses) |
| Only the user's replies count as answers | ASPI |
| minimal / normal / thorough levels | *Steerable Clarification Policies* (cost-conditioned behavior) |
| Separate read-only scout subagent | *Ask or Assume?* (detection separated from execution) |

## 8. Evaluating the skill

Build a small internal set of 30–60 real past instructions, stratified by L0/L1/L2 and by whether they include irreversible actions. Run each with the skill on and off, and compare:

- **Effectiveness:** resolve or acceptance rate; boundary-violation rate, using UnderSpecBench's Wrong Target and OverScope categories; share of first deliverables the user accepts.
- **Efficiency:** questions per task, user answer time, total time and tokens, rework rounds (compare SWE-chat's pushback rate).
- **Calibration quality:** over-asking rate (L0 tasks that got questions), under-asking rate (high-impact gaps found later that weren't asked about), and the share of assumptions later overturned.

Use promptfoo for regression tests on prompt changes. With enough data and a metric, DSPy or GEPA can optimize the wording of SKILL.md. Tune the hook threshold (`PROMPT_CALIBRATOR_THRESHOLD`, default 3) against the over-asking and under-asking rates, and add each misclassified prompt to `tests/test_calibrate_gate.py`.

## 9. Limitations

- Many 2026 results (UnderSpecBench, SWE-RPG, Ambig-DS, ASPI, SWE-chat) are arXiv preprints and not all are peer-reviewed. The figures here were checked against the arXiv abstracts; check the full papers before citing them elsewhere.
- Asking thresholds depend heavily on the model. Claude models tend to spot underspecification more readily, while Codex models lean toward action. Evaluate the skill separately on each model you use.
- The hook is a keyword heuristic with false positives and negatives. It only nudges; the skill makes the call.
- "Ask in one round" conflicts with multi-turn requirement discovery. The `thorough` level is the compromise.

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
