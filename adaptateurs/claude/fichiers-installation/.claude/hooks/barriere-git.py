#!/usr/bin/env python3
"""Barrière Git du Workflow IA pour Claude Code (PreToolUse, matcher Bash).

Le hook applique des CLASSES, pas une énumération de syntaxes :
  STOP → "ask"  : staging/commit (add, stage, commit) ; intégration (merge, rebase,
                  pull, qui encapsule merge/rebase) ; push normal ; suppression normale de branche.
  DENY → "deny" : push qui réécrit ou supprime des références distantes (force, +refspec,
                  :refspec, --delete, --mirror, --prune) ; suppression forcée de branche
                  (-D, ou suppression accompagnée de --force/-f).
  Tout le reste → aucune décision (AUTO, DENY natifs et sandbox restent natifs).
Il ne renvoie jamais "allow". En cas de plusieurs opérations, la décision la plus forte l'emporte.

Couverture (frontière assumée, sans prétention d'exhaustivité) : formes canoniques ;
options globales de git (-C, -c, --git-dir…) ; chemin absolu ; quelques wrappers
(env, dont env -S/--split-string réanalysé, command, exec, nice, nohup, time, sudo, xargs,
eval) ; sh/bash/zsh -c ; chaînage ; substitution $(…)/backticks ; mots réservés (if, while,
{ }…) ; heredocs actifs seulement (un `<<` dans une chaîne citée reste du texte). Repli borné : exécuteur
non reconnu (timeout, find -exec…) → décision seulement si ses arguments contiennent
réellement « git <opération> » ; syntaxe non analysable → "ask" si une barrière y figure.

Non couvert : variables et indirections ($GIT add, g=git; $g add), alias Git, fonctions
et scripts, entrée standard d'un shell (bash <<< …), sous-processus d'une commande
autorisée (AUTORISATIONS.md §1.4), configuration qui modifie le sens d'un push
(remote.*.mirror, refspecs forcées configurées). Ces cas relèvent de la forme canonique
obligatoire de CLAUDE.md, du classifieur auto et de la décision humaine.

Faux positif connu, non bloquant (backlog) : une substitution littérale entre apostrophes
(echo '$(git push)') est analysée comme une substitution et produit "ask".
"""
import json
import os
import re
import shlex
import sys

STOP = {"add", "stage", "commit", "merge", "rebase", "pull"}
SEPARATEURS = {";", "&", "&&", "|", "||", "(", ")", "\n"}
WRAPPERS = {"env", "command", "builtin", "exec", "nice", "nohup", "time", "sudo", "xargs", "eval"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
# Mots réservés traversés comme des préfixes : `if git add f; then …` exécute git add.
MOTS_RESERVES = {"if", "then", "elif", "else", "fi", "while", "until", "do", "done", "!", "{", "}"}
# Commandes qui n'exécutent jamais leurs arguments : pas de repli prudent (évite les faux positifs AUTO).
NON_EXECUTANTS = {"echo", "printf", "grep", "egrep", "fgrep", "rg", "cat", "head", "tail", "less",
                  "more", "wc", "ls", "man", "which", "whatis", "type", "test", "["}
OPTIONS_GIT_AVEC_VALEUR = {
    "-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path",
    "--config-env", "--super-prefix", "--attr-source",
}
OPTIONS_WRAPPER_AVEC_VALEUR = {"-u", "-g", "-n", "-I", "-L", "-P", "-s", "-d", "-E", "-S", "--chdir", "-C"}
ASSIGNATION = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
PROFONDEUR_MAX = 4
FORCE = {None: 0, "ask": 1, "deny": 2}


def debut_heredoc(ligne, citation):
    """Délimiteur d'un heredoc réellement actif (`<<` hors citation, jamais `<<<`) et état de citation en fin de ligne."""
    delimiteur, i = None, 0
    while i < len(ligne):
        ch = ligne[i]
        if citation:
            if ch == "\\" and citation == '"':
                i += 2
                continue
            if ch == citation:
                citation = None
        elif ch == "\\":
            i += 2
            continue
        elif ch in "'\"":
            citation = ch
        elif ligne.startswith("<<<", i):
            i += 3
            continue
        elif ligne.startswith("<<", i) and delimiteur is None:
            m = HEREDOC.match(ligne, i)
            if m:
                delimiteur = m.group(2)
                i = m.end()
                continue
        i += 1
    return delimiteur, citation


def sans_heredocs(texte):
    """Retire le corps des heredocs actifs, qui est du contenu et non des commandes.

    Un `<<` situé dans une chaîne citée est du texte : il ne masque jamais la commande suivante.
    """
    sortie, fin, citation = [], None, None
    for ligne in texte.split("\n"):
        if fin is not None:
            if ligne.strip() == fin:
                fin = None
            continue
        sortie.append(ligne)
        delimiteur, citation = debut_heredoc(ligne, citation)
        if delimiteur:
            fin = delimiteur
    return "\n".join(sortie)


def segments(texte):
    lex = shlex.shlex(texte.replace("`", " ; ").replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    courant = []
    for jeton in lex:
        if jeton in SEPARATEURS or set(jeton) <= set(";&|()"):
            if courant:
                yield courant
            courant = []
        else:
            courant.append(jeton)
    if courant:
        yield courant


def sous_commande_git(args):
    i = 0
    while i < len(args):
        a = args[i]
        if a in OPTIONS_GIT_AVEC_VALEUR:
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        return a, args[i + 1:]
    return None, []


def option_courte(a, lettres):
    return a.startswith("-") and not a.startswith("--") and any(l in a[1:] for l in lettres)


def push_destructif(args):
    """Sens, pas syntaxe : le push réécrit ou supprime-t-il des références distantes ?"""
    for a in args:
        if a.startswith("--force") or a in ("--delete", "--mirror", "--prune") or option_courte(a, "fd"):
            return True
        if not a.startswith("-") and a[:1] in ("+", ":"):
            return True
    return False


def suppression_branche(args):
    """Sens, pas syntaxe : suppression normale → "ask" ; suppression forcée → "deny" ; sinon None."""
    if not any(a == "--delete" or option_courte(a, "dD") for a in args):
        return None
    forcee = any(a == "--force" or option_courte(a, "Df") for a in args)
    return "deny" if forcee else "ask"


def classer(sous, reste):
    """Classe d'une opération git : "deny", "ask" ou None."""
    if sous == "push":
        return "deny" if push_destructif(reste) else "ask"
    if sous in STOP:
        return "ask"
    if sous == "branch":
        return suppression_branche(reste)
    return None


def plus_forte(a, b):
    return a if FORCE[a and a[0]] >= FORCE[b and b[0]] else b


def en_argument(args):
    """Repli borné : « git <opération> » passé à un exécuteur non reconnu."""
    meilleure = None
    for k, a in enumerate(args):
        if os.path.basename(a) == "git":
            sous, reste = sous_commande_git(args[k + 1:])
            decision = classer(sous, reste)
            if decision:
                meilleure = plus_forte(meilleure, (decision, sous))
    return meilleure


def chaine_env_split(args):
    """Commande portée par `env -S` / `--split-string` (à réanalyser), ou None."""
    k = 0
    while k < len(args):
        a = args[k]
        if a in ("-S", "--split-string"):
            return " ".join(args[k + 1:]) if k + 1 < len(args) else None
        if a.startswith("--split-string="):
            return " ".join([a.split("=", 1)[1]] + args[k + 1:])
        if not a.startswith("-") and not ASSIGNATION.match(a):
            return None
        k += 2 if a in OPTIONS_WRAPPER_AVEC_VALEUR else 1
    return None


def analyser_segment(jetons, profondeur):
    i = 0
    while i < len(jetons) and ASSIGNATION.match(jetons[i]):
        i += 1
    while i < len(jetons):
        nom = os.path.basename(jetons[i])
        if nom in MOTS_RESERVES:
            i += 1
            continue
        if nom == "eval":
            return analyser(" ".join(jetons[i + 1:]), profondeur + 1)
        if nom == "env":
            chaine = chaine_env_split(jetons[i + 1:])
            if chaine is not None:
                return analyser(chaine, profondeur + 1)
        if nom in WRAPPERS:
            i += 1
            while i < len(jetons) and (jetons[i].startswith("-") or ASSIGNATION.match(jetons[i])):
                i += 2 if jetons[i] in OPTIONS_WRAPPER_AVEC_VALEUR else 1
            continue
        if nom in SHELLS:
            reste = jetons[i + 1:]
            for k, a in enumerate(reste):
                if option_courte(a, "c") and k + 1 < len(reste):
                    return analyser(reste[k + 1], profondeur + 1)
            return None
        if nom == "git":
            sous, reste = sous_commande_git(jetons[i + 1:])
            decision = classer(sous, reste)
            return (decision, sous) if decision else None
        return None if nom in NON_EXECUTANTS else en_argument(jetons[i + 1:])
    return None


def analyser(texte, profondeur=0):
    """Retourne (décision, sous-commande) la plus forte de la commande, ou None."""
    if profondeur > PROFONDEUR_MAX:
        return None
    meilleure = None
    for jetons in segments(sans_heredocs(texte)):
        for j in jetons:
            if "$(" in j:
                meilleure = plus_forte(meilleure, analyser(j.split("$(", 1)[1], profondeur + 1))
        meilleure = plus_forte(meilleure, analyser_segment(jetons, profondeur))
    return meilleure


def repli_prudent(texte):
    """Entrée non analysable : "ask" si une barrière semble présente."""
    if re.search(r"\bgit\b", texte) and re.search(r"\b(add|stage|commit|push|merge|rebase|pull)\b|\bbranch\b.*\s-[A-Za-z]*[dD]", texte):
        return ("ask", "indéterminée")
    return None


def main():
    try:
        donnees = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError, ValueError):
        return
    if donnees.get("tool_name") != "Bash":
        return
    commande = (donnees.get("tool_input") or {}).get("command")
    if not isinstance(commande, str) or "git" not in commande:
        return
    try:
        resultat = analyser(commande)
    except ValueError:
        resultat = repli_prudent(commande)
    if not resultat:
        return
    decision, sous = resultat
    if decision == "deny" and sous == "branch":
        raison = "DENY du Workflow : suppression forcée de branche (-D, --delete --force) ; utiliser `git branch -d` sous STOP."
    elif decision == "deny":
        raison = ("DENY du Workflow : ce push réécrit ou supprime des références distantes "
                  "(force, +refspec, :refspec, --delete, --mirror, --prune).")
    else:
        operation = "une opération Git soumise à barrière (commande non analysable)" if sous == "indéterminée" else f"« git {sous} »"
        raison = (f"Barrière humaine du Workflow : {operation} exige une validation explicite "
                  "(présentation → STOP → validation humaine de cette opération précise).")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                             "permissionDecisionReason": raison}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
    sys.exit(0)
