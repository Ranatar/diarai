"""Другая исходная параметризация поверхности гаммы: луч из центра RGB-куба (в линейном? нет — в sRGB-координатах
куба, как у автора), направление d повернуто так, что серая диагональ вертикальна (белое — +z), красный — по +x.
Точка поверхности: c + d·0.5/max|d_i|; затем sRGB -> линейный -> OKLab.
Куб выпуклый, центр внутри — касательных лучей нет, плотность ограничена (кроме, возможно, чёрной вершины:
у кубического корня OKLab бесконечная производная в нуле).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otvet import lin2ok  # noqa

Z = np.array([1, 1, 1]) / np.sqrt(3)
X = np.array([2, -1, -1]) / np.sqrt(6)
Y = np.cross(Z, X)
ROT = np.stack([X, Y, Z])  # строки — оси «сферы» в координатах куба


def srgb2lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def cube_point(d):
    """d (n,3) на сфере (ось z — к белому) -> точка поверхности куба в sRGB [0,1]³."""
    c = d @ ROT  # в координаты куба
    return 0.5 + 0.5 * c / np.abs(c).max(1, keepdims=True)


def surf(d):
    """-> (L, a, b) в OKLab."""
    return lin2ok(srgb2lin(np.clip(cube_point(d), 0, 1)))
