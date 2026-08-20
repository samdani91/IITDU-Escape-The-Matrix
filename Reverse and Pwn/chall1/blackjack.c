#include <stdio.h>

void print_flag(void)
{
    /* XOR-encoded with key 0x5A */
    unsigned char encoded[] = {
        0x13, 0x13, 0x0e, 0x19, 0x0e, 0x1c, 0x21, 0x32,
        0x6b, 0x2e, 0x17, 0x69, 0x05, 0x2d, 0x6b, 0x2e,
        0x32, 0x05, 0x0e, 0x32, 0x69, 0x1c, 0x36, 0x6e,
        0x3d, 0x27
    };

    int length = sizeof(encoded) / sizeof(encoded[0]);

    printf("\nCongratulations!\n");
    printf("You found the hidden winning hand!\n\n");

    for (int i = 0; i < length; i++)
        putchar(encoded[i] ^ 0x5A);

    printf("\n");
}

int calculate_score(int card1, int card2)
{
    return card1 + card2;
}

int hidden_check(int card1, int card2)
{
    /*
     * A score of 21 is necessary, but not sufficient.
     * The hidden winning hand is 8 + 13.
     */
    if (card1 + card2 != 21)
        return 0;

    if ((card1 + 4) * (card2 - 5) == 96)
        return 1;

    return 0;
}

int main(void)
{
    int card1, card2;

    printf("========================================\n");
    printf("             BLACKJACK\n");
    printf("========================================\n\n");

    printf("Dealer's visible card: 9\n\n");

    printf("Enter your first card (1-13): ");
    if (scanf("%d", &card1) != 1)
        return 1;

    printf("Enter your second card (1-13): ");
    if (scanf("%d", &card2) != 1)
        return 1;

    if (card1 < 1 || card1 > 13 ||
        card2 < 1 || card2 > 13)
    {
        printf("\nInvalid card value!\n");
        printf("Cards must be between 1 and 13.\n");
        return 1;
    }

    int score = calculate_score(card1, card2);

    printf("\nYour hand: %d + %d\n", card1, card2);
    printf("Your score: %d\n", score);
    printf("Dealer's score: 20\n\n");

    if (score > 21)
    {
        printf("You busted!\n");
        return 0;
    }

    if (hidden_check(card1, card2))
    {
        print_flag();
        return 0;
    }

    if (score == 21)
    {
        printf("BLACKJACK!\n");
        printf("But something seems to be missing...\n");
    }
    else if (score > 20)
    {
        printf("You win!\n");
    }
    else
    {
        printf("You lose!\n");
    }

    return 0;
}
