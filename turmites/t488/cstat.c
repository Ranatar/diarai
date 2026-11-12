/* ./cstat RULE TAU0 LOG2N : энтропия состояний узлов (16 значений) по посещённым узлам */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]),lg=atoi(argv[3]); int L=2048;
  int W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int X=L/2,Y=L/2,k=0,sig=1; f[(size_t)Y*L+X]|=16;
  for(long long t=1;t<=(1LL<<lg);t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; if(X<1||Y<1||X>=L-1||Y>=L-1){printf("%s %d край\n",R,atoi(argv[2]));return 0;} f[(size_t)Y*L+X]|=16;}
    else{k=(k+sig)&3;tau=1;}
  }
  long long h[16]={0},n=0; for(size_t i=0;i<(size_t)L*L;i++) if(f[i]&16){h[f[i]&15]++;n++;}
  double H=0,mx=0; for(int i=0;i<16;i++) if(h[i]){double q=(double)h[i]/n;H-=q*log2(q); if(q>mx)mx=q;}
  printf("%s %d узлов %lld энтропия %.2f макс %.3f\n",R,atoi(argv[2]),n,H,mx);
}
