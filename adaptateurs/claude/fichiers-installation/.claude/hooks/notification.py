#!/usr/bin/env python3

import json
import subprocess
import sys

try:
    data = json.load(sys.stdin)

    notification_type = data.get("notification_type", "")
    message = data.get("message", "Claude Code demande ton attention.")

    if notification_type == "permission_prompt":
        title = "Claude Code — Autorisation"
        sound = "Glass"
    elif notification_type == "idle_prompt":
        title = "Claude Code — Terminé"
        sound = "Pop"
    else:
        sys.exit(0)

    script = (
        'display notification '
        + json.dumps(message, ensure_ascii=False)
        + ' with title '
        + json.dumps(title, ensure_ascii=False)
        + ' sound name '
        + json.dumps(sound, ensure_ascii=False)
    )

    subprocess.run(
        ["osascript", "-e", script],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

except Exception:
    # Une notification ne doit jamais perturber Claude Code.
    pass

sys.exit(0)
