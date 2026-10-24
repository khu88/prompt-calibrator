# Prompt Calibrator

[English](#english) · [简体中文](#简体中文)

---

## English

Prompt Calibrator is a pre-flight step for AI agents. Before an agent starts a long, multi-agent, or risky task, it works out what the request leaves unspecified. It answers what it can from the project, asks you at most three high-value questions, and writes the result into a short, verifiable brief. The run starts from a clear spec instead of a guess.

It ships as an [Agent Skill](https://agentskills.io/specification) that works in Claude Code, Codex, Claude apps, and any agent that reads `SKILL.md`, `AGENTS.md`, or a rules file. Claude Code also gets a read-only subagent and a prompt hook.

**Evaluation status:** Automated tests cover the prompt hook. This repository does not yet include end-to-end benchmark results for the skill's effect on task success, time, or token use. Research figures below describe the cited studies, not measured results for Prompt Calibrator. The hook adds a reminder; it does not enforce an execution or permission boundary.

### Why

Vague requests rarely make agents fail outright. They make agents guess, and on a long run an early wrong guess turns into rounds of trial and error that waste time and tokens. On underspecified DevOps instructions, coding agents cross at least one action boundary in 55.8–67.8% of runs. Feeding requirements in over several turns costs LLMs 39% on average. Detecting underspecification separately from execution brings resolve rates back close to fully specified instructions. Sources are in [docs/research.md](docs/research.md).

### How it works

```
your request
  → triage: L0 pass-through · L1 light · L2 full
  → ground: read project instructions, code, and tests; answer what it can
  → gap scan: 12 dimensions (done criteria, target, scope, implicit requirements, risk, …)
  → ask or assume: at most 3 multiple-choice questions; everything else becomes a logged assumption
  → Calibrated Brief: goal, red lines, done criteria, decisions, assumptions, confirm-before list
  → execute or delegate with sub-briefs → re-calibrate only on defined triggers
```

| Level | When | What the agent does |
|---|---|---|
| L0 | A one-sentence change, a read-only question, or "just do it" on reversible work | Acts immediately; no calibration |
| L1 | Bounded, reversible, a few gaps | States its understanding, assumptions, and verification, then acts without waiting |
| L2 | Long-horizon, multi-agent, cross-module, irreversible, or a vague goal | Asks up to 3 questions, writes a brief, waits for your confirmation |

An irreversible action with an uncertain target, such as deleting "the unused stuff" or deploying to "the server", always needs a confirmed target list. If you don't answer, the default is the safest option, such as a dry-run.

### Install

Most commands below run from the root of a clone:

```bash
git clone https://github.com/khu88/prompt-calibrator.git
cd prompt-calibrator
```

#### Claude Code: plugin (recommended)

Installs the skill, the `calibration-scout` subagent, and the prompt hook:

```bash
claude plugin marketplace add khu88/prompt-calibrator
claude plugin install prompt-calibrator@prompt-calibrator
```

You can also run `/plugin marketplace add khu88/prompt-calibrator` and `/plugin install prompt-calibrator@prompt-calibrator` inside a session, or pass a local clone path instead of `khu88/prompt-calibrator`. Restart Claude Code if it is already running. The hook needs `python3` on your `PATH`.

#### Claude Code: skill only

```bash
mkdir -p ~/.claude/skills && cp -R skills/prompt-calibrator ~/.claude/skills/
```

To install for one project only, copy the folder into that project's `.claude/skills/` instead.

Optionally, add the subagent:

```bash
mkdir -p ~/.claude/agents && cp agents/calibration-scout.md ~/.claude/agents/
```

Optionally, add the hook. Copy `hooks/calibrate_gate.py` to `~/.claude/hooks/`, then merge this into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/hooks/calibrate_gate.py\"", "timeout": 5 }] }
    ]
  }
}
```

#### Claude apps (web and desktop)

1. Package the skill:

   ```bash
   mkdir -p dist && cd skills && zip -r ../dist/prompt-calibrator.zip prompt-calibrator -x '*.DS_Store'
   ```

2. In Claude, go to **Settings → Capabilities** and turn on **Code execution and file creation**.
3. Go to **Customize → Skills**, click **+**, choose **Create skill → Upload a skill**, and select `dist/prompt-calibrator.zip`.

#### Codex

```bash
mkdir -p ~/.agents/skills && cp -R skills/prompt-calibrator ~/.agents/skills/
```

To install for one repository only, copy the folder into `<your-repo>/.agents/skills/` instead. Then add the trigger rules to your repository's `AGENTS.md`, or to `~/.codex/AGENTS.md` to apply them everywhere:

```bash
cat adapters/AGENTS.snippet.md >> <your-repo>/AGENTS.md
```

#### Other agents

- **Tools that support Agent Skills (`SKILL.md`)**: copy `skills/prompt-calibrator/` into the tool's skills folder.
- **Tools that only read AGENTS.md or a rules file** (Cursor rules, Cline rules, custom instructions, system prompts): paste the contents of `adapters/AGENTS.snippet.md`. It is self-contained and works without the skill.

### Usage

#### When it runs

It runs automatically when a request is long-horizon, multi-agent or parallel, cross-module, irreversible (delete, migrate, deploy, production, sending messages, spending), vague, or missing a definition of done. Small, clear requests (L0) pass straight through. In Claude Code, the hook also adds a reminder when a prompt looks risky.

#### Run it explicitly

| Where | How |
|---|---|
| Claude Code (plugin) | `/prompt-calibrator:prompt-calibrator <your task>` |
| Claude Code (skill only) | `/prompt-calibrator <your task>` |
| Codex | `$prompt-calibrator <your task>`, or pick it from `/skills` |
| Claude apps and other agents | "Calibrate this first: <your task>" |

#### Example session

```
You:    Switch auth from sessions to JWT, frontend and backend. Use parallel agents.

Agent:  L2: cross-module change with parallel agents, so full calibration.
        Q1. How should signed-in users transition? (affects: whether a dual-stack period is needed)
          A. Accept both session and JWT for 2 weeks (recommended: no forced logout)
          B. Force everyone to sign in again at launch
          Default if unanswered: A
        Q2. Where should the frontend keep the token? (affects: XSS/CSRF defenses)
          A. httpOnly cookie + CSRF token (recommended)   B. In memory + refresh cookie   C. localStorage
          Default if unanswered: A
        Q3. Is mobile/ in scope? (affects: number of subagents)
          A. Yes   B. No, keep the API backward compatible
          Default if unanswered: B
        Reply like "1A 2C 3B", or "go with the recommendations".

You:    1A 2A 3B

Agent:  Calibrated Brief: sessions → JWT
        Goal · Red lines · Done when · Scope · Decisions · Assumptions · Confirm before · Plan · Verification
        Confirm and I'll start.

You:    Go.
```

#### Answer the questions

- Reply with option letters: `1A 2C 3B`.
- Reply "go with the recommendations" to accept every recommended option.
- Answer in your own words if no option fits.
- Unanswered questions take the stated default. For irreversible actions, the default is always the safest option.

#### Review the brief

- At L2 the agent shows the brief and waits. Reply "go" to start, or correct any line, for example "assumption 2 is wrong: we use pnpm".
- At L1 the agent states its understanding and assumptions in a few lines and starts right away. Interrupt if anything is wrong.
- For long tasks the brief is saved to `.calibration/brief.md` in your project, and the agent re-reads it at each milestone. Add `.calibration/` to your `.gitignore` if you don't want to commit it.
- During execution the agent stops only when an assumption proves false, the scope must grow, the same approach fails twice, or an action from the brief's confirm-before list is next.

#### Options

| Say | Effect |
|---|---|
| "calibrate minimal", "just do it", "stop asking" | At most 1 blocking question. Irreversible targets are still confirmed. |
| *(nothing)* | `normal`: at most 3 questions in one round |
| "calibrate thorough" | Up to 2 rounds of 3 questions, for exploring requirements |
| "Write a prompt for Codex: …", "refine this prompt" | Brief-only mode: returns a pasteable, calibrated prompt and executes nothing |

Questions and briefs follow the language you write in. In non-interactive runs (headless, CI, subagents) the agent never blocks. It takes the defaults, skips or dry-runs irreversible steps, and lists the open questions in its final report.

#### Hook settings (Claude Code)

- Start a prompt with `*` to skip the hook for that prompt.
- Set `PROMPT_CALIBRATOR_THRESHOLD` in the `env` block of `settings.json` to tune sensitivity. The default is `3`; a lower value flags more prompts, and `off` disables the hook.

  ```json
  { "env": { "PROMPT_CALIBRATOR_THRESHOLD": "4" } }
  ```

### Update and uninstall

Plugin:

```bash
claude plugin marketplace update prompt-calibrator
claude plugin update prompt-calibrator@prompt-calibrator
claude plugin uninstall prompt-calibrator@prompt-calibrator
```

Skill-only installs: run `git pull` and copy the folder again to update; delete the copied `prompt-calibrator` folder to uninstall.

### Repository layout

```
.claude-plugin/              Claude Code plugin manifest and single-plugin marketplace
skills/prompt-calibrator/    The portable Agent Skill
  SKILL.md                   Workflow, rules, modes
  references/                Gap checklist, question design, brief templates, examples
agents/calibration-scout.md  Claude Code subagent: read-only grounding and gap scan
hooks/                       Claude Code UserPromptSubmit hook and its config
adapters/AGENTS.snippet.md   Standalone rules for Codex and other AGENTS.md or rules-file tools
docs/research.md             Design rationale, evidence, evaluation plan
tests/                       Hook tests
```

### Development

Run the hook tests (Python 3.8+ standard library only):

```bash
python3 -m unittest discover -s tests
```

Validate the plugin and marketplace manifests:

```bash
claude plugin validate .
```

When you change the hook's keyword lists, add every misclassified prompt as a test case. Before changing the skill's wording, read [docs/research.md](docs/research.md#8-evaluating-the-skill): it explains how to measure whether the skill helps, using resolve rate, boundary violations, questions per task, and over- and under-asking rates.

### License

[MIT](LICENSE)

---

## 简体中文

Prompt Calibrator 是 AI agent 执行任务前的“校准”环节。在 agent 开始长程、多 agent 或高风险任务之前，它先找出需求中没有说清的地方：能从项目里查到的自己查，再向你提出最多三个关键问题，最后把结果整理成一份简短、可验证的任务简报（Calibrated Brief）。这样 agent 从清晰的规格出发，而不是从猜测出发。

它以 [Agent Skill](https://agentskills.io/specification) 形式提供，可用于 Claude Code、Codex、Claude 网页版和桌面版，以及任何能读取 `SKILL.md`、`AGENTS.md` 或规则文件的 agent。Claude Code 还可以额外使用一个只读子 agent 和一个提示词 hook。

**评估状态：** 自动化测试覆盖提示词 hook；仓库目前尚未提供该 skill 对任务成功率、耗时或 token 用量影响的端到端评测结果。下文研究数字来自所引用的研究，并非 Prompt Calibrator 的实测结果。hook 只提供提醒，不强制执行操作或权限边界。

### 为什么需要

模糊的需求很少让 agent 直接失败，而是让它去“猜”。在长任务中，一开始猜错，后面就是一轮又一轮的试错，白白浪费时间和 token。研究显示：面对欠规格的 DevOps 指令，coding agent 有 55.8–67.8% 的运行至少越过一条操作边界；需求分多轮零散给出时，LLM 的表现平均下降 39%；把“欠规格检测”从执行中单独拿出来，解决率可以回到接近完整规格的水平。出处见 [docs/research.md](docs/research.md)。

### 工作流程

```
你的需求
  → 分级：L0 直通 · L1 轻校准 · L2 完整校准
  → 取证：阅读项目说明、代码和测试，能自己回答的就不问
  → 缺口扫描：12 个维度（完成标准、目标对象、范围、隐性需求、风险……）
  → 问还是假设：最多 3 个选择题；其余缺口用默认值补全，并记为假设
  → 校准简报：目标、红线、完成标准、已决策事项、假设、需确认的操作
  → 执行，或用子简报委派给子 agent → 仅在约定的情况下重新校准
```

| 等级 | 适用情况 | agent 的做法 |
|---|---|---|
| L0 | 一句话能说清的改动、只读问题，或对可逆操作说了“直接做” | 直接执行，不校准 |
| L1 | 范围明确、可逆、只有少量缺口 | 先用几行说明理解、假设和验证方式，然后直接执行，不等待 |
| L2 | 长程、多 agent、跨模块、不可逆，或目标本身模糊 | 最多问 3 个问题，写出简报，等你确认后再执行 |

如果是不可逆操作且目标不确定（例如删除“没用的东西”、部署到“服务器”），一定会先请你确认具体对象清单。你不回答时，默认取最安全的选项（例如只做 dry-run）。

### 安装

下面大多数命令都在克隆后的仓库根目录下运行：

```bash
git clone https://github.com/khu88/prompt-calibrator.git
cd prompt-calibrator
```

#### Claude Code：插件方式（推荐）

一次装好 skill、`calibration-scout` 子 agent 和提示词 hook：

```bash
claude plugin marketplace add khu88/prompt-calibrator
claude plugin install prompt-calibrator@prompt-calibrator
```

也可以在会话中运行 `/plugin marketplace add khu88/prompt-calibrator` 和 `/plugin install prompt-calibrator@prompt-calibrator`，或者把 `khu88/prompt-calibrator` 换成本地克隆的路径。如果 Claude Code 已在运行，装好后请重启。hook 需要 `PATH` 中有 `python3`。

#### Claude Code：只装 skill

```bash
mkdir -p ~/.claude/skills && cp -R skills/prompt-calibrator ~/.claude/skills/
```

只想在某个项目里用，就把文件夹复制到该项目的 `.claude/skills/` 下。

可选：添加子 agent：

```bash
mkdir -p ~/.claude/agents && cp agents/calibration-scout.md ~/.claude/agents/
```

可选：添加 hook。把 `hooks/calibrate_gate.py` 复制到 `~/.claude/hooks/`，再把以下内容合并进 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/hooks/calibrate_gate.py\"", "timeout": 5 }] }
    ]
  }
}
```

#### Claude 网页版和桌面版

1. 打包 skill：

   ```bash
   mkdir -p dist && cd skills && zip -r ../dist/prompt-calibrator.zip prompt-calibrator -x '*.DS_Store'
   ```

2. 在 Claude 中打开 **Settings → Capabilities**，开启 **Code execution and file creation**。
3. 打开 **Customize → Skills**，点 **+**，选择 **Create skill → Upload a skill**，上传 `dist/prompt-calibrator.zip`。

#### Codex

```bash
mkdir -p ~/.agents/skills && cp -R skills/prompt-calibrator ~/.agents/skills/
```

只想在某个仓库里用，就复制到 `<你的仓库>/.agents/skills/`。然后把触发规则追加到仓库的 `AGENTS.md`；如果想对所有项目生效，就追加到 `~/.codex/AGENTS.md`：

```bash
cat adapters/AGENTS.snippet.md >> <你的仓库>/AGENTS.md
```

#### 其他 agent

- **支持 Agent Skills（`SKILL.md`）的工具**：把 `skills/prompt-calibrator/` 复制到该工具的 skills 目录。
- **只读取 AGENTS.md 或规则文件的工具**（Cursor rules、Cline rules、自定义指令、系统提示词）：粘贴 `adapters/AGENTS.snippet.md` 的内容即可。它是自包含的，不装 skill 也能用。

### 使用方法

#### 什么时候自动触发

遇到以下请求时会自动触发：长程任务、多 agent 或并行、跨模块、不可逆操作（删除、迁移、部署、生产环境、对外发消息、花钱）、需求模糊，或没有完成标准。简单明确的请求（L0）直接放行。在 Claude Code 中，hook 还会在提示词看起来有风险时额外提醒 agent。

#### 手动调用

| 平台 | 调用方式 |
|---|---|
| Claude Code（插件） | `/prompt-calibrator:prompt-calibrator <你的任务>` |
| Claude Code（只装 skill） | `/prompt-calibrator <你的任务>` |
| Codex | `$prompt-calibrator <你的任务>`，或在 `/skills` 中选择 |
| Claude 网页版、桌面版及其他 agent | “先校准一下：<你的任务>” |

#### 示例对话

```
你：    把认证从 session 换成 JWT，前后端都要改，可以开多个 agent 并行。

Agent： L2：跨模块改动且多 agent 并行，进入完整校准。
        Q1. 已登录用户如何过渡？（影响：是否需要双栈兼容期）
          A. session 与 JWT 同时有效 2 周（推荐：用户无感）
          B. 上线即强制全部重新登录
          不回答则按 A
        Q2. 前端 token 存在哪里？（影响：XSS/CSRF 防护方案）
          A. httpOnly cookie + CSRF token（推荐）   B. 内存 + refresh cookie   C. localStorage
          不回答则按 A
        Q3. mobile/ 是否在本次范围内？（影响：子 agent 数量）
          A. 在   B. 不在，只保证接口向后兼容
          不回答则按 B
        回复如“1A 2C 3B”，或直接说“按推荐”。

你：    1A 2A 3B

Agent： 校准简报：session → JWT
        目标 · 红线 · 完成标准 · 范围 · 已决策 · 假设 · 需确认操作 · 计划 · 验证
        确认后开始执行。

你：    开始。
```

#### 回答问题

- 用选项字母回复：`1A 2C 3B`。
- 回复“按推荐”，即全部采用推荐选项。
- 选项都不合适时，直接用自己的话回答。
- 没回答的问题按默认值处理；涉及不可逆操作时，默认值总是最安全的选项。

#### 确认简报

- L2：agent 先展示简报并等待你确认。回复“开始”即可执行，也可以直接修改某一条，例如“假设 2 不对，我们用 pnpm”。
- L1：agent 用几行说明理解和假设后立即开始。如有不对，随时打断纠正。
- 长任务的简报会保存到项目中的 `.calibration/brief.md`，agent 在每个里程碑都会重新查看。不想提交的话，把 `.calibration/` 加进 `.gitignore`。
- 执行过程中，agent 只在以下情况停下来：假设被证伪、需要扩大范围、同一方法连续失败两次，或者下一步是简报中列为“需确认”的操作。

#### 选项

| 你这样说 | 效果 |
|---|---|
| “校准 minimal”“直接做”“别问了” | 最多 1 个阻断性问题；不可逆操作的目标仍会确认 |
| （不说） | `normal`：一轮最多 3 个问题 |
| “校准 thorough” | 最多 2 轮、每轮 3 个问题，适合需求探索阶段 |
| “帮我写一份给 Codex 的提示词：……”“完善这段提示词” | 只出简报模式：输出可直接粘贴的校准后提示词，不执行任务 |

提问和简报会使用你所用的语言。在无人值守的场景（headless、CI、子 agent）中，agent 不会卡住等待：它采用默认值，跳过不可逆步骤或只做 dry-run，并把未决问题列在最终报告里。

#### Hook 设置（Claude Code）

- 提示词以 `*` 开头，可以跳过本次 hook 检查。
- 在 `settings.json` 的 `env` 中设置 `PROMPT_CALIBRATOR_THRESHOLD` 来调整灵敏度。默认值为 `3`，数值越小提醒越多；设为 `off` 则关闭 hook。

  ```json
  { "env": { "PROMPT_CALIBRATOR_THRESHOLD": "4" } }
  ```

### 更新与卸载

插件方式：

```bash
claude plugin marketplace update prompt-calibrator
claude plugin update prompt-calibrator@prompt-calibrator
claude plugin uninstall prompt-calibrator@prompt-calibrator
```

只装 skill 的方式：`git pull` 后重新复制文件夹即可更新；删除复制过去的 `prompt-calibrator` 文件夹即可卸载。

### 目录结构

```
.claude-plugin/              Claude Code 插件清单和单插件 marketplace
skills/prompt-calibrator/    可移植的 Agent Skill
  SKILL.md                   流程、规则、模式
  references/                缺口清单、提问设计、简报模板、示例
agents/calibration-scout.md  Claude Code 子 agent：只读取证与缺口扫描
hooks/                       Claude Code UserPromptSubmit hook 及其配置
adapters/AGENTS.snippet.md   适用于 Codex 及其他读取 AGENTS.md 或规则文件的工具的独立规则
docs/research.md             设计依据、研究证据、评估方法（英文）
tests/                       hook 测试
```

### 开发

运行 hook 测试（只需 Python 3.8+ 标准库）：

```bash
python3 -m unittest discover -s tests
```

校验插件和 marketplace 清单：

```bash
claude plugin validate .
```

修改 hook 的关键词列表时，把每个误判的提示词都加成测试用例。修改 skill 措辞前，请先阅读 [docs/research.md](docs/research.md#8-evaluating-the-skill)，其中说明了如何衡量 skill 是否有效：解决率、越界操作率、每个任务的提问数，以及过度提问率和漏问率。

### 许可证

[MIT](LICENSE)
