/* Профиль по r/R: плотность посещений (на узел кольца) и msd за LAG. ./cprof RULE TAU0 LOG2T0 LOG2T1 LAG */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]); long long T0=1LL<<atoi(argv[3]),T1=1LL<<atoi(argv[4]); int lag=atoi(argv[5]);
  int L=4096,W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int X=L/2,Y=L/2,k=0,sig=1;
  int minx=X,maxx=X,miny=Y,maxy=Y; double cx=X,cy=Y,Rad=1;
  double cnt[12]={0},msd[12]={0},nm[12]={0},area[12]={0}; int px=X,py=Y;
  for(long long t=1;t<T1;t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; f[(size_t)Y*L+X]|=16; if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1;}
    if(t==T0){cx=(minx+maxx)/2.0;cy=(miny+maxy)/2.0;Rad=(maxx-minx+maxy-miny)/4.0;px=X;py=Y;}
    if(t>T0){ double r=hypot(X-cx,Y-cy)/Rad; int b=(int)(r*10); if(b<12) cnt[b]++;
      if((t-T0)%lag==0){ double r0=hypot(px-cx,py-cy)/Rad; int b0=(int)(r0*10); if(b0<12){msd[b0]+=(double)(X-px)*(X-px)+(double)(Y-py)*(Y-py); nm[b0]++;} px=X;py=Y; } }
  }
  for(int x=0;x<L;x++)for(int y=0;y<L;y++) if(f[(size_t)y*L+x]&16){double r=hypot(x-cx,y-cy)/Rad;int b=(int)(r*10); if(b<12) area[b]++;}
  double tot=0,ta=0; for(int b=0;b<12;b++){tot+=cnt[b];ta+=area[b];}
  printf("%s R=%.0f\n r/R   плотн(отн)  msd/LAG   плотн*msd\n",R,Rad);
  for(int b=0;b<10;b++) if(area[b]>0&&nm[b]>0){ double rho=(cnt[b]/tot)/(area[b]/ta); double D=msd[b]/nm[b]/lag; printf(" %.1f   %6.2f     %.4f    %.3f\n",b/10.0,rho,D,rho*D);}
}
