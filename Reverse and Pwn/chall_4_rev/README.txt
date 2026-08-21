IITCTF — GHOST PROTOCOL

Category: Reverse Engineering
Difficulty: Medium-Hard

The machine was recovered from a sealed laboratory after an
unexplained system failure.

Most research data was destroyed.

One executable survived.

It identifies itself only as GHOST.

Find the protocol the researchers tried to erase.

File:
    ghost_protocol

Run:
    chmod +x ghost_protocol
    ./ghost_protocol

Objective:
Reverse the command/state logic, discover the hidden protocol
sequence, reach the recovered memory fragment, and recover the flag.

Hints:
- The documented commands are not the whole story.
- Look at command dispatch.
- There are legacy commands.
- Track the 16-bit state variable.
- A magic state is checked.
- The final flag is encoded, not stored as plaintext.

Flag:
    IITCTF{gh05t_pr0t0c0l_unf0ld3d}

Organizer:
Distribute only `ghost_protocol`.
Do not distribute the source or writeup.
No nc is required.
