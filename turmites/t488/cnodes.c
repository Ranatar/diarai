/* Состав узлов по r/R: доли 16 состояний (биты N E S W). ./cnodes RULE TAU0 LOG2T */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]); long long T=1LL<<atoi(argv[3]);
  int L=4096,W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int X=L/2,Y=L/2,k=0,sig=1; f[(size_t)Y*L+X]|=16;
  int minx=X,maxx=X,miny=Y,maxy=Y;
  for(long long t=1;t<T;t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; f[(size_t)Y*L+X]|=16; if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1;}
  }
  double cx=(minx+maxx)/2.0,cy=(miny+maxy)/2.0,Rad=(maxx-minx+maxy-miny)/4.0;
  double h[5][16]={{0}},n[5]={0};
  for(int x=0;x<L;x++)for(int y=0;y<L;y++){unsigned char v=f[(size_t)y*L+x]; if(!(v&16))continue; double r=hypot(x-cx,y-cy)/Rad; int b=(int)(r*5); if(b>4)continue; h[b][v&15]++; n[b]++;}
  printf("%s: доли состояний узла (%%) по кольцам r/R 0-.2 .2-.4 .4-.6 .6-.8 .8-1; число чёрных бит\n",R);
  for(int s=0;s<16;s++){ printf("%2d (%d%d%d%d) b=%d:",s,s&1,(s>>1)&1,(s>>2)&1,(s>>3)&1,__builtin_popcount(s)); for(int b=0;b<5;b++) printf(" %5.1f",100*h[b][s]/n[b]); printf("\n"); }
  printf("ср. чёрных:"); for(int b=0;b<5;b++){double m=0; for(int s=0;s<16;s++) m+=h[b][s]*__builtin_popcount(s); printf(" %.3f",m/n[b]);} printf("\n");
}
