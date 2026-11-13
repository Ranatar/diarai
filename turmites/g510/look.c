/* 510: картинка полоски в момент t. ./look D0 N */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 2048
unsigned char f[L][L];
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long N=atoll(argv[2]);
  int To[2]={6,7},Ts[2]={6,2};
  int x=L/2,y=L/2,d=d0; int x0=L,x1=0,y0=L,y1=0;
  for(long long t=0;t<N;t++){
    int c=f[y][x]&1; f[y][x]|=2;
    if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y;
    d=(d+((x&1)?Ts[c]:To[c]))&7; f[y][x]^=1; x+=DX[d]; y+=DY[d];
  }
  printf("bbox x %d..%d y %d..%d ant %d %d d %d\n",x0-L/2,x1-L/2,y0-L/2,y1-L/2,x-L/2,y-L/2,d);
  for(int yy=y1;yy>=y0;yy--){for(int xx=x0;xx<=x1;xx++){int v=f[yy][xx];char ch=' ';
    if(((xx^L/2)&1)!=((yy^L/2)&1)) ch=' '; else if(!(v&2)) ch='.'; else ch=(v&1)?'#':'o';
    if(xx==x&&yy==y)ch='A'; putchar(ch);} putchar('\n');}
}
