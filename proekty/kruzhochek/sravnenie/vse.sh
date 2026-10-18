#!/bin/sh
# Лист «Кружочек через движок maps». Запуск: sh proekty/kruzhochek/sravnenie/vse.sh (из корня пространства)
# Цвет — куб «Кружочка» (белое — северный полюс, красный — λ = 0). Растры — во временной ext/tmp/kr/.
set -e
T=ext/tmp/kr
S=proekty/kruzhochek/sravnenie
mkdir -p $T
node $S/raster.mjs mollweide 300 $T/a.bin
node $S/raster.mjs goode 300 $T/b.bin
node $S/raster.mjs peirce 300 $T/c.bin
node $S/raster.mjs spilhaus 300 $T/d.bin
node $S/raster.mjs august 300 $T/e.bin
node $S/raster.mjs berghaus 300 $T/f.bin
node $S/raster.mjs armadillo 300 $T/g.bin
node $S/raster.mjs healpix 300 $T/h.bin
node $S/raster.mjs gilbert 300 $T/i.bin
python3 -I $S/cvet.py $S/maps-kruzhochek.png \
  "$T/a.bin:300:Mollweide (у автора нет)" "$T/b.bin:300:Goode" "$T/c.bin:300:Peirce quincuncial" \
  "$T/d.bin:300:Spilhaus" "$T/e.bin:300:August epicycloidal" "$T/f.bin:300:Berghaus star" \
  "$T/g.bin:300:Armadillo" "$T/h.bin:300:HEALPix" "$T/i.bin:300:Gilbert two-world"
