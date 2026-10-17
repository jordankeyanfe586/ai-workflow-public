#!/usr/bin/env python3

import json
import subprocess
import sys

event = ""

try:
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event != "Stop":
        sys.exit(0)

    script = (
        'display notification '
        + json.dumps(
            "Codex a terminé et attend ton attention.",
            ensure_ascii=False,
        )
        + ' with title '
        + json.dumps(
            "Codex — Terminé",
            ensure_ascii=False,
        )
        + ' sound name '
        + json.dumps(
            "Pop",
            ensure_ascii=False,
        )
    )

    subprocess.run(
        ["osascript", "-e", script],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

except Exception:
    # Une notification ne doit jamais perturber Codex.
    pass

finally:
    # Stop exige une sortie JSON valide lorsqu'un Hook termine avec succès.
    if event == "Stop":
        print("{}")

sys.exit(0)
