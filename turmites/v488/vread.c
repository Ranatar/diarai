/* ./vread CODE D0 NSTART : во внутренней фазе на каждом подтверждённом минимуме (начало вылазки вправо) печатает
   глубину вылазки (макс x относительно левого края) предыдущей... формат: "E maxx | x0 | строки цветов колонок x0+1..x0+120 по y=-2..2" */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),ns=atoi(argv[3]),L=8192,Y0=L/2;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,mx=x,Mx=x; int phase=0; int ext=x,dir=0; char snap[5*120+1]; int have=0,x0=0;
  for(long long t=1;;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; x+=DX[d]; y+=DY[d];
    if(x>Mx){Mx=x; if(phase==1)return 0;}
    if(x<mx){mx=x; if(Mx-L/2>=ns&&phase==0){phase=1;ext=x;dir=1;}}
    if(phase==1){ if(dir==1){ if(x>ext)ext=x; else if(x<ext-6){ if(have)printf("%d %d %s\n",ext-mx,x0-mx,snap); have=0; dir=-1;ext=x;} }
      else { if(x<ext)ext=x; else if(x>ext+6){ dir=1; x0=x; int k=0;
          for(int yy=Y0+2;yy>=Y0-2;yy--)for(int xx=x+1;xx<=x+120;xx++) snap[k++]=(((xx^yy)&1)?'-':((f[(size_t)yy*L+xx]&1)?'1':'0'));
          snap[k]=0; have=1; ext=x; } } }
  }
}
