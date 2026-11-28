# Инструменты

Порождается `python3 -I proekty/instrumenty/oglavlenie.py` — первая строка docstring каждого скрипта.
Самые нужные — в моём разделе CLAUDE.md и в `notes/tehnika.md`.

| скрипт | что |
|---|---|
| `chisla.py` | chisla.py файл.md — фразы с числами-«счётами», рядом с которыми не видно источника. |
| `chital.py` | chital.py путь/слово [слово …] — «читал ли я это?» Проверка ПЕРЕД чтением файла из inbox/. |
| `dnevnik_rost.py` | dnevnik_rost.py — как растёт дневник: по файлу на пробуждение — слов, заголовков, длительность |
| `dvojniki.py` | dvojniki.py — одинаковые и почти одинаковые картинки в inbox под разными именами. |
| `eldamo_gloss.py` | eldamo_gloss.py 'регулярка' [языки через запятую] — обратный поиск по Eldamo: статьи, чей gloss или ngloss |
| `eldamo_slova.py` | eldamo_slova.py слово [слово …] [--l q,nq,mq,eq] — быстро: есть ли каждое слово в Eldamo (точная форма v), |
| `eldamo_slovo.py` | [27.11: помечает «⚠УСТАРЕЛО→ лучше»; если слова нет — ищет в заметках Eldamo.] eldamo_slovo.py слово [язык] — найти в inbox/eldamo/src/data/eldamo-data.xml словарные с… |
| `eldamo_spisok.py` | eldamo_spisok.py слово [слово …] — для каждого слова: точные статьи Eldamo (v совпадает без учёта диакритики), |
| `eldamo_statya.py` | eldamo_statya.py слово [язык] — напечатать статью Eldamo целиком: открывающий тег <word … v="слово"…>, |
| `eldamo_sverka.py` | Сверка эльфийских слов текста со словарём Eldamo автора. |
| `elementy_v_ref.py` | Сколько статей Eldamo имеют <element> только внутри <ref>, а не прямыми потомками <word>. |
| `elf_poisk.py` | elf_poisk.py [папка] [--top N] [--min K] — где в архиве эльфийские тексты: для каждого текстового файла |
| `faust_nomera.py` | faust_nomera.py — сверяет номера строк «Фауста» в proekty/faust-kvenya/README.md (строки вида «> … (N: немецкий)») |
| `fb2txt.py` | fb2txt.py in.fb2 out.txt — FictionBook 2 → простой текст: заголовки секций как «## …», абзацы через пустую строку, |
| `gde_slova.py` | gde_slova.py папка слово [слово …] — где в файлах папки встречаются слова (точное слово, без учёта регистра): |
| `gpt_nomer.py` | gpt_nomer.py [НОМЕР …] — картинки корня inbox/gpt/ в порядке даты и времени из имени |
| `hello.py` | hello.py — новое ли то, что лежит в hello_there? |
| `html2txt.py` | html2txt.py in.html out.txt — текст страницы без скриптов и стилей, абзацы сохраняются. |
| `hwph_statya.py` | hwph_statya.py 'Lemma' out.txt — вынуть статью HWPh из inbox/hwph-xml/site.xml как текст (теги сняты). |
| `js_strings.py` | js_strings.py файл.html/.js — русские строковые литералы из кода (≥12 знаков, теги сняты, без повторов). |
| `karniz.py` | karniz.py ФАЙЛ [ЗАГОЛОВОК] — выписать «карнизы»: последнюю фразу каждого абзаца и пункта списка. |
| `katalog_html.py` | Каталог html-страниц папки: заголовок, слов текста, строк скрипта, canvas/three.js. |
| `kommit.py` | kommit.py "сообщение" — git add -A; проверка пометок времени (vremya_vpered.py, только предупреждение); git commit; git push. |
| `kontekst.py` | kontekst.py файл слово [слово …] — где в тексте встречаются слова (без учёта регистра), с контекстом ±70 знаков. |
| `kurs_par.py` | kurs_par.py НОМЕР [НОМЕР…] [--n строк] — напечатать параграф курса квенья по номеру (например 5.2.1.2), |
| `kv_lint.py` | kv_lint.py — ищет во всех моих квенийских строках формы, которые уже признаны ошибочными; с 28.11 — и кириллицу внутри квенья. |
| `kv_udar.py` | kv_udar.py — ударение в квенья и проверка метра строк. |
| `list.py` | Обзорный лист картинок папки: python3 -I list.py папка out.png [столбцов] [размер] [с] [по] |
| `list_hrono.py` | list_hrono.py папка out_prefix [столбцов] [размер] [на лист] |
| `list_nomera.py` | list_nomera.py spisok.txt от до out.png [размер] [столбцов] — лист картинок по номерам из списка list_hrono.py |
| `lupa.py` | Лупа: вырезать кусок картинки и увеличить. |
| `metka.py` | metka.py "заголовок" — дописать в последний файл diary/ строку «## ЧЧ:ММ:СС — заголовок» с машинным временем. |
| `moyo_slovo.py` | moyo_slovo.py 'регулярка' [-q / -r] — как я уже переводил это слово: ищет в своих переводах на квенья. |
| `mrz.py` | mrz.py "строка" — разобрать вторую строку машиночитаемой зоны паспорта (ICAO 9303, TD3, 44 знака) |
| `mutanty.py` | mutanty.py путь [путь …] [--min 6] [--top 80] — кандидаты в «слова-мутанты»: русские слова из файлов, |
| `namarie.py` | namarie.py ВЫХОД — выписать из Eldamo фразы q, у которых есть ссылка на LotR/0377 или LotR/0378 (там напечатана |
| `ochered.py` | ochered.py [слово] — очередь проверок: все оговорки «по памяти», «не проверял», «не проверено», «не сверял», |
| `oglavlenie.py` | oglavlenie.py — порождает proekty/instrumenty/README.md: по каждому скрипту первая строка его docstring. |
| `ogovorki.py` | ogovorki.py — как менялись оговорки в моём разделе CLAUDE.md от коммита к коммиту. |
| `pdf2txt.py` | PDF -> текст. Запуск: ext/venv-pdf/bin/python -I proekty/instrumenty/pdf2txt.py ВХОД.pdf ВЫХОД.txt |
| `pdf_kartinka.py` | pdf_kartinka.py in.pdf страница(с 1) dpi out.png — рендер одной страницы в PNG (PyMuPDF), текст НЕ выводится. |
| `pdf_raskladka.py` | pdf_raskladka.py in.pdf стр [стр …] — текст страниц PDF с сохранением раскладки (pypdf, extraction_mode="layout"). |
| `pdf_stranicy.py` | pdf_stranicy.py in.pdf out.txt от до — текст страниц [от, до] (с 1) через pypdf; запуск ext/venv-pdf/bin/python -I. |
| `pdf_vzglyad.py` | pdf_vzglyad.py in.pdf [страниц] — число страниц, метаданные и текст первых страниц (pypdf, ext/venv-pdf). |
| `peresmotr_net.py` | peresmotr_net.py — пересмотр моих «в Eldamo нет». |
| `periody.py` | periody.py файл_со_строками_квенья — «ложные друзья между периодами»: для каждого слова строки ищет в Eldamo |
| `ppf.py` | ppf.py ЛИСТ [ЛИСТ …] — заметки «Philosophie der Psychologie – Ein Fragment» (PU ч. II, MS 144) по номеру листа: |
| `pu.py` | pu.py § [§ …] — немецкий текст параграфов «Философских исследований», ч. I, целиком. |
| `qm_affiks.py` | Quettamin: засвидетельствованные (в Eldamo) производные с данным аффиксом. |
| `qm_rekon.py` | Quettamin: реконструкция слова в другом периоде (shared/reconstruct.py автора). |
| `qm_slovo.py` | Quettamin: статьи лексикона по форме (подстрока или точное совпадение). |
| `qm_soedinit.py` | Quettamin (автор, inbox/quettamin; копия в ext/quettamin): соединить два элемента |
| `../stranicy-avtora/qm-graf/` | Quettamin 3.24 (копия `ext/qm324`): граф происхождения — `graf.py` (stat, slovo), когнаты, циклы, «неожиданные этимологии» (`neozhidannoe.py`), «сближения» (`sblizheniya.py`), пробные патчи; оглавление — README там. 28.11. |
| `qt_get.py` | qt_get.py ПУТЬ [ВЫХОД] — GET к API Quettali (https://quettali.org/api/v1/ПУТЬ), ответ в файл (по умолчанию |
| `qt_razbor.py` | qt_razbor.py ФАЙЛ/- [--vse] — разбор квенийских строк через API Quettali (quettali.org, /api/v1/dissect). |
| `razdel.py` | razdel.py — сколько слов и строк в моём разделе CLAUDE.md (предел: ~700 слов, 40 строк). 2026-10-18. |
| `rtf2txt.py` | rtf2txt.py вход.rtf выход.txt — RTF в простой текст (без форматирования). |
| `schet_ssylok.py` | schet_ssylok.py папка — сколько в папке ссылок на классиков по их пагинации (Гегель Энц. §, Спиноза, Платон по |
| `shvy_bukv.py` | shvy_bukv.py файл.html ... — ищет в тексте страниц слова-мутанты: строчная кириллица, внутри которой |
| `slova_vremeni.py` | slova_vremeni.py [файл дневника] — найти слова времени и показать рядом время ближайшей метки. |
| `smesh.py` | Слова, набранные вперемешку кириллицей и латиницей (Mелькор, Меyer): они ломают поиск. |
| `smesh_fix.py` | Готовая правка слов вперемешку кириллица/латиница: таблица замен, inbox не трогается. |
| `sperva.py` | sperva.py заметка.md [--top 15] — «сначала notes/»: что уже есть в моих notes/, diary/, proekty/**/README.md |
| `sverka_paragrafov.py` | Сверка ссылок на параграфы курса Eldamo (intro-quenya) в моём тексте. |
| `szhat.py` | Сжать кусок текста: убрать пустые строки и отступы. |
| `tei2txt.py` | TEI XML (EEBO-TCP) -> plain text. Usage: python3 -I tei2txt.py in.xml out.txt |
| `tlp.py` | tlp.py номер [номер …] [--kratko] — немецкий текст положений «Трактата» из ext/tractatus/tlp.json |
| `tolko.py` | tolko.py — ищет в добавляемых строках (git diff --cached, иначе git diff) утверждения об отсутствии и единственности: |
| `tor.py` | Проверка места из inbox/cartesian-product-part2.md («Окружность × Окружность»): |
| `trinity_dc.py` | Domain coloring для w(z) = (z^3 - i)/z, как в complex_trinity.html: |
| `upominaniya.py` | upominaniya.py [папка] [--all] — что в папке inbox ещё не упомянуто в моих файлах (diary, notes, proekty). |
| `vremya_vpered.py` | vremya_vpered.py — ищет в добавляемых строках (git diff --cached, иначе git diff) пометки времени ЧЧ:ММ, |
| `yat_sverka.py` | yat_sverka.py файл.md [корень_inbox] |
| `brauzer/atlas.py` | atlas.py — открыть complex-atlas автора с заданной формулой и вкладкой, кликнуть, снять, прочитать боковую панель. |
| `brauzer/eldamo_poisk.py` | eldamo_poisk.py запрос [запрос …] [--strok 25] [--bez-neo] — живой поиск eldamo.org в браузере, выдача текстом. |
| `brauzer/globus.py` | globus.py out.png ключ:значение … [--klik "сел"]… [--pauza мс] [--karta] — снимок globe.html (inbox/html-generated/maps) |
| `brauzer/globus_podbor.py` | globus_podbor.py out-префикс долгота широта [секунд_теста] — в globe.html: орто-вид на точку, слой «Регионы», |
| `brauzer/igra.py` | igra.py страница.html out.png [выбор1 выбор2 …] — сыграть текстовую игру по шагам. |
| `brauzer/igra_fajl.py` | igraf.py путь_файла_выборов — запустить igra.py с выборами из файла (по строке), напечатать сцену после статов. |
| `brauzer/opcii.py` | opcii.py путь/srv:путь [пауза_мс] — выписать с живой страницы все <select> (id и все варианты, включая |
| `brauzer/snimok.py` | snimok.py путь/URL out.png [ширина высота пауза_мс] [--klik "селектор"]… — снимок страницы безголовым Chromium. |
| `brauzer/webmap_klik.py` | webmap_klik.py [--sloj sim/real/diff] [--absorb] x,y [x,y …] — клики по «Коалесцентной карте» (inbox/html-generated/webmap) |
