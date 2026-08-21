#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Deliberately vulnerable challenge. */
void override_core(void)
{
    puts("\n==============================================================");
    puts("                    AI CORE OVERRIDDEN");
    puts("==============================================================\n");
    puts("Containment protocol disabled.");
    puts("The AI has accepted your override.\n");
    puts("                         FLAG");
    puts("              IITCTF{ch00s3_w1s3ly_pwn3r}");
    puts("==============================================================");
    puts("                         Created by AribZobair");
    puts("==============================================================");
    exit(0);
}

void diagnostics_console(void)
{
    char name[128];

    puts("\n==============================================================");
    puts("                    DIAGNOSTICS CONSOLE");
    puts("==============================================================");
    puts("\"Identify yourself before diagnostics can begin.\"");
    printf("\nIdentifier: ");
    fflush(stdout);

    if (!fgets(name, sizeof(name), stdin))
        exit(1);

    name[strcspn(name, "\n")] = '\0';

    puts("\nAI CORE is analyzing your identifier...");
    printf("Diagnostic result: ");
    printf(name);                 /* format-string vulnerability */
    puts("");
    puts("\"Anomalous input detected.\"");

    puts("");
}

void maintenance_subsystem(void)
{
    int choice;

    puts("\n--------------------------------------------------------------");
    puts("The maintenance subsystem responds.");
    puts("AI: \"Would you like to repair the containment system?\"");
    puts("\n[1] Begin maintenance.");
    puts("[2] Abort maintenance.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 1) {
        puts("\nMaintenance channel opened.");
        puts("AI: \"Interesting. You are attempting a repair.\"");
    } else {
        puts("\nMaintenance channel closed.");
        puts("AI: \"A sensible decision... perhaps.\"");
    }
}

void network_subsystem(void)
{
    int choice;

    puts("\n--------------------------------------------------------------");
    puts("A restricted network subsystem appears.");
    puts("\n[1] Inspect network status.");
    puts("[2] Request emergency uplink.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 2) {
        puts("\nEmergency uplink denied.");
        puts("AI: \"That interface is not available to you.\"");
    } else {
        puts("\nNetwork status: NOMINAL.");
        puts("No useful information was found.");
    }
}

void memory_console(void)
{
    char response[64];

    puts("\n==============================================================");
    puts("                    MEMORY CONSOLE");
    puts("==============================================================");
    puts("You have reached a restricted AI memory interface.");
    puts("\nThe terminal displays:");
    puts("  \"ENTER DIAGNOSTIC OVERRIDE STRING.\"");
    printf("\n> ");
    fflush(stdout);

    gets(response);                /* stack buffer overflow */

    puts("\nAI CORE processes your request...");
    puts("Access remains restricted.");
    puts("The override was rejected.");
}

void control_center(void)
{
    int choice;

    puts("\n==============================================================");
    puts("                    CONTROL CENTER");
    puts("==============================================================");
    puts("\nThe AI presents two available control interfaces.");
    puts("\n[1] Continue to maintenance interface.");
    puts("[2] Open diagnostics interface.");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 2)
        diagnostics_console();

    /*
     * Either route eventually reaches the vulnerable memory console.
     * The choices provide narrative navigation, not an arbitrary
     * gate to the actual pwn portion.
     */
    memory_console();
}

void ai_interface(void)
{
    int choice;

    puts("\n==============================================================");
    puts("                    AI CORE // OVERRIDE");
    puts("==============================================================");
    puts("\nThe containment system is unstable.");
    puts("The AI has locked itself inside its control environment.");
    puts("\nAvailable interfaces:");
    puts("\n[1] Maintenance");
    puts("[2] Network");
    printf("> ");
    scanf("%d", &choice);
    getchar();

    if (choice == 1)
        maintenance_subsystem();
    else if (choice == 2)
        network_subsystem();
    else
        puts("\nThe AI ignores the invalid interface request.");

    control_center();
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("==============================================================");
    puts("                    IIT AI CORE // OVERRIDE");
    puts("==============================================================");
    puts("\nAn experimental AI has entered containment mode.");
    puts("The emergency control terminal is still responding.");
    puts("\n[1] Access AI core");
    puts("[2] Disconnect");
    printf("> ");

    int choice;
    scanf("%d", &choice);
    getchar();

    if (choice == 1)
        ai_interface();
    else
        puts("\nConnection terminated.");

    return 0;
}
