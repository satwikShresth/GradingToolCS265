#include <stdio.h>
#include <string.h>

#define MAX_LENGTH 100

int main() {
    char message[MAX_LENGTH];
    int i, length;

    printf("Enter a message: ");
    for (i = 0; i < MAX_LENGTH - 1 && (message[i] = getchar()) != '\n'; i++);
    length = i;

    printf("Reversal is: ");
    for (i = 0; i < length; i++) {
        putchar(message[i]);
    }
    putchar('\n');

    return 0;
}