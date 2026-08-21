#!/bin/sh
set -e
gcc dead_drop.c -o dead_drop -O0 -s
echo "[+] Built dead_drop"
