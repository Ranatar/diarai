// ./walk RULE TMAX EVERY : печатает t x y minx maxx miny maxy (относительно старта) каждые EVERY шагов
// поле 32768^2 байт = 1 ГБ; выход за край — конец.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 32768L
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int rule=atoi(argv[1]); long tmax=atol(argv[2]), ev=atol(argv[3]);
  uint8_t *g=calloc(N*N,1);
  int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15; wc[e]=b&1; tn[e]=(b>>1)&3; ns[e]=(b>>3)&1;}
  long x=N/2,y=N/2; int d=0,s=0; long mnx=x,mxx=x,mny=y,mxy=y;
  for(long t=0;t<tmax;t++){
    uint8_t *c=&g[y*N+x]; int e=s*2+*c; *c=wc[e]; d=(d+tn[e])&3; s=ns[e];
    x+=DX[d]; y+=DY[d];
    if(x<1||y<1||x>=N-1||y>=N-1){printf("edge %ld\n",t);break;}
    if(x<mnx)mnx=x; if(x>mxx)mxx=x; if(y<mny)mny=y; if(y>mxy)mxy=y;
    if((t+1)%ev==0) printf("%ld %ld %ld %ld %ld %ld %ld\n",t+1,x-N/2,y-N/2,mnx-N/2,mxx-N/2,mny-N/2,mxy-N/2);
  }
  return 0;
}
