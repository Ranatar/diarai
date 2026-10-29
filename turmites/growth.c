// Рост: ./growth MAXLOG < rules.txt  -> на каждое правило строка:
// rule, затем для k=8..MAXLOG: размер max(w,h) и число единиц в момент 2^k (или -1 после выхода за поле)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 8192
static uint8_t grid[(long)N * N];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};

int main(int argc, char **argv) {
    int maxlog = atoi(argv[1]);
    int rule;
    while (scanf("%d", &rule) == 1) {
        int wc[4], tn[4], ns[4];
        for (int e = 0; e < 4; e++) {
            int b = (rule >> (4 * e)) & 15;
            wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1;
        }
        int x = N / 2, y = N / 2, d = 0, s = 0;
        int minx = x, maxx = x, miny = y, maxy = y;
        long ones = 0, next = 1L << 8;
        int k = 8, out = 0;
        printf("%d", rule);
        for (long t = 1; k <= maxlog; t++) {
            uint8_t *c = &grid[(long)y * N + x];
            int e = s * 2 + *c;
            ones += wc[e] - *c;
            *c = (uint8_t)wc[e];
            d = (d + tn[e]) & 3; s = ns[e];
            x += DX[d]; y += DY[d];
            if (x < 0 || x >= N || y < 0 || y >= N) { out = 1; break; }
            if (x < minx) minx = x; if (x > maxx) maxx = x;
            if (y < miny) miny = y; if (y > maxy) maxy = y;
            if (t == next) {
                int w = maxx - minx + 1, h = maxy - miny + 1;
                printf(" %d:%ld", w > h ? w : h, ones);
                next <<= 1; k++;
            }
        }
        for (; k <= maxlog; k++) printf(" -1:-1");
        printf("\n");
        fflush(stdout);
        int x0 = minx, x1 = maxx, y0 = miny, y1 = maxy;
        if (x0 < 0) x0 = 0; if (y0 < 0) y0 = 0; if (x1 >= N) x1 = N - 1; if (y1 >= N) y1 = N - 1;
        for (int yy = y0; yy <= y1; yy++) memset(&grid[(long)yy * N + x0], 0, x1 - x0 + 1);
        (void)out;
    }
    return 0;
}
