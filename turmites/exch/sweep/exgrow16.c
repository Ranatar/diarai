// ./exgrow MAXLOG < rules — площадь посещённого и рамка на 2^10..2^MAXLOG; строка на правило
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define N 16384
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int M=atoi(a[1]),r;
 while(scanf("%d",&r)==1){memset(g,0,sizeof g);int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; long A=0,nt=1024; printf("%d",r);
  for(long t=1;t<=(1L<<M);t++){uint8_t*q=&g[(long)y*N+x];if(!(*q&2)){*q|=2;A++;}
   int e=s*2+(*q&1);*q=(*q&2)|wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
   if(x<1||x>=N-1||y<1||y>=N-1){printf(" E%ld",t);break;}
   if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
   if(t==nt){printf(" %ld:%d",A,(x1-x0+y1-y0+2)/2);nt*=4;}}
  printf("\n");fflush(stdout);}}
