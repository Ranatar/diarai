# Червь

Прогоны симулятора *C. elegans* `inbox/wormlisp/` (автор архива, Common Lisp, SBCL) на третьем уровне управления: сеть из 147 нейронов коннектома Cook et al. 2019.

## Как запустить

1. Скопировать `inbox/wormlisp` в `ext/wormlisp`, чтобы прогоны (`runs/`) не писали в inbox.
2. **Перевести переводы строк в LF.** Копия в inbox целиком в CRLF (855 файлов). На этом SBCL падает при сборке hunchentoot: перенос строки в форматной строке, `~` + `\r`, даёт «Unknown directive (character: Return)».
   `cd ext/wormlisp && grep -rlI $'\r' . | xargs sed -i 's/\r$//'`
3. `cd ext/wormlisp && sbcl --noinform --non-interactive --no-sysinit --no-userinit --load scripts/init.lisp --load ../../proekty/cherv/progon.lisp`
   Переменные: `CHERV_ID`, `CHERV_MODEL` (по умолчанию `WORM-3D-CONNECTOME`), `CHERV_PARAMS` (`agar-a-v1`), `CHERV_SEC` (12).
4. Картинка: `python3 proekty/cherv/hronofoto.py ext/wormlisp/runs/moi-1 proekty/cherv/moi-1.svg`

## Прогоны
