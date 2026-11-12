// ./drift RULE T0 T1 LAG : по r/R (R = полуширина рамки, бины 0.1) — плотность (отн. площади кольца в квадрате) и средний радиальный сдвиг за LAG
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int LAG=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; static int hx[1<<16],hy[1<<16],hb[1<<16]; static double hr[1<<16];
 double cnt[12]={0},dt_[12]={0},dr[12]={0},d2[12]={0}; long nd[12]={0};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){double R=(x1-x0+y1-y0)/4.0; double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0;
   double u=fmax(fabs(x-cx),fabs(y-cy))/R; int b=(int)(u*10); if(b>11)b=11; cnt[b]++;
   int j=t&0xffff; hx[j]=x;hy[j]=y;hb[j]=b;
   if(t-T0>=LAG){int i=(t-LAG)&0xffff; double ex=hx[i]-cx,ey=hy[i]-cy,rr=hypot(ex,ey); if(rr>0){double ddx=x-hx[i],ddy=y-hy[i];
     dr[hb[i]]+=(ddx*ex+ddy*ey)/rr; dt_[hb[i]]+=(ex*ddy-ey*ddx)/rr; d2[hb[i]]+=ddx*ddx+ddy*ddy; nd[hb[i]]++;}}}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d]; if(x<2||y<2||x>N-3||y>N-3){printf("%d EDGE %ld\n",r,t);return 0;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double tot=0;for(int b=0;b<12;b++)tot+=cnt[b];
 double R_=0,Tg=0,M=0;long K=0; for(int b=1;b<=5;b++){R_+=dr[b];Tg+=dt_[b];M+=d2[b];K+=nd[b];}
 printf("%d L %d rad %+.5f tang %+.5f msd %.3f dens0 %.2f dens3 %.2f dens7 %.2f\n",r,x1-x0,R_/K/LAG,Tg/K/LAG,M/K/LAG,cnt[0]/tot/0.01,cnt[3]/tot/0.07,cnt[7]/tot/0.15);}
