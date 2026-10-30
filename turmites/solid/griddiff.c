// ./griddiff R1 R2 MAXLOG — на 2^k: число клеток, где цвета двух полей различаются, единиц у каждого
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[2][N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r[2]={atoi(a[1]),atoi(a[2])};int ML=atoi(a[3]);int wc[2][4],tn[2][4],ns[2][4];
 for(int k=0;k<2;k++)for(int e=0;e<4;e++){int b=(r[k]>>(4*e))&15;wc[k][e]=b&1;tn[k][e]=(b>>1)&3;ns[k][e]=(b>>3)&1;}
 int x[2]={N/2,N/2},y[2]={N/2,N/2},d[2]={0,0},s[2]={0,0}; long ones[2]={0,0}; long diff=0; long nt=1024;
 for(long t=1;t<=(1L<<ML);t++){
  for(int k=0;k<2;k++){long i=(long)y[k]*N+x[k]; uint8_t*q=&g[k][i]; int e=s[k]*2+*q; int nw=wc[k][e];
   if(nw!=*q){ int other=g[1-k][i]; int before=(*q!=other); *q=nw; int after=(nw!=other); diff+=after-before; ones[k]+=nw?1:-1; }
   d[k]=(d[k]+tn[k][e])&3;s[k]=ns[k][e];x[k]+=DX[d[k]];y[k]+=DY[d[k]];
   if(x[k]<1||x[k]>=N-1||y[k]<1||y[k]>=N-1){printf("край\n");return 0;}}
  if(t==nt){printf("2^%d различий %ld единиц %ld %ld позиции (%d,%d) (%d,%d)\n",__builtin_ctzl(t),diff,ones[0],ones[1],x[0]-N/2,y[0]-N/2,x[1]-N/2,y[1]-N/2);nt*=2;}}}
