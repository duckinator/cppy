#pymacros "macros.py"
#include <stdio.h>

int main() {
    const char spaces[11] = buffer!(' ', 10);
    printf("'%s'\r\n", spaces);
    return 0;
}
