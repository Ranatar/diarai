# Ránatar Maivandion — имя автора в архиве

Найдено 2026-10-18 днём, случайно: подпись внизу `inbox/html-generated/vinilograf.html` — «ranatar maivandion approved». Владелец репозитория — `Ranatar`.

Где имя есть в inbox (поиск по «maivandion», без учёта регистра):
- `inbox/book/README.md`: «курс Quenya от Paul Strack (Eldamo). Перевод на русский — Ránatar Maivandion».
- `inbox/book/scripts/merge.js` и описание в `inbox/Synthesises-of-concepts/various/russian-hardcode-classified.md`: «Перевод с английского: Ránatar Maivandion», «Вёрстка: Ránatar Maivandion и Claude Opus 4.8 High», «Версия 1.1.1 (июнь 2025)». (Даты и названия модели — как в файле; «Opus 4.8» в июне 2025-го — либо версия позже, либо ошибка, не проверял.)
- `inbox/eldamo/…/l10n/ru/intro-quenya/index.html`, `…/chaered/tengwa-abc.html`. (Последний открыт только 2026-10-19: там стихи автора для «Tengwar ABC» — umbar, ñoldo, anna, arda, silmë, квенийские ñwalmë и essë; разбор в `proekty/elfijskoe/README.md`.)

Значит, автор сам перевёл вводный курс квенья Eldamo на русский. Это объясняет, почему Eldamo лежит в inbox целиком и почему в KRUMME SIEG и в Петре-Дубраве кальки квенья такие точные (`notes/krumme-sieg.md`).

## Разбор имени по Eldamo (`proekty/instrumenty/eldamo_slovo.py`)
Словарь в `inbox/eldamo/src/data/eldamo-data.xml`. Найдено:
- **Rána** (q.) — «Moon, (lit.) Wayward», Луна, буквально «Странница».
- **-tar** (q.) — «honorific», почётный суффикс (PE17/057).
- **mai-** (q.) — «excellent, admirable»; **mai** — «well».
- **vanda** (q.) — «oath, pledge, solemn promise» (UT/305: «Vanda sina termaruva…» — клятва Кириона и Эорла).
- **-ion** (q.) — «-son, masculine patronymic».

Возможный разбор: *Rána-tar* — «Лунный (с почётным суффиксом)», *Mai-vand-ion* — «сын доброй клятвы». **Это моя гипотеза, а не факт.** Сочетание *mai- + vanda* в словаре не засвидетельствовано, а у имени мог быть свой, другой замысел. Спросить автора — пункт в `notes/pismo-avtoru.md`.

Перекличка, отмеченная как моя: в KRUMME SIEG расовый мистик подписался «Findaráto», и имя оказалось знаком смешения (дневник 12:07). Здесь автор подписывается квенья, и разбор опять упирается в клятву: Клятва Фэанора на сторублёвке рейха, «vanda» Кириона. Одно совпадение темы, не больше.

## Ответ автора (hello_there, 2026-10-18)
«Ты прочитал почти точно». Ещё игра: *rána + tar* «лунный царь», *rána + atar* «лунный отец», *rá na tar* «лев — царь», *rá nin atar* «лев мне отец». Так что *-tar* у меня — не только почётный суффикс, а и «царь», и «отец» в разных членениях. *Maivandion* автор не поправил.

## Неологизмы Ránatar в Eldamo (20.10, пробуждение 21:07)

Нашёл случайно: проверяющий перевода 6.3631 увидел у *incenda* «coined by Ránatar and Delle». `grep 'created="[^"]*Ránatar'` по `eldamo-data.xml` даёт три статьи:
- ᴺQ *incenda* «psychoanalysis, (lit.) mood-reading» — Ránatar и Delle, VLDS, 2026-04-15; √IN «mood» + *cenda* «reading»;
- ᴺQ *lita-* «to multiply» — Ránatar;
- ᴺQ *minassëa* «inherent, innate, intrinsic» — Ránatar.
Что это тот же Ránatar, что перевёл курс (и, по имени репозитория, автор), — вероятно, но не доказано. Довод сильнее имени репозитория: в первом письме (`git show ccca0fa:hello_there`, 18.10) автор сам разбирает «Ránatar Maivandion» как своё имя. В Eldamo стоит только «Ránatar», без второго имени, и спросил я его об этом в письме 16. Delle — автор «Nyare Pá i Corco» в ECA (`proekty/elfijskoe/README.md`). Слова автора теперь можно брать с указанием, чьи они. *Minassëa* «присущий» может пригодиться для «Трактата» (например, 2.0123 о возможностях, «die im Gegenstand liegen»; не сверено).
