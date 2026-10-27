// Record a real website flow for /cte-demo, with a visible cursor and a timing log for zoom-follow.
//   node record_demo.cjs <steps.json> <outdir>
// steps.json: {"url": "...", "viewport": [1200, 1000], "steps": [
//   {"say": "open", "wait": 1500},
//   {"click": "text=Select a file", "file": "/abs/sample.jpg", "say": "upload"},
//   {"move": "css=selector", "say": "hover result"}, {"scroll": 400}, {"wait": 2000}]}
// Writes <outdir>/demo.webm and <outdir>/demo-log.json: [{t, say, box:{x,y,w,h}}] (t in seconds from video start)
// so the HyperFrames zoom can target each action's box. The cursor is a real DOM element injected into the page.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const out = process.argv[3];
  const [w, h] = cfg.viewport || [1200, 1000];
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1,
    recordVideo: { dir: out, size: { width: w, height: h } } });
  const p = await ctx.newPage();
  const t0 = Date.now();
  const log = [];
  const now = () => (Date.now() - t0) / 1000;
  await p.goto(cfg.url, { waitUntil: 'networkidle', timeout: 60000 });
  for (const t of [/reject/i, /accept all/i, /^accept$/i, /got it/i]) { try { await p.getByRole('button', { name: t }).first().click({ timeout: 700 }); break; } catch (e) {} }
  await p.addStyleTag({ content: `#cte-cursor{position:fixed;left:0;top:0;width:28px;height:28px;z-index:2147483647;pointer-events:none;transform:translate(${w/2}px,${h/2}px)}` });
  await p.evaluate(() => {
    const c = document.createElement('div'); c.id = 'cte-cursor';
    c.innerHTML = '<svg width="28" height="28" viewBox="0 0 22 30"><path d="M1 1 L1 24 L7 18 L11 28 L15 26 L11 17 L19 17 Z" fill="#111" stroke="#fff" stroke-width="1.6"/></svg>';
    document.body.appendChild(c);
    document.addEventListener('mousemove', (e) => { c.style.transform = `translate(${e.clientX}px,${e.clientY}px)`; });
  });
  await p.mouse.move(w / 2, h / 2);
  const boxOf = async (sel) => { const bb = await p.locator(sel).first().boundingBox(); return bb && { x: bb.x, y: bb.y, w: bb.width, h: bb.height }; };
  for (const s of cfg.steps) {
    if (s.move || s.click) {
      const sel = s.move || s.click;
      const bb = await boxOf(sel);
      if (bb) await p.mouse.move(bb.x + bb.w / 2, bb.y + bb.h / 2, { steps: 28 });
      log.push({ t: now(), say: s.say || sel, box: bb });
      if (s.click) {
        if (s.file) { const [fc] = await Promise.all([p.waitForEvent('filechooser'), p.mouse.down().then(() => p.mouse.up())]); await fc.setFiles(s.file); }
        else { await p.mouse.down(); await p.mouse.up(); }
      }
    }
    if (s.scroll) { await p.mouse.wheel(0, s.scroll); log.push({ t: now(), say: s.say || 'scroll', box: null }); }
    if (s.waitFor) { await p.locator(s.waitFor).first().waitFor({ timeout: 30000 }); log.push({ t: now(), say: s.say || 'ready', box: await boxOf(s.waitFor) }); }
    await p.waitForTimeout(s.wait || 900);
  }
  log.push({ t: now(), say: 'end', box: null });
  const vpath = await p.video().path();
  await ctx.close(); await b.close();
  fs.renameSync(vpath, `${out}/demo.webm`);
  fs.writeFileSync(`${out}/demo-log.json`, JSON.stringify(log, null, 1));
  console.log(JSON.stringify(log));
})();
