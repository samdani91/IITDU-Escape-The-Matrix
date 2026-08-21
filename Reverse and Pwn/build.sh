#!/bin/sh
set -e
gcc ghost_protocol.c -o ghost_protocol -O0 -s
echo '[+] Built ghost_protocol'
