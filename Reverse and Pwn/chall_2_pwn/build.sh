#!/bin/sh
set -e
gcc room_404.c -o room_404 -O0 -fno-omit-frame-pointer -fno-stack-protector -no-pie -Wl,-z,relro
echo "[+] Built room_404"
