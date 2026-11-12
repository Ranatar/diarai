// ./pat3 RULE T : частоты узоров 3×3 (+чётность клетки) в кольцах u=0-.2,.2-.4,.4-.6,.6-.8 (u — чебышёвское расстояние/R)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static double h[4][1024]; double n[4];
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0;
 for(int j=y0+1;j<y1;j++)for(int i=x0+1;i<x1;i++){double u=(abs(i-cx)>abs(j-cy)?abs(i-cx):abs(j-cy))/R;int b=(int)(u*5);if(b>3)continue;
  int p=0;for(int dy=-1;dy<=1;dy++)for(int dx=-1;dx<=1;dx++)p=p*2+g[(long)(j+dy)*N+i+dx];p=p*2+((i+j)&1);h[b][p]++;n[b]++;}
 for(int p=0;p<1024;p++){double f[4];int z=0;for(int b=0;b<4;b++){f[b]=h[b][p]/n[b];if(h[b][p]<50)z=1;}if(z)continue;
  printf("%4d %.5f %.5f %.5f %.5f %.3f\n",p,f[0],f[1],f[2],f[3],f[0]/f[3]);}}
