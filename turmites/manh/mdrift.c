/* ./mdrift CODE LOG2T0 LOG2T1 LAG — дрейф в толще (0.1<r/R<0.5) для муравья на разметке; tang>0 — по часовой (экран) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int code=atoi(argv[1]); long long T0=1LL<<atoi(argv[2]),T1=1LL<<atoi(argv[3]); int lag=atoi(argv[4]),L=4096;
  int W[4],T[4]; for(int e=0;e<4;e++){int v=(code>>(3*e))&7;W[e]=v>>2;T[e]=v&3;}
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,d=0,tau=0,minx=x,maxx=x,miny=y,maxy=y,px=x,py=y; double cx=x,cy=y,R=1,sr=0,st=0,n=0;
  for(long long t=1;t<T1;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; int e=2*tau+c; if(W[e]!=c)f[i]^=1;
    d=(d+T[e])&3; int nx=x+DX[d],ny=y+DY[d]; if(d&1) tau=(nx<x?nx:x)&1; else tau=((ny<y?ny:y)+1)&1; x=nx;y=ny;
    if(x<1||y<1||x>=L-1||y>=L-1){printf("%d край\n",code);return 0;}
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
    if(t==T0){cx=(minx+maxx)/2.0;cy=(miny+maxy)/2.0;R=(maxx-minx+maxy-miny)/4.0;px=x;py=y;}
    if(t>T0&&(t-T0)%lag==0){double rx=px-cx,ry=py-cy,r=sqrt(rx*rx+ry*ry); if(r>0.1*R&&r<0.5*R){double dx=x-px,dy=y-py; sr+=(dx*rx+dy*ry)/r; st+=(-dx*ry+dy*rx)/r; n++;} px=x;py=y;}
  }
  printf("%d R=%.0f rad %+.5f tang %+.5f\n",code,R,sr/n/lag,st/n/lag);
}
