/* ./vev CODE D0 LOG2N NFROM : события — касание левого (l) / правого (r) края и прирост (R/L), с временем, начиная с n>=NFROM */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),lg=atoi(argv[3]),nf=atoi(argv[4]),L=8192;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,mx=x,Mx=x,px;
  for(long long t=1;t<=(1LL<<lg);t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; px=x; x+=DX[d]; y+=DY[d];
    int on=(Mx-L/2)>=nf;
    if(x>Mx){Mx=x; if(on)printf("R %lld\n",t);} else if(x<mx){mx=x; if(on)printf("L %lld\n",t);}
    else if(on){ if(x>=Mx-1&&px<Mx-1)printf("r %lld\n",t); if(x<=mx+1&&px>mx+1)printf("l %lld\n",t);} 
    if((Mx-L/2)>=nf+8)break; }
}
