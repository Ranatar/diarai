#!/bin/sh
# глубокий прогон: ./deep.sh LIST MAXLOG TIMEOUT OUTDIR
while read r; do
  [ -f tabs/$r ] || python3 gtab.py $r > tabs/$r
  timeout $3 ./fastglide $r tabs/$r $2 th40 > $4/$r.txt
done < $1
