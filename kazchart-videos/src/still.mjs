import { createRequire } from 'node:module'; import fs from 'node:fs'; import { pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require(require.resolve('playwright', { paths: (process.env.NODE_PATH || '').split(':') }));
const [engineHtml, specPath, out, t] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(pathToFileURL(engineHtml).href); await p.evaluate(() => document.fonts.ready);
await p.evaluate(([s, t]) => window.KZ.render(s, t), [spec, +t]); await p.screenshot({ path: out }); await b.close();
