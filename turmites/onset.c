// Начало шоссе: ./onset MAXSTEPS < rules.txt
// Идёт до выхода за поле (или MAXSTEPS), хранит всю историю ходов,
// ищет период p (до PMAX) на хвосте, затем откатывается назад, пока sym[t]==sym[t+p].
// Вывод: rule steps_run escaped period dx dy onset
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifndef N
#define N 8192
#endif
#define PMAX 200000
#define MINW 20000   // периодичность должна держаться хотя бы столько последних шагов
static uint8_t grid[(long)N * N];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};

int main(int argc, char **argv) {
    long maxsteps = atol(argv[1]);
    uint8_t *sym = malloc(maxsteps + 1);
    int16_t *hx = malloc(2 * (maxsteps + 1)), *hy = malloc(2 * (maxsteps + 1));
    int rule;
    while (scanf("%d", &rule) == 1) {
        int wc[4], tn[4], ns[4];
        for (int e = 0; e < 4; e++) {
            int b = (rule >> (4 * e)) & 15;
            wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1;
        }
        int x = N / 2, y = N / 2, d = 0, s = 0, escaped = 0;
        int minx = x, maxx = x, miny = y, maxy = y;
        long t;
        for (t = 0; t < maxsteps; t++) {
            uint8_t *c = &grid[(long)y * N + x];
            int e = s * 2 + *c;
            sym[t] = (uint8_t)(e | (d << 2));
            hx[t] = (int16_t)(x - N / 2); hy[t] = (int16_t)(y - N / 2);
            *c = (uint8_t)wc[e];
            d = (d + tn[e]) & 3; s = ns[e];
            x += DX[d]; y += DY[d];
            if (x < 0 || x >= N || y < 0 || y >= N) { escaped = 1; t++; break; }
            if (x < minx) minx = x; if (x > maxx) maxx = x;
            if (y < miny) miny = y; if (y > maxy) maxy = y;
        }
        int p = 0, ddx = 0, ddy = 0;
        long lim = t / 3; if (lim > PMAX) lim = PMAX;
        for (int q = 1; q <= lim && !p; q++) {
            int ok = 1;
            long win = 2L * q > MINW ? 2L * q : MINW;
            if (t - 1 - win - q < 0) break;
            for (long k = 0; k < win; k++)
                if (sym[t - 1 - k] != sym[t - 1 - k - q]) { ok = 0; break; }
            if (!ok) continue;
            int dx1 = hx[t - 1] - hx[t - 1 - q], dy1 = hy[t - 1] - hy[t - 1 - q];
            int dx2 = hx[t - 1 - q] - hx[t - 1 - 2 * q], dy2 = hy[t - 1 - q] - hy[t - 1 - 2 * q];
            if (dx1 == dx2 && dy1 == dy2) { p = q; ddx = dx1; ddy = dy1; }
        }
        long onset = -1;
        if (p) {
            long i = t - 1 - p;
            while (i >= 0 && sym[i] == sym[i + p]) i--;
            onset = i + 1;
        }
        printf("%d %ld %d %d %d %d %ld\n", rule, t, escaped, p, ddx, ddy, onset);
        fflush(stdout);
        int x0 = minx, x1 = maxx, y0 = miny, y1 = maxy;
        if (x0 < 0) x0 = 0; if (y0 < 0) y0 = 0; if (x1 >= N) x1 = N - 1; if (y1 >= N) y1 = N - 1;
        for (int yy = y0; yy <= y1; yy++) memset(&grid[(long)yy * N + x0], 0, x1 - x0 + 1);
    }
    return 0;
}
