/* ./vin CODE D0 NSTART : внутренняя фаза после прироста до n=NSTART: «развороты» — локальные экстремумы x
   на пробегах длиннее 6 (удвоенных) клеток; печатает x разворота относительно левого края и время */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),ns=atoi(argv[3]),L=8192;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,mx=x,Mx=x; int phase=0; long long t0=0;
  int ext=x,dir=0; long long text=0;
  for(long long t=1;;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; x+=DX[d]; y+=DY[d];
    if(x>Mx){Mx=x; if(phase==1){printf("конец фазы t=%lld\n",t-t0);return 0;}}
    if(x<mx){mx=x; if(Mx-L/2>=ns&&phase==0){phase=1;t0=t;ext=x;dir=1;printf("width %d\n",Mx-mx);}}
    if(phase==1){ if(dir==1){ if(x>ext){ext=x;text=t;} else if(x<ext-6){printf("max %d %lld\n",ext-mx,text-t0);dir=-1;ext=x;text=t;} }
      else { if(x<ext){ext=x;text=t;} else if(x>ext+6){printf("min %d %lld\n",ext-mx,text-t0);dir=1;ext=x;text=t;} } }
  }
}
