// Доля «полётных» шагов: вход прозрачный (цвет не меняется, прямо, состояние то же).
// ./flightscan MAXLOG < rules : rule ntransp frac@2^(MAXLOG-4) frac@2^(MAXLOG-2) frac@2^MAXLOG ones w h (или esc)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define N 4096
static uint8_t g[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int maxlog=atoi(argv[1]); int rule;
  while(scanf("%d",&rule)==1){
    memset(g,0,sizeof g);
    int wc[4],tn[4],ns[4],tr[4],ntr=0;
    for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;
      tr[e]=(wc[e]==(e&1))&&tn[e]==0&&ns[e]==(e>>1); ntr+=tr[e];}
    printf("%d %d",rule,ntr);
    if(!ntr){printf(" -\n");continue;}
    int x=N/2,y=N/2,d=0,s=0,minx=x,maxx=x,miny=y,maxy=y; long ones=0,t=0; int esc=0;
    for(int k=1;k<=maxlog&&!esc;k++){
      long end=1L<<k, fl=0;
      for(;t<end;t++){
        uint8_t*c=&g[(long)y*N+x]; int col=*c; int e=s*2+col; fl+=tr[e];
        ones+=wc[e]-col; *c=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
        if(x<0||x>=N||y<0||y>=N){esc=1;break;}
        if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
      }
      if(!esc&&(k==maxlog-4||k==maxlog-2||k==maxlog)) printf(" %.3f",(double)fl/(end/2));
    }
    if(esc) printf(" esc@%ld",t); else printf(" %ld %d %d",ones,maxx-minx+1,maxy-miny+1);
    printf("\n"); fflush(stdout);
  }
}
