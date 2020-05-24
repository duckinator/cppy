#include <stdio.h>
#include <string.h>

#define buffer(chr, length) memset((char[length + 1]){0}, chr, length)

int main() {
    const char *aaaa = buffer('A', 10);
    printf("'%s'\r\n", aaaa);
    return 0;
}
