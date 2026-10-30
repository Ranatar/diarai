// ./samein R1 R2 STEPS — совпадают ли последовательности входов (состояние,цвет) двух турмитов; печать первого расхождения
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 4096
static uint8_t g1[N*N], g2[N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int c,char**a){int r[2]={atoi(a[1]),atoi(a[2])};long T=atol(a[3]);int wc[2][4],tn[2][4],ns[2][4];
 for(int k=0;k<2;k++)for(int e=0;e<4;e++){int b=(r[k]>>(4*e))&15;wc[k][e]=b&1;tn[k][e]=(b>>1)&3;ns[k][e]=(b>>3)&1;}
 int x[2]={N/2,N/2},y[2]={N/2,N/2},d[2]={0,0},s[2]={0,0}; uint8_t*G[2]={g1,g2};
 for(long t=0;t<T;t++){int e[2];
  for(int k=0;k<2;k++){uint8_t*q=&G[k][(long)y[k]*N+x[k]];e[k]=s[k]*2+*q;*q=wc[k][e[k]];d[k]=(d[k]+tn[k][e[k]])&3;s[k]=ns[k][e[k]];x[k]+=DX[d[k]];y[k]+=DY[d[k]];
   if(x[k]<1||x[k]>=N-1||y[k]<1||y[k]>=N-1){printf("%d %d край на t=%ld, совпадали\n",r[0],r[1],t);return 0;}}
  if(e[0]!=e[1]){printf("%d %d расходятся на t=%ld\n",r[0],r[1],t);return 0;}}
 printf("%d %d совпадают %ld шагов\n",r[0],r[1],T);}
