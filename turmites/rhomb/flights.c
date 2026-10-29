// Полёты 2845: отрезки, пройденные в состоянии 0 по чёрному. По эпохам [2^(k-1),2^k):
// число полётов, средняя длина, доля шагов в полёте, прирост единиц, ширина рамки.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int rule=atoi(argv[1]); int maxlog=atoi(argv[2]);
  int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0,minx=x,maxx=x,miny=y,maxy=y;
  long ones=0,t=0; long nfl=0,flsteps=0,curfl=0; long dirc[4]={0};
  long prevones=0;
  for(int k=1;k<=maxlog;k++){
    long end=1L<<k; nfl=0;flsteps=0; for(int i=0;i<4;i++)dirc[i]=0;
    long maxfl=0;
    for(;t<end;t++){
      uint8_t*c=&g[(long)y*N+x]; int col=*c; int e=s*2+col;
      if(e==1){curfl++;} else if(curfl){nfl++;flsteps+=curfl;if(curfl>maxfl)maxfl=curfl;dirc[d]++;curfl=0;}
      ones+=wc[e]-col; *c=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
      if(x<0||x>=N||y<0||y>=N){printf("escaped\n");return 0;}
      if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
    }
    if(k>=10) printf("2^%d ones=%ld d_ones=%ld w=%d h=%d flights=%ld meanlen=%.1f maxlen=%ld frac=%.3f fl/newcell=%.1f dirs=%ld/%ld/%ld/%ld\n",
      k,ones,ones-prevones,maxx-minx+1,maxy-miny+1,nfl,nfl?(double)flsteps/nfl:0,maxfl,(double)flsteps/(end/2),
      ones>prevones?(double)nfl/(ones-prevones):0,dirc[0],dirc[1],dirc[2],dirc[3]);
    prevones=ones; fflush(stdout);
  }
}
