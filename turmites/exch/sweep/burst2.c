// ./burst2 RULE T0 T1 : каждая вспышка новых клеток: начало (t, место отн. рамки, напр., сост.), конец, размер
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; long last=-1000,bs=0,bt0=0; int lx=0,ly=0;
 char tr[64]; int tp=0;
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(!(*q&2)){*q|=2; if(t>=T0){ if(t-last>50){ if(bs)printf(" end (%d,%d) size %ld dur %ld\n",lx-N/2,ly-N/2,bs,last-bt0);
      printf("t %ld gap %ld L %d at (%d,%d) rel x0+%d x1-%d y0+%d y1-%d d %d s %d prev ",t,t-last,x1-x0,x-N/2,y-N/2,x-x0,x1-x,y-y0,y1-y,d,s);
      for(int k=0;k<32;k++)putchar(tr[(tp+k)&31]); bs=0;bt0=t;} bs++; last=t; lx=x;ly=y;}}
  int e=s*2+(*q&1);*q=(*q&2)|wc[e];tr[tp]="NRUL"[tn[e]]; tp=(tp+1)&31; d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 printf("\n");
}
