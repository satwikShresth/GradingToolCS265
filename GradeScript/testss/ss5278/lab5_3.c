#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
	FILE *fp;
	char line[101];

	fp = fopen("fruits.txt", "r");

	if (fp == NULL) {
		printf("Can't open file \n");
		exit(-1);
	}
	while (fgets(line, 100, fp) != NULL) {
		printf("I read line= %s \n", line);
	}
}
