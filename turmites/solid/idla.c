// Игрушка IDLA с полётами: из клетки, где прибавили, муравей летит по осям (направление случайно),
// длина полёта — геометрическая со средним L0 (обрыв на «поре»), пока не выйдет на белую клетку; её — в тело.
// Шаги = сумма длин полётов. ./idla L0 AREA SEED -> печать A t на удвоениях A; out.pgm
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[N*N];
static uint64_t rs=88172645463325252ULL; static inline uint64_t rng(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int argc,char**argv){ double L0=atof(argv[1]); long AR=atol(argv[2]); rs+=atol(argv[3])*2654435761ULL;
  int c=N/2; g[(long)c*N+c]=1; long A=1, t=0, nextA=1024; int x=c,y=c; double p=1.0/L0;
  int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
  while(A<AR){ int d=(rng()>>30)&3; double u=((rng()>>11)+1.0)/9007199254740993.0; long len=1+(long)(log(u)/log(1-p));
    for(long i=0;i<len;i++){ x+=DX[d]; y+=DY[d]; t++; if(!g[(long)y*N+x]){ g[(long)y*N+x]=1; A++; break; } }
    if(x<5||y<5||x>N-5||y>N-5) break;
    if(A>=nextA){ printf("%ld %ld\n",A,t); nextA*=2; } }
  return 0; }
