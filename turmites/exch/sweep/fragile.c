// ./fork RULE T0 T1 EVERY LAG : настоящий муравей; каждые EVERY шагов — пробники из его места на LAG шагов с откатом:
// 0 — точная копия (контроль), 1 — случайное направление, 2 — состояние наоборот, 3 — направление наоборот. Радиальный/круговой сдвиг.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static long chg[1<<16];static uint8_t old[1<<16];
int wc[4],tn[4],ns[4];
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int EV=atoi(a[4]),LAG=atoi(a[5]);
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y; srand(7);
 double m2[4]={0}; double sr[4][4]={{0}},st[4][4]={{0}};long n[4]={0}; int CP[5]={0,64,256,1024,4096};
 for(long t=0;t<T1;t++){
  if(t>=T0&&t%EV==0){double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0,u=fmax(fabs(x-cx),fabs(y-cy))/R;
   if(u>0.1&&u<0.6)for(int k=0;k<4;k++){int X=x,Y=y,D=d,S=s,m=0; if(k==1)D=rand()&3; if(k==2)S^=1; if(k==3)D=(D+2)&3;
    int px[5],py[5];px[0]=X;py[0]=Y;int ci=1;
    for(int i=0;i<4096;i++){long p=(long)Y*N+X;chg[m]=p;old[m]=g[p];m++;int e=S*2+(g[p]&1);g[p]=wc[e];D=(D+tn[e])&3;S=ns[e];X+=DX[D];Y+=DY[D]; if(X<2||Y<2||X>N-3||Y>N-3){printf("%d EDGE\n",r);return 0;} if(i+1==CP[ci]){px[ci]=X;py[ci]=Y;ci++;}}
    for(int i=m-1;i>=0;i--)g[chg[i]]=old[i];
    double ex=x-cx,ey=y-cy,rr=hypot(ex,ey); if(rr<1)continue; for(int w=0;w<4;w++){double ddx=px[w+1]-px[w],ddy=py[w+1]-py[w]; sr[k][w]+=(ddx*ex+ddy*ey)/rr/(CP[w+1]-CP[w]); st[k][w]+=(ex*ddy-ey*ddx)/rr/(CP[w+1]-CP[w]);} {double ddx=px[4]-px[3],ddy=py[4]-py[3]; m2[k]+=ddx*ddx+ddy*ddy;} n[k]++;}}
  uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d]; if(x<2||y<2||x>N-3||y>N-3){printf("%d EDGE\n",r);return 0;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 printf("%d %ld msd_copy %.2f msd_rand %.2f msd_flip %.2f msd_rev %.2f\n",r,n[0],m2[0]/n[0]/3072,m2[1]/n[1]/3072,m2[2]/n[2]/3072,m2[3]/n[3]/3072);}
