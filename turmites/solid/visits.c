// ./visits RULE T0 DT out.pgm : карта посещений муравья в окне [T0, T0+DT): посещённые — черным, остальное тело серым
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[N*N], v[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int rule=atoi(a[1]);long T0=atol(a[2]),DT=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,mnx=x,mxx=x,mny=y,mxy=y; long cnt=0;
 for(long t=0;t<T0+DT;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e]|2;d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(t>=T0){ if(!v[(long)y*N+x]) cnt++; v[(long)y*N+x]=1;}
  if(x<mnx)mnx=x;if(x>mxx)mxx=x;if(y<mny)mny=y;if(y>mxy)mxy=y;}
 FILE*f=fopen(a[4],"wb");fprintf(f,"P5\n%d %d\n255\n",mxx-mnx+1,mxy-mny+1);
 for(int yy=mny;yy<=mxy;yy++)for(int xx=mnx;xx<=mxx;xx++){long i=(long)yy*N+xx;fputc(v[i]?0:(g[i]&2?200:255),f);}
 fclose(f);fprintf(stderr,"distinct visited %ld\n",cnt);}
