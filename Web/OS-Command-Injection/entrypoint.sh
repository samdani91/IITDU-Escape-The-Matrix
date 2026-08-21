#!/bin/sh
set -eu
FLAG_DIR="/flagdata"
FLAG_FILE="$FLAG_DIR/flag.txt"
mkdir -p "$FLAG_DIR"
if [ ! -f "$FLAG_FILE" ]; then
    RANDOM_FLAG="$(python - <<'PY'
import secrets
print(secrets.token_hex(12))
PY
)"
    printf 'IITCTF{%s}\n' "$RANDOM_FLAG" > "$FLAG_FILE"
    chmod 0400 "$FLAG_FILE"
    chown ctfuser:ctfuser "$FLAG_FILE"
    echo "[IITCTF] New challenge flag generated."
else
    echo "[IITCTF] Existing challenge flag loaded."
fi
exec "$@"
