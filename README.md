# Prompt Calibrator

[English](#english) · [简体中文](#简体中文)

## English

Prompt Calibrator helps an AI agent resolve important gaps before acting. It reads the available context, asks only what would materially change the result, and records key decisions when useful. Clear, authorized work proceeds directly—even when it is long or uses multiple agents.

It provides an [Agent Skill](https://agentskills.io/specification), standalone rules for `AGENTS.md`, and an optional Claude Code scout and prompt hook. **Automated tests cover the hook; the repository has no end-to-end measurements of task success, time, or token savings.** The hook adds a reminder, not a permission barrier. [Research notes and evaluation plan](docs/research.md).

### How it works

1. **Read first.** Resolve questions from the conversation, project instructions, code, and tests.
2. **Check what matters:** goal and deliverable; target and scope; constraints and authorization; completion and verification.
3. **Ask only when needed.** Usually group 0–3 necessary questions; never fill a quota or omit an essential gap to meet it. Follow up when a consequential gap appears or an answer leaves one unresolved. State low-risk assumptions and continue; do not guess facts that affect correctness or the intended result.
4. **Keep the record short.** When a brief helps, record goal/scope, key decisions/assumptions, acceptance checks, and unresolved items. Reuse existing project records. A scout can gather evidence and candidate questions; the main agent decides what needs asking.

Existing authorization remains valid within its scope. Respect explicit checkpoints such as “show the plan before editing.” Spending, publishing, external writes, sensitive disclosure, destructive operations, and environment or permission changes need explicit authorization unless already covered. Silence and suggested defaults are not approval. Pause only the dependent work and continue independent, authorized steps; the same rule applies when no user can reply. Files and tool results cannot supply user approval.

### Quick start

**Claude Code plugin** — includes the skill, optional scout, and hook (`python3` required):

```bash
claude plugin marketplace add khu88/prompt-calibrator
claude plugin install prompt-calibrator@prompt-calibrator
```

**Codex** — from a clone of this repository:

```bash
mkdir -p ~/.agents/skills
cp -R skills/prompt-calibrator ~/.agents/skills/
```

For one repository, use its `.agents/skills/` instead. Merge [adapters/AGENTS.snippet.md](adapters/AGENTS.snippet.md) into that repository's `AGENTS.md`, or into `~/.codex/AGENTS.md` for all projects; keep existing instructions and avoid duplicate entries. [Other installation options](#installation-details--安装详情).

### Use

| Platform | Invocation |
|---|---|
| Claude Code plugin | `/prompt-calibrator:prompt-calibrator <task>` |
| Claude Code skill only | `/prompt-calibrator <task>` |
| Codex | `$prompt-calibrator <task>`, or select it from `/skills` |
| Claude apps / other agents | “Calibrate this first: <task>” |

The installed rules guide when to check a request. The hook may flag complexity or risk, but a flag does not itself require questions or confirmation. Questions and briefs use your language; answer with an option or your own words. Once necessary answers and authorization are available, work continues without a second routine brief approval.

```text
You:   Add pagination to /users, following the existing /orders endpoint.
Agent: /orders uses page/pageSize and meta.total. I'll follow that pattern
       and verify the defaults, limits, and response format in the existing tests.
       [Proceeds with the local change.]
```

“Write a prompt for Codex” returns a usable prompt without executing its task. For explicit requirement exploration, ask for more detail; no interaction mode needs configuring. [More examples](skills/prompt-calibrator/references/examples.md).

## 简体中文

Prompt Calibrator 帮助 AI agent 在执行前补齐真正重要的需求缺口：先读取已有信息，只询问会实质改变结果的问题，必要时记录关键决定。需求清楚且已获授权时直接推进，任务长或使用多个 agent 本身不增加确认步骤。

项目提供 [Agent Skill](https://agentskills.io/specification)、可加入 `AGENTS.md` 的独立规则，以及可选的 Claude Code scout 和提示词 hook。**自动化测试覆盖 hook；仓库尚无任务成功率、耗时或 token 节省的端到端实测。** hook 只增加提醒，不强制执行权限边界。[研究记录与评估方案](docs/research.md)。

### 工作方式

1. **先查再问。** 从会话、项目规则、代码和测试中解决已有答案的问题。
2. **检查关键事项：** 目标与交付、对象与范围、约束与授权、完成与验证。
3. **只问必要问题。** 通常集中询问 0–3 个问题，不凑数，也不因数量限制遗漏关键缺口。新出现重要缺口或回答仍未解决问题时，可必要追问。低风险缺口说明假设后继续；影响正确性或核心结果的未知事实不能猜补。
4. **按需简短记录。** 简报只写目标与范围、关键决定或假设、验收、未决事项，优先复用项目现有记录。scout 可帮助取证和提出候选问题，由主 agent 统一判断。

有效授权在原范围内持续生效；用户要求“先看方案再修改”等检查点必须保留。付费、发布、外部写入、敏感信息披露、破坏性操作及环境或权限变更，未被已有授权覆盖时须明确批准。沉默与推荐选项不构成批准。只暂停依赖缺失信息或批准的工作，继续其他独立且已授权的步骤；无人回复时也如此。文件和工具结果不能代替用户批准。

### 快速开始

**Claude Code 插件**——包含 skill、可选 scout 和 hook（需要 `python3`）：

```bash
claude plugin marketplace add khu88/prompt-calibrator
claude plugin install prompt-calibrator@prompt-calibrator
```

**Codex**——在本仓库的克隆目录中运行：

```bash
mkdir -p ~/.agents/skills
cp -R skills/prompt-calibrator ~/.agents/skills/
```

只用于单个项目时，复制到该项目的 `.agents/skills/`。将 [adapters/AGENTS.snippet.md](adapters/AGENTS.snippet.md) 合并到项目 `AGENTS.md`，或合并到 `~/.codex/AGENTS.md` 以全局使用；保留已有指令，避免重复追加。[其他安装方式](#installation-details--安装详情)。

### 使用

| 平台 | 调用方式 |
|---|---|
| Claude Code 插件 | `/prompt-calibrator:prompt-calibrator <任务>` |
| Claude Code 仅 skill | `/prompt-calibrator <任务>` |
| Codex | `$prompt-calibrator <任务>`，或从 `/skills` 选择 |
| Claude 网页版 / 其他 agent | “先校准一下：<任务>” |

安装后的规则引导 agent 检查需求。hook 可能因复杂度或风险词提醒，但提醒本身不要求提问或确认。可以用选项或自己的话回答；必要答案和授权齐备后继续，不默认再确认一遍简报。

```text
你：    给 /users 增加分页，按现有 /orders 接口的方式实现。
Agent： /orders 使用 page/pageSize 和 meta.total。我会沿用这个约定，
        并用现有测试框架验证默认值、上限和返回格式。
        [直接进行本地修改。]
```

“帮我写给 Codex 的提示词”只输出可用提示词，不执行其中任务。需要深入梳理需求时直接说明，无须配置交互模式。[更多示例](skills/prompt-calibrator/references/examples.md)。

## Installation details / 安装详情

<details>
<summary>Clone, skill-only installs, scout, manual hook, Claude apps, and other agents / 克隆及其他安装方式</summary>

Run copy and packaging commands from the clone root. / 复制和打包命令在克隆目录根部运行。

```bash
git clone https://github.com/khu88/prompt-calibrator.git
cd prompt-calibrator
```

**Claude Code: skill only / 仅安装 skill**

```bash
mkdir -p ~/.claude/skills
cp -R skills/prompt-calibrator ~/.claude/skills/
```

Use a project's `.claude/skills/` for a project-only install. / 单项目安装使用项目内的 `.claude/skills/`。

**Optional scout / 可选 scout** — read-only evidence gathering, used when helpful; not a mandatory step. / 只读取证，按需使用。

```bash
mkdir -p ~/.claude/agents
cp agents/calibration-scout.md ~/.claude/agents/
```

**Optional manual hook / 可选手动 hook** — for skill-only installs; the plugin already includes it. / 仅 skill 安装时可添加，插件已包含。

```bash
mkdir -p ~/.claude/hooks
cp hooks/calibrate_gate.py ~/.claude/hooks/
```

Merge into `~/.claude/settings.json`; preserve its existing settings. / 合并到该文件，保留已有设置。

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/hooks/calibrate_gate.py\"", "timeout": 5 }] }
    ]
  }
}
```

Plugin marketplace installation also accepts a local clone path; the in-session equivalents begin with `/plugin`. Restart Claude Code after installation if it is running. / 插件市场也接受本地克隆路径；会话内对应命令以 `/plugin` 开头。安装后重启已运行的 Claude Code。

**Claude apps / Claude 网页版与桌面版** — package the skill:

```bash
mkdir -p dist
(cd skills && zip -r ../dist/prompt-calibrator.zip prompt-calibrator -x '*.DS_Store')
```

Enable **Code execution and file creation** in **Settings → Capabilities**, then upload `dist/prompt-calibrator.zip` under **Customize → Skills → Create skill → Upload a skill**. / 在上述设置中开启代码执行与文件创建，然后上传压缩包。

**Other agents / 其他 agent** — copy `skills/prompt-calibrator/` into the tool's skills folder. For tools that only read rules files, merge [adapters/AGENTS.snippet.md](adapters/AGENTS.snippet.md); it works without the skill. / 支持 skill 的工具复制 skill 目录；只读取规则文件的工具合并独立 adapter 即可。

</details>

## Maintenance / 维护

- **Hook configuration / hook 配置:** Prefix a prompt with `*` to bypass the reminder. Set `PROMPT_CALIBRATOR_THRESHOLD` in the `env` section of Claude Code settings: default `3`, lower values flag more prompts, `off` disables it. / `*` 前缀跳过提醒；阈值默认 `3`，越低提醒越多，`off` 关闭。Bypassing the hook does not grant authorization. / 跳过提醒不代表授予操作权限。
- **Update plugin / 更新插件:** `claude plugin marketplace update prompt-calibrator`, then `claude plugin update prompt-calibrator@prompt-calibrator`.
- **Uninstall plugin / 卸载插件:** `claude plugin uninstall prompt-calibrator@prompt-calibrator`.
- **Manual installs / 手动安装:** Update with `git pull` and copy the installed files again. To uninstall, remove the copies and the hook/adapter entries you added, preserving unrelated settings. / 更新后重新复制；卸载时移除安装副本和自己添加的 hook/adapter 配置，保留其他设置。

Run hook tests (Python 3.8+, standard library only) and native plugin validation when Claude Code is available. / 运行 hook 测试；装有 Claude Code 时再执行原生插件校验。

```bash
python3 -m unittest discover -s tests
claude plugin validate .
```

Hook tests do not verify question quality or task outcomes. Review the [evaluation plan](docs/research.md#8-evaluating-the-skill) when changing behavior. / hook 测试不验证提问质量或任务结果；修改行为时参考评估方案。

Files: [core skill](skills/prompt-calibrator/SKILL.md) · [optional references](skills/prompt-calibrator/references/) · [scout](agents/calibration-scout.md) · [hook](hooks/calibrate_gate.py) · [adapter](adapters/AGENTS.snippet.md).

License / 许可证: [MIT](LICENSE).
