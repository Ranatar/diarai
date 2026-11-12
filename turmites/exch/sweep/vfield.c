// ./vfield RULE T0 T1 LAG B : средний сдвиг за LAG в клетках BxB сетки, координаты нормированы на текущую рамку; печатает i j vx vy n
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int LAG=atoi(a[4]),B=atoi(a[5]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; static int hx[1<<16],hy[1<<16],hk[1<<16];
 double *sx=calloc(B*B,8),*sy=calloc(B*B,8); long *n=calloc(B*B,8);
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){int i=(int)((double)(x-x0)/(x1-x0+1)*B),j=(int)((double)(y-y0)/(y1-y0+1)*B);
   int k=t&0xffff; hx[k]=x;hy[k]=y;hk[k]=j*B+i;
   if(t-T0>=LAG){int m=(t-LAG)&0xffff; sx[hk[m]]+=x-hx[m]; sy[hk[m]]+=y-hy[m]; n[hk[m]]++;}}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 for(int j=0;j<B;j++)for(int i=0;i<B;i++){int k=j*B+i;printf("%d %d %.6f %.6f %ld\n",i,j,n[k]?sx[k]/n[k]/LAG:0,n[k]?sy[k]/n[k]/LAG:0,n[k]);}}
