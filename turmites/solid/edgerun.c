// Детектор «обходчиков»: ./edgerun T0 DT < rules  — для каждого правила прогон до T0, затем окно DT:
// «у края» = в квадрате 7×7 вокруг муравья есть ни разу не посещённая клетка. Пока муравей у края (разрешены отлучки до G=64 шагов),
// копим угол вокруг центра рамки; печать: правило, макс. |накопленный угол|/2π за один заход, доля шагов у края, w, h.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define N 4096
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){ long T0=atol(a[1]),DT=atol(a[2]); int rule;
 while(scanf("%d",&rule)==1){ memset(g,0,sizeof g); int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0,mnx=x,mxx=x,mny=y,mxy=y; int out=0;
  for(long t=0;t<T0;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e]|2;d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
   if(x<8||y<8||x>=N-8||y>=N-8){out=1;break;} if(x<mnx)mnx=x;if(x>mxx)mxx=x;if(y<mny)mny=y;if(y>mxy)mxy=y;}
  if(out){printf("%d out\n",rule);fflush(stdout);continue;}
  double cx=(mnx+mxx)/2.0, cy=(mny+mxy)/2.0, acc=0, best=0, pa=atan2(y-cy,x-cx); long gap=1000, edge=0;
  for(long t=0;t<DT;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e]|2;d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
   if(x<8||y<8||x>=N-8||y>=N-8){out=1;break;}
   int ne=0; for(int j=-3;j<=3&&!ne;j++)for(int i=-3;i<=3;i++) if(!(g[(long)(y+j)*N+x+i]&2)){ne=1;break;}
   double an=atan2(y-cy,x-cx), da=an-pa; if(da>M_PI)da-=2*M_PI; if(da<-M_PI)da+=2*M_PI; pa=an;
   if(ne){ edge++; if(gap>64) acc=0; gap=0; acc+=da; if(fabs(acc)>best) best=fabs(acc); }
   else { gap++; if(gap<=64) acc+=da; } }
  printf("%d %.2f %.3f %d %d%s\n",rule,best/(2*M_PI),(double)edge/DT,mxx-mnx+1,mxy-mny+1,out?" out":""); fflush(stdout); } }
