#include <stdio.h>
int main() {
    int n;
    unsigned long long factorial = 1;
    if (scanf("%d", &n) != 1) { 
        printf("Invalid input. Please enter an integer.\n");
        return 1;
    }
    if (n < 0) {
        printf("Factorial is not defined for negative numbers.\n");
        return 1;
    }
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }
    printf("Factorial of %d = %llu\n", n, factorial);
    return 0;
}
