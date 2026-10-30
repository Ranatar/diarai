// ./onesig < rules — число единиц на 2^12,2^14,...,2^20 (подпись для поиска сдвинутых двойников)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define N 2048
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(){int r; while(scanf("%d",&r)==1){memset(g,0,sizeof g);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0; long o=0,nt=4096; printf("%d",r);
 for(long t=1;t<=(1L<<20);t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+*q;o+=wc[e]-*q;*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<1||x>=N-1||y<1||y>=N-1){printf(" E");break;} if(t==nt){printf(" %ld",o);nt*=4;}}
 printf("\n");}}
