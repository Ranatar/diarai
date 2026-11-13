#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 2048
unsigned char f[L][L];
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long N=atoll(argv[2]);
  int To[2]={6,7},Ts[2]={6,2}; int x=L/2,y=L/2,d=d0;
  for(long long t=0;t<N;t++){
    int c=f[y][x]&1; int nd=(d+((x&1)?Ts[c]:To[c]))&7;
    printf("%lld (%d,%d) c%d d%d->%d\n",t,(x-L/2),(y-L/2),c,d,nd);
    d=nd; f[y][x]^=1; x+=DX[d]; y+=DY[d];
  }
}
