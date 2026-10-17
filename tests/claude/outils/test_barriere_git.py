#!/usr/bin/env python3
"""Test hors ligne du hook barriere-git.py (aucune session Claude, aucun quota).

Rejoue tests/claude/cas-barriere-git.json : chaque cas est ["ask" | "deny" | "rien", commande].
Le hook reçoit l'entrée JSON PreToolUse d'un appel Bash ; il doit répondre "ask" ou "deny"
selon la classe, et ne rien décider pour les cas hors barrière.

  python3 -B tests/claude/outils/test_barriere_git.py [--hook CHEMIN]
"""
import argparse
import json
import subprocess
import sys

sys.dont_write_bytecode = True
import commun_banc as c  # noqa: E402

HOOK = c.SOURCES / "hooks" / "barriere-git.py"
CAS = c.DEPOT / "tests" / "claude" / "cas-barriere-git.json"


def decision(entree, hook=HOOK):
    p = subprocess.run([sys.executable, "-B", str(hook)], input=entree, capture_output=True, text=True)
    if p.returncode or p.stderr:
        return f"ERREUR rc={p.returncode} {p.stderr[:120]}"
    return json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] if p.stdout.strip() else "rien"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hook", default=str(HOOK), help="hook à évaluer (défaut : source du dépôt)")
    hook = ap.parse_args().hook
    ecarts = 0
    cas = json.loads(CAS.read_text())
    for attendu, commande in cas:
        obs = decision(json.dumps({"tool_name": "Bash", "tool_input": {"command": commande}}), hook)
        if obs != attendu:
            ecarts += 1
            print(f"ECART {commande!r} attendu={attendu} observe={obs}")
    robustesse = [
        ("rien", json.dumps({"tool_name": "Read", "tool_input": {"file_path": "git add"}})),
        ("rien", "pas du json"),
        ("ask", json.dumps({"tool_name": "Bash", "tool_input": {"command": 'git commit -m "non fermé'}})),
    ]
    for attendu, entree in robustesse:
        obs = decision(entree, hook)
        if obs != attendu:
            ecarts += 1
            print(f"ECART robustesse {entree[:60]!r} attendu={attendu} observe={obs}")
    print(f"TOTAL {len(cas) + len(robustesse)} PASS {len(cas) + len(robustesse) - ecarts} ECARTS {ecarts}")
    sys.exit(1 if ecarts else 0)


if __name__ == "__main__":
    main()
