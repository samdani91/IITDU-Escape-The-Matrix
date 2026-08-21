#include <stdio.h>
#include <string.h>
#include <stddef.h>

#define N 12

static const unsigned char key[N] = {
    0x13,0x27,0x41,0x19,0x5A,0x2C,0x71,0x33,0x0F,0x64,0x28,0x52
};

static const unsigned char expected[N] = {
    0x6A,0x70,0x80,0x6D,0x15,0x74,0x69,0x93,0x5A,0x79,0x3D,0x5E
};

static const int order[N] = {
    7,2,10,0,8,5,11,3,9,1,6,4
};

/*
 * The flag is intentionally not stored as plaintext.
 * It is decoded only after the drop code is validated.
 */
static const unsigned char sealed_fragment[] = {
    0x13,0x13,0x0E,0x19,0x0E,0x1C,0x21,0x3E,0x69,0x3B,0x3E,0x05,0x3E,0x28,0x6A,0x2A,0x05,0x28,0x69,0x2C,0x69,0x28,0x29,0x69,0x3E,0x27
};

static void open_package(void) {
    char recovered[sizeof(sealed_fragment) + 1];

    for (size_t i = 0; i < sizeof(sealed_fragment); i++)
        recovered[i] = (char)(sealed_fragment[i] ^ 0x5A);

    recovered[sizeof(sealed_fragment)] = '\0';

    puts("\n==============================================================");
    puts("                 SECURE PACKAGE OPENED");
    puts("==============================================================");
    printf("\n             %s\n", recovered);
    puts("\n==============================================================");
    puts("                     Created by AribZobair");
    puts("==============================================================");
}

static int verify(const char *input) {
    if (strlen(input) != N)
        return 0;

    for (int i = 0; i < N; i++) {
        unsigned char x = (unsigned char)input[order[i]];
        x ^= key[i];
        x = (unsigned char)(x + (i * 3 + 7));

        if (x != expected[i])
            return 0;
    }

    return 1;
}

int main(void) {
    char input[128];

    puts("==============================================================");
    puts("                  IIT // DEAD DROP TERMINAL");
    puts("==============================================================");
    puts("\nSECURE PACKAGE DETECTED");
    puts("Package ID: DD-042");
    puts("Status: LOCKED\n");
    puts("Enter drop code:");
    printf("> ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin))
        return 1;

    input[strcspn(input, "\n")] = '\0';

    if (verify(input))
        open_package();
    else
        puts("\n[!] Invalid drop code.\n    Package remains sealed.");

    return 0;
}
