// ./burst RULE T0 T1 : вспышки новых клеток (разрыв <= G=50 шагов) на [T0,T1]: размер, длительность
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0; long last=-1000,bs=0,bt0=0,nnew=0; long hist[40]={0}; long wsum[40]={0};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(!(*q&2)){*q|=2; if(t>=T0){nnew++; if(t-last>50){ if(bs){int k=0;while((1L<<(k+1))<=bs)k++;hist[k]++;wsum[k]+=bs;} bs=0;bt0=t;} bs++; last=t;}}
  int e=s*2+(*q&1);*q=(*q&2)|wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];}
 printf("new %ld in %ld\n",nnew,T1-T0);
 for(int k=0;k<40;k++)if(hist[k])printf("size 2^%d: %ld bursts, %ld cells\n",k,hist[k],wsum[k]);
}
