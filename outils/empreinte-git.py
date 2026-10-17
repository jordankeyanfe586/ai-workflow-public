#!/usr/bin/env python3
import hashlib
import os
import subprocess
import sys
import threading
from pathlib import Path

GIT = "/usr/bin/git"
CHUNK = 1024 * 1024

args = sys.argv[1:]
if args not in ([], ["--initial"]):
    print("Usage: empreinte-git.py [--initial]", file=sys.stderr)
    raise SystemExit(2)
initial = args == ["--initial"]

if not Path(GIT).is_file() or not os.access(GIT, os.X_OK):
    print(f"Git approuvé introuvable ou non exécutable : {GIT}", file=sys.stderr)
    raise SystemExit(127)


def git_env():
    env = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_PAGER": "cat",
    }
    for name in ("HOME", "TMPDIR", "XDG_CONFIG_HOME"):
        value = os.environ.get(name)
        if value:
            env[name] = value
    return env


ENV = git_env()
BASE = [GIT, "--no-pager", "-c", "core.fsmonitor=false", "-c", "color.ui=false"]


def git(root, *args, check=True):
    p = subprocess.run(
        [*BASE, *args], cwd=root, env=ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if check and p.returncode:
        sys.stderr.buffer.write(p.stderr)
        raise SystemExit(p.returncode)
    return p


probe = git(None, "rev-parse", "--show-toplevel", check=False)
if probe.returncode:
    print("HORS_DEPOT")
    raise SystemExit(2)

root = Path(os.fsdecode(probe.stdout.rstrip(b"\n")))
h = hashlib.sha256()


def add(label, data):
    h.update(label + b"\0")
    h.update(data)
    h.update(b"\0")


def add_git(label, *args):
    h.update(label + b"\0")

    p = subprocess.Popen(
        [*BASE, *args], cwd=root, env=ENV, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    errors = bytearray()

    def drain_stderr():
        while True:
            chunk = p.stderr.read(CHUNK)
            if not chunk:
                break
            errors.extend(chunk)

    stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
    stderr_thread.start()

    while True:
        chunk = p.stdout.read(CHUNK)
        if not chunk:
            break
        h.update(chunk)

    returncode = p.wait()
    stderr_thread.join()

    if returncode:
        sys.stderr.buffer.write(errors)
        raise SystemExit(returncode)

    h.update(b"\0")


def add_file(label, path):
    h.update(label + b"\0")
    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    h.update(b"\0")


head_p = git(root, "rev-parse", "--verify", "HEAD", check=False)
head = head_p.stdout.strip() if not head_p.returncode else b"UNBORN"

branch_p = git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
branch = branch_p.stdout.strip() if not branch_p.returncode else b"DETACHED"

add(b"root", os.fsencode(str(root.resolve())))
add(b"head", head)
add(b"branch", branch)

add_git(b"index", "diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv")
add_git(b"worktree", "diff", "--binary", "--no-ext-diff", "--no-textconv")

untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0")
for raw in sorted(x for x in untracked if x):
    add(b"path", raw)
    path = root / os.fsdecode(raw)
    try:
        if path.is_symlink():
            add(b"link", os.fsencode(os.readlink(path)))
        elif path.is_file():
            add_file(b"file", path)
    except FileNotFoundError:
        add(b"race", b"MISSING")

etat = h.hexdigest()[:20]

if initial:
    status_raw = git(root, "status", "--short", "--untracked-files=all").stdout
    status = os.fsdecode(status_raw).rstrip()
    count = len(status.splitlines()) if status else 0

    print(f"DEPOT={root.name}")
    print(f"RACINE={root}")
    print(f"BRANCHE={os.fsdecode(branch)}")
    print(f"HEAD={os.fsdecode(head)[:12]}")
    print(f"ETAT={etat}")
    print("WORKTREE=PROPRE" if not status else f"WORKTREE=MODIFIE ({count})")
    if status:
        print("PREEXISTANTS:")
        print(status)
else:
    print(f"ETAT={etat}")
    print(f"HEAD={os.fsdecode(head)[:12]}")
    print(f"BRANCHE={os.fsdecode(branch)}")
