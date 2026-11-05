// ./exview RULE STEPS OUT.pgm [xor] — поле после STEPS шагов; xor=1 — в шахматной раскраске (c ^ (x+y)&1), кадр по рамке
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[N*N], v[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);int X=c>4?atoi(a[4]):1;
 int wc[4],tn[4],ns[4];for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];v[(long)y*N+x]=1;int e=s*2+*q;*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<1||x>=N-1||y<1||y>=N-1){fprintf(stderr,"край %ld\n",t);break;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 x0-=2;y0-=2;x1+=2;y1+=2; FILE*f=fopen(a[3],"wb"); fprintf(f,"P5 %d %d 255\n",x1-x0+1,y1-y0+1);
 for(int j=y0;j<=y1;j++)for(int i=x0;i<=x1;i++){long k=(long)j*N+i;int col=g[k]^(X?((i+j)&1):0);
  fputc(v[k]?(col?0:255):(col?90:200),f);} fclose(f); fprintf(stderr,"рамка %d x %d\n",x1-x0-3,y1-y0-3);}
