IITCTF — DEAD DROP

Category: Reverse Engineering
Difficulty: Easy

Scenario
--------
An anonymous source left a small utility on an isolated machine.
The program claims to be a harmless file-verification tool.

It isn't.

Recover the drop code and retrieve what was left behind.

File
----
dead_drop

Run
---
    chmod +x dead_drop
    ./dead_drop

Objective
---------
Reverse the validation routine and recover the 12-character drop code.

Hints
-----
- Start with the validation function in Ghidra.
- The input characters are processed in a non-obvious order.
- The comparison uses simple byte transformations.
- The package contents are not stored as plaintext.

Flag
----
IITCTF{d3ad_dr0p_r3v3rs3d}

Organizer
---------
Distribute only `dead_drop`.
Do not distribute the source or build script.
Do not host this challenge with nc.
