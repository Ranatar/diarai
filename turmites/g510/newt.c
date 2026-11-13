/* 4.8.8 вант (код v488): моменты новых плиток. ./newt D0 LOG2N CODE -> t x y */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 8192
static unsigned char f[L][L];
int main(int argc,char**argv){ int d=atoi(argv[1]); long long N=1LL<<atoi(argv[2]); int code=atoi(argv[3]);
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)}; int x=L/2,y=L/2;
  for(long long t=0;t<N;t++){ int c=f[y][x]&1; if(!(f[y][x]&2)){f[y][x]|=2; printf("%lld %d %d\n",t,x-L/2,y-L/2);}
    d=(d+((x&1)?Ts[c]:To[c]))&7; f[y][x]^=1; x+=DX[d]; y+=DY[d]; if(x<4||y<4||x>L-4||y>L-4)break; } }
