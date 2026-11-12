// РОТОРНЫЙ муравей (Эйлеров ходок: ротор +1 по часовой при каждом посещении, случайные начальные; аргумент 1 — зерно). ./drift RULE T0 T1 LAG : по r/R (R = полуширина рамки, бины 0.1) — плотность (отн. площади кольца в квадрате) и средний радиальный сдвиг за LAG
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]); srand(r);long T0=atol(a[2]),T1=atol(a[3]);int LAG=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(long i=0;i<(long)N*N;i++)g[i]=rand()&3;
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; static int hx[1<<16],hy[1<<16],hb[1<<16]; static double hr[1<<16];
 double cnt[12]={0},dt_[12]={0},dr[12]={0},d2[12]={0}; long nd[12]={0};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){double R=(x1-x0+y1-y0)/4.0; double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0;
   double u=fmax(fabs(x-cx),fabs(y-cy))/R; int b=(int)(u*10); if(b>11)b=11; cnt[b]++;
   int j=t&0xffff; hx[j]=x;hy[j]=y;hb[j]=b;
   if(t-T0>=LAG){int i=(t-LAG)&0xffff; double ex=hx[i]-cx,ey=hy[i]-cy,rr=hypot(ex,ey); if(rr>0){double ddx=x-hx[i],ddy=y-hy[i];
     dr[hb[i]]+=(ddx*ex+ddy*ey)/rr; dt_[hb[i]]+=(ex*ddy-ey*ddx)/rr; d2[hb[i]]+=ddx*ddx+ddy*ddy; nd[hb[i]]++;}}}
  *q=(*q+1)&3;d=*q;x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double tot=0;for(int b=0;b<12;b++)tot+=cnt[b];
 printf("L %d lag %d\n",x1-x0,LAG);
 for(int b=0;b<11;b++){double area=((b+1)*(b+1)-b*b)/100.0; if(b==10)area=0.21;
  printf("u %.1f dens %.3f drift/lag %+.5f tang/lag %+.5f msd/lag %.3f  n %ld\n",b/10.0,cnt[b]/tot/area,nd[b]?dr[b]/nd[b]/LAG:0,nd[b]?dt_[b]/nd[b]/LAG:0,nd[b]?d2[b]/nd[b]/LAG:0,nd[b]);}}
