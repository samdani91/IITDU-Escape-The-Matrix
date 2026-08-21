#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>

#define KEY_LEN 15
#define FLAG_LEN 27
#define SCREEN_WIDTH 62

static const unsigned char A[KEY_LEN] = {
    0x42, 0x17, 0xA9, 0x3C, 0x71,
    0x28, 0xD4, 0x56, 0x8B, 0x19,
    0xE2, 0x64, 0x35, 0xC1, 0x7A
};

static const unsigned char B[KEY_LEN] = {
    0x19, 0x27, 0x31, 0x0D, 0x22,
    0x16, 0x2B, 0x3C, 0x11, 0x2E,
    0x09, 0x35, 0x1C, 0x2A, 0x17
};

static const unsigned char encoded_flag[FLAG_LEN] = {
    0x13, 0x22, 0x28, 0xCE, 0xCA, 0xE9, 0xBB, 0xE5, 0x81, 0x87, 0x35, 0x63, 0x12, 0x43, 0x79, 0x69, 0x04, 0x24, 0xB9, 0xE8, 0xCD, 0xDC, 0xE3, 0xD4, 0xC7, 0x7E
};

static void center_text(const char *s) {
    int n = (int)strlen(s);
    int left = (SCREEN_WIDTH - n) / 2;
    if (left < 0) left = 0;
    printf("%*s%s\n", left, "", s);
}

static void right_text(const char *s) {
    int n = (int)strlen(s);
    int left = SCREEN_WIDTH - n;
    if (left < 0) left = 0;
    printf("%*s%s\n", left, "", s);
}

static void generate_product_id(char *id) {
    unsigned int seed =
        (unsigned int)time(NULL) ^
        (unsigned int)getpid() ^
        (unsigned int)(uintptr_t)&seed;
    srand(seed);
    unsigned int x = (unsigned int)(rand() & 0xFFFF);
    unsigned int y = (unsigned int)(rand() & 0xFFFF);
    snprintf(id, 14, "IIT-%04X-%04X", x, y);
}

static void derive_material(const char *id, unsigned char m[KEY_LEN]) {
    unsigned int a = 0, b = 0;
    sscanf(id, "IIT-%04X-%04X", &a, &b);

    m[0] = (unsigned char)(a >> 8);
    m[1] = (unsigned char)a;
    m[2] = (unsigned char)(b >> 8);
    m[3] = (unsigned char)b;

    m[4] = m[2] ^ m[0];
    m[5] = m[3] * m[1];
    m[6] = m[3] + m[2];
    m[7] = m[2] + m[1];

    m[8] = m[5] ^ 0x5A;
    m[9] = m[5] ^ 0xA7;

    for (int i = 10; i < KEY_LEN; i++)
        m[i] = m[i - 2] ^ m[i - 5] ^ (unsigned char)(i * 13);
}

static void make_key(const unsigned char m[KEY_LEN], char out[KEY_LEN + 1]) {
    static const char alphabet[] =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    for (int i = 0; i < KEY_LEN; i++) {
        unsigned char v =
            (unsigned char)(((A[i] * m[i]) ^ 0x37) ^ B[i]);
        v = (unsigned char)(v + i * 7);

        v ^= B[i];
        v = (unsigned char)(v - i * 7);
        v ^= 0x37;

        out[i] = alphabet[v % 36];
    }
    out[KEY_LEN] = '\0';
}

static int valid_format(const char *s, char normalized[KEY_LEN + 1]) {
    if (strlen(s) != 18) return 0;
    int j = 0;
    for (int i = 0; i < 18; i++) {
        if (i == 4 || i == 9 || i == 14) {
            if (s[i] != '-') return 0;
        } else {
            if (!isalnum((unsigned char)s[i])) return 0;
            normalized[j++] = (char)toupper((unsigned char)s[i]);
        }
    }
    normalized[j] = '\0';
    return j == KEY_LEN;
}

static int validate(const char *entered, const char *id) {
    unsigned char material[KEY_LEN];
    char correct[KEY_LEN + 1];
    derive_material(id, material);
    make_key(material, correct);
    return strcmp(entered, correct) == 0;
}

static void success(const char *id) {
    char flag[FLAG_LEN + 1];
    for (int i = 0; i < FLAG_LEN; i++) {
        unsigned char mask = (unsigned char)(0x5A + i * 17);
        flag[i] = (char)(encoded_flag[i] ^ mask);
    }
    flag[FLAG_LEN] = '\0';

    printf("\n");
    printf("==============================================================\n");
    printf("                 [✓] ACTIVATION SUCCESSFUL\n");
    printf("==============================================================\n\n");
    printf("  Product:       IIT Secure Suite Professional\n");
    printf("  Version:       6.4.1\n");
    printf("  Status:        ACTIVATED\n\n");
    printf("       Your software has been successfully activated.\n\n");
    printf("                Product ID: %s\n\n", id);
    center_text(flag);
    printf("\n");
    right_text("Created by AribZobair");
    printf("\n==============================================================\n");
}

static void banner(const char *id) {
    printf("==============================================================\n");
    printf("                 IIT SECURE SUITE 2026\n");
    printf("                    Product Activation\n");
    printf("==============================================================\n\n");
    printf("  Product:       IIT Secure Suite\n");
    printf("  Edition:       Professional\n");
    printf("  Version:       6.4.1\n");
    printf("  Product ID:    %s\n\n", id);
    printf("  This copy of IIT Secure Suite requires activation.\n");
    printf("  Please enter your activation key below.\n\n");
}

int main(void) {
    char id[14];
    char input[128];
    char normalized[KEY_LEN + 1];

    generate_product_id(id);
    banner(id);

    printf("  Activation Key:\n  > ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin)) return 1;
    input[strcspn(input, "\n")] = '\0';

    printf("\n  [*] Loading license configuration...\n");
    usleep(150000);
    printf("  [*] Checking product information...\n");
    usleep(150000);

    if (!valid_format(input, normalized)) {
        printf("\n  [!] Activation failed.\n\n");
        printf("      Error Code: LIC-104\n");
        printf("      Reason: Invalid activation key format.\n\n");
        printf("      Expected format: XXXX-XXXX-XXXX-XXX\n");
        return 0;
    }

    printf("  [*] Validating activation key...\n");
    usleep(200000);
    printf("  [*] Checking Product ID...\n");
    usleep(200000);

    if (validate(normalized, id))
        success(id);
    else {
        printf("\n  [!] Activation failed.\n\n");
        printf("      Error Code: LIC-203\n");
        printf("      Reason: Invalid activation key for this Product ID.\n\n");
        printf("      Please calculate a new key for this installation.\n");
    }
    return 0;
}
