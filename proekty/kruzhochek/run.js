// Запуск эскиза автора (inbox/нян/*.html) без браузера: canvas и DOM подменены.
// Рисуется один кадр (первый вызов requestAnimationFrame или прямой draw()).
// Результат: сырой PPM (P6).  node run.js in.html out.ppm [таймаут_мс]
// Эскизы прочитаны: внешних вызовов нет, используют только canvas/ImageData.
'use strict';
const fs = require('fs');
const vm = require('vm');

const [inp, out, tmo] = process.argv.slice(2);
const html = fs.readFileSync(inp, 'utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(m => m[1]);

let last = null;
const canvas = {
  width: 300, height: 150, style: {},
  getContext() {
    return {
      createImageData(w, h) { w = Math.floor(Math.abs(w)); h = Math.floor(Math.abs(h)); return { width: w, height: h, data: new Uint8ClampedArray(w * h * 4) }; },
      putImageData(img) { last = img; },
      clearRect() {}, fillRect() {},
    };
  },
};
const frames = [];
const sandbox = {
  Math, console: { log() {} },
  document: { getElementById: () => canvas, bgColor: '' },
  requestAnimationFrame(f) { frames.push(f); },
};
// vm-контекст давал 37 с на эскиз (глобальные переменные в нём медленные).
// Поэтому код эскиза оборачивается в функцию: его var становятся локальными.
// Это не песочница; оправдание — эскизы прочитаны (см. шапку). Таймаут — снаружи (timeout).
void vm; void tmo;
// Как в браузере: ошибка обрывает скрипт, но уже нарисованное остаётся.
const err = e => console.error('ошибка в эскизе: ' + String(e).slice(0, 100));
for (const s of scripts) {
  try {
    new Function('document', 'requestAnimationFrame', 'console', s)(
      sandbox.document, sandbox.requestAnimationFrame, sandbox.console);
  } catch (e) { err(e); }
}
if (!last && frames.length) { try { frames.shift()(); } catch (e) { err(e); } }
if (!last) { console.error('нет кадра'); process.exit(2); }

const { width: w, height: h, data } = last;
const bg = sandbox.document.bgColor === 'white' ? 255 : 0;
const body = Buffer.alloc(w * h * 3);
for (let p = 0, q = 0; p < w * h; p++, q += 4) {
  const a = data[q + 3];
  body[p * 3] = a ? data[q] : bg;
  body[p * 3 + 1] = a ? data[q + 1] : bg;
  body[p * 3 + 2] = a ? data[q + 2] : bg;
}
fs.writeFileSync(out, Buffer.concat([Buffer.from(`P6\n${w} ${h}\n255\n`), body]));
