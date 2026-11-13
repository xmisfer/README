import { createRequire } from 'node:module'; import fs from 'node:fs'; import { pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require(require.resolve('playwright', { paths: (process.env.NODE_PATH || '').split(':') }));
const [html, spec, out, ...ts] = process.argv.slice(2); const sc = JSON.parse(fs.readFileSync(spec, 'utf8'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: sc.width, height: sc.height } });
await p.goto(pathToFileURL(html).href); await p.evaluate(() => document.fonts.ready);
for (const [i, t] of ts.entries()) { await p.evaluate(([s, t]) => window.KZ.render(s, t), [sc, +t]); await p.screenshot({ path: `${out}-${i}.png` }); }
await b.close();
