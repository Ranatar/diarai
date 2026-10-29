// Отрисовка одного турмита: ./render RULE STEPS out.pgm
// Пишет PGM задетого прямоугольника: фон 255, цвет 1 = 0, след посещений серым не рисуем.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define N 4096
static uint8_t grid[N * N];
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};

int main(int argc, char **argv) {
    int rule = atoi(argv[1]);
    long steps = atol(argv[2]);
    int wc[4], tn[4], ns[4];
    for (int e = 0; e < 4; e++) {
        int b = (rule >> (4 * e)) & 15;
        wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1;
    }
    int x = N / 2, y = N / 2, d = 0, s = 0;
    int minx = x, maxx = x, miny = y, maxy = y;
    long t;
    for (t = 0; t < steps; t++) {
        uint8_t *c = &grid[(long)y * N + x];
        int e = s * 2 + (*c & 1);
        *c = (uint8_t)(wc[e] | 2);   // бит1 = клетка посещалась
        d = (d + tn[e]) & 3; s = ns[e];
        x += DX[d]; y += DY[d];
        if (x < 0 || x >= N || y < 0 || y >= N) break;
        if (x < minx) minx = x; if (x > maxx) maxx = x;
        if (y < miny) miny = y; if (y > maxy) maxy = y;
    }
    FILE *f = fopen(argv[3], "wb");
    int w = maxx - minx + 1, h = maxy - miny + 1;
    fprintf(f, "P5\n%d %d\n255\n", w, h);
    for (int yy = miny; yy <= maxy; yy++)
        for (int xx = minx; xx <= maxx; xx++) {
            uint8_t v = grid[(long)yy * N + xx];
            fputc(v & 1 ? 20 : (v & 2 ? 215 : 255), f);
        }
    fclose(f);
    fprintf(stderr, "rule %d: %ld steps, %dx%d\n", rule, t, w, h);
    return 0;
}
