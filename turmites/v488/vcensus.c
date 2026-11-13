/* Перепись вантов на плитках паркета 4.8.8 (13-е пробуждение).
   Вант: на плитке цвета c поворачивает, перекрашивает её и шагает. Восьмиугольники — в (2i,2j), квадраты — в (2i+1,2j+1)
   (удвоенные координаты); 8 направлений по 45°, 0 — восток, +1 — против часовой (в координатах y вверх).
   Правило: To[0],To[1] ∈ 0..7 (поворот на восьмиугольнике, ×45°), Ts[0],Ts[1] ∈ {0,2,4,6} (на квадрате; только чётные,
   иначе из квадрата не попасть в восьмиугольник). Код = To0 + 8 To1 + 64 (Ts0/2) + 256 (Ts1/2), 1024 правила.
   Лэнгтон (OEIS A308973): To0=7 (направо 45°), To1=1, Ts0=6, Ts1=2 → 7+8+64*3+256*1 = 463.
   Старт: восьмиугольник (0,0), направление D0 (0 — к восьмиугольнику, 1 — к квадрату).
   ./vcensus LOG2N L D0 [from to] -> code n(N/16) n(N/4) n(N) black edge */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){
  int lg=atoi(argv[1]),L=atoi(argv[2]),d0=atoi(argv[3]); int from=argc>4?atoi(argv[4]):0,to=argc>5?atoi(argv[5]):1024;
  unsigned char*f=malloc((size_t)L*L);
  for(int code=from;code<to;code++){
    int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
    memset(f,0,(size_t)L*L);
    int x=L/2&~1,y=L/2&~1,d=d0; long long N=1LL<<lg,n1=0,n2=0,cells=0,black=0,edge=-1,t;
    for(t=1;t<=N;t++){
      size_t i=(size_t)y*L+x; int c=f[i]&1; if(!(f[i]&2)){f[i]|=2;cells++;}
      d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; black+=c?-1:1;
      x+=DX[d]; y+=DY[d];
      if(x<2||y<2||x>=L-2||y>=L-2){edge=t;break;}
      if(t==(N>>4))n1=cells; if(t==(N>>2))n2=cells;
    }
    printf("%d %lld %lld %lld %lld %lld\n",code,n1,n2,cells,black,edge); fflush(stdout);
  }
}
