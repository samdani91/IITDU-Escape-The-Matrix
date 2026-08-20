IITCTF - CHOOSE YOUR OWN PWNVENTURE

Category: Pwn
Difficulty: Hard
Flag: IITCTF{ch00s3_w1s3ly_pwn3r}

Files:
    pwnventure.c
    pwnventure
    pwnventure_writeup.txt

Intended vulnerabilities:
    printf(name)   -> format-string information leak
    gets(response) -> stack buffer overflow

Intended exploit:
    format-string leak -> PIE base -> stack overflow -> ret2win

Build:
    gcc pwnventure.c -o pwnventure -O0 -fno-stack-protector -fPIE -pie

Distribute only the compiled challenge binary.

Author:
    Created by AribZobair
