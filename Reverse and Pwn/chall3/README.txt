IITCTF - OVERRIDE

Category: Pwn
Difficulty: Hard
Flag: IITCTF{ch00s3_w1s3ly_pwn3r}

SCENARIO
--------
An experimental AI has entered containment mode.

The emergency control terminal is still responding, but the AI's
interfaces are restricted. Navigate the available interfaces,
reach the protected memory console, and find a way to override
the AI core.

Files:
    pwnventure.c
    pwnventure
    build.sh
    pwnventure_writeup.txt

PLAYER DISTRIBUTION
-------------------
Distribute only:

    pwnventure

The source, build script, and writeup are organizer files.

REMOTE DEPLOYMENT
-----------------
This challenge is intended to run as a remote TCP service.

Players should receive:

    nc <HOST> <PORT>

Run the binary in an isolated container/sandbox.

INTENDED VULNERABILITIES
------------------------
The underlying challenge mechanics are unchanged:

    printf(name)
        -> format-string information leak

    gets(response)
        -> stack-based buffer overflow

INTENDED EXPLOIT
----------------
Format-string leak
    -> PIE base recovery
    -> stack overflow
    -> ret2win / control-flow redirection
    -> override_core()
    -> flag

BUILD
-----
    chmod +x build.sh
    ./build.sh

The intended Linux x86-64 build uses PIE, no stack canary, and NX.
