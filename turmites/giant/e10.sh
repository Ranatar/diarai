#!/bin/sh
# ./e10.sh LIST OUT : каждое правило из LIST до 10^10 (big, ck/e_RULE), итог в OUT; пропускает уже посчитанные
cd "$(dirname "$0")"
while read r; do
  grep -q "^$r " $2 2>/dev/null && continue
  BIG_FINAL=1 ./big_e $r ck/e_$r 10000000000 > tmp_$r.txt 2>&1
  echo "$r $(grep HIGHWAY tmp_$r.txt) $(tail -n 1 tmp_$r.txt)" >> $2
  mv tmp_$r.txt last_$(basename $2)
done < $1
