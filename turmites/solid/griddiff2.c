// ./griddiff2 R1 R2 STEPS SX SY — различия поля1(x,y) и поля2(x+SX,y+SY) после STEPS шагов
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[2][N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r[2]={atoi(a[1]),atoi(a[2])};long T=atol(a[3]);int sx=atoi(a[4]),sy=atoi(a[5]);int wc[2][4],tn[2][4],ns[2][4];
 for(int k=0;k<2;k++)for(int e=0;e<4;e++){int b=(r[k]>>(4*e))&15;wc[k][e]=b&1;tn[k][e]=(b>>1)&3;ns[k][e]=(b>>3)&1;}
 for(int k=0;k<2;k++){int x=N/2,y=N/2,d=0,s=0; for(long t=0;t<T;t++){uint8_t*q=&g[k][(long)y*N+x];int e=s*2+*q;*q=wc[k][e];d=(d+tn[k][e])&3;s=ns[k][e];x+=DX[d];y+=DY[d];}}
 long df=0,o=0; for(int y=2;y<N-2;y++)for(int x=2;x<N-2;x++){ if(g[0][(long)y*N+x]!=g[1][(long)(y+sy)*N+x+sx]) df++; o+=g[0][(long)y*N+x]; }
 printf("сдвиг (%d,%d): различий %ld из %ld единиц\n",sx,sy,df,o);}
