// ./asym RULE T : в каждом секторе (В,С,З,Ю; 0.2<u<0.8) частоты узоров 3×3 (+чётность x, y центра) и самые асимметричные пары p / поворот180(p)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static double h[4][2048]; double n[4];
int rot(int p){int q=0;for(int k=0;k<9;k++)if(p>>k&1)q|=1<<(8-k);return q;}
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 for(long t=0;t<T;t++){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
 double cx=(x0+x1)/2.0,cy=(y0+y1)/2.0,R=(x1-x0+y1-y0)/4.0;
 for(int j=y0+1;j<y1;j++)for(int i=x0+1;i<x1;i++){double ex=i-cx,ey=j-cy,u=fmax(fabs(ex),fabs(ey))/R;if(u<.2||u>.8)continue;int S;
  if(ex>=fabs(ey))S=0;else if(-ey>=fabs(ex))S=1;else if(-ex>=fabs(ey))S=2;else S=3;
  int p=0,k=0;for(int dy=-1;dy<=1;dy++)for(int dx=-1;dx<=1;dx++)p|=g[(long)(j+dy)*N+i+dx]<<(k++);
  p|=((i-N/2)&1)<<9|((j-N/2)&1)<<10; h[S][p]++;n[S]++;}
 const char*nm="ENWS";
 for(int S=0;S<4;S++){double best[3]={0};int bp[3]={0};
  for(int p=0;p<2048;p++){int q=rot(p&511)|(p&1536); if(q<=p)continue; double a_=h[S][p],b=h[S][q]; if(a_+b<200)continue; double z=(a_-b)/sqrt(a_+b);
   for(int m=0;m<3;m++)if(fabs(z)>fabs(best[m])){for(int k2=2;k2>m;k2--){best[k2]=best[k2-1];bp[k2]=bp[k2-1];}best[m]=z;bp[m]=p;break;}}
  printf("%c n=%.0f:",nm[S],n[S]);for(int m=0;m<3;m++)printf("  p%d z=%+.1f (%.0f/%.0f)",bp[m],best[m],h[S][bp[m]],h[S][rot(bp[m]&511)|(bp[m]&1536)]);printf("\n");}}
