// Долгий счёт одного турмита 2x2 с сохранением состояния.
// Поле 65536^2 клеток, плитки 8x8 бит в uint64 (муравей внутри плитки ходит в регистре).
//   ./big RULE CKPT TMAX [SECONDS]
// Если файл CKPT есть — продолжает с него, иначе начинает с пустого поля.
// Каждые 2^k шагов печатает: t x y  bbox(minx maxx miny maxy) — координаты от старта.
// Останавливается: t>=TMAX, прошло SECONDS секунд, муравей ушёл от рамки
// (последней напечатанной) дальше чем на ESC клеток, или край поля. Перед выходом пишет CKPT.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define LOGN 16
#define N (1L << LOGN)
#define TN (N >> 3)            // плиток по стороне
#define ESC 4096
#define RBUF (1L << 25)
#define PMAX (1 << 20)
static uint8_t *sym; static int32_t *hx, *hy;
#define I(t) ((t) & (RBUF - 1))
// поиск периода и начала по кольцевому буферу (как в onsetr); t — число сделанных шагов, t0 — первый шаг буфера
static int detect(int64_t t, int64_t t0, int *pp, int *dx, int *dy, int64_t *on) {
    int64_t have = t - t0 < RBUF ? t - t0 : RBUF, lo = t - have;
    for (int q = 1; q <= PMAX; q++) {
        int64_t win = 2L * q > 20000 ? 2L * q : 20000;
        if (t - 1 - win - q < lo) break;
        int ok = 1;
        for (int64_t k = 0; k < win; k++) if (sym[I(t - 1 - k)] != sym[I(t - 1 - k - q)]) { ok = 0; break; }
        if (!ok) continue;
        int64_t a = I(t - 1), b = I(t - 1 - q), c2 = I(t - 1 - 2 * q);
        int dx1 = hx[a] - hx[b], dy1 = hy[a] - hy[b], dx2 = hx[b] - hx[c2], dy2 = hy[b] - hy[c2];
        if (dx1 == dx2 && dy1 == dy2) {
            int64_t i = t - 1 - q;
            while (i >= lo && sym[I(i)] == sym[I(i + q)]) i--;
            *pp = q; *dx = dx1; *dy = dy1; *on = (i < lo) ? -(i + 1) : i + 1; return 1;
        }
    }
    return 0;
}

static uint64_t *tiles;
static const int DX[4] = {0, 1, 0, -1}, DY[4] = {-1, 0, 1, 0};

typedef struct { int64_t t, x, y; int32_t d, s; int64_t mnx, mxx, mny, mxy; int64_t rule; } hdr_t;

static int save(const char *fn, hdr_t *h) {
    char tmp[1024]; snprintf(tmp, sizeof tmp, "%s.tmp", fn);
    FILE *f = fopen(tmp, "wb"); if (!f) return -1;
    fwrite(h, sizeof *h, 1, f);
    long ty0 = h->mny >> 3, ty1 = h->mxy >> 3, tx0 = h->mnx >> 3, tx1 = h->mxx >> 3;
    for (long ty = ty0; ty <= ty1; ty++) fwrite(&tiles[ty * TN + tx0], 8, tx1 - tx0 + 1, f);
    fclose(f); rename(tmp, fn); return 0;
}
static int load(const char *fn, hdr_t *h) {
    FILE *f = fopen(fn, "rb"); if (!f) return -1;
    if (fread(h, sizeof *h, 1, f) != 1) { fclose(f); return -1; }
    long ty0 = h->mny >> 3, ty1 = h->mxy >> 3, tx0 = h->mnx >> 3, tx1 = h->mxx >> 3;
    for (long ty = ty0; ty <= ty1; ty++)
        if (fread(&tiles[ty * TN + tx0], 8, tx1 - tx0 + 1, f) != (size_t)(tx1 - tx0 + 1)) { fclose(f); return -2; }
    fclose(f); return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: big RULE CKPT TMAX [SECONDS]\n"); return 1; }
    int rule = atoi(argv[1]); const char *ck = argv[2];
    int64_t tmax = atoll(argv[3]); double secs = argc > 4 ? atof(argv[4]) : 1e18;
    tiles = calloc((size_t)TN * TN, 8); sym = malloc(RBUF); hx = malloc(4 * RBUF); hy = malloc(4 * RBUF); if (!tiles) { fprintf(stderr, "no mem\n"); return 1; }
    // таблица: вход e = s*2+c -> wc | tn<<1 | ns<<3
    int wc[4], tn[4], ns[4];
    for (int e = 0; e < 4; e++) { int b = (rule >> (4 * e)) & 15; wc[e] = b & 1; tn[e] = (b >> 1) & 3; ns[e] = (b >> 3) & 1; }
    hdr_t h;
    if (load(ck, &h) == 0) {
        if (h.rule != rule) { fprintf(stderr, "ckpt rule mismatch\n"); return 1; }
        fprintf(stderr, "resume t=%lld\n", (long long)h.t);
    } else {
        memset(&h, 0, sizeof h); h.rule = rule; h.x = h.y = N / 2; h.mnx = h.mxx = h.mny = h.mxy = N / 2;
    }
    int64_t t = h.t; int d = h.d, s = h.s;
    int q = (s << 2) | d, LUT[16], LX[8], LY[8];
    for (int qq = 0; qq < 8; qq++) { LX[qq] = DX[qq & 3]; LY[qq] = DY[qq & 3];
        for (int c = 0; c < 2; c++) { int e = ((qq >> 2) << 1) | c; int nd = ((qq & 3) + tn[e]) & 3;
            LUT[(qq << 1) | c] = (ns[e] << 2) | nd | ((c ^ wc[e]) << 4); } }
    long tx = h.x >> 3, ty = h.y >> 3; int lx = h.x & 7, ly = h.y & 7;
    uint64_t w = tiles[ty * TN + tx];
    long mnx = h.mnx >> 3, mxx = h.mxx >> 3, mny = h.mny >> 3, mxy = h.mxy >> 3;   // рамка в плитках
    long rmnx = mnx, rmxx = mxx, rmny = mny, rmxy = mxy;   // рамка на момент последнего отчёта
    int64_t next = 1; while (next <= t) next <<= 1;
    time_t t0 = time(NULL); int why = 0; uint64_t nex = 0;
    const long esc = ESC >> 3;
    while (t < tmax) {
        int64_t lim = next < tmax ? next : tmax;
        // внутренний цикл: до отчёта
        while (t < lim) {
            int bit = (ly << 3) | lx;
            int c = (int)((w >> bit) & 1);
            int L = LUT[(q << 1) | c];
            w ^= (uint64_t)(L >> 4) << bit;
            { long i = t & (RBUF - 1); sym[i] = (uint8_t)((q >> 2) << 1 | c) | (uint8_t)((q & 3) << 2);
              hx[i] = (int32_t)(tx * 8 + lx); hy[i] = (int32_t)(ty * 8 + ly); }
            q = L & 7;
            lx += LX[q]; ly += LY[q]; t++;
            if ((lx | ly) & ~7) {
                tiles[ty * TN + tx] = w;
                if (lx < 0) { lx = 7; tx--; } else if (lx > 7) { lx = 0; tx++; }
                if (ly < 0) { ly = 7; ty--; } else if (ly > 7) { ly = 0; ty++; }
                w = tiles[ty * TN + tx];
                if (tx < mnx) { mnx = tx; if (tx < 1) { why = 3; break; } if (rmnx - tx > esc) { why = 2; break; } }
                if (tx > mxx) { mxx = tx; if (tx > TN - 2) { why = 3; break; } if (tx - rmxx > esc) { why = 2; break; } }
                if (ty < mny) { mny = ty; if (ty < 1) { why = 3; break; } if (rmny - ty > esc) { why = 2; break; } }
                if (ty > mxy) { mxy = ty; if (ty > TN - 2) { why = 3; break; } if (ty - rmxy > esc) { why = 2; break; } }
                if (!(++nex & 0x3FFFFF)) {
                    if (difftime(time(NULL), t0) > secs) { why = 1; break; }
                    if (!(nex & 0xFFFFFFF)) { rmnx = mnx; rmxx = mxx; rmny = mny; rmxy = mxy; }
                }
            }
        }
        if (why == 2) {
            int p, dx, dy; int64_t on;
            if (detect(t, h.t, &p, &dx, &dy, &on)) {
                printf("HIGHWAY rule %d period %d d=(%d,%d) onset %lld  (escape at %lld)\n", rule, p, dx, dy, (long long)on, (long long)t);
                fflush(stdout); break;
            }
            printf("false escape at %lld\n", (long long)t); fflush(stdout);
            why = 0; rmnx = mnx; rmxx = mxx; rmny = mny; rmxy = mxy;
            continue;
        }
        if (why) break;
        if (t == next) {
            printf("%lld %ld %ld  %ld %ld %ld %ld\n", (long long)t, tx * 8 + lx - N / 2, ty * 8 + ly - N / 2,
                   mnx * 8 - N / 2, mxx * 8 + 7 - N / 2, mny * 8 - N / 2, mxy * 8 + 7 - N / 2);
            fflush(stdout);
            rmnx = mnx; rmxx = mxx; rmny = mny; rmxy = mxy; next <<= 1;
        }
    }
    if (why == 0 && getenv("BIG_FINAL")) {   // в конце: не петля ли (или шоссе внутри рамки)
        int p, dx, dy; int64_t on;
        if (detect(t, h.t, &p, &dx, &dy, &on))
            printf("PERIODIC rule %d period %d d=(%d,%d) onset %lld\n", rule, p, dx, dy, (long long)on);
    }
    tiles[ty * TN + tx] = w;
    d = q & 3; s = q >> 2;
    h.t = t; h.x = tx * 8 + lx; h.y = ty * 8 + ly; h.d = d; h.s = s;
    h.mnx = mnx * 8; h.mxx = mxx * 8 + 7; h.mny = mny * 8; h.mxy = mxy * 8 + 7;
    // при выходе за рамку текущая плитка уже вне сохранённой рамки? нет: рамка обновлена до break
    save(ck, &h);
    const char *W[] = {"tmax", "time", "escape", "edge"};
    printf("stop %s t=%lld x=%ld y=%ld  bbox %ld %ld %ld %ld  %.0fs\n", W[why], (long long)t, (long)(h.x - N / 2), (long)(h.y - N / 2),
           (long)(h.mnx - N / 2), (long)(h.mxx - N / 2), (long)(h.mny - N / 2), (long)(h.mxy - N / 2), difftime(time(NULL), t0));
    return 0;
}
