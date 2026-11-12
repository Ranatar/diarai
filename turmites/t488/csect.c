/* Дрифт в крупной модели: ./cdrift RULE TAU0 LOG2T0 LOG2T1 LAG
   окно [2^T0, 2^T1): каждые LAG шагов смещение узла за LAG; радиальная и круговая (по часовой на экране, y вниз) части
   относительно центра посещённых узлов, в толще 0.1<r/R<0.5; плюс доля обходов кругов по часовой (σ=+1). */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]); int a0=atoi(argv[3]),a1=atoi(argv[4]),lag=atoi(argv[5]);
  int L=4096,W[2][2],Ex[2][2];
  for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1);
  int X=L/2,Y=L/2,k=0,sig=1; long long T0=1LL<<a0,T1=1LL<<a1;
  int minx=X,maxx=X,miny=Y,maxy=Y; long long cwsteps=0,sqsteps=0;
  double sr=0,st=0,n=0,vx[8]={0},vy[8]={0},vn[8]={0}; int px=X,py=Y;
  double cx=X,cy=Y,Rad=1;
  for(long long t=1;t<T1;t++){
    unsigned char*p=&f[(size_t)Y*L+X];
    int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c];
    if(w!=c)*p^=1<<k;
    int oct=0;
    if(tau==0){ if(e==0) oct=1; else sig=(e==1)?1:-1; }
    else { if(e==2) oct=1; else if(e==0) sig=-sig; }
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0;
      if(X<1||Y<1||X>=L-1||Y>=L-1){printf("край\n");return 0;}
      if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1; if(t>=T0){sqsteps++; if(sig>0)cwsteps++;}}
    if(t==T0){cx=(minx+maxx)/2.0;cy=(miny+maxy)/2.0;Rad=(maxx-minx+maxy-miny)/4.0;px=X;py=Y;}
    if(t>T0 && (t-T0)%lag==0){
      double rx=px-cx,ry=py-cy,r=sqrt(rx*rx+ry*ry);
      if(r>0.1*Rad && r<0.5*Rad){ double dx=X-px,dy=Y-py; sr+=(dx*rx+dy*ry)/r; st+=(-dx*ry+dy*rx)/r; n++; {double a=atan2(ry,rx); int sct=((int)floor((a+M_PI)/(M_PI/4)+0.5))%8; vx[sct]+=dx;vy[sct]+=dy;vn[sct]++;} }
      px=X;py=Y;
    }
  }
  for(int q=0;q<8;q++) printf("  сектор %3.0f°: v=(%+.5f,%+.5f) угол v %4.0f°\n",-180+45.0*q,vx[q]/vn[q]/lag,vy[q]/vn[q]/lag,atan2(vy[q],vx[q])*180/M_PI);
  printf("%s τ0=%d R=%.0f rad %+.5f tang %+.5f (на шаг; tang>0 = по часовой на экране)  круги по часовой %.3f\n",
    R,atoi(argv[2]),Rad,sr/n/lag,st/n/lag,(double)cwsteps/(sqsteps?sqsteps:1));
}
