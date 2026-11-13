/* события роста: t, сторона (L/R), x0,x1 ; ./ev D0 N */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 8192
unsigned char f[3][L];
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long N=atoll(argv[2]);
  int To[2]={6,7},Ts[2]={6,2}; int x=L/2,y=0,d=d0; int x0=x,x1=x;
  for(long long t=0;t<N;t++){
    if(y>0||y<-2){printf("off y %d\n",y);return 1;}
    if(x<x0){x0=x;printf("%lld L %d %d\n",t,x0-L/2,x1-L/2);} if(x>x1){x1=x;printf("%lld R %d %d\n",t,x0-L/2,x1-L/2);}
    unsigned char*c=&f[-y][x]; int cc=*c; d=(d+((x&1)?Ts[cc]:To[cc]))&7; *c^=1; x+=DX[d]; y+=DY[d];
    if(x<4||x>L-4)return 0;
  }
}
