#!/usr/bin/env python3
"""Contrôles hors ligne de l'édition publique ; uniquement des fixtures temporaires."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "adaptateurs/claude/fichiers-installation/.claude/hooks/barriere-git.py"
LAUNCHER = ROOT / "adaptateurs/codex/fichiers-installation/.codex/bin/review-native-codex"

def decision(command):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    result = subprocess.run([sys.executable, "-B", str(HOOK)], input=payload, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] if result.stdout.strip() else None

class PublicTests(unittest.TestCase):
    def test_hook_staging(self):
        self.assertEqual(decision("git add fictif.txt"), "ask")

    def test_hook_forced_push(self):
        self.assertEqual(decision("git push --force origin main"), "deny")

    def test_hook_invalid_payload(self):
        p = subprocess.run([sys.executable, "-B", str(HOOK)], input="not-json", capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout), (0, ""))

    def test_quoted_heredoc_literal(self):
        # Chaîne fournie au hook seulement : aucune commande shell exécutée.
        self.assertIsNone(decision("cat <<'EOF'\n$(git add fictif.txt)\nEOF"))

    def test_unquoted_heredoc_known_gap(self):
        # Constat de limite existante, pas une preuve de protection réussie.
        self.assertIsNone(decision("cat <<EOF\n$(git add fictif.txt)\nEOF"))

    def launcher(self, args, mode="ok"):
        with tempfile.TemporaryDirectory(prefix="workflow-launcher-") as d:
            work = Path(d)
            fake = work / "codex"
            fake.write_text("#!" + sys.executable + "\nimport json,os,sys\nfrom pathlib import Path\nPath(os.environ['CAPTURE']).write_text(json.dumps(sys.argv[1:]))\nmode=os.environ['FAKE_MODE']\nif mode=='error':sys.exit(9)\nif mode=='ok':print('FAKE_REVIEW_OK')\n")
            fake.chmod(0o700)
            env = {**os.environ, "PATH": str(work) + os.pathsep + os.environ["PATH"], "TMPDIR": str(work), "CAPTURE": str(work / "argv.json"), "FAKE_MODE": mode}
            result = subprocess.run(["/bin/sh", str(LAUNCHER), *args], cwd=work, env=env, capture_output=True, text=True)
            argv = json.loads((work / "argv.json").read_text()) if (work / "argv.json").exists() else None
            self.assertEqual(list(work.glob("review-native-codex.*")), [])
            return result, argv

    def test_launcher_uncommitted(self):
        p, argv = self.launcher(["--uncommitted"])
        self.assertEqual(p.returncode, 0)
        self.assertEqual(argv, ["exec", "--sandbox", "read-only", "--config", 'approval_policy="never"', "--config", 'model_reasoning_effort="high"', "review", "--uncommitted"])

    def test_launcher_base(self):
        p, argv = self.launcher(["--base", "main"])
        self.assertEqual(p.returncode, 0)
        self.assertEqual(argv[-2:], ["--base", "main"])

    def test_launcher_commit(self):
        p, argv = self.launcher(["--commit", "deadbeef"])
        self.assertEqual(p.returncode, 0)
        self.assertEqual(argv[-2:], ["--commit", "deadbeef"])

    def test_launcher_rejects_invalid_arguments(self):
        for args in [[], ["--sandbox", "danger"], ["--uncommitted", "extra"], ["--commit", "not-a-sha"], ["--base", "--bad"], ["--help", "extra"]]:
            with self.subTest(args=args):
                p, argv = self.launcher(args)
                self.assertEqual(p.returncode, 64)
                self.assertIsNone(argv)

    def test_launcher_propagates_failure(self):
        p, _ = self.launcher(["--uncommitted"], "error")
        self.assertEqual(p.returncode, 9)

    def test_launcher_rejects_empty_result(self):
        p, _ = self.launcher(["--uncommitted"], "empty")
        self.assertEqual(p.returncode, 70)

    def test_fingerprint_disposable_repository(self):
        with tempfile.TemporaryDirectory(prefix="workflow-fingerprint-") as d:
            work = Path(d)
            env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_OPTIONAL_LOCKS": "0"}
            subprocess.run(["/usr/bin/git", "init", "-q", str(work)], env=env, check=True, capture_output=True)
            (work / "fixture.txt").write_text("first")
            index = work / ".git/index"
            before_index = index.read_bytes() if index.exists() else None
            cmd = [sys.executable, "-B", str(ROOT / "outils/empreinte-git.py")]
            first = subprocess.check_output(cmd, cwd=work, env=env)
            self.assertEqual(first, subprocess.check_output(cmd, cwd=work, env=env))
            (work / "fixture.txt").write_text("second")
            self.assertNotEqual(first, subprocess.check_output(cmd, cwd=work, env=env))
            self.assertEqual(before_index, index.read_bytes() if index.exists() else None)
            self.assertEqual(subprocess.check_output(["/usr/bin/git", "status", "--porcelain"], cwd=work, env=env), b"?? fixture.txt\n")

    def test_installation_simulation_preserves_foreign_settings(self):
        def merge(original, fragment):
            result = copy.deepcopy(original)
            for key, value in fragment.items():
                result[key] = merge(result.get(key, {}), value) if isinstance(value, dict) else copy.deepcopy(value)
            return result
        with tempfile.TemporaryDirectory(prefix="workflow-install-") as d:
            home = Path(d)
            settings = home / ".claude/settings.json"
            settings.parent.mkdir()
            original = {"theme": "example", "mcpServers": {"fictif": {}}, "permissions": {"unrelatedExample": "keep"}}
            settings.write_text(json.dumps(original))
            backup = settings.read_bytes()
            fragment = json.loads((ROOT / "adaptateurs/claude/configuration-workflow.json").read_text())["fragment_settings"]
            settings.write_text(json.dumps(merge(original, fragment)))
            merged = json.loads(settings.read_text())
            self.assertEqual(merged["theme"], "example")
            self.assertEqual(merged["permissions"]["unrelatedExample"], "keep")
            self.assertEqual(merged["mcpServers"], original["mcpServers"])
            settings.write_bytes(backup)
            self.assertEqual(json.loads(settings.read_text()), original)
            # Vérifie les liens relatifs et fichiers statiques sans toucher au vrai HOME.
            target = home / ".codex/bin/review-native-codex"
            target.parent.mkdir(parents=True)
            target.write_bytes(LAUNCHER.read_bytes())
            link = home / ".local/bin/review-native-codex"
            link.parent.mkdir(parents=True)
            link.symlink_to("../../.codex/bin/review-native-codex")
            self.assertEqual(link.resolve(), target.resolve())
            self.assertEqual(link.read_bytes(), LAUNCHER.read_bytes())

if __name__ == "__main__":
    unittest.main(verbosity=2)
