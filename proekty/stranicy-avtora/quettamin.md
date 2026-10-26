# Quettamin: замечания по ходу использования

Quettamin — проект автора, `inbox/quettamin`, Eldamo 0.8.13. Я собрал его копию в `ext/quettamin` (`scripts/build.py --no-tests`). Вызываю через свои обёртки: `proekty/instrumenty/qm_soedinit.py`, `qm_slovo.py`, `qm_affiks.py`.

## 1. ta-глаголы + *-ima*: правило PE22/156 модель не знает (26.10)

**Что видно.** `qm_soedinit.py parta- -ima` даёт: *parima* 0,333, *partima* 0,333, *partaima* 0,167, *partāima* 0,056. Форма автора (*nanpartaima*, `inbox/Suite_.txt`, 1.2) оказывается только третьей.

**Почему.** В таблице аффиксов (`branches/quenya/data/affixes.json`) 15 случаев с *-ima*. Из основ на гласный там только *ista- → istima* (*-a* выпадает) и *ferya- → férima* (выпадает *-ya*). Первый вариант *parima* — перенос *ferya- → férima* на *-ta*: при нём исчезает целый слог основы, *-ta*. Ни в одном слове с *-ima* такого нет.

**Что у Толкина.** Статья Eldamo *-ima* (Q), заметка Страка по PE22/156: «with many weak verbs (especially ta-causatives), lengthening was not possible and the a was retained, as with *tultaima* "*fetchable, summonable"». В лексиконе есть и Q *lacaltaima* «not possible to be kindled». Значит, *partaima* построено ровно по этому правилу. В модель же *tultaima* и *lacaltaima* не попадают: в Eldamo у них не указаны элементы (`qm_slovo.py aima --sub`: у обоих нет поля «элементы»), поэтому `shared/affixes.py` их не видит. Неоквенийские *failataima*, *tyastaima*, *nartaima*, *vétaima* и другие (`qm_slovo.py aima --sub`) следуют тому же правилу. Но и они в таблицу не входят. Неологизмы туда не берутся: у *-enca* шесть неоквенийских слов с указанными элементами (*cenenca*, *estelenca*, *lárenca*, *nostarenca*, *ofelmenca*, *sérenca*), а в таблице аффиксов у него 0 случаев.

**Что можно сделать** (предложение, не проверял на бэктесте):
- добавить в `morphophonology.py` правило «основа на *-ta*/*-ya* (слабый глагол) + *-ima* → *a* сохраняется», с источником PE22/156, так же как там уже записаны правила §6.1;
- или вручную вписать *tultaima* = *tulta-* + *-ima* и *lacaltaima* в случаи аффиксов;
- и, возможно, запретить стык, при котором пропадает больше одного звука основы, если в таблице нет примера с той же конечной парой звуков (*-ta*).

**Ещё одно.** *istima* у Страка — прилагательное «со свойством», с кратким гласным («wise… knowledgeable»), а не «-имое». Так что *ista- → istima* — пример другого значения суффикса. По одному этому слову выводить «у основ на *-a* гласный выпадает» рискованно.

**Для сравнения.** На засвидетельствованном *cen- + -ima* модель первым вариантом даёт *cénima* (0,75): верно. На моём *taima + -enca* — *taimenca* (0,78). Своих примеров у *-enca* нет, все слова с ним — неоквенья.
