#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 4096
unsigned char f[L][L];
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long N=atoll(argv[2]);
  int To[2]={6,7},Ts[2]={6,2}; int x=L/2,y=L/2,d=d0; int Y=L/2;
  long long sq=0,bad=0,badcols=0; int maxbad=0; long long hist[8]={0};
  for(long long t=0;t<N;t++){
    if(x&1){ sq++; int nb=0; for(int xx=L/2-300;xx<L/2+300;xx+=2) if((f[Y][xx]&1)!=(f[Y-2][xx]&1)) nb++;
      if(nb){bad++;badcols+=nb;} if(nb>maxbad)maxbad=nb; if(nb<8)hist[nb]++; if(y!=Y-1)printf("square off row %d\n",y-Y);}
    int c=f[y][x]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[y][x]^=1; x+=DX[d]; y+=DY[d];
  }
  printf("square visits %lld, with T!=B %lld, max %d; hist",sq,bad,maxbad); for(int i=0;i<8;i++)printf(" %lld",hist[i]); printf("\n");
}
