/* Будущее и прошлое смещение: ./cfb RULE TAU0 LOG2T0 LOG2T1 LAG — по отсчётам каждые LAG шагов в окне:
   вперёд x(i+1)-x(i), назад x(i-1)-x(i), радиальная/круговая части (толща 0.1<r/R<0.5, центр и R — на начало окна) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]); long long T0=1LL<<atoi(argv[3]),T1=1LL<<atoi(argv[4]); int lag=atoi(argv[5]);
  int L=4096,W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int X=L/2,Y=L/2,k=0,sig=1;
  int minx=X,maxx=X,miny=Y,maxy=Y; long long ns=(T1-T0)/lag+2; int*px=malloc(ns*4),*py=malloc(ns*4); long long n=0;
  for(long long t=1;t<T1;t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1;}
    if(t>=T0 && (t-T0)%lag==0){px[n]=X;py[n]=Y;n++;}
  }
  double cx=(minx+maxx)/2.0,cy=(miny+maxy)/2.0,Rad=(maxx-minx+maxy-miny)/4.0;
  double fr=0,ft=0,br=0,bt=0; long long m=0;
  for(long long i=1;i+1<n;i++){
    double rx=px[i]-cx,ry=py[i]-cy,r=sqrt(rx*rx+ry*ry); if(r<0.1*Rad||r>0.5*Rad) continue;
    double ux=rx/r,uy=ry/r;
    double fx=px[i+1]-px[i],fy=py[i+1]-py[i],bx=px[i-1]-px[i],by=py[i-1]-py[i];
    fr+=fx*ux+fy*uy; ft+=-fx*uy+fy*ux; br+=bx*ux+by*uy; bt+=-bx*uy+by*ux; m++;
  }
  printf("%s τ0=%d R=%.0f вперёд rad %+.5f tang %+.5f | назад rad %+.5f tang %+.5f (на шаг)\n",R,atoi(argv[2]),Rad,fr/m/lag,ft/m/lag,br/m/lag,bt/m/lag);
}
