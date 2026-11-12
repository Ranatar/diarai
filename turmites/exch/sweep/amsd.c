// ./amsd RULE T0 T1 : msd муравья по лагам 2^k на отрезке [T0,T1]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g[(long)N*N]; static int16_t *px,*py;
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r=atoi(a[1]);long T0=atol(a[2]),T1=atol(a[3]);int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 px=malloc(2*(T1-T0+1));py=malloc(2*(T1-T0+1));
 int x=N/2,y=N/2,d=0,s=0;
 for(long t=0;t<=T1;t++){ if(t>=T0){px[t-T0]=x-N/2;py[t-T0]=y-N/2;}
  uint8_t*q=&g[(long)y*N+x];int e=s*2+(*q&1);*q=wc[e];d=(d+tn[e])&3;s=ns[e];x+=DX[d];y+=DY[d];}
 long n=T1-T0;
 for(long L=1;L<n/4;L*=2){double m=0;long k=0;for(long i=0;i+L<=n;i+=1+L/64){double dx=px[i+L]-px[i],dy=py[i+L]-py[i];m+=dx*dx+dy*dy;k++;}
  printf("%ld %.1f %.3f\n",L,m/k,m/k/L);}
}
