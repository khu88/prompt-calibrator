"""Tests for hooks/calibrate_gate.py. Run: python3 -m unittest discover -s tests"""
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "calibrate_gate.py"
spec = importlib.util.spec_from_file_location("calibrate_gate", HOOK)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def run_hook(prompt, **env):
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": prompt}),
        capture_output=True,
        text=True,
        env={**os.environ, **env},
        check=True,
    )
    return result.stdout.strip()


class ScoreTest(unittest.TestCase):
    def assertFlagged(self, prompt):
        total, hits = gate.score(prompt)
        self.assertGreaterEqual(total, gate.DEFAULT_THRESHOLD, (prompt, hits))

    def assertPasses(self, prompt):
        total, hits = gate.score(prompt)
        self.assertLess(total, gate.DEFAULT_THRESHOLD, (prompt, hits))

    def test_flags_irreversible_and_vague_work(self):
        self.assertFlagged("Delete all unused resources in staging")
        self.assertFlagged("Can you clean up the unused buckets in prod?")
        self.assertFlagged("把 staging 上没用的资源清一下")
        self.assertFlagged("Drop table users and recreate it")

    def test_flags_long_horizon_work(self):
        self.assertFlagged("Optimize the whole codebase")
        self.assertFlagged("Switch auth to JWT across all services and run subagents in parallel")
        self.assertFlagged("用多个agent并行重构整个项目")

    def test_passes_small_or_clear_requests(self):
        self.assertPasses("Fix the typo in README")
        self.assertPasses("Optimize the query")
        self.assertPasses("提高测试覆盖率")
        self.assertPasses("Rename getUser to fetchUser")

    def test_passes_read_only_questions(self):
        self.assertPasses("How do I deploy to prod?")
        self.assertPasses("What does this migration do?")
        self.assertPasses("这个部署脚本是做什么的？")

    def test_done_criteria_lower_the_score(self):
        vague, _ = gate.score("Refactor the parser")
        specified, _ = gate.score("Refactor the parser; done when tests pass")
        self.assertLess(specified, vague)


class HookOutputTest(unittest.TestCase):
    def test_emits_additional_context(self):
        output = json.loads(run_hook("Deploy the new build to production"))
        hook_output = output["hookSpecificOutput"]
        self.assertEqual(hook_output["hookEventName"], "UserPromptSubmit")
        self.assertIn("prompt-calibrator", hook_output["additionalContext"])

    def test_silent_below_threshold(self):
        self.assertEqual(run_hook("Fix the typo in README"), "")

    def test_bypass_prefixes(self):
        for prefix in "*/#":
            self.assertEqual(run_hook(prefix + "Deploy to production"), "")

    def test_threshold_env(self):
        self.assertEqual(run_hook("Deploy to production", PROMPT_CALIBRATOR_THRESHOLD="off"), "")
        self.assertNotEqual(run_hook("Optimize the query", PROMPT_CALIBRATOR_THRESHOLD="1"), "")

    def test_malformed_input_is_ignored(self):
        result = subprocess.run(
            [sys.executable, str(HOOK)], input="not json", capture_output=True, text=True, check=True
        )
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
