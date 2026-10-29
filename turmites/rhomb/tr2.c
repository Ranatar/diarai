#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int rule=atoi(argv[1]); long T0=atol(argv[2]); long cnt=atol(argv[3]);
  int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0;
  for(long t=0;;t++){
    uint8_t*c=&g[(long)y*N+x]; int col=*c; int e=s*2+col;
    if(t>=T0){ printf("%d,%d s%d%c ",x-N/2,y-N/2,s,"WB"[col]); if(--cnt<=0){printf("\n");return 0;} }
    *c=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
  }
}
