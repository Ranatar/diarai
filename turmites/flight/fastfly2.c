// Общий ускоритель полётов: прозрачный вход (цвет тот же, прямо, состояние то же) проскакивается
// поиском первой клетки другого цвета по битовым строкам R и столбцам C. Точный счёт.
// ./fastfly RULE MAXLOG [thumbdir] : на каждом 2^k (первый шаг, где t >= 2^k) печатает t ones w h доля_полёта
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#ifndef N
#define N 16384
#endif
#define W (N/64)
static uint64_t *R,*C;
static inline int get(int x,int y){return (R[(long)y*W+(x>>6)]>>(x&63))&1;}
static inline void set(int x,int y,int v){
  uint64_t m=1ULL<<(x&63), m2=1ULL<<(y&63);
  if(v){R[(long)y*W+(x>>6)]|=m; C[(long)x*W+(y>>6)]|=m2;}
  else {R[(long)y*W+(x>>6)]&=~m; C[(long)x*W+(y>>6)]&=~m2;}
}
// первая клетка с цветом != col от p (включительно) по направлению dir; -1/N если до края нет
static long firstdiff(const uint64_t*a,long p,int dir,int col){
  uint64_t inv = col? ~0ULL : 0ULL; // v = a^inv: биты, где цвет != col ... для col=1: ~a
  if(dir>0){ long w=p>>6; uint64_t v=(a[w]^inv) & (~0ULL<<(p&63));
    while(!v){ if(++w>=W) return N; v=a[w]^inv; } return (w<<6)+__builtin_ctzll(v); }
  else { long w=p>>6; int b=p&63; uint64_t v=(a[w]^inv) & (b==63?~0ULL:((1ULL<<(b+1))-1));
    while(!v){ if(--w<0) return -1; v=a[w]^inv; } return (w<<6)+63-__builtin_clzll(v); }
}
// миниатюра рамки до 512 px: серое = доля единиц в блоке
static void thumb(const char*fn,int minx,int maxx,int miny,int maxy){
  FILE*f=fopen(fn,"wb");
  int bw=maxx-minx+1,bh=maxy-miny+1,S=bw>bh?bw:bh, P=S<512?S:512; fprintf(f,"P5\n%d %d\n255\n",P,P);
  for(int i=0;i<P;i++)for(int j=0;j<P;j++){ int cnt=0,tot=0; int x0=minx+(long)j*S/P,x1=minx+(long)(j+1)*S/P,y0=miny+(long)i*S/P,y1=miny+(long)(i+1)*S/P;
    if(x1==x0)x1++; if(y1==y0)y1++;
    for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;if(xx<=maxx&&yy<=maxy)cnt+=get(xx,yy);}
    fputc(255-255*cnt/tot,f);} fclose(f);
}
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int rule=atoi(argv[1]); int maxlog=atoi(argv[2]); const char*td=argc>3?argv[3]:0;
  R=calloc((long)N*W,8); C=calloc((long)N*W,8);
  int wc[4],tn[4],ns[4],tr[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;
    tr[e]=(wc[e]==(e&1))&&tn[e]==0&&ns[e]==(e>>1);}
  // обобщённые полёты: для цвета c и (s,d) — цикл периода p со сносом по оси, все записи = c
  int cp[2][2][4]={{{0}}}, cdx[2][2][4], cdy[2][2][4], fn_[2][2][4]; int fpx[2][2][4][16], fpy[2][2][4][16];
  for(int c=0;c<2;c++)for(int s0=0;s0<2;s0++)for(int d0=0;d0<4;d0++){
    int ss=s0,dd=d0,xx=0,yy=0,ok=1,n=0;
    for(int st=1;st<=16;st++){ int e=ss*2+c; if(wc[e]!=c){ok=0;break;}
      fpx[c][s0][d0][n]=xx; fpy[c][s0][d0][n]=yy; n++;
      dd=(dd+tn[e])&3; ss=ns[e]; xx+=DX[dd]; yy+=DY[dd];
      if(ss==s0&&dd==d0){ if((xx==0)!=(yy==0)){cp[c][s0][d0]=st;cdx[c][s0][d0]=xx;cdy[c][s0][d0]=yy;fn_[c][s0][d0]=n;} break; } }
    (void)ok;
  }
  if(getenv("GEN")){ for(int c=0;c<2;c++)for(int s0=0;s0<2;s0++)for(int d0=0;d0<4;d0++) if(cp[c][s0][d0]) fprintf(stderr,"c%d s%d d%d p%d (%d,%d)\n",c,s0,d0,cp[c][s0][d0],cdx[c][s0][d0],cdy[c][s0][d0]); }
  int gen=getenv("GEN")!=0;
  int x=N/2,y=N/2,d=0,s=0,minx=x,maxx=x,miny=y,maxy=y; long t=0,ones=0,flt=0,flt0=0,t0=0; int k=10;
  long tstop=getenv("TSTOP")?atol(getenv("TSTOP")):-1;
  for(;;){
    if(tstop>0 && t>=tstop){ printf("stop t=%ld ones=%ld w=%d h=%d\n",t,ones,maxx-minx+1,maxy-miny+1);
      if(td){ char fn[256]; sprintf(fn,"%s/%d-t%ld.pgm",td,rule,tstop); thumb(fn,minx,maxx,miny,maxy);} break; }
    while(k<=maxlog && t>=(1L<<k)){
      printf("2^%d t=%ld ones=%ld w=%d h=%d fl=%.3f\n",k,t,ones,maxx-minx+1,maxy-miny+1,t>t0?(double)(flt-flt0)/(t-t0):0); fflush(stdout);
      flt0=flt; t0=t;
      if(td && k>=28){ char fn[256]; sprintf(fn,"%s/%d-%d.pgm",td,rule,k); thumb(fn,minx,maxx,miny,maxy); }
      k++;
    }
    if(k>maxlog) break;
    int col=get(x,y); int e=s*2+col;
    if(gen && !tr[e] && cp[col][s][d]){
      int p=cp[col][s][d], ax=cdx[col][s][d], ay=cdy[col][s][d], nf=fn_[col][s][d];
      long m=1L<<40; int hor=(ay==0); int a=hor?abs(ax):abs(ay); int sg=hor?(ax>0?1:-1):(ay>0?1:-1);
      for(int i=0;i<nf && m>0;i++){
        int fx=fpx[col][s][d][i], fy=fpy[col][s][d][i];
        // клетки x+fx + k*ax (k<m) должны быть цвета col: длина пробега от x+fx по направлению
        long q,len;
        if(hor){ int yy=y+fy; if(yy<0||yy>=N){m=0;break;} long st=x+fx; if(st<0||st>=N){m=0;break;}
          q=firstdiff(R+(long)yy*W,st,sg,col); len=(q-st)*sg; }
        else { int xx=x+fx; if(xx<0||xx>=N){m=0;break;} long st=y+fy; if(st<0||st>=N){m=0;break;}
          q=firstdiff(C+(long)xx*W,st,sg,col); len=(q-st)*sg; }
        long mk=(len+a-1)/a; // k*a < len  =>  k < len/a
        if(mk<m)m=mk;
      }
      if(m>=2){ m-=1; { long lim=((1L<<k)-t)/p; if(m>lim) m=lim; } if(m<1) goto nogen; t+=m*p; flt+=m*p; x+=m*ax; y+=m*ay;
        if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
        if(x<0||x>=N||y<0||y>=N){printf("escape at t=%ld\n",t);break;}
        continue; }
    }
    nogen:
    if(tr[e]){
      long n; // клеток того же цвета подряд, начиная с текущей
      if(DY[d]==0){ long q=firstdiff(R+(long)y*W,x,DX[d],col); if(q<0||q>=N){printf("escape at t=%ld\n",t);break;} n=(q-x)*DX[d]; x=q; }
      else { long q=firstdiff(C+(long)x*W,y,DY[d],col); if(q<0||q>=N){printf("escape at t=%ld\n",t);break;} n=(q-y)*DY[d]; y=q; }
      t+=n; flt+=n;
    } else {
      ones+=wc[e]-col; if(wc[e]!=col) set(x,y,wc[e]); d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d]; t++;
      if(x<0||x>=N||y<0||y>=N){printf("escape at t=%ld\n",t);break;}
    }
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
  }
  return 0;
}
