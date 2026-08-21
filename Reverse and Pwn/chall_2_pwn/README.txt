IITCTF — ROOM 404

Category: Pwn
Difficulty: Medium-Hard

THE INFINITE HOTEL
------------------
Every room is occupied.

Room 1 has a guest.
Room 2 has a guest.
Room 3 has a guest.
...
Room 403 is occupied.
Room 405 is occupied.

But the receptionist insists:

    "There is no Room 404."

Make the hotel find the room that supposedly does not exist.

FILE
----
room_404

RUN
---
    chmod +x room_404
    ./room_404

OBJECTIVE
---------
Exploit the hotel's reservation system and reach the hidden Room 404
handler to recover the flag.

INTENDED CONCEPT
----------------
Use-after-free / stale heap pointer with a same-size heap allocation,
followed by overwriting a function pointer.

High-level path:

    Check in guest
          |
          v
    Check out guest
          |
          v
    Dangling guests[slot] pointer
          |
          v
    Submit reservation packet
          |
          v
    Same-size heap chunk is reused
          |
          v
    Overwrite checkout callback
          |
          v
    Trigger checkout
          |
          v
    room_404()
          |
          v
    FLAG

PLAYER HINTS
------------
Hint 1:
    "The hotel keeps an old reservation after checkout."

Hint 2:
    "Look at what happens to a Guest object after free()."

Hint 3:
    "The checkout handler is stored inside the Guest object."

DEPLOYMENT
----------
This is a local downloadable Pwn challenge.

Distribute only:
    room_404

Do not distribute:
    room_404.c
    build.sh
    writeup.txt

No nc is required.

FLAG
----
IITCTF{h1lb3rt_f0und_r00m_404}
