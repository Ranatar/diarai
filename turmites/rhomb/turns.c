// События поворота направо (s1 на белом) у 2845: t, x, y, новое направление; и между ними — сколько клеток прибавилось.
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
  int x=N/2,y=N/2,d=0,s=0; long ones=0,lastones=0,lastt=0;
  int minx=x,maxx=x,miny=y,maxy=y;
  for(long t=0;;t++){
    uint8_t*c=&g[(long)y*N+x]; int col=*c; int e=s*2+col;
    if(e==2 && t>=T0){ printf("ones=%ld %ld %d %d %c dt=%ld dones=%ld box x[%d,%d] y[%d,%d]\n",ones,t,x-N/2,y-N/2,"NESW"[(d+1)&3],t-lastt,ones-lastones,minx-N/2,maxx-N/2,miny-N/2,maxy-N/2); lastt=t; lastones=ones; if(--cnt<=0) return 0;}
    ones+=wc[e]-col; *c=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
  }
}
