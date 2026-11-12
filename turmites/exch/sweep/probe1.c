// ./probe1 RULE T NPROBE : на шаге T из места муравья — пробник с перевёрнутым состоянием; печать позиции каждые 256 шагов до 8192
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
 printf("bbox %d..%d %d..%d  ant %d %d\n",x0-N/2,x1-N/2,y0-N/2,y1-N/2,x-N/2,y-N/2);
 s^=1; char tr[80];int tp=0;
 for(int t=1;t<=8192;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(t>8192-40)tr[tp++]="NRUL"[tn[e]];
  if(t%512==0)printf("%d:(%d,%d) ",t,x-N/2,y-N/2);}
 tr[tp]=0;printf("\nпоследние повороты %s\n",tr);}
