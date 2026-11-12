/* Площадь Леви в крупной модели: ./clevy RULE TAU0 LOG2T0 LOG2T1 LAG
   на отрезках по LAG шагов окна: A = 1/2 Σ (Δx dy − Δy dx) от начала отрезка (экран, y вниз: A>0 — по часовой).
   Печатает <A>/LAG, msd/LAG и безразмерное <A>/msd. Только узловые ходы (съезды). */
#include <stdio.h>
#include <stdlib.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]); long long T0=1LL<<atoi(argv[3]),T1=1LL<<atoi(argv[4]); int lag=atoi(argv[5]);
  int L=4096,W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); if(getenv("BG")) for(size_t i=0;i<(size_t)L*L;i++) f[i]=15;
  int X=L/2,Y=L/2,k=0,sig=1; long long sx=0,sy=0; double A=0,SA=0,SM=0; long long nseg=0;
  for(long long t=1;t<T1;t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){int dx=DX[k],dy=DY[k]; X+=dx;Y+=dy;k=(k+2)&3;tau=0; if(X<1||Y<1||X>=L-1||Y>=L-1){printf("край\n");return 0;}
      if(t>=T0){ A+=0.5*(sx*dy-sy*dx); sx+=dx; sy+=dy; } }
    else{k=(k+sig)&3;tau=1;}
    if(t>=T0 && (t-T0)%lag==lag-1){ SA+=A; SM+=(double)sx*sx+(double)sy*sy; nseg++; A=0;sx=0;sy=0; }
  }
  printf("%s τ0=%d%s lag %d  <A>/шаг %+.5f  msd/шаг %.4f  <A>/msd %+.4f\n",R,atoi(argv[2]),getenv("BG")?" BG":"",lag,SA/nseg/lag,SM/nseg/lag,SA/SM);
}
