// ./sect RULE T : по четырём секторам (В,С,З,Ю; глубина > 20) — частоты пар соседей по x и по y: 00,01,10,11
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
 double hx[4][4]={{0}},hy[4][4]={{0}},n[4]={0}; int cx=(x0+x1)/2,cy=(y0+y1)/2;
 for(int j=y0+20;j<y1-20;j++)for(int i=x0+20;i<x1-20;i++){int dx=i-cx,dy=j-cy,S;
  if(abs(dx)<30&&abs(dy)<30)continue;
  if(dx>abs(dy))S=0;else if(-dy>abs(dx))S=1;else if(-dx>abs(dy))S=2;else if(dy>abs(dx))S=3;else continue;
  int v=g[(long)j*N+i],vx=g[(long)j*N+i+1],vy=g[(long)(j+1)*N+i]; hx[S][v*2+vx]++; hy[S][v*2+vy]++; n[S]++;}
 const char*nm="ENWS"; for(int S=0;S<4;S++){printf("%c x:",nm[S]);for(int k=0;k<4;k++)printf(" %.4f",hx[S][k]/n[S]);printf("  y:");for(int k=0;k<4;k++)printf(" %.4f",hy[S][k]/n[S]);printf("\n");}}
