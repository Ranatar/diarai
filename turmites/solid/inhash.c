// ./inhash STEPS < rules — хэш последовательности входов (состояние,цвет) первых STEPS шагов (FNV-1a); край поля — хэш до края
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define N 2048
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){long T=atol(a[1]);int r;
 while(scanf("%d",&r)==1){memset(g,0,sizeof g);int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0; uint64_t h=1469598103934665603ULL; long t;
  for(t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+*q;h=(h^(uint64_t)e)*1099511628211ULL;*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
   if(x<1||x>=N-1||y<1||y>=N-1)break;}
  printf("%d %016llx %ld\n",r,(unsigned long long)h,t);}}
