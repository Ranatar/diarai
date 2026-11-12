/* ./cimg RULE TAU0 LOG2N OUT.pgm [L] — картинка крупной модели: яркость = число чёрных битов в узле (0..4), непосещённые — 255 */
#include <stdio.h>
#include <stdlib.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]),lg=atoi(argv[3]); int L=argc>5?atoi(argv[5]):2048;
  int W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int X=L/2,Y=L/2,k=0,sig=1; f[(size_t)Y*L+X]|=16;
  int minx=X,maxx=X,miny=Y,maxy=Y;
  for(long long t=1;t<=(1LL<<lg);t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; if(X<1||Y<1||X>=L-1||Y>=L-1){fprintf(stderr,"край t=%lld\n",t);break;}
      f[(size_t)Y*L+X]|=16; if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1;}
  }
  int w=maxx-minx+1,h=maxy-miny+1; FILE*o=fopen(argv[4],"wb"); fprintf(o,"P5 %d %d 255\n",w,h);
  for(int y=miny;y<=maxy;y++)for(int x=minx;x<=maxx;x++){unsigned char v=f[(size_t)y*L+x];
    int b=__builtin_popcount(v&15); fputc((v&16)?(200-45*b):255,o);}
  fclose(o); fprintf(stderr,"%dx%d\n",w,h);
}
