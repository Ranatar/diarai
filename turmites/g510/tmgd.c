/* Диагональный вариант tmg: машина Тьюринга из полоски ванта 4.8.8, растущей под 45°.
   ./tmgd CODE D0 N DIAG out.txt [G]  (клетка = G соседних диагоналей)   (DIAG=+1: полоса вдоль (1,1), -1: вдоль (1,-1))
   Клетка ленты k = (x+DIAG*y)/2, ряд m = (x-DIAG*y)/2 (у всех плиток x,y одной чётности).
   Сначала прогон N шагов на большом поле — диапазон m; затем извлечение.
   Вывод (как у tmg): s c side ns nc cnt, где s = ряд<<3|d при входе в клетку, c = содержимое клетки (биты по рядам).
   В stdout: ROWS MOFF START (START = s начального входа) и число конфликтов. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define B 4096
#define L 16384
#define RM 12
static unsigned char g[B][B];
static unsigned char f[RM][L];
#define HS (1<<24)
static long long hk[HS]; static long long hv[HS]; static long long hc[HS];
int main(int argc,char**argv){
  int code=atoi(argv[1]),d0=atoi(argv[2]); long long N=atoll(argv[3]); int dg=atoi(argv[4]);
  int G=argc>6?atoi(argv[6]):1; int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  /* проход 1: диапазон m */
  int x=0,y=0,d=d0,mlo=0,mhi=0;
  for(long long t=0;t<N;t++){ int gx=x+B/2,gy=y+B/2; if(gx<1||gy<1||gx>=B-1||gy>=B-1){fprintf(stderr,"проход 1: край\n");return 1;}
    int m=(x-dg*y)/2; if(m<mlo)mlo=m; if(m>mhi)mhi=m;
    int c=g[gy][gx]; d=(d+((x&1)?Ts[c]:To[c]))&7; g[gy][gx]^=1; x+=DX[d]; y+=DY[d]; }
  int rows=mhi-mlo+1, moff=-mlo; if(rows>RM){printf("ширина %d > %d\n",rows,RM);return 1;}
  /* проход 2: машина */
  x=0;y=0;d=d0; int k0=0, tile=0, ein=-1; long long cont=0; long long conf=0; int start=-1;
  #define CONT(K) ({long long c_=0; for(int q=0;q<G;q++) for(int r=0;r<rows;r++) c_|=(long long)f[r][(K)*G+q+L/2]<<(q*rows+r); c_;})
  for(long long t=0;t<N;t++){
    int kk=(x+dg*y)/2, k=(kk>=0?kk/G:-((-kk+G-1)/G)), m=(x-dg*y)/2, r=m+moff;
    if(r<0||r>=rows){printf("вышел из полосы t=%lld\n",t);return 1;}
    if(kk+L/2<2||kk+L/2>=L-2)break;
    if(t==0){tile=k; ein=r<<3|d; start=ein; cont=CONT(k);}
    else if(k!=tile){ long long c2=CONT(tile); int side=k>tile; int ns=r<<3|d;
      long long key=((long long)ein<<40|cont)+1; unsigned h=(unsigned)((unsigned long long)key*11400714819323198485ull>>40)%HS; while(hk[h]&&hk[h]!=key)h=(h+1)%HS;
      long long v=(long long)side<<60|(long long)ns<<40|c2; if(hk[h]&&hv[h]!=v)conf++; hk[h]=key; hv[h]=v; hc[h]++;
      tile=k; ein=ns; cont=CONT(k); }
    unsigned char*c=&f[r][kk+L/2]; int cc=*c; d=(d+((x&1)?Ts[cc]:To[cc]))&7; *c^=1; x+=DX[d]; y+=DY[d];
  }
  long long nk=0; FILE*o=fopen(argv[5],"w");
  for(int h=0;h<HS;h++) if(hk[h]){nk++; long long key=hk[h]-1,v=hv[h]; fprintf(o,"%lld %lld %lld %lld %lld %lld\n",key>>40,key&((1LL<<40)-1),(v>>60)&1,(v>>40)&255,v&((1LL<<40)-1),hc[h]);}
  fclose(o);
  printf("rows %d moff %d start %d строк %lld конфликтов %lld\n",rows,moff,start,nk,conf);
  (void)k0; return 0;
}
