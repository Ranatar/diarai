// filosofometr.js файл… — прогнать тексты через performPhilosophicalAnalysis() из
// inbox/html-generated/philosophometer.html (функция вынимается из страницы как есть, без правок).
// 2026-10-18, пробуждение 21:20: измерить себя прибором автора.
const fs = require('fs');
const html = fs.readFileSync('/home/diarai/diarai/inbox/html-generated/philosophometer.html', 'utf8');
const start = html.indexOf('function performPhilosophicalAnalysis');
const end = html.indexOf('function updateDeviceState');
const fn = new Function(html.slice(start, end) + '; return performPhilosophicalAnalysis;')();
const status = s => s === 0 ? 'ПРИЕМЛЕМО' : s <= 3 ? 'ПОДОЗРИТЕЛЬНО' : s <= 6 ? 'ПСЕВДОФИЛОСОФИЯ' : 'ШАРЛАТАНСТВО';
// --reiting папка [N] — обойти .md/.txt папки и показать N худших по тяжести и баллу
if (process.argv[2] === '--reiting') {
  const path = require('path'); const out = [];
  const walk = d => { for (const e of fs.readdirSync(d, {withFileTypes: true})) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p); else if (/\.(md|txt)$/.test(e.name)) { const a = fn(fs.readFileSync(p, 'utf8')); out.push([a.severity, a.score, p, a.diagnosis]); } } };
  walk(process.argv[3]);
  out.sort((x, y) => y[0] - x[0] || y[1] - x[1]);
  const n = +(process.argv[4] || 10);
  const st = {}; for (const o of out) st[status(o[0])] = (st[status(o[0])] || 0) + 1;
  console.log('файлов', out.length, JSON.stringify(st));
  for (const [sv, sc, p, d] of out.slice(0, n)) console.log(`${status(sv)} (${sv}, ${sc})  ${p}\n   · ` + d.join('\n   · '));
  process.exit(0);
}
for (const f of process.argv.slice(2)) {
  const t = fs.readFileSync(f, 'utf8');
  const a = fn(t);
  console.log(`== ${f}\n   балл ${a.score}, тяжесть ${a.severity} → ${status(a.severity)}; слов ${a.wordCount}, предложений ${a.sentenceCount}`);
  for (const d of a.diagnosis) console.log('   · ' + d);
}
