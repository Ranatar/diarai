// ./secdrift RULE T0 T1 LAG : средний вектор сдвига за LAG в секторах В,С,З,Ю (треугольники рамки) по глубине (доля от R: 0-.25,.25-.5,.5-.75,.75-.9)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int LAG=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; static int hx[1<<16],hy[1<<16],hk[1<<16];
 double sx[4][4]={{0}},sy[4][4]={{0}}; long n[4][4]={{0}};
 for(long t=0;t<=T1;t++){uint8_t*q=&g[(long)y*N+x];
  if(t>=T0){double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0; double ex=x-cx,ey=y-cy; int S;
   if(ex>=fabs(ey))S=0;else if(-ey>=fabs(ex))S=1;else if(-ex>=fabs(ey))S=2;else S=3;
   double u=fmax(fabs(ex),fabs(ey))/R; int b=u<.25?0:u<.5?1:u<.75?2:u<.9?3:-1;
   int j=t&0xffff; hx[j]=x;hy[j]=y;hk[j]=b<0?-1:S*4+b;
   if(t-T0>=LAG){int i=(t-LAG)&0xffff; if(hk[i]>=0){int SS=hk[i]/4,bb=hk[i]%4; sx[SS][bb]+=x-hx[i]; sy[SS][bb]+=y-hy[i]; n[SS][bb]++;}}}
  int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 const char*nm="ENWS"; printf("L %d (y вниз; vx,vy на шаг ×1e4)\n",x1-x0);
 for(int S=0;S<4;S++){printf("%c:",nm[S]);for(int b=0;b<4;b++)printf("  (%+6.1f,%+6.1f)",1e4*sx[S][b]/n[S][b]/LAG,1e4*sy[S][b]/n[S][b]/LAG);printf("\n");}}
