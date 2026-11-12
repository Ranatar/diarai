// ./runs RULE T0 T1 W : распределение |сдвига| за окно W (гистограмма по 2^k), и где начинаются большие сдвиги (> L/4)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int W=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y,sx=0,sy=0; long h[20]={0}; int nb=0;
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0 && (t-T0)%W==0){ if(t>T0){double dd=hypot(x-sx,y-sy);int k=0;while((1<<(k+1))<=dd)k++;h[k]++;
     if(dd>(x1-x0)/4.0&&nb<15){nb++;printf("big %.0f from (%d,%d) to (%d,%d) L %d\n",dd,sx-N/2,sy-N/2,x-N/2,y-N/2,x1-x0);}}
    sx=x;sy=y;}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 for(int k=0;k<20;k++)if(h[k])printf("|d| 2^%d: %ld\n",k,h[k]);}
