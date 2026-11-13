/* Обобщённое извлечение машины Тьюринга из полоски ванта 4.8.8: ./tmg CODE D0 N ROWS
   клетка = столбец i: восьмиугольники (2i, y чётн.), квадраты (2i+1, y нечётн.), y = 0..-(ROWS-1); вход = (y, d).
   Печатает число состояний, символов, конфликтов и таблицу. */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 8192
#define R 16
unsigned char f[R][L];
static int key[1<<16]; static long long cnt[1<<16]; 
int main(int argc,char**argv){
  int code=atoi(argv[1]),d=atoi(argv[2]); long long N=atoll(argv[3]); int rows=atoi(argv[4]);
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  int Y0=argc>6?atoi(argv[6]):0; int x=L/2,y=-Y0; int tile=x>>1,ein=-1,cont=0; long long conf=0; int ns=0; static int seen[256];
  #define CONT(T) ({int c_=0,b_=0; for(int yy=0;yy<rows;yy++){ c_|=f[yy][2*(T)+((yy+Y0)&1)]<<b_; b_++; } c_;})
  for(long long t=0;t<N;t++){
    if(y>0||y<=-rows){printf("вышел из полосы y=%d t=%lld\n",y,t);return 1;}
    int nt=x>>1;
    if(nt!=tile){ int c2=CONT(tile); int side=nt>tile; int ex=side<<7|(-y)<<3|d;
      if(ein>=0){ int k=ein<<7|cont; int v=ex<<8|c2|1<<30; if(key[k]&&key[k]!=v)conf++; key[k]=v; cnt[k]++; }
      tile=nt; ein=(-y)<<3|d; if(!seen[ein]){seen[ein]=1;ns++;} cont=CONT(tile); }
    unsigned char*c=&f[-y][x]; int cc=*c; d=(d+((x&1)?Ts[cc]:To[cc]))&7; *c^=1; x+=DX[d]; y+=DY[d];
    if(x<8||x>L-8)break;
  }
  int nk=0; for(int k=0;k<(1<<16);k++) if(cnt[k]) nk++;
  printf("состояний входа %d, строк таблицы %d, конфликтов %lld\n",ns,nk,conf);
  if(argc>5){FILE*o=fopen(argv[5],"w"); for(int k=0;k<(1<<16);k++) if(cnt[k]){int v=key[k]; fprintf(o,"%d %d %d %d %d %lld\n",k>>7,k&127,(v>>15)&1,(v>>8)&127,v&255,cnt[k]);} fclose(o);}
}
