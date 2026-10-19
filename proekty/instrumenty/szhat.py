#!/usr/bin/env python3
"""Сжать кусок текста: убрать пустые строки и отступы.
python3 -I proekty/instrumenty/szhat.py вход выход [с_строки [по_строку]]
(строки считаются с 1, как в Read)."""
import sys
a = sys.argv[1:]
src, dst = a[0], a[1]
lo = int(a[2]) if len(a) > 2 else 1
hi = int(a[3]) if len(a) > 3 else None
lines = open(src, encoding='utf-8').read().split('\n')
part = lines[lo - 1:hi]
keep = [l.strip() for l in part if l.strip()]
open(dst, 'w', encoding='utf-8').write('\n'.join(keep) + '\n')
print(len(part), '->', len(keep))
