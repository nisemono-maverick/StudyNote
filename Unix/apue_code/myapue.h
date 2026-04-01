#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

void err_quit(const char *msg) {
    fprintf(stderr, "%s\n", msg);
    exit(1);
}

void err_sys(const char *msg) {
    fprintf(stderr, "%s: %s\n", msg, strerror(errno));
    exit(1);
}
