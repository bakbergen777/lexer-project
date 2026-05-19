/* ----------------------------------------------------------
 * test.c  -  sample input that exercises every token category
 * ---------------------------------------------------------- */
#include <stdio.h>

// single-line comment: compute factorial of n
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

float average(int a, int b) {
    /* multi-line comment
       returns the arithmetic mean */
    return (a + b) / 2.0;
}

int main(void) {
    int   x      = 42;
    float pi     = 3.14159;
    char  letter = 'A';
    const char *msg = "Hello, Compiler!";

    for (int i = 0; i < 5; i++) {
        x += factorial(i);
    }

    if (x >= 100 && pi != 0.0) {
        printf("%s x=%d avg=%f\n", msg, x, average(x, 7));
    } else {
        printf("small\n");
    }

    return 0;
}

/* The next line contains a stray '@' to demonstrate error reporting */
int bad@token = 0;
