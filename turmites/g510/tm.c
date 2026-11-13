/* Извлечь машину Тьюринга 510: клетка ленты = плитка i: восьмиугольники (2i,0),(2i,-2), квадрат (2i+1,-1).
   Вход в клетку: (ряд y, направление d). Печатает таблицу (вход, содержимое) -> (выход: сторона, ряд, d; новое содержимое), число раз */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 8192
unsigned char f[3][L];
long long cnt[64][8]; int res[64][8];
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long N=atoll(argv[2]);
  int To[2]={6,7},Ts[2]={6,2}; int x=L/2,y=0,d=d0;
  int tile=x>>1, ein=-1, cont=0;
  for(long long t=0;t<N;t++){
    int nt=x>>1;
    if(nt!=tile){ int c2=f[0][2*tile]|f[2][2*tile]<<1|f[1][2*tile+1]<<2; int side=nt>tile;
      int ex=side<<5|(-y)<<3|d; if(ein>=0){ if(cnt[ein][cont]&&res[ein][cont]!=(ex<<3|c2)){printf("conflict\n");}
        res[ein][cont]=ex<<3|c2; cnt[ein][cont]++; }
      tile=nt; ein=(-y)<<3|d; cont=f[0][2*tile]|f[2][2*tile]<<1|f[1][2*tile+1]<<2; }
    unsigned char*c=&f[-y][x]; int cc=*c; d=(d+((x&1)?Ts[cc]:To[cc]))&7; *c^=1; x+=DX[d]; y+=DY[d];
    if(x<8||x>L-8)break;
  }
  for(int e=0;e<64;e++)for(int c=0;c<8;c++)if(cnt[e][c]){int r=res[e][c];
    printf("in y%d d%d  T%dB%dS%d -> %s y%d d%d  T%dB%dS%d  %lld\n",-(e>>3),e&7,c&1,c>>1&1,c>>2, (r>>8)?"R":"L",-((r>>6)&3),(r>>3)&7,r&1,r>>1&1,r>>2&1,cnt[e][c]);}
}
