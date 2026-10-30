// ./layers RULE T1 T2: моменты роста рамки (w) в [T1,T2): печать t w и промежутков
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int rule=atoi(a[1]);long T1=atol(a[2]),T2=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,mnx=x,mxx=x,mny=y,mxy=y; long last=-1,n=0; double sg=0;
 for(long t=0;t<T2;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+*q;*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  int gr=0; if(x<mnx){mnx=x;gr=1;} if(x>mxx){mxx=x;gr=1;} if(y<mny){mny=y;gr=1;} if(y>mxy){mxy=y;gr=1;}
  if(gr && t>=T1){ if(last>=0){ long dt=t-last; if(n<12||dt>100000) printf("t=%ld w=%d h=%d dt=%ld\n",t,mxx-mnx+1,mxy-mny+1,dt); n++; sg+=dt;} last=t; } }
 printf("events %ld mean dt %.0f\n",n,n?sg/n:0); }
