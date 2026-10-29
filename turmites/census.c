// Перепись турмитов: 2 состояния × 2 цвета, относительные повороты.
// Правило — 16 бит: для входа e = state*2 + color четыре бита
//   бит0 = записываемый цвет, бит1-2 = поворот (0 прямо, 1 направо, 2 разворот, 3 налево),
//   бит3 = следующее состояние.
// Запуск: ./census FROM TO STEPS  -> CSV в stdout.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 4096          // сторона поля
#define H 65536         // длина истории (степень двойки)
#define PMAX 8192       // максимальный искомый период шоссе

static uint8_t grid[N * N];
static uint8_t sym[H];
static int32_t hx[H], hy[H];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};

// ищем период p: последние 3p символов p-периодичны, смещение за p шагов постоянно
static int find_period(long t, int *ddx, int *ddy) {
    if (t < 3) return 0;
    long lim = t / 3; if (lim > PMAX) lim = PMAX; if (lim > H / 3) lim = H / 3;
    for (int p = 1; p <= lim; p++) {
        int ok = 1;
        for (long k = 0; k < 2L * p; k++) {
            long a = (t - 1 - k) & (H - 1), b = (t - 1 - k - p) & (H - 1);
            if (sym[a] != sym[b]) { ok = 0; break; }
        }
        if (!ok) continue;
        long i0 = (t - 1) & (H - 1), i1 = (t - 1 - p) & (H - 1), i2 = (t - 1 - 2 * p) & (H - 1);
        int dx1 = hx[i0] - hx[i1], dy1 = hy[i0] - hy[i1];
        int dx2 = hx[i1] - hx[i2], dy2 = hy[i1] - hy[i2];
        if (dx1 != dx2 || dy1 != dy2) continue;
        *ddx = dx1; *ddy = dy1;
        return p;
    }
    return 0;
}

int main(int argc, char **argv) {
    int from = atoi(argv[1]), to = atoi(argv[2]);
    long steps = atol(argv[3]);
    printf("rule,steps_run,escaped,minx,maxx,miny,maxy,ones,last_growth,period,pdx,pdy\n");
    for (int rule = from; rule < to; rule++) {
        int wc[4], tn[4], ns[4];
        for (int e = 0; e < 4; e++) {
            int b = (rule >> (4 * e)) & 15;
            wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1;
        }
        int x = N / 2, y = N / 2, d = 0, s = 0;
        int minx = x, maxx = x, miny = y, maxy = y;
        long ones = 0, last_growth = 0, t;
        int escaped = 0;
        for (t = 0; t < steps; t++) {
            uint8_t *c = &grid[(long)y * N + x];
            int e = s * 2 + *c;
            long hi = t & (H - 1);
            sym[hi] = (uint8_t)(e | (d << 2));
            hx[hi] = x; hy[hi] = y;
            ones += wc[e] - *c;
            *c = (uint8_t)wc[e];
            d = (d + tn[e]) & 3;
            s = ns[e];
            x += DX[d]; y += DY[d];
            if (x < 0 || x >= N || y < 0 || y >= N) { escaped = 1; t++; break; }
            if (x < minx) { minx = x; last_growth = t; }
            if (x > maxx) { maxx = x; last_growth = t; }
            if (y < miny) { miny = y; last_growth = t; }
            if (y > maxy) { maxy = y; last_growth = t; }
        }
        int pdx = 0, pdy = 0;
        int p = find_period(t, &pdx, &pdy);
        printf("%d,%ld,%d,%d,%d,%d,%d,%ld,%ld,%d,%d,%d\n", rule, t, escaped,
               minx - N / 2, maxx - N / 2, miny - N / 2, maxy - N / 2, ones, last_growth, p, pdx, pdy);
        // очистить только задетый прямоугольник
        int x0 = minx, x1 = maxx, y0 = miny, y1 = maxy;
        if (x0 < 0) x0 = 0; if (y0 < 0) y0 = 0; if (x1 >= N) x1 = N - 1; if (y1 >= N) y1 = N - 1;
        for (int yy = y0; yy <= y1; yy++) memset(&grid[(long)yy * N + x0], 0, x1 - x0 + 1);
    }
    return 0;
}
