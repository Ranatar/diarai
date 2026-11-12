/* ./mstat CODE LOG2N : энтропия раскраски блоков 2×2 (выровненных по чётным координатам) по посещённым блокам */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int code=atoi(argv[1]),lg=atoi(argv[2]),L=2048; int W[4],T[4]; for(int e=0;e<4;e++){int v=(code>>(3*e))&7;W[e]=v>>2;T[e]=v&3;}
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2,y=L/2,d=0,tau=0;
  for(long long t=1;t<=(1LL<<lg);t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; f[i]|=2; int e=2*tau+c; if(W[e]!=c)f[i]^=1;
    d=(d+T[e])&3; int nx=x+DX[d],ny=y+DY[d]; if(d&1) tau=(nx<x?nx:x)&1; else tau=((ny<y?ny:y)+1)&1; x=nx;y=ny;
    if(x<2||y<2||x>=L-2||y>=L-2){printf("%d край\n",code);return 0;} }
  double h[16]={0},n=0;
  for(int by=0;by<L;by+=2)for(int bx=0;bx<L;bx+=2){ int v=0,vis=0; for(int k=0;k<4;k++){unsigned char q=f[(size_t)(by+(k>>1))*L+bx+(k&1)]; v|=(q&1)<<k; vis|=q&2;} if(vis){h[v]++;n++;} }
  double H=0,mx=0; for(int k=0;k<16;k++) if(h[k]){double q=h[k]/n;H-=q*log2(q); if(q>mx)mx=q;}
  printf("%d блоков %.0f энтропия %.2f макс %.3f\n",code,n,H,mx);
}
