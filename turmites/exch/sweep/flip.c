// ./flip RULE T FRAC HALF LAG W NW [NOFLIP]: на шаге T (когда муравей вне квадрата) поворачивает на 180° квадрат поля
// с центром (cx+FRAC*R, cy) и полустороной HALF*R (центр поворота полуцелый — решётка рёбер сохраняется);
// затем окнами по W печатает средний сдвиг за LAG для стартов в квадрате (и до поворота одно окно).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int wc[4],tn[4],ns[4],x=N/2,y=N/2,d=0,s=0,x0=N/2,x1=N/2,y0=N/2,y1=N/2;
static inline void step(){uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];
 if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
int px0,px1,py0,py1;
static inline int in(int X,int Y){return X>=px0&&X<=px1&&Y>=py0&&Y<=py1;}
static int hx[1<<16],hy[1<<16];
void win(long W,int LAG,const char*tag){double sx=0,sy=0;long n=0;
 for(long t=0;t<W+LAG;t++){int k=t&0xffff;hx[k]=x;hy[k]=y; if(t>=LAG){int m=(t-LAG)&0xffff; if(in(hx[m],hy[m])){sx+=x-hx[m];sy+=y-hy[m];n++;}} step();}
 printf("%s vx %+.5f vy %+.5f n %ld\n",tag,sx/n/LAG,sy/n/LAG,n);}
int main(int c,char**a){int r=atoi(a[1]);long T=atol(a[2]);double FR=atof(a[3]),HA=atof(a[4]);int LAG=atoi(a[5]);long W=atol(a[6]);int NW=atoi(a[7]);int nof=c>8;
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 for(long t=0;t<T-W-LAG;t++)step();
 double R=(x1-x0+y1-y0)/4.0; int cx=(x0+x1)/2+(int)(FR*R), cy=(y0+y1)/2, h=(int)(HA*R);
 px0=cx-h;px1=cx+h+1;py0=cy-h;py1=cy+h+1; // чётный размер 2h+2: центр поворота полуцелый
 win(W,LAG,"before");
 while(in(x,y))step();
 if(!nof)for(int j=py0;j<=py1;j++)for(int i=px0;i<=px1;i++){int i2=px0+px1-i,j2=py0+py1-j; long p=(long)j*N+i,q=(long)j2*N+i2; if(p<q){uint8_t z=g[p];g[p]=g[q];g[q]=z;}}
 for(int w=0;w<NW;w++)win(W,LAG,nof?"control":"after ");
}
