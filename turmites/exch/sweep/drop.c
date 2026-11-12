// ./drop RULE T K LAG : поле на шаге T заморожено; K раз сажаем нового муравья (случайные клетка с 0.2<u<0.7, направление, состояние),
// LAG шагов с откатом изменений; средний радиальный и круговой сдвиг. Сравнение: настоящий муравей (drift2).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static long chg[1<<16];static uint8_t old[1<<16];
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);int K=atoi(a[3]),LAG=atoi(a[4]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0; srand(12345);
 double sr[2][2]={{0}},st[2][2]={{0}};long n[2][2]={{0}};
 for(int k=0;k<K;k++){int X,Y;double u;do{X=x0+rand()%(x1-x0+1);Y=y0+rand()%(y1-y0+1);u=fmax(fabs(X-cx),fabs(Y-cy))/R;}while(u<0.2||u>0.7);
  int D=rand()&3,S=rand()&1,S0=S; int sx=X,sy=Y,m=0;
  for(int t=0;t<LAG;t++){long p=(long)Y*N+X;chg[m]=p;old[m]=g[p];m++;int e=S*2+(g[p]&1);g[p]=wc[e];D=(D+tn[e])&3;S=ns[e];X+=DX[D];Y+=DY[D];}
  for(int i=m-1;i>=0;i--)g[chg[i]]=old[i];
  double ex=sx-cx,ey=sy-cy,rr=hypot(ex,ey),ddx=X-sx,ddy=Y-sy; int b=(u<0.45);
  sr[S0][b]+=(ddx*ex+ddy*ey)/rr; st[S0][b]+=(ex*ddy-ey*ddx)/rr; n[S0][b]++;}
 for(int S0=0;S0<2;S0++)for(int b=0;b<2;b++)printf("s%d %s rad/шаг %+.5f tang/шаг %+.5f n %ld\n",S0,b?"u.2-.45":"u.45-.7",sr[S0][b]/n[S0][b]/LAG,st[S0][b]/n[S0][b]/LAG,n[S0][b]);
}
