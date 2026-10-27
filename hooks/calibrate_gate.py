#!/usr/bin/env python3
"""UserPromptSubmit hook for prompt-calibrator.

Scores each submitted prompt for signs of irreversible, long-horizon,
multi-agent, or vague work. When the score reaches the threshold, it adds a
short note to Claude's context recommending the prompt-calibrator skill.
It never blocks a prompt.

Bypass: start the prompt with "*". Prompts starting with "/" or "#" are ignored.
Threshold: env PROMPT_CALIBRATOR_THRESHOLD (integer, default 3; "off" disables).
"""
import json
import os
import re
import sys

DEFAULT_THRESHOLD = 3
LONG_PROMPT_CHARS = 400

# Keyword patterns cover English and Chinese prompts.
SIGNALS = [
    (
        "irreversible",
        3,
        r"\b(delete|purge|wipe|truncate|drop (table|database|column|index|schema|collection)|rm -rf"
        r"|reset --hard|force[- ]?push|git push|overwrite|migrat\w*|deploy\w*|publish|go live|rollback"
        r"|roll back|prod|production|staging|send (an? |the )?(emails?|messages?|newsletters?)"
        r"|revoke|rotate (the )?(keys?|secrets?|credentials?))\b"
        r"|删除|删掉|删库|清理|清空|清掉|清除|清一下|迁移|部署|上线|线上|生产环境|正式环境|回滚|发布"
        r"|覆盖掉|强制覆盖|覆写|重置|群发|撤销权限|轮换密钥",
    ),
    (
        "long-horizon",
        2,
        r"\b(in parallel|parallel|sub-?agents?|multi-?agents?|end[- ]to[- ]end|from scratch|full[- ]stack"
        r"|overhaul|(whole|entire) (repo|repository|codebase|project|app|system)"
        r"|all (services|modules|endpoints|pages)|across (the )?(codebase|repo|services|modules))\b"
        r"|并行|多个?\s*agent|子\s*agent|子代理|全量|整个(仓库|项目|系统|代码库|应用)"
        r"|所有(服务|模块|接口|页面)|端到端|从零|从头|全栈|一整套",
    ),
    (
        "vague",
        1,
        r"\b(optimi[sz]e|clean ?up|tidy|refactor|improve|polish|enhance|make it (better|nicer|work)"
        r"|fix (it|this|things)|etc|somehow|whatever|something like|unused|as needed)\b"
        r"|优化|整理|重构|完善|改进|改善|修一下|弄一下|搞一下|处理一下|看着办|尽量|相关的|之类|没用的|不用的"
        r"|随便|差不多",
    ),
]

ACCEPTANCE = re.compile(
    r"\b(tests? pass\w*|should|must|expect\w*|acceptance|done when|definition of done|criteria|verify)\b"
    r"|验收|完成标准|成功标准|测试通过|必须|应当|应该|期望|预期|验证",
    re.IGNORECASE,
)

# Read-only questions ("how do I deploy?") rarely need calibration.
QUESTION = re.compile(
    r"^(what|why|how|where|which|who|explain|describe|summari[sz]e|tell me)\b"
    r"|[?？]\s*$|^(什么|为什么|怎么|如何|哪|解释|说明|介绍|是否)|吗\s*$",
    re.IGNORECASE,
)


def score(prompt):
    """Return (score, signal labels) for a prompt."""
    total, hits = 0, []
    for label, weight, pattern in SIGNALS:
        if re.search(pattern, prompt, re.IGNORECASE):
            total += weight
            hits.append(label)
    if len(prompt) > LONG_PROMPT_CHARS:
        total += 1
        hits.append("long")
    if total > 0 and not ACCEPTANCE.search(prompt):
        total += 1
        hits.append("no-done-criteria")
    if total > 0 and QUESTION.search(prompt):
        total -= 2
        hits.append("question")
    return total, hits


def threshold():
    raw = os.environ.get("PROMPT_CALIBRATOR_THRESHOLD", "").strip().lower()
    if raw in ("off", "false", "none"):
        return None
    try:
        return int(raw) if raw else DEFAULT_THRESHOLD
    except ValueError:
        return DEFAULT_THRESHOLD


def main():
    limit = threshold()
    if limit is None:
        return 0
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0  # Malformed input: never interfere.

    prompt = str(payload.get("prompt", "")).strip()
    if not prompt or prompt[0] in "*/#":
        return 0

    total, hits = score(prompt)
    if total < limit:
        return 0

    note = (
        "[prompt-calibrator] Signals: {} (score {}). Check context and existing decisions first. "
        "Use prompt-calibrator when clarification is needed or requested; task size or multiple agents "
        "alone do not require questions. Proceed within existing authorization, honor user checkpoints, "
        "and ask only for necessary answers or missing approval. Silence is not authorization; pause "
        "only dependent work."
    ).format(", ".join(hits), total)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": note,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
