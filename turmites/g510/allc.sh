#!/bin/sh
# все счётчики 4.8.8: строки полосы по картинке, машина, матрица счёта
cd "$(dirname "$0")"
while read code D a b; do
  bb=$(./lookg $D 4000000 $code | head -1)
  ytop=$(echo "$bb" | awk '{split($5,a,"\\.\\."); print a[2]}'); ybot=$(echo "$bb" | awk '{split($5,a,"\\.\\."); print a[1]}')
  xr=$(echo "$bb" | awk '{split($3,a,"\\.\\."); print a[2]-a[1]}')
  rows=$((ytop-ybot+1))
  if [ $rows -gt 15 ]; then echo "$code $D: высота $rows (растёт не по x)"; continue; fi
  r=$(./tmg $code $D 30000000 $rows cm/tm_${code}_$D.txt $ytop 2>&1 | tail -1)
  case "$r" in *вышел*) echo "$code $D: $r"; continue;; esac
  st=$((ytop*8+D))
  echo "$code $D rows=$rows ($r) $(timeout 300 python3 cmat.py cm/tm_${code}_$D.txt $st 2000000 2>&1 | tail -1)"
done < counters.txt
