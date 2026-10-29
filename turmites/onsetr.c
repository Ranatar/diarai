// onset с кольцевым буфером: память не зависит от длины прогона.
// ./onsetr MAXSTEPS < rules  -> rule steps escaped period dx dy onset
// Если откат дошёл до начала буфера, onset печатается со знаком минус: «начало не позже |onset|»
// (тогда пересчитать обычным onset или увеличить R).
// Поле N×N (по умолчанию 8192, -DN=4096 для проверки края).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifndef N
#define N 8192
#endif
#define R (1L << 23)        // длина буфера (степень двойки), 8M шагов
#define PMAX 200000
#ifndef MINW
#define MINW 20000
#endif
static uint8_t grid[(long)N * N];
static uint8_t sym[R];
static int16_t hx[R], hy[R];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};
#define I(t) ((t) & (R - 1))

int main(int argc, char **argv) {
    long maxsteps = atol(argv[1]);
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
            long i = I(t);
            sym[i] = (uint8_t)(e | (d << 2));
            hx[i] = (int16_t)(x - N / 2); hy[i] = (int16_t)(y - N / 2);
            *c = (uint8_t)wc[e];
            d = (d + tn[e]) & 3; s = ns[e];
            x += DX[d]; y += DY[d];
            if (x < 0 || x >= N || y < 0 || y >= N) { escaped = 1; t++; break; }
            if (x < minx) minx = x; if (x > maxx) maxx = x;
            if (y < miny) miny = y; if (y > maxy) maxy = y;
        }
        long have = t < R ? t : R;            // сколько истории в буфере
        long lo = t - have;                    // самый ранний шаг в буфере
        int p = 0, ddx = 0, ddy = 0;
        long mw = MINW < have / 3 ? MINW : have / 3;
        for (int q = 1; q <= PMAX && !p; q++) {
            long win = 2L * q > mw ? 2L * q : mw;
            if (t - 1 - win - q < lo) break;
            int ok = 1;
            for (long k = 0; k < win; k++)
                if (sym[I(t - 1 - k)] != sym[I(t - 1 - k - q)]) { ok = 0; break; }
            if (!ok) continue;
            long a = I(t - 1), b = I(t - 1 - q), c2 = I(t - 1 - 2 * q);
            int dx1 = hx[a] - hx[b], dy1 = hy[a] - hy[b];
            int dx2 = hx[b] - hx[c2], dy2 = hy[b] - hy[c2];
            if (dx1 == dx2 && dy1 == dy2) { p = q; ddx = dx1; ddy = dy1; }
        }
        long onset = -1;
        if (p) {
            long i = t - 1 - p;
            while (i >= lo && sym[I(i)] == sym[I(i + p)]) i--;
            onset = i + 1;
            if (i < lo && lo > 0) onset = -onset;   // упёрлись в начало буфера
        }
        printf("%d %ld %d %d %d %d %ld\n", rule, t, escaped, p, ddx, ddy, onset);
        fflush(stdout);
        int x0 = minx, x1 = maxx, y0 = miny, y1 = maxy;
        if (x0 < 0) x0 = 0; if (y0 < 0) y0 = 0; if (x1 >= N) x1 = N - 1; if (y1 >= N) y1 = N - 1;
        for (int yy = y0; yy <= y1; yy++) memset(&grid[(long)yy * N + x0], 0, x1 - x0 + 1);
    }
    return 0;
}
