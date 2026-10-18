// sverka.mjs — формулы «Кружочка» (2017–2020, руками автора) против движка html-generated/maps (2026).
// Запуск: node proekty/kruzhochek/sravnenie/sverka.mjs
// Формулы К. переписаны дословно из эскизов (файл указан у каждой); где взял из своего README — так и сказано.
// Сравнение — с точностью до подобия (сдвиг, масштаб, поворот, отражение): у К. свои оси и масштаб холста.
import * as M from '../../../inbox/html-generated/maps/projections.js';

const { sin, cos, tan, asin, acos, atan2, sqrt, abs, log, PI } = Math;
const D = PI / 180;
const LAST = {};

// К.: широта φ = π/2 − acos(z/|r|), долгота λ = atan2(x, y) — от оси y.
const K = {
  // Kruzhochek1_3-14 и др.: x6 = lambda; y6 = phi
  equirect: (l, p) => [l, p],
  // Kruzhochek1 и др.: x/(1−z) — стереографическая из северного полюса (центр карты — южный)
  stereo_S: (l, p) => [cos(p) * sin(l) / (1 - sin(p)), cos(p) * cos(l) / (1 - sin(p))],
  // Ламберт x·√(2/(1−z))
  laea_S: (l, p) => [cos(p) * sin(l) * sqrt(2 / (1 - sin(p))), cos(p) * cos(l) * sqrt(2 / (1 - sin(p)))],
  // Kruzhochek1_3-9-2 (закомментировано): (π/2−φ)·sin λ, −(π/2−φ)·cos λ — Постель, центр — северный полюс
  aeqd_N: (l, p) => [(PI / 2 - p) * sin(l), -(PI / 2 - p) * cos(l)],
  // Kruzhochek1_3-9-2, строки 160–164
  winkel3: (l, p) => {
    const phi1 = acos(2 / PI), alpha = acos(cos(p) * cos(l / 2)), s = sin(alpha) / alpha;
    return [(1 / 2) * (l * cos(phi1) + 2 * cos(p) * sin(l / 2) / s), (1 / 2) * (p + sin(p) / s)];
  },
  // Kruzhochek1_3-10-2, строки 160–177 (Sx, Sy — знаки λ и φ)
  vandergrinten: (l, p) => {
    const Sx = Math.sign(l) || 1, Sy = Math.sign(p) || 1;
    const theta = asin(abs(2 * p / PI));
    if (p === 0) return [l, 0];
    if (l === 0) return [0, Sy * PI * tan(theta / 2)];
    const G = cos(theta) / (sin(theta) + cos(theta) - 1), P = G * (2 / sin(theta) - 1);
    const A = (1 / 2) * abs(PI / l - l / PI), Q = A * A + G;
    return [Sx * PI * (A * (G - P * P) + sqrt(A * A * (G - P * P) ** 2 - (P * P + A * A) * (G * G - P * P))) / (P * P + A * A),
            Sy * PI * (P * Q - A * sqrt((A * A + 1) * (P * P + A * A) - Q * Q)) / (P * P + A * A)];
  },
  // Kruzhochek1-5-6-2 (2020), строки 203–207
  bonne45: (l, p) => {
    const phi1 = PI / 4, rho = 1 / tan(phi1) + phi1 - p, E = l * cos(p) / rho;
    return [rho * sin(E), 1 / tan(phi1) - rho * cos(E)];
  },
  // Kruzhochek1_3-14, строки 155–160
  polyconic: (l, p) => p === 0 ? [l, 0] :
    [(1 / tan(p)) * sin(l * sin(p)), p + (1 / tan(p)) * (1 - cos(l * sin(p)))],
  // из моего README (не из эскиза): λ cos φ
  sinusoidal: (l, p) => [l * cos(p), p],
  // из моего README: asin(cos φ sin λ), atan2(tg φ, cos λ)
  cassini: (l, p) => [asin(cos(p) * sin(l)), atan2(tan(p), cos(l))],
  // из моего README: ½·ln((1+sin λ cos φ)/(1−sin λ cos φ))
  tmerc: (l, p) => [0.5 * log((1 + sin(l) * cos(p)) / (1 - sin(l) * cos(p))), atan2(tan(p), cos(l))],
};

const PAIRS = [
  ['equirect', 'equirect', {}], ['stereo_S', 'stereographic', { phi1: -PI / 2 }], ['laea_S', 'laea', { phi1: -PI / 2 }],
  ['aeqd_N', 'aeqd', { phi1: PI / 2 }], ['winkel3', 'winkel3', {}], ['vandergrinten', 'vandergrinten', {}],
  ['bonne45', 'bonne', { phi1: PI / 4 }], ['polyconic', 'polyconic', {}], ['sinusoidal', 'sinusoidal', {}],
  ['cassini', 'cassini', {}], ['tmerc', 'tmerc', {}],
];

function grid(kid) {
  const pts = [];
  const lmax = kid === 'tmerc' || kid === 'cassini' ? 80 : 175;
  for (let L = -lmax; L <= lmax; L += 5) for (let F = -80; F <= 80; F += 5) {
    if (kid === 'stereo_S' && F > 60) continue;           // у полюса проекции — бесконечность
    if (kid === 'laea_S' && F > 80) continue;
    pts.push([L * D, F * D]);
  }
  return pts;
}

// Подобие: w ≈ a·z + b (a, b — комплексные), z или conj(z). Остаток — RMS / RMS(w).
function fit(Z, W) {
  const n = Z.length;
  const mean = (A) => A.reduce((s, q) => [s[0] + q[0] / n, s[1] + q[1] / n], [0, 0]);
  let best = Infinity;
  for (const refl of [false, true]) {
    const Zr = Z.map(([x, y]) => [x, refl ? -y : y]);
    const mz = mean(Zr), mw = mean(W);
    let nr = 0, ni = 0, d = 0, ww = 0;
    for (let i = 0; i < n; i++) {
      const zx = Zr[i][0] - mz[0], zy = Zr[i][1] - mz[1], wx = W[i][0] - mw[0], wy = W[i][1] - mw[1];
      nr += zx * wx + zy * wy; ni += zx * wy - zy * wx; d += zx * zx + zy * zy; ww += wx * wx + wy * wy;
    }
    const ar = nr / d, ai = ni / d;
    let r = 0;
    for (let i = 0; i < n; i++) {
      const zx = Zr[i][0] - mz[0], zy = Zr[i][1] - mz[1];
      const px = ar * zx - ai * zy, py = ar * zy + ai * zx;
      r += (px - (W[i][0] - mw[0])) ** 2 + (py - (W[i][1] - mw[1])) ** 2;
    }
    const res = sqrt(r / ww);
    if (res < best) best = res, LAST.v ={ scale: Math.hypot(ar, ai), angle: atan2(ai, ar) / D, refl };
  }
  return best;
}

console.log('формула К.\tдвижок maps\tточек\tостаток (RMS, доля)\tмасштаб\tповорот°\tотражение');
for (const [kid, mid, P] of PAIRS) {
  const Z = [], W = [];
  for (const [l, p] of grid(kid)) {
    const a = K[kid](l, p), b = M.project(mid, l, p, P);
    if ([...a, ...b].every(Number.isFinite)) { Z.push(a); W.push(b); }
  }
  const r = fit(Z, W), s = LAST.v;
  console.log(`${kid}\t${mid}\t${Z.length}\t${r.toExponential(2)}\t${s.scale.toFixed(4)}\t${s.angle.toFixed(1)}\t${s.refl}`);
}
