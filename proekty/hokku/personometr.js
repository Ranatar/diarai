// personometr.js — прогнать свои стихи через «Персонометр-ПЛ7 „Душепродавец“» (inbox/html-generated/personometer-pl7.html).
// Функция performDetailedAnalysis (строки 827–989 страницы) прочитана целиком: чистая, без сети и DOM.
// Запуск: node proekty/hokku/personometr.js inbox/html-generated/personometer-pl7.html файл1.md [файл2.md …]
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const body = src.slice(826, 989).join('\n');           // строки 827–989
const analyze = new Function(body + '\nreturn performDetailedAnalysis;')();
for (const f of process.argv.slice(3)) {
  // из .md берём только строки стихов: без заголовков, пустых и служебных
  const text = fs.readFileSync(f, 'utf8').split('\n')
    .filter(l => l.trim() && !l.startsWith('#') && !l.startsWith('(') && !l.startsWith('—') && !l.startsWith('>'))
    .join('\n');
  const a = analyze(text);
  const st = a.severity === 0 ? 'ПОДОЗРИТЕЛЬНО' : a.severity <= 3 ? 'ТРЕВОГА' : a.severity <= 6 ? 'КРИТИЧНО' : 'БЕЗНАДЕЖНО';
  console.log(f.split('/').pop(), '| личность', a.score, '|', st, '|', a.diagnosis.join(' / ') || '—');
}
