/* ./vsnap CODE D0 LOG2N : в каждый момент прироста правого края печатает строки полоски (y = -2..2 удвоенные) */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),lg=atoi(argv[3]),L=4096,Y0=L/2;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,mx=x,Mx=x;
  for(long long t=1;t<=(1LL<<lg);t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; x+=DX[d]; y+=DY[d];
    if(x<mx)mx=x; if(x>Mx){Mx=x; printf("n=%d t=%lld ant y=%d d=%d\n",Mx-L/2,t,y-Y0,d);
      for(int yy=Y0+2;yy>=Y0-2;yy--){ for(int xx=mx;xx<=Mx;xx++){ if(((xx^yy)&1)) {putchar(' ');continue;} unsigned char q=f[(size_t)yy*L+xx]; putchar(q&1?'#':(q?'.':'.'));} putchar('\n');} } }
}
