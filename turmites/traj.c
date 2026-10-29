// Ход муравья как строка: ./traj T0 LEN < rules -> "rule SYMS", SYMS[i] = 'a' + color*4 + turn на шаге T0+i.
// Повороты относительные, поэтому строка не зависит от поворота/сдвига всей картины.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 8192
static uint8_t grid[(long)N * N];
static long vis[1 << 20];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};

int main(int argc, char **argv) {
    long t0 = atol(argv[1]), len = atol(argv[2]);
    char *buf = malloc(len + 1);
    int rule;
    while (scanf("%d", &rule) == 1) {
        int wc[4], tn[4], ns[4];
        for (int e = 0; e < 4; e++) {
            int b = (rule >> (4 * e)) & 15;
            wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1;
        }
        int x = N / 2, y = N / 2, d = 0, s = 0;
        for (long t = 0; t < t0 + len; t++) {
            uint8_t *c = &grid[(long)y * N + x];
            int e = s * 2 + *c;
            if (t >= t0) buf[t - t0] = (char)('a' + *c * 4 + tn[e]);
            *c = (uint8_t)wc[e];
            vis[t] = (long)y * N + x;
            d = (d + tn[e]) & 3; s = ns[e];
            x += DX[d]; y += DY[d];   // T0+LEN < N/2, за край не выйдет
        }
        for (long t = 0; t < t0 + len; t++) grid[vis[t]] = 0;
        buf[len] = 0;
        printf("%d %s\n", rule, buf);
    }
    return 0;
}
