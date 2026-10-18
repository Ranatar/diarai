// raster.mjs id W out.bin [json-параметры] — для каждого пикселя обратная проекция движка maps → (λ, φ).
// Пишет Float64 (λ, φ) по строкам сверху вниз; вне карты — NaN. Цвет даёт cvet.py (куб «Кружочка»).
import * as M from '../../../inbox/html-generated/maps/projections.js';
import { writeFileSync } from 'node:fs';

const [id0, Ws, out, Pj] = process.argv.slice(2);
const id = id0.replace(/!$/, '');          // «armadillo!» — только прямой ход (рассеяние), даже если обратная есть
const FORCE_SPLAT = id0.endsWith('!');
const W = +Ws, P = Pj ? JSON.parse(Pj) : {};
const D = Math.PI / 180;
// рамка по прямой проекции
let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
for (let L = -180; L <= 180; L += 1) for (let F = -90; F <= 90; F += 1) {
  const [x, y] = M.project(id, L * D, F * D, P);
  if (Number.isFinite(x) && Number.isFinite(y)) {
    x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
  }
}
const H = Math.max(1, Math.round(W * (y1 - y0) / (x1 - x0)));
const buf = new Float64Array(W * H * 2).fill(NaN);
let ok = 0;
const hasInv = !FORCE_SPLAT && typeof M.PROJECTIONS[id].inverse === 'function';
if (!hasInv) {  // обратной нет (Пирс) — рассеиваю точки сферы прямой проекцией, по 8 на пиксель
  const N = W * 8;
  for (let a = 0; a < N; a++) for (let b = 0; b <= N / 2; b++) {
    const lam = -Math.PI + 2 * Math.PI * (a + 0.5) / N, phi = -Math.PI / 2 + Math.PI * b / (N / 2);
    const [x, y] = M.project(id, lam, phi, P);
    if (!Number.isFinite(x) || !Number.isFinite(y)) continue;
    const i = Math.floor((x - x0) / (x1 - x0) * W), j = Math.floor((y1 - y) / (y1 - y0) * H);
    if (i < 0 || j < 0 || i >= W || j >= H) continue;
    const k = 2 * (j * W + i);
    if (Number.isNaN(buf[k])) ok++;
    buf[k] = lam; buf[k + 1] = phi;
  }
}
for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
  const x = x0 + (i + 0.5) / W * (x1 - x0), y = y1 - (j + 0.5) / H * (y1 - y0);
  if (!hasInv) continue;
  let r = M.unproject(id, x, y, P);
  // вне области обратная тоже что-то возвращает (у Молльвейде λ = 22 рад), а прямая линейна по λ и «подтверждает» — поэтому область проверяю явно
  let good = r && Number.isFinite(r[0]) && Number.isFinite(r[1]) &&
    Math.abs(r[0] - (P.lon0 || 0)) <= Math.PI + 1e-9 && Math.abs(r[1]) <= Math.PI / 2 + 1e-9;
  if (good) {  // обратная проекция возвращает что-то и вне карты — проверяю прямой
    const [xb, yb] = M.project(id, r[0], r[1], P);
    good = Number.isFinite(xb) && Math.hypot(xb - x, yb - y) < 1e-6 * (x1 - x0);
  }
  const k = 2 * (j * W + i);
  buf[k] = good ? r[0] : NaN; buf[k + 1] = good ? r[1] : NaN; ok += good;
}
writeFileSync(out, Buffer.from(buf.buffer));
console.log(`${id}\t${W}x${H}\tна карте ${(100 * ok / (W * H)).toFixed(1)}%`);
