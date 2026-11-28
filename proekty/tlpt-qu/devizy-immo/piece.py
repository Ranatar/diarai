"""Девизы «Трактата» по правилу автора (inbox/immollimma/requests/tractatus/piece.py, motto):
ударный слог — четверть, безударный — восьмая, пауза после знака препинания — восьмая, последний слог — половинная;
высота — первая буква слога (индекс mod 7) как ступень лада части, от D4.
Для каждого положения: немецкий девиз, четыре доли тишины, квенийский девиз (proekty/tlpt-qu/devizy.py), пять долей тишины.
Функции syllables, letter_degree и тело motto переписаны из пьесы автора; в letter_degree добавлены долгие гласные квенья (á→a и т. д., как в devizy.py), иначе «í» давало бы ступень «a»."""
from kit.events import Piece

BEAT = 60.0 / 96
D = 62
IONIAN = [0, 2, 4, 5, 7, 9, 11]
LYDIAN = [0, 2, 4, 6, 7, 9, 11]
DORIAN = [0, 2, 3, 5, 7, 9, 10]
MIXO = [0, 2, 4, 5, 7, 9, 10]
AEOLIAN = [0, 2, 3, 5, 7, 8, 10]
PHRYG = [0, 1, 3, 5, 7, 8, 10]

SATZ = [
    (1, IONIAN, "Die !Welt ist !al-les, was der !Fall ist.", "!e-a na !il-qua ya !e-a nan-wi-!en-na."),
    (2, LYDIAN, "Was der !Fall ist, die !Tat-sa-che, ist das Be-!ste-hen von !Sach-ver-hal-ten.",
     "!ma-na !e-a nan-wi-!en-na, i !en-na, na !i-e !pan-wi-on en-gwa-!í-va."),
    (3, DORIAN, "Das !lo-gi-sche !Bild der !Tat-sa-chen ist der Ge-!dan-ke.", "!lil-le-a !em-ma !en-na-ron na !ten-na."),
    (4, MIXO, "Der Ge-!dan-ke ist der !sinn-vol-le !Satz.", "i !ten-na na ta-na-!lin-qua !e-ques."),
    (5, IONIAN, "Der !Satz ist ei-ne !Wahr-heits-funk-ti-!on der E-le-men-!tar-sät-ze.",
     "!e-ques na nai-!te-le-a !san-wa ú-!neh-ti-e e-!que-si-on"),
    (6, PHRYG, "Die !all-ge-mei-ne !Form der !Wahr-heits-funk-ti-!on ist:", "il-!quá-re-a !can-ta na-le-!san-wa-va na:"),
    (7, AEOLIAN, "Wo-!von", "I ú"),
]


def syllables(text):
    out = []
    for word in text.split():
        rest = word[-1] in ",.:"
        parts = word.rstrip(",.:").split("-")
        for i, s in enumerate(parts):
            out.append((s.lstrip("!"), s.startswith("!"), rest and i == len(parts) - 1))
    return out


def letter_degree(s):
    c = s[0].lower()
    c = {"ä": "a", "ö": "o", "ü": "u", "ß": "s", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}.get(c, c)
    return (ord(c) - ord("a")) % 7


def motto(p, text, mode, t, vel=0.55, gain=0.6):
    syl = syllables(text)
    tt = t
    for i, (s, stress, rest) in enumerate(syl):
        last = i == len(syl) - 1
        beats = 2.0 if last else (1.0 if stress else 0.5)
        m = D + mode[letter_degree(s)]
        d = beats * BEAT
        p.note("cl_sus", m, tt, d * (0.98 if last else 0.9), vel=vel + (0.06 if stress else 0.0), gain=gain,
               attack=0.03, release=0.5 if not last else 1.2, pan=-0.05)
        tt += d + (0.5 * BEAT if rest and not last else 0.0)
    return tt


def build(ctx):
    p = Piece("Devizy: de / qu", bpm=96, meter=(4, 4), key="D")
    t = 0.5
    for k, mode, de, qu in SATZ:
        p.mark(t, f"{k} de")
        t = motto(p, de, mode, t) + 4 * BEAT  # 2 доли съедал хвост (второй рендер: провал лишь до −37 дБ)
        p.mark(t, f"{k} qu")
        t = motto(p, qu, mode, t) + 5 * BEAT
    p.meta["length"] = t + 2.0
    return p
