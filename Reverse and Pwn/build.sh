#!/bin/sh
gcc pwnventure.c -o pwnventure -O0 -fno-stack-protector -fPIE -pie -Wno-deprecated-declarations -Wno-implicit-function-declaration -D_GNU_SOURCE -Wl,--undefined=gets
