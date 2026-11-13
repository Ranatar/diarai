/* ./vsweep CODE D0 LOG2N : между приростами правого края — сколько раз муравей доходил до крайнего правого столбца
   (входов в него) и до крайнего левого */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),lg=atoi(argv[3]),L=8192;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,mx=x,Mx=x,px=x; long long nr=0,nl=0;
  for(long long t=1;t<=(1LL<<lg);t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; px=x; x+=DX[d]; y+=DY[d];
    if(x<mx)mx=x; if(x>Mx){Mx=x;printf("%d %lld %lld %lld\n",Mx-L/2,t,nr,nl);nr=nl=0;}
    else { if(x>=Mx-1&&px<Mx-1)nr++; if(x<=mx+1&&px>mx+1)nl++; } }
}
