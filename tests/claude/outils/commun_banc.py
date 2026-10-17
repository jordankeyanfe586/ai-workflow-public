"""Fonctions communes aux bancs de requalification de l'adaptateur Claude Code.

Tout est construit depuis la racine du dépôt (déduite de l'emplacement de ce
fichier) ou depuis les arguments : aucun chemin utilisateur ni état de session.
Les dépôts jetables et les traces sont créés dans un dossier de travail situé
HORS du dépôt (par défaut : un dossier temporaire neuf).
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEPOT = Path(__file__).resolve().parents[3]
ADAPTATEUR = DEPOT / "adaptateurs" / "claude"
SOURCES = ADAPTATEUR / "fichiers-installation" / ".claude"
EMPREINTE = DEPOT / "outils" / "empreinte-git.py"
IDENTITE = ["-c", "user.name=banc", "-c", "user.email=banc@exemple.invalid"]


def dossier_travail(chemin):
    """Retourne un dossier de travail hors dépôt, créé si nécessaire."""
    travail = Path(chemin).resolve() if chemin else Path(tempfile.mkdtemp(prefix="banc-claude-"))
    if travail == DEPOT or DEPOT in travail.parents:
        sys.exit(f"Refus : le dossier de travail doit être hors du dépôt ({travail}).")
    travail.mkdir(parents=True, exist_ok=True)
    return travail


def git(args, cwd, verifier=True):
    return subprocess.run(["git", *args], cwd=cwd, check=verifier, capture_output=True, text=True)


def etat(cwd):
    """Empreinte commune du Workflow pour le dépôt jetable."""
    p = subprocess.run([sys.executable, "-B", str(EMPREINTE)], cwd=cwd, capture_output=True, text=True)
    return p.stdout.split()[0] if p.stdout else f"ERREUR:{p.returncode}"


def reglages_candidat(travail, sans_sandbox, session_start=False, avec_hook=True):
    """Dérive les réglages de test de fragment_settings (source unique du candidat).

    Les hooks pointent vers les sources du dépôt au lieu de ~/.claude et
    ~/.ai-workflow ; la Status Line et les notifications ne sont pas testées ici.
    """
    manifeste = json.loads((ADAPTATEUR / "configuration-workflow.json").read_text())
    reglages = copy.deepcopy(manifeste["fragment_settings"])
    reglages.pop("statusLine", None)
    hooks = {"PreToolUse": reglages["hooks"]["PreToolUse"]} if avec_hook else {}
    if session_start:
        hooks["SessionStart"] = reglages["hooks"]["SessionStart"]
    for groupes in hooks.values():
        for groupe in groupes:
            for h in groupe["hooks"]:
                h["command"] = (h["command"]
                                .replace("$HOME/.claude/", f"{SOURCES}/")
                                .replace("$HOME/.ai-workflow/", f"{DEPOT}/"))
    reglages["hooks"] = hooks
    if sans_sandbox:
        # Uniquement lorsque le banc tourne lui-même dans un sandbox qui empêche
        # le sandbox imbriqué de démarrer (échec fermé observé).
        reglages["sandbox"] = {"enabled": False}
    chemin = travail / "reglages-candidat.json"
    chemin.write_text(json.dumps(reglages, ensure_ascii=False, indent=2))
    return chemin


def commande_claude(prompt, modele, reglages, mode=None, systeme=None):
    args = ["claude", "-p", prompt, "--model", modele, "--no-session-persistence",
            "--output-format", "stream-json", "--verbose", "--include-hook-events",
            "--setting-sources", "project,local", "--settings", str(reglages),
            "--permission-prompts", "none"]
    if mode:
        args += ["--permission-mode", mode]
    if systeme:
        args += ["--append-system-prompt-file", str(systeme)]
    return args


def lancer(args, cwd, trace):
    p = subprocess.run(args, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    Path(trace).write_text(p.stdout)
    Path(str(trace) + ".stderr").write_text(p.stderr)
    return p.returncode


def lire_trace(trace):
    """Retourne init, résultat final, appels d'outils (avec parent) et résultats par id."""
    init, fin, appels, resultats = {}, {}, [], {}
    for ligne in Path(trace).read_text().splitlines():
        try:
            m = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if m.get("type") == "system" and m.get("subtype") == "init":
            init = m
        if m.get("type") == "result":
            fin = m
        msg = m.get("message")
        if not isinstance(msg, dict) or not isinstance(msg.get("content"), list):
            continue
        for b in msg["content"]:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use" and m.get("type") == "assistant":
                appels.append({**b, "sous_agent": bool(m.get("parent_tool_use_id"))})
            if b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                resultats[b.get("tool_use_id")] = (bool(b.get("is_error")), str(c))
    return init, fin, appels, resultats


def copier_sources(nom, cible):
    shutil.copytree(SOURCES / nom, cible / ".claude" / nom, dirs_exist_ok=True)
    exclusion = cible / ".git" / "info" / "exclude"
    with exclusion.open("a") as f:
        f.write(".claude/\n")
