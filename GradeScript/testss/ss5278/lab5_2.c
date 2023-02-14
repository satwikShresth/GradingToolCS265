#include <stdio.h>
#include <string.h>

#define MAX_LENGTH 100

int main(void) {
    char *message;
    char *p;

    printf("Enter a message: ");
    scanf("%s",message);

    p = message + strlen(message) - 1;

    printf("Reversal is: ");
    while (&p >= message) {
        putchar(*p);
        p--;
    }
    printf("\n");

    return 0;
}
