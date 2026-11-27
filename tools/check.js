// QA for every built preview in docs/. Run: node tools/check.js   (after python3 tools/build.py)
// Checks: structure/SEO basics, preview safety (noindex + banner), links/anchors, mobile overflow,
// JS errors, button contrast, working lead forms, and saves 1440px + 390px screenshots to qa/.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..'), DOCS = path.join(ROOT, 'docs'), QA = path.join(ROOT, 'qa');
fs.mkdirSync(QA, { recursive: true });
const slugs = fs.readdirSync(DOCS).filter(d => fs.existsSync(path.join(DOCS, d, 'index.html')));

function lum([r, g, b]) { const f = c => { c /= 255; return c <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4) }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b) }
function ratio(a, b) { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05) }
const rgb = s => (s.match(/[\d.]+/g) || []).slice(0, 4).map(Number);

(async () => {
  const browser = await chromium.launch();
  const report = [];
  for (const slug of slugs) {
    const url = 'file://' + path.join(DOCS, slug, 'index.html');
    const r = { slug, pass: [], fail: [], warn: [] };
    const ok = (c, msg) => (c ? r.pass : r.fail).push(msg);
    for (const [name, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
      const page = await browser.newPage({ viewport: vp });
      const errs = [];
      page.on('pageerror', e => errs.push(e.message));
      page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|ERR_|net::/.test(m.text())) errs.push(m.text()) });
      await page.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => {});
      await page.waitForTimeout(1200);
      const d = await page.evaluate(() => {
        const q = s => [...document.querySelectorAll(s)];
        const ids = new Set(q('[id]').map(e => e.id));
        const badAnchors = q('a[href^="#"]').map(a => a.getAttribute('href')).filter(h => h.length > 1 && !ids.has(h.slice(1)));
        const blankNoRel = q('a[target=_blank]').filter(a => !/noopener/.test(a.rel)).length;
        const deadLinks = q('a').filter(a => !a.getAttribute('href') || a.getAttribute('href') === '#').length;
        const tel = q('a[href^="tel:"]').map(a => a.getAttribute('href'));
        const btns = q('.btn, button').filter(b => b.offsetParent).slice(0, 12).map(b => {
          const cs = getComputedStyle(b); let bg = cs.backgroundColor, el = b;
          while ((bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') && el.parentElement) { el = el.parentElement; bg = getComputedStyle(el).backgroundColor } if (bg === 'rgba(0, 0, 0, 0)') bg = 'rgb(255, 255, 255)';
          return { t: b.textContent.trim().slice(0, 30), fg: cs.color, bg, h: b.getBoundingClientRect().height };
        });
        return {
          title: document.title, desc: !!document.querySelector('meta[name=description]'),
          h1: q('h1').length, noindex: /noindex/.test(document.querySelector('meta[name=robots]')?.content || ''),
          banner: document.body.innerText.includes('Preview only'), badAnchors, blankNoRel, deadLinks, tel,
          leftover: /\{\{|\[PHONE\]|tel:0000/.test(document.documentElement.outerHTML),
          sw: document.documentElement.scrollWidth, vw: innerWidth, btns,
          forms: q('form[data-lead]').length, lang: document.documentElement.lang,
          imgsNoAlt: q('img:not([alt])').length, iframesNoTitle: q('iframe:not([title])').length,
        };
      });
      if (name === 'desktop') {
        ok(d.title && d.desc, 'title + meta description');
        ok(d.h1 === 1, `exactly one h1 (found ${d.h1})`);
        ok(d.noindex, 'preview is noindex');
        ok(d.banner, 'preview banner visible');
        ok(!d.leftover, 'no leftover placeholders');
        ok(d.badAnchors.length === 0, 'in-page links resolve' + (d.badAnchors.length ? ' ' + d.badAnchors : ''));
        ok(d.blankNoRel === 0, 'external links use rel=noopener');
        ok(d.deadLinks === 0, 'no empty links');
        ok(d.tel.every(t => /^tel:\+?\d{8,}$/.test(t)), 'phone links valid' + (d.tel.length ? ` (${[...new Set(d.tel)].join(', ')})` : ' (no phone, call-back form used)'));
        ok(d.imgsNoAlt === 0 && d.iframesNoTitle === 0, 'images/iframes labelled');
        ok(d.lang === 'en-AU', 'lang=en-AU');
        const low = d.btns.filter(b => ratio(rgb(b.fg), rgb(b.bg)) < 4.5 && ratio(rgb(b.fg), rgb(b.bg)) > 1.01).map(b => `${b.t} ${ratio(rgb(b.fg), rgb(b.bg)).toFixed(1)}:1`);
        (low.length ? r.warn : r.pass).push(low.length ? 'button contrast below 4.5: ' + low.join('; ') : 'button text contrast ≥ 4.5:1');
        // form test (preview mode shows success without sending)
        if (d.forms) {
          const sent = await page.evaluate(() => {
            const f = document.querySelector('form[data-lead]');
            f.querySelectorAll('input[required]').forEach(i => { i.value = i.type === 'tel' ? '0400 000 000' : 'QA Test' });
            f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', { cancelable: true }));
            return new Promise(res => setTimeout(() => res(f.classList.contains('sent')), 300));
          });
          ok(sent, 'lead form validates + shows success');
          const blocked = await page.evaluate(() => { const f = document.createElement('div'); return true });
        }
      } else {
        ok(d.sw <= d.vw + 1, `no horizontal scroll at 390px (${d.sw}px)`);
        const small = d.btns.filter(b => b.h < 44).map(b => `${b.t} ${Math.round(b.h)}px`);
        (small.length ? r.warn : r.pass).push(small.length ? 'tap targets under 44px: ' + small.join('; ') : 'tap targets ≥ 44px');
      }
      ok(errs.length === 0, `no JS errors (${name})` + (errs.length ? ': ' + errs.join(' | ') : ''));
      await page.reload({ waitUntil: 'load' }).catch(() => {}); await page.waitForTimeout(900);
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)) } scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)) });
      await page.screenshot({ path: path.join(QA, `${slug}-${name}.png`), fullPage: true });
      await page.close();
    }
    report.push(r);
  }
  await browser.close();
  let md = `# QA report\n\n_${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC · ${slugs.length} sites_\n\n`;
  for (const r of report) {
    md += `## ${r.slug} ${r.fail.length ? '❌' : r.warn.length ? '⚠️' : '✅'}\n` + r.fail.map(x => `- ❌ ${x}`).concat(r.warn.map(x => `- ⚠️ ${x}`), r.pass.map(x => `- ✅ ${x}`)).join('\n') + '\n\n';
  }
  fs.writeFileSync(path.join(QA, 'REPORT.md'), md);
  for (const r of report) console.log(`${r.fail.length ? 'FAIL' : r.warn.length ? 'WARN' : 'PASS'} ${r.slug}` + [...r.fail, ...r.warn].map(x => '\n   - ' + x).join(''));
})();
