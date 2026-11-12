// ./sw RULE MAXLOG : моменты роста рамки (x1-x0) для подметальщика; печатает t, ширина, высота
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]),M=atoi(a[2]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y,w=0,h=0;
 for(long t=1;t<=(1L<<M);t++){uint8_t*q=&g[(long)y*N+x];
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<1||x>=N-1||y<1||y>=N-1){printf("E %ld\n",t);break;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
  if(x1-x0!=w||y1-y0!=h){w=x1-x0;h=y1-y0;printf("%ld %d %d %d %d\n",t,w,h,x-N/2,y-N/2);}}
}
