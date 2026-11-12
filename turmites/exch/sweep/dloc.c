// ./dloc RULE T0 T1 LAG : по глубине (расст. до ближайшей стороны рамки, бины 2^i) — доля времени/ожидаемая и msd за LAG шагов
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int LAG=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; static int hx[1<<16],hy[1<<16],hb[1<<16];
 double cnt[16]={0},exp_[16]={0},m2[16]={0}; long nm[16]={0}; int lw=0,lh=0; double ce[16]={0};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){int dx=x-x0<x1-x?x-x0:x1-x, dy=y-y0<y1-y?y-y0:y1-y; int m=dx<dy?dx:dy; int b=0; while((2<<b)<=m+1)b++;
   cnt[b]++; int W=x1-x0+1,H=y1-y0+1; double A=(double)W*H;
   if(W!=lw||H!=lh){lw=W;lh=H;for(int i=0;i<16;i++){int lo=(1<<i)-1,hi=(2<<i)-1;
     double in=0; for(int k=lo;k<hi&&2*k<W&&2*k<H;k++) in+=2.0*(W-2*k)+2.0*(H-2*k)-4; ce[i]=in/A;}}
   for(int i=0;i<16;i++)exp_[i]+=ce[i];
   int j=t&0xffff; hx[j]=x;hy[j]=y;hb[j]=b; if(t-T0>=LAG){int i=(t-LAG)&0xffff; double ddx=x-hx[i],ddy=y-hy[i]; m2[hb[i]]+=ddx*ddx+ddy*ddy; nm[hb[i]]++;}}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 printf("L %d lag %d\n",x1-x0,LAG);for(int i=0;i<16;i++)if(exp_[i]>0)printf("depth %4d-%4d dens %.3f msd/lag %.3f\n",(1<<i)-1,(2<<i)-2,cnt[i]/exp_[i],nm[i]?m2[i]/nm[i]/LAG:0);
}
