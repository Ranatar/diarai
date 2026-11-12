// ./swap RULE T K DX0 W NW : до T, затем меняет местами квадраты K×K в центре (0,0) и в (DX0,0); считает посещения квадратов A(центр) и B(DX0,0) окнами по W, NW окон до и после
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int wc[4],tn[4],ns[4],x=N/2,y=N/2,d=0,s=0;
int K,D0;
static inline void step(){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];}
static inline int in(int cx){return abs(x-N/2-cx)<=K/2&&abs(y-N/2)<=K/2;}
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);K=atoi(a[3]);D0=atoi(a[4]);long W=atol(a[5]);int NW=atoi(a[6]);
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 for(long t=0;t<T-NW*W;t++)step();
 for(int w=0;w<NW;w++){long A=0,B=0;for(long t=0;t<W;t++){A+=in(0);B+=in(D0);step();}printf("before A %ld B %ld\n",A,B);}
 if(getenv("NOSWAP")==0)for(int j=-K/2;j<=K/2;j++)for(int i=-K/2;i<=K/2;i++){long p=(long)(N/2+j)*N+N/2+i,q=(long)(N/2+j)*N+N/2+D0+i;uint8_t z=g[p];g[p]=g[q];g[q]=z;}
 // муравей, если стоит в квадрате, остаётся на месте (поле под ним поменялось)
 for(int w=0;w<NW*4;w++){long A=0,B=0;for(long t=0;t<W;t++){A+=in(0);B+=in(D0);step();}printf("after A %ld B %ld\n",A,B);}
}
