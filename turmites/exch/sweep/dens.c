// ./dens RULE T0 T1 : доля времени в квадратах k×k у углов рамки (отн. равномерного), и в полосе ширины k у сторон
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int K[6]={2,4,8,16,32,64};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; double cc[6]={0},ce[6]={0},uc[6]={0},ue[6]={0};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){int dx=x-x0<x1-x?x-x0:x1-x, dy=y-y0<y1-y?y-y0:y1-y; double A=(double)(x1-x0+1)*(y1-y0+1), P=2.0*(x1-x0+1+y1-y0+1);
   for(int i=0;i<6;i++){ if(dx<K[i]&&dy<K[i])cc[i]++; uc[i]+=4.0*K[i]*K[i]/A; int m=dx<dy?dx:dy; if(m<K[i])ce[i]++; ue[i]+=P*K[i]/A;}}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 printf("L %d\n",x1-x0);for(int i=0;i<6;i++)printf("k %d corner %.3f edge %.3f\n",K[i],cc[i]/uc[i],ce[i]/ue[i]);
}
