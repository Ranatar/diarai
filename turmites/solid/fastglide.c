// Ускоритель глайдеров: муравей + конечный набор дырок, повторяющийся со сдвигом по оси в сплошном фоне
// (таблица из gtab.py). Если впереди по ходу всех прочитанных клеток фон — прыжок на m периодов. Точный счёт.
// ./fastglide RULE TABFILE MAXLOG [thumbdir]   (TSTOP=t — стоп с миниатюрой; NOGL=1 — без прыжков, для сверки)
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
static long firstdiff(const uint64_t*a,long p,int dir,int col){
  uint64_t inv = col? ~0ULL : 0ULL;
  if(dir>0){ long w=p>>6; uint64_t v=(a[w]^inv) & (~0ULL<<(p&63));
    while(!v){ if(++w>=W) return N; v=a[w]^inv; } return (w<<6)+__builtin_ctzll(v); }
  else { long w=p>>6; int b=p&63; uint64_t v=(a[w]^inv) & (b==63?~0ULL:((1ULL<<(b+1))-1));
    while(!v){ if(--w<0) return -1; v=a[w]^inv; } return (w<<6)+63-__builtin_clzll(v); }
}
static void thumb(const char*fn,int minx,int maxx,int miny,int maxy){
  FILE*f=fopen(fn,"wb");
  int bw=maxx-minx+1,bh=maxy-miny+1,S=bw>bh?bw:bh, P=S<512?S:512; fprintf(f,"P5\n%d %d\n255\n",P,P);
  for(int i=0;i<P;i++)for(int j=0;j<P;j++){ int cnt=0,tot=0; int x0=minx+(long)j*S/P,x1=minx+(long)(j+1)*S/P,y0=miny+(long)i*S/P,y1=miny+(long)(i+1)*S/P;
    if(x1==x0)x1++; if(y1==y0)y1++;
    for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;if(xx<=maxx&&yy<=maxy)cnt+=get(xx,yy);}
    fputc(255-255*cnt/tot,f);} fclose(f);
}
typedef struct { int c,p,vx,vy,nh,nf; int hx[16],hy[16]; int fx[64],fy[64]; } G;
static G tab[4096]; static int nt=0; static int idx[2][4][512], nidx[2][4];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int rule=atoi(argv[1]); FILE*tf=fopen(argv[2],"r"); int maxlog=atoi(argv[3]); const char*td=argc>4?argv[4]:0;
  int s_,d_;
  while(nt<4096 && fscanf(tf,"%d %d %d %d %d %d %d",&tab[nt].c,&s_,&d_,&tab[nt].p,&tab[nt].vx,&tab[nt].vy,&tab[nt].nh)==7){
    G*g=&tab[nt]; for(int i=0;i<g->nh;i++) if(fscanf(tf,"%d %d",&g->hx[i],&g->hy[i])!=2) return 1;
    if(fscanf(tf,"%d",&g->nf)!=1) return 1; for(int i=0;i<g->nf;i++) if(fscanf(tf,"%d %d",&g->fx[i],&g->fy[i])!=2) return 1;
    if(g->nh>16||g->nf>64) return 2;
    if(nidx[s_][d_]<512) idx[s_][d_][nidx[s_][d_]++]=nt; nt++; }
  fclose(tf);
  int nogl=getenv("NOGL")!=0;
  R=calloc((long)N*W,8); C=calloc((long)N*W,8);
  int wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0,minx=x,maxx=x,miny=y,maxy=y; long t=0,ones=0,gl=0,gl0=0,t0=0,jumps=0; int k=10;
  long tstop=getenv("TSTOP")?atol(getenv("TSTOP")):-1;
  const int M=40;
  for(;;){
    if(tstop>0 && t>=tstop){ printf("stop t=%ld ones=%ld w=%d h=%d\n",t,ones,maxx-minx+1,maxy-miny+1);
      if(td){ char fn[256]; sprintf(fn,"%s/%d-t%ld.pgm",td,rule,tstop); thumb(fn,minx,maxx,miny,maxy);} break; }
    while(k<=maxlog && t>=(1L<<k)){
      printf("2^%d t=%ld ones=%ld w=%d h=%d gl=%.4f jumps=%ld\n",k,t,ones,maxx-minx+1,maxy-miny+1,t>t0?(double)(gl-gl0)/(t-t0):0,jumps); fflush(stdout);
      gl0=gl; t0=t;
      if(td && k>=26){ char fn[256]; sprintf(fn,"%s/%d-%d.pgm",td,rule,k); thumb(fn,minx,maxx,miny,maxy); }
      k++;
    }
    if(k>maxlog) break;
    if(x<M||x>=N-M||y<M||y>=N-M){printf("escape at t=%ld ones=%ld w=%d h=%d\n",t,ones,maxx-minx+1,maxy-miny+1);break;}
    if(!nogl) for(int q=0;q<nidx[s][d];q++){ G*g=&tab[idx[s][d][q]]; int c=g->c, ok=1;
      for(int i=0;i<g->nh&&ok;i++) if(get(x+g->hx[i],y+g->hy[i])==c) ok=0;
      for(int i=0;i<g->nf&&ok;i++){ int fx=g->fx[i],fy=g->fy[i], hole=0;
        for(int j=0;j<g->nh;j++) if(g->hx[j]==fx&&g->hy[j]==fy) hole=1;
        if(!hole && get(x+fx,y+fy)!=c) ok=0; }
      if(!ok) continue;
      // совпало: дырки временно в фон, считаем пробег
      for(int i=0;i<g->nh;i++) set(x+g->hx[i],y+g->hy[i],c);
      int hor=(g->vy==0); int a=hor?abs(g->vx):abs(g->vy); int sg=hor?(g->vx>0?1:-1):(g->vy>0?1:-1);
      long m=1L<<40;
      for(int pass=0;pass<2;pass++){ int n=pass?g->nh:g->nf; for(int i=0;i<n;i++){
        int fx=pass?g->hx[i]:g->fx[i], fy=pass?g->hy[i]:g->fy[i]; long st,q,len;
        if(hor){ st=x+fx; q=firstdiff(R+(long)(y+fy)*W,st,sg,c); }
        else   { st=y+fy; q=firstdiff(C+(long)(x+fx)*W,st,sg,c); }
        len=(q-st)*sg; long mk=(len-1)/a+1; if(mk<m)m=mk; } }
      m-=2; { long lim=((1L<<k)-t)/g->p; if(m>lim) m=lim; }
      if(m<1){ for(int i=0;i<g->nh;i++) set(x+g->hx[i],y+g->hy[i],1-c); continue; }
      long mx=m*g->vx, my=m*g->vy;
      for(int i=0;i<g->nh;i++) set(x+mx+g->hx[i],y+my+g->hy[i],1-c);
      x+=mx; y+=my; t+=m*g->p; gl+=m*g->p; jumps++;
      if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
      goto next;
    }
    { int col=get(x,y); int e=s*2+col;
      ones+=wc[e]-col; if(wc[e]!=col) set(x,y,wc[e]); d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d]; t++;
      if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y; }
    next:;
  }
  return 0;
}
