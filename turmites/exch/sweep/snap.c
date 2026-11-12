// ./snap RULE T W OUT : поле на шаге T (бит 0) и посещения за последние W шагов; пишет OUT.pgm (поле) и OUT_v.pgm (лог посещений), рамка
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N]; static uint32_t v[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]),W=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=1;t<=T;t++){uint8_t*q=&g[(long)y*N+x]; if(t>T-W)v[(long)y*N+x]++;
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 char fn[256];int w=x1-x0+1,h=y1-y0+1;uint32_t mx=1;
 for(int j=y0;j<=y1;j++)for(int i=x0;i<=x1;i++)if(v[(long)j*N+i]>mx)mx=v[(long)j*N+i];
 sprintf(fn,"%s.pgm",a[4]);FILE*f=fopen(fn,"wb");fprintf(f,"P5 %d %d 255\n",w,h);
 for(int j=y0;j<=y1;j++)for(int i=x0;i<=x1;i++)fputc(g[(long)j*N+i]?0:255,f);fclose(f);
 sprintf(fn,"%s_v.pgm",a[4]);f=fopen(fn,"wb");fprintf(f,"P5 %d %d 255\n",w,h);
 for(int j=y0;j<=y1;j++)for(int i=x0;i<=x1;i++){uint32_t z=v[(long)j*N+i];fputc(z?255-(int)(220*log(1+z)/log(1+mx)):255,f);}fclose(f);
 printf("bbox %d %d %d %d ant %d %d max visits %u\n",x0-N/2,x1-N/2,y0-N/2,y1-N/2,x-N/2,y-N/2,mx);}
