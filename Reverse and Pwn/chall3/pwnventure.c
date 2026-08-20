#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Deliberately vulnerable challenge. */
void win(void)
{
    puts("\n==============================================================");
    puts("                 TREASURE UNLOCKED!");
    puts("==============================================================\n");
    puts("The vault recognizes your questionable decisions.\n");
    puts("                         FLAG\n");
    puts("              IITCTF{ch00s3_w1s3ly_pwn3r}\n");
    puts("==============================================================");
    puts("                         Created by AribZobair");
    puts("==============================================================");
    exit(0);
}

void fortune_teller(void)
{
    char name[128];

    puts("\n==============================================================");
    puts("                    THE FORTUNE TELLER");
    puts("==============================================================");
    puts("\"Tell me your name, traveler, and I shall reveal your destiny.\"");
    printf("\nName: ");
    fflush(stdout);

    if (!fgets(name, sizeof(name), stdin))
        exit(1);

    name[strcspn(name, "\n")] = '\0';

    puts("\nThe fortune teller studies you carefully...");
    printf("Your destiny says: ");
    printf(name);                 /* format-string vulnerability */
    puts("");
    puts("\"Interesting. Very interesting.\"");

    puts("");
}

void goblin(void)
{
    int choice;

    puts("\n--------------------------------------------------------------");
    puts("A tiny goblin wearing a suspiciously formal hat approaches.");
    puts("Goblin: \"Are we friends?\"");
    puts("\n[1] Obviously.");
    puts("[2] I don't trust tiny formal goblins.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 1) {
        puts("\nThe goblin beams.");
        puts("\"Excellent! Have two coins.\"");
    } else {
        puts("\nThe goblin looks offended.");
        puts("\"Understandable. Have a terrible day.\"");
    }
}

void dragon(void)
{
    int choice;

    puts("\n--------------------------------------------------------------");
    puts("A dragon blocks your path.");
    puts("\n[1] Fight the dragon.");
    puts("[2] Compliment its scales.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 2) {
        puts("\nThe dragon is deeply moved.");
        puts("\"Nobody notices my scales anymore.\"");
        puts("It gives you a coin and moves aside.");
    } else {
        puts("\nYou challenge the dragon.");
        puts("The dragon challenges your life insurance.");
        puts("You wisely retreat.");
    }
}

void treasure_room(void)
{
    char response[64];

    puts("\n==============================================================");
    puts("                    THE TREASURE ROOM");
    puts("==============================================================");
    puts("You find an ancient terminal.");
    puts("\nThe terminal displays:");
    puts("  \"SPEAK THE ANCIENT PASSWORD.\"");
    printf("\n> ");
    fflush(stdout);

    gets(response);                /* stack buffer overflow */

    puts("\nThe terminal processes your answer...");
    puts("Nothing happens.");
    puts("The treasure remains locked.");
}

void castle(void)
{
    int choice;

    puts("\n==============================================================");
    puts("                      OLD CASTLE");
    puts("==============================================================");
    puts("\nA guard asks whether you are brave enough to enter.");
    puts("\n[1] Enter the castle.");
    puts("[2] Ask the fortune teller for advice.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 2)
        fortune_teller();

    /*
     * Either route reaches the treasure room, so choices are not
     * an arbitrary gate to the actual pwn portion.
     */
    treasure_room();
}

void start_adventure(void)
{
    int choice;

    puts("\n==============================================================");
    puts("              CHOOSE YOUR OWN PWNVENTURE");
    puts("==============================================================");
    puts("\nYou wake up in a strange place.");
    puts("A wooden sign reads:");
    puts("\n    \"Your choices have consequences.\"");
    puts("\nYou see two paths.");
    puts("\n[1] The Friendly Path");
    puts("[2] The Suspicious Path");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 1)
        goblin();
    else if (choice == 2)
        dragon();
    else
        puts("\nYou choose neither path. Bold strategy.");

    castle();
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("==============================================================");
    puts("               CHOOSE YOUR OWN PWNVENTURE");
    puts("==============================================================");
    puts("\nA completely normal adventure awaits.");
    puts("\n[1] Start adventure");
    puts("[2] Exit");
    printf("> ");

    int choice;
    scanf("%d", &choice);
    getchar();

    if (choice == 1)
        start_adventure();
    else
        puts("\nYou leave. Probably for the best.");

    return 0;
}
