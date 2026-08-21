#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAX_GUESTS 8

typedef struct Guest Guest;
typedef void (*checkout_cb)(Guest *);

struct Guest {
    char name[32];
    unsigned long room;
    checkout_cb checkout;
};

static Guest *guests[MAX_GUESTS];
static Guest *last_packet;

static void normal_checkout(Guest *g) {
    printf("\n[+] Guest '%s' has checked out of Room %lu.\n", g->name, g->room);
}

static void room_404(Guest *g) {
    (void)g;

    static const unsigned char sealed_fragment[] = {
        0x13,0x13,0x0E,0x19,0x0E,0x1C,0x21,0x32,0x6B,0x36,0x38,0x69,0x28,0x2E,0x05,0x3C,0x6A,0x2F,0x34,0x3E,0x05,0x28,0x6A,0x6A,0x37,0x05,0x6E,0x6A,0x6E,0x27
    };

    char recovered[sizeof(sealed_fragment) + 1];

    for (size_t i = 0; i < sizeof(sealed_fragment); i++)
        recovered[i] = (char)(sealed_fragment[i] ^ 0x5A);

    recovered[sizeof(sealed_fragment)] = '\0';

    puts("\n==============================================================");
    puts("                    ROOM 404 FOUND");
    puts("==============================================================");
    puts("\nReceptionist:");
    puts("\"I told you that room did not exist.\"");
    puts("\nThe hotel shifts around you.");
    printf("\nFLAG: %s\n", recovered);
    puts("\n==============================================================");
    exit(0);
}

static void banner(void) {
    puts("==============================================================");
    puts("                    THE INFINITE HOTEL");
    puts("==============================================================");
    puts("\n                 ALL ROOMS ARE OCCUPIED");
    puts("\nRoom 1       OCCUPIED");
    puts("Room 2       OCCUPIED");
    puts("Room 3       OCCUPIED");
    puts("...");
    puts("Room 403     OCCUPIED");
    puts("Room 404     ----------------");
    puts("Room 405     OCCUPIED");
    puts("\nReceptionist:");
    puts("\"There is no Room 404.\"");
}

static int read_num(const char *prompt, unsigned long *out) {
    char buf[64], *end;

    printf("%s", prompt);
    if (!fgets(buf, sizeof(buf), stdin))
        return 0;

    *out = strtoul(buf, &end, 0);
    return end != buf;
}

static int choose_slot(void) {
    unsigned long x;

    if (!read_num("Guest slot (0-7): ", &x))
        return -1;

    if (x >= MAX_GUESTS) {
        puts("[!] Invalid guest slot.");
        return -1;
    }

    return (int)x;
}

static void check_in(void) {
    int slot = choose_slot();
    if (slot < 0)
        return;

    if (guests[slot]) {
        puts("[!] That slot is occupied.");
        return;
    }

    Guest *g = malloc(sizeof(Guest));
    if (!g)
        exit(1);

    printf("Guest name: ");
    if (!fgets(g->name, sizeof(g->name), stdin)) {
        free(g);
        return;
    }

    g->name[strcspn(g->name, "\n")] = '\0';

    unsigned long room;

    if (!read_num("Room number: ", &room)) {
        free(g);
        return;
    }

    g->room = room;
    g->checkout = normal_checkout;
    guests[slot] = g;

    printf("[+] Welcome, %s. Room %lu is yours.\n", g->name, g->room);
}

static void view_guest(void) {
    int slot = choose_slot();

    if (slot < 0)
        return;

    if (!guests[slot]) {
        puts("[!] No guest in that slot.");
        return;
    }

    Guest *g = guests[slot];

    printf("\nGuest: %s\n", g->name);
    printf("Room : %lu\n", g->room);
    puts("Status: OCCUPIED");
}

static void check_out(void) {
    int slot = choose_slot();

    if (slot < 0)
        return;

    if (!guests[slot]) {
        puts("[!] No guest in that slot.");
        return;
    }

    /*
     * INTENTIONAL BUG:
     * The heap object is freed but the pointer in guests[slot] is not
     * cleared. This creates the dangling pointer used by the challenge.
     */
    free(guests[slot]);

    puts("[+] Guest checked out.");
    puts("[!] Reservation pointer retained for archival purposes.");
}

static void reservation_packet(void) {
    int slot = choose_slot();

    if (slot < 0)
        return;

    /*
     * Same-size allocation. After checkout(), malloc() can reuse the
     * recently freed Guest chunk.
     */
    Guest *packet = malloc(sizeof(Guest));

    if (!packet)
        exit(1);

    puts("\nReservation packet format:");
    puts("  32 bytes: guest label");
    puts("   8 bytes: room number");
    puts("   8 bytes: checkout handler");

    printf("Packet bytes (hex, up to 48 bytes): ");

    char line[256];

    if (!fgets(line, sizeof(line), stdin)) {
        free(packet);
        return;
    }

    unsigned int values[sizeof(Guest)];
    size_t count = 0;
    char *p = line;

    while (*p && count < sizeof(Guest)) {
        while (*p == ' ' || *p == '\t' || *p == '\n')
            p++;

        if (!*p)
            break;

        char *end;
        unsigned long v = strtoul(p, &end, 16);

        if (end == p)
            break;

        values[count++] = (unsigned int)(v & 0xff);
        p = end;
    }

    memset(packet, 0, sizeof(Guest));

    for (size_t i = 0; i < count; i++)
        ((unsigned char *)packet)[i] = (unsigned char)values[i];

    puts("[+] Reservation packet stored.");
    puts("[+] The hotel has made room for one more.");

    /*
     * Keep the reclaimed chunk allocated so the stale pointer in
     * guests[slot] continues to reference it.
     */
    last_packet = packet;
}

static void trigger(void) {
    int slot = choose_slot();

    if (slot < 0)
        return;

    if (!guests[slot]) {
        puts("[!] No guest record.");
        return;
    }

    puts("[*] Calling checkout handler...");
    guests[slot]->checkout(guests[slot]);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    banner();

    for (;;) {
        puts("\n--------------------------------------------------------------");
        puts("1. Check in guest");
        puts("2. View room");
        puts("3. Check out guest");
        puts("4. Submit reservation packet");
        puts("5. Trigger checkout handler");
        puts("6. Leave hotel");
        puts("--------------------------------------------------------------");

        unsigned long choice;

        if (!read_num("\nChoice: ", &choice))
            break;

        switch (choice) {
            case 1:
                check_in();
                break;
            case 2:
                view_guest();
                break;
            case 3:
                check_out();
                break;
            case 4:
                reservation_packet();
                break;
            case 5:
                trigger();
                break;
            case 6:
                puts("\n[+] Goodbye.");
                return 0;
            default:
                puts("[!] Unknown choice.");
                break;
        }
    }

    return 0;
}
