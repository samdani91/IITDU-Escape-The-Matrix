IITCTF — Challenge 1
======================

Challenge Title
---------------
All or Nothing

Category
--------
Reverse Engineering

Difficulty
----------
Easy

Description
-----------
The dealer has dealt you two cards, but something feels unusual.

Can you figure out what the program is checking and hit the
magic blackjack total?

Files
-----
blackjack

How to Run
----------
Make the binary executable if necessary:

    chmod +x blackjack

Run it with:

    ./blackjack

Objective
---------
Reverse engineer the binary and determine the two card values
that satisfy the program's hidden conditions.

Once you determine the correct values, enter them into the program
to retrieve the flag.

Hints
-----
- Look at the main function in a reverse-engineering tool such as Ghidra.
- Pay attention to the mathematical conditions involving the cards.
- Valid card values are in the range 1–13.
- The program is checking for a blackjack-related total.

Tools
-----
Recommended:
- Ghidra
- strings
- objdump (optional)

Flag
-----------
IITCTF{h1tM3_w1th_Th3Fl4g}

Author - AribZobair

Organizer Notes
---------------
This is a local binary reverse-engineering challenge.

Do NOT host this challenge using nc.

Distribute only the `blackjack` binary to players.

