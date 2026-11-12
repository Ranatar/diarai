// ./prof RULE T : профиль поля по глубине (доля c=1; доля пар соседей по x с равным цветом)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double n[16]={0},one[16]={0},eqx[16]={0},chk[16]={0};
 for(int j=y0;j<=y1;j++)for(int i=x0;i<=x1;i++){int dx=i-x0<x1-i?i-x0:x1-i,dy=j-y0<y1-j?j-y0:y1-j,m=dx<dy?dx:dy,b=0;while((2<<b)<=m+1)b++;
  int v=g[(long)j*N+i]; n[b]++; one[b]+=v; eqx[b]+=(v==g[(long)j*N+i+1]); chk[b]+=v^((i+j)&1);}
 printf("L %d\n",x1-x0);for(int b=0;b<16;b++)if(n[b])printf("depth %4d+ c1 %.3f eqx %.3f c~ %.3f\n",(1<<b)-1,one[b]/n[b],eqx[b]/n[b],chk[b]/n[b]);}
