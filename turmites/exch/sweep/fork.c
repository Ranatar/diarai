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
 double sr[4]={0},st[4]={0};long n[4]={0};
 for(long t=0;t<T1;t++){
  if(t>=T0&&t%EV==0){double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0,u=fmax(fabs(x-cx),fabs(y-cy))/R;
   if(u>0.1&&u<0.6)for(int k=0;k<4;k++){int X=x,Y=y,D=d,S=s,m=0; if(k==1)D=rand()&3; if(k==2)S^=1; if(k==3)D=(D+2)&3;
    for(int i=0;i<LAG;i++){long p=(long)Y*N+X;chg[m]=p;old[m]=g[p];m++;int e=S*2+(g[p]&1);g[p]=wc[e];D=(D+tn[e])&3;S=ns[e];X+=DX[D];Y+=DY[D];}
    for(int i=m-1;i>=0;i--)g[chg[i]]=old[i];
    double ex=x-cx,ey=y-cy,rr=hypot(ex,ey),ddx=X-x,ddy=Y-y; if(rr<1)continue; sr[k]+=(ddx*ex+ddy*ey)/rr; st[k]+=(ex*ddy-ey*ddx)/rr; n[k]++;}}
  uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 const char*nm[4]={"копия","случ.направл.","сост.наоборот","направл.наоборот"};
 for(int k=0;k<4;k++)printf("%-18s rad/шаг %+.5f tang/шаг %+.5f n %ld\n",nm[k],sr[k]/n[k]/LAG,st[k]/n[k]/LAG,n[k]);}
