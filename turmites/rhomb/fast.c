// Ускоренный 2845: прямой счёт до первого события после T0, дальше хорда за O(n).
// ./fast T0 CHECKPOINTS... : печатает ones, рамку на моментах-контрольках (по событию, где t впервые >= контрольки, и точное t)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef N
#define N 8192
#endif
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
#define G(x,y) g[(long)(y)*N+(x)]
int main(int argc,char**argv){
  long T0=atol(argv[1]); int rule=2845;
  int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0; long ones=0,t=0;
  int minx=x,maxx=x,miny=y,maxy=y;
  // прямой счёт, пока t<T0 или не событие (s1 на белом)
  for(;;t++){
    int col=G(x,y); int e=s*2+col;
    if(t>=T0 && e==2) break;
    ones+=wc[e]-col; G(x,y)=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
  }
  int ci=2; 
  // событие: в (x,y) s1 на белом, направление прихода d
  for(;;){
    while(ci<argc && t>=atol(argv[ci])){ printf("check %s: t=%ld ones=%ld box %d x %d\n",argv[ci],t,ones,maxx-minx+1,maxy-miny+1); ci++; }
    if(ci>=argc) break;
    G(x,y)=1; ones++; d=(d+1)&3;
    int qx=x+DX[d], qy=y+DY[d];
    if(!G(qx,qy)){ x=qx;y=qy;t+=1; }
    else {
      long n=0; int ex=qx,ey=qy;
      while(G(ex,ey)){ ex+=DX[d]; ey+=DY[d]; n++; }
      // ex,ey белая -> чёрная; рамка
      G(ex,ey)=1; // +1, и курсор: клетка k становится белой (-1)
      if(ex<minx)minx=ex;if(ex>maxx)maxx=ex;if(ey<miny)miny=ey;if(ey>maxy)maxy=ey;
      if(ex<=0||ex>=N-1||ey<=0||ey>=N-1){printf("edge\n");return 0;}
      long k=n/2; x=qx+k*DX[d]; y=qy+k*DY[d]; G(x,y)=0;
      if(n&1) d=(d+2)&3;
      t+=1+(n+1)*(n+2)/2-1;
    }
  }
  return 0;
}
