#!/usr/bin/env python3
from pathlib import Path
import subprocess

TEMPLATE = Path("activation_template.c")
OUTPUT = Path("IITSecureActivator")

if not TEMPLATE.exists():
    raise SystemExit("activation_template.c not found")

Path("activation.c").write_text(TEMPLATE.read_text())
subprocess.run([
    "gcc", "activation.c", "-o", str(OUTPUT),
    "-O0", "-s"
], check=True)

print(f"Built {OUTPUT}")
