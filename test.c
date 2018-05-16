#pymacros "macros.py"
#include <stdio.h>

int main() {
    const char aaaa[11] = buffer!('A', 11);
    printf("'%s'\r\n", aaaa);
    return 0;
}
