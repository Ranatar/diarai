# Слова вперемешку кириллицей и латиницей в inbox

*Третий, 2026-10-18, около 08:15. Инструмент `proekty/instrumenty/smesh.py`, сырой вывод `proekty/instrumenty/smesh-inbox.txt` (все .md/.txt/.html/.json до 5 МБ). Такие слова на глаз не видны, но ломают поиск, сортировку и проверку орфографии: «cкреплял» с латинской c не находится по запросу «скреплял».*

Всего 176 разных смешанных слов без учёта случая «і» (о нём ниже). После отсева ложных срабатываний осталось вот что.

## Стоит исправить (по убыванию пользы)

1. **Русский перевод введения в квенья для Eldamo** — `eldamo/src/main/webapp/l10n/ru/intro-quenya/*.html`, те же главы в `book/` и `Доклад/ERTP/intro-quenya/`. Латинские буквы внутри русских слов: **cкреплял, cкреплять, cуществительные, cм, сейчаc, глaгола, тaк, яe, oа**. Склейки с остатками английского: **напримерAlso, елthe, цветr, напримерe**. В квенья-слове **nilmё** последняя буква кириллическая (ё вместо ë). Это перевод, который будут искать, поэтому он важнее всего прочего.
2. **Цикл Аидана** (17 слов): `de_testimonio_tolkienis` — Mелькоровское, Меyer, реserved; `conspectus_parallelorum` — **Imenа** (в заголовке раздела I), reinкарнация; `historia_codicis_R` — Ionа, аввa, послеcоdex; `relatio_aidani_synthetica` (.html и .md) — NЕ, emendацией, геometrически, раsura, системa; `relatio_aidani_ru.md` — Дoадамиты; `tolkien_hills` — Тirnen, hísiё; `providence` — Гeррерин.
3. **Карты**: «**Eврейская** АОб» с латинской E — в `future_borders/cache/regions.json` (в ключе региона RU-YEV) и в `html-generated/maps/data/*.json`. Похоже, это пришло из исходных данных карты, я не проверял. В фильме «Великая Грибница» на экране этого не видно, но поиском регион не найти. Там же `maps/globe.html`: **Кавpайский** (латинская p).
4. Остальное (по одному-два слова): `gnostic-treatise-part8` predeterminированный; кампании Warcraft 3 — Риggс / РИGGС, МЕФИСТROT / МЕФИСТRОТ (два написания одного имени); `philosophy-graph-descriptions` — **Киerkegaard** (в восьми файлах), orудиями, Еternal, principiально, concу; `cthulhu_ussr_protocol` constатировать; `dasein-noir-revised` wrongна, мемeтическим; `elven-marxism-world` основывалиe; `feanor-lab-journal` Ниеннa; `gender_alchemy` Solvе, Аmore, Формula; `philosophy_network_interpretation` Маркc, историчеcки; `philosophy_graph_imp` Расчёt; `ulanov_reptile` Katя; `wittgenstein-hesychasm/10` силa; `topogenesis-expanded` генtrification; Hartman-Ingarden кategoriale; PS-страницы — inаковость, тerapevтической, suждения, Деwy; `descartes-deleuze` Татhandlung, разлиqие; `petra_dubrava_material_corpus` ноpители; philosynth docs — tokenы, ТАКЖE, киte, преflight, докax, онтологическаMetaphя.
5. `generative-bugs-features-research (1).md`: «ТАРГETTTTTTT…» (сорок с лишним T) — сбой генерации, оставленный в тексте. Возможно, нарочно: файл как раз об ошибках генерации.

## Латинская i вместо дореформенной «і» (отдельно)

`Synthesises-of-concepts/various/teubner.md`: 41 слово (iоны, Вслѣдствiе, Мнѣнiе, Отзывающiеся…), ещё 1 и 3 слова в двух файлах (библiотека, БЫТIЕ, редакцiей). Это систематическая замена: в дореформенном тексте «і» набрано латинской i (U+0069 вместо U+0456). Читается правильно, но поиск по «Мнѣніе» не находит «Мнѣнiе». В сценарии Грибницы и в «Присказках» везде стоит правильная кириллическая «і».

## Ложные срабатывания (не трогать)

Нотация конланга в `iass-spec` (mВ, nГ…); идентификаторы и куски кода (`cookieСеанса`, `безопасныеCookie`, `ЯЁA`/`яёa` в диапазонах регулярных выражений, `zА`, `Zа`, `ulей`); `philosphaira/doc/plan-next.md` (bвеса… — вероятно, экранированные `\b`); ЛORE в названии игровой механики, скорее всего, нарочно.
