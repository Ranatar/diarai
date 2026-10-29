// Активность пятна: ./activity MAXLOG < rules -> rule  k:visited:active ...
// Для каждой клетки храним номер «эпохи» последнего изменения цвета (эпоха k = шаги [2^(k-1), 2^k)).
// На отметке 2^k печатаем: сколько клеток посещено всего и сколько изменено за последнюю эпоху.
// Хаос: active/visited держится примерно постоянным. Двойное шоссе, челнок, клин: пятно замерзает, доля падает.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#ifndef N
#define N 8192
#endif
static uint8_t grid[(long)N * N];   // бит0 = цвет, бит7 = посещалась, биты1..6 = эпоха последнего изменения
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
        printf("%d", rule);
        long t = 0;
        int esc = 0;
        for (int k = 1; k <= maxlog && !esc; k++) {
            long end = 1L << k;
            uint8_t ep = (uint8_t)(k << 1);
            for (; t < end; t++) {
                uint8_t *c = &grid[(long)y * N + x];
                int col = *c & 1;
                int e = s * 2 + col;
                if (wc[e] != col) *c = (uint8_t)(0x80 | ep | wc[e]);
                else *c |= 0x80;
                d = (d + tn[e]) & 3; s = ns[e];
                x += DX[d]; y += DY[d];
                if (x < 0 || x >= N || y < 0 || y >= N) { esc = 1; break; }
                if (x < minx) minx = x; if (x > maxx) maxx = x;
                if (y < miny) miny = y; if (y > maxy) maxy = y;
            }
            if (esc || k < 10) continue;
            long vis = 0, act = 0;
            for (int yy = miny; yy <= maxy; yy++) {
                uint8_t *row = &grid[(long)yy * N];
                for (int xx = minx; xx <= maxx; xx++) {
                    uint8_t v = row[xx];
                    if (v & 0x80) { vis++; if ((v & 0x7e) == ep) act++; }
                }
            }
            printf(" %d:%ld:%ld", k, vis, act);
        }
        printf(esc ? " esc\n" : "\n");
        fflush(stdout);
        for (int yy = miny; yy <= maxy; yy++) memset(&grid[(long)yy * N + minx], 0, maxx - minx + 1);
    }
    return 0;
}
