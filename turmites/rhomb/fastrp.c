// 2845 ускоренно, битовые строки R и столбцы C. ./fastb MAXLOG [thumbdir]
// Прямой счёт до 2^20, затем хорды. На каждом 2^k (первое событие после) печатает t, ones, рамку; миниатюру 512 в thumbdir.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef N
#define N 16384
#endif
#define W (N/64)
static uint64_t *R,*C; // R[y*W + x/64] бит x%64; C[x*W + y/64]
static inline int get(int x,int y){return (R[(long)y*W+(x>>6)]>>(x&63))&1;}
static inline void set(int x,int y,int v){
  uint64_t m=1ULL<<(x&63), m2=1ULL<<(y&63);
  if(v){R[(long)y*W+(x>>6)]|=m; C[(long)x*W+(y>>6)]|=m2;}
  else {R[(long)y*W+(x>>6)]&=~m; C[(long)x*W+(y>>6)]&=~m2;}
}
// первая белая от позиции p (включительно) в строке arr, направление +1/-1; возвращает индекс
static inline long firstzero(uint64_t*a,long p,int dir){
  if(dir>0){ long w=p>>6; uint64_t v=~a[w] & (~0ULL<<(p&63));
    while(!v){ w++; v=~a[w]; } return (w<<6)+__builtin_ctzll(v); }
  else { long w=p>>6; int b=p&63; uint64_t v=~a[w] & (b==63?~0ULL:((1ULL<<(b+1))-1));
    while(!v){ w--; v=~a[w]; } return (w<<6)+63-__builtin_clzll(v); }
}
static uint64_t rs=88172645463325252ULL; static inline uint64_t rng(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs>>11;}
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){ if(getenv("SEED")) rs=strtoull(getenv("SEED"),0,10)*2654435761ULL+1;
  int maxlog=atoi(argv[1]); const char*td=argc>2?argv[2]:0;
  R=calloc((long)N*W,8); C=calloc((long)N*W,8);
  int rule=2845, wc[4],tn[4],ns[4];
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int x=N/2,y=N/2,d=0,s=0; long ones=0,t=0; int minx=x,maxx=x,miny=y,maxy=y;
  for(;;t++){
    int col=get(x,y); int e=s*2+col;
    if(t>=(1L<<20) && e==2) break;
    ones+=wc[e]-col; set(x,y,wc[e]); d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
  }
  int k=21; long chords=0;
  for(;;){
    while(k<=maxlog && t>=(1L<<k)){
      printf("2^%d t=%ld ones=%ld w=%d h=%d chords=%ld\n",k,t,ones,maxx-minx+1,maxy-miny+1,chords); fflush(stdout);
      if(td && k>=30){ char fn[256]; sprintf(fn,"%s/r2845-%d.pgm",td,k); FILE*f=fopen(fn,"wb");
        int bw=maxx-minx+1,bh=maxy-miny+1,S=bw>bh?bw:bh, P=512; fprintf(f,"P5\n%d %d\n255\n",P,P);
        for(int i=0;i<P;i++)for(int j=0;j<P;j++){ int cnt=0,tot=0; int x0=minx+(long)j*S/P,x1=minx+(long)(j+1)*S/P,y0=miny+(long)i*S/P,y1=miny+(long)(i+1)*S/P;
          if(x1==x0)x1++; if(y1==y0)y1++;
          for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;if(xx<=maxx&&yy<=maxy)cnt+=get(xx,yy);}
          fputc(255-255*cnt/tot,f);} fclose(f);}
      k++;
    }
    if(k>maxlog) break;
    set(x,y,1); ones++; d=(d+1)&3;
    int qx=x+DX[d], qy=y+DY[d];
    if(!get(qx,qy)){ x=qx;y=qy;t+=1; continue; }
    long n; int ex,ey;
    if(DY[d]==0){ long e2=firstzero(R+(long)qy*W,qx,DX[d]); ex=e2; ey=qy; n=(e2-qx)*DX[d]; }
    else { long e2=firstzero(C+(long)qx*W,qy,DY[d]); ex=qx; ey=e2; n=(e2-qy)*DY[d]; }
    set(ex,ey,1);
    if(ex<minx)minx=ex;if(ex>maxx)maxx=ex;if(ey<miny)miny=ey;if(ey>maxy)maxy=ey;
    if(ex<=64||ex>=N-65||ey<=64||ey>=N-65){printf("edge at t=%ld\n",t);break;}
    long kk=n/2; x=qx+kk*DX[d]; y=qy+kk*DY[d]; set(x,y,0);
    if(RANDOM? (rng()&1) : (n&1)) d=(d+2)&3;
    t+=(n+1)*(n+2)/2; chords++;
  }
  if(getenv("PROF")){ FILE*f=fopen(getenv("PROF"),"w"); long sx=0,sy=0,n=0;
    for(int yy=miny;yy<=maxy;yy++)for(int w=minx>>6;w<=maxx>>6;w++){uint64_t v=R[(long)yy*W+w]; int c=__builtin_popcountll(v); n+=c; sy+=(long)c*yy; while(v){int b=__builtin_ctzll(v); sx+=(w<<6)+b; v&=v-1;}}
    fprintf(f,"# n=%ld cx=%.2f cy=%.2f\n",n,(double)sx/n,(double)sy/n);
    for(int yy=miny;yy<=maxy;yy++){int a=-1,b=-1,cnt=0; for(int xx=minx;xx<=maxx;xx++) if(get(xx,yy)){if(a<0)a=xx;b=xx;cnt++;} fprintf(f,"%d %d %d %d\n",yy,a,b,cnt);}
    fclose(f);}
  return 0;
}
