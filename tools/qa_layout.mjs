#!/usr/bin/env node
/**
 * Layout + legibility gate for a HyperFrames video, run on the live preview before any render.
 *
 *   npx hyperframes preview --background           (in the video folder)
 *   NODE_PATH=$(npm root -g) node tools/qa_layout.mjs <project-id> [--step 0.2] [--port 3002] [--from 0] [--to end]
 *
 * Seeks the composition every --step seconds and inspects the real DOM (what the renderer paints):
 *   OVERLAP   two text blocks overlap                                             -> FAIL
 *   COVERED   a shape or image is painted on top of text (e.g. a block over "CPU") -> FAIL
 *   CROWDED   text sits < 16 px from a box's border (inside or outside it)        -> FAIL
 *   SAFE      text outside y 240-1480 (frame 0 / the cover is exempt), or under the right rail (x > 940, y > 950) -> FAIL
 *   OFFFRAME  text cut by the frame edge for > 0.4 s (fly-ins/outs are shorter) -> FAIL
 *   SMALL     a screenshot's text renders under 26 px tall: give the <img> data-text-px="<text height in image px>" -> FAIL
 * An issue must hold for 3+ consecutive samples (0.6 s at --step 0.2) to count, so fly-ins and cuts don't trip it.
 * Captions (.cap) are allowed to sit over other things; text hidden by opacity < 0.15 is ignored.
 * Exit code 1 if anything fails. Creator rule (2026-10-27): this must PASS before the draft render.
 */
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(`--${k}`); return i >= 0 ? args[i + 1] : d; };
const project = args.find((a) => !a.startsWith("--") && args[args.indexOf(a) - 1]?.startsWith("--") !== true);
if (!project) { console.error("usage: node tools/qa_layout.mjs <project-id> [--step 0.2]"); process.exit(2); }
const STEP = +opt("step", 0.2), PORT = opt("port", "3002");
const MIN_GAP = 16, MIN_TEXT_PX = 26, SAFE_TOP = 240, SAFE_BOTTOM = 1480, RAIL_X = 940, RAIL_Y = 950;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(`http://localhost:${PORT}/api/projects/${project}/preview`, { waitUntil: "networkidle", timeout: 90000 });
await page.waitForFunction(() => window.__player && typeof window.__player.renderSeek === "function", null, { timeout: 60000 });
await page.evaluate(() => window.__player.enableRenderMode && window.__player.enableRenderMode());
const duration = await page.evaluate(() => +(window.__player.getDuration() || document.querySelector('[data-composition-id="main"]')?.dataset.duration));
const from = +opt("from", 0), to = +(opt("to", duration));

function inspect([t, C]) {
  const { MIN_GAP, MIN_TEXT_PX, SAFE_TOP, SAFE_BOTTOM, RAIL_X, RAIL_Y } = C;
  const root = document.querySelector('[data-composition-id="main"]');
  const R = root.getBoundingClientRect(), sc = R.width / 1080;
  const norm = (r) => ({ x: (r.left - R.left) / sc, y: (r.top - R.top) / sc, w: r.width / sc, h: r.height / sc });
  const visible = (el) => {
    let o = 1;
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === "none" || cs.visibility === "hidden") return 0;
      o *= +cs.opacity;
    }
    return o;
  };
  const label = (el) => (el.id ? `#${el.id}` : el.className && typeof el.className === "string" ? `${el.tagName.toLowerCase()}.${el.className.split(" ")[0]}` : el.tagName.toLowerCase());
  const path = (el) => { const p = []; for (let e = el; e && e !== root && p.length < 3; e = e.parentElement) if (e.id) p.push(`#${e.id}`); return p.reverse().join(" ") || label(el); };

  // text blocks: elements with their own non-empty text, measured by their text ranges
  const texts = [];
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const seen = new Map();
  for (let n; (n = tw.nextNode());) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (["SCRIPT", "STYLE", "TITLE"].includes(el.tagName)) continue;
    const op = visible(el); if (op < 0.15) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rects = [...r.getClientRects()].filter((q) => q.width > 2 && q.height > 2).map(norm);
    if (!rects.length) continue;
    const blk = el.closest("div,p,li,h1,h2,h3") || el;
    const key = blk;
    if (!seen.has(key)) seen.set(key, { el: blk, id: path(blk), text: "", rects: [], cap: !!blk.closest(".cap") });
    const e = seen.get(key); e.text += n.textContent.trim() + " "; e.rects.push(...rects);
  }
  for (const v of seen.values()) {
    const xs = v.rects.map((q) => q.x), ys = v.rects.map((q) => q.y);
    v.box = { x: Math.min(...xs), y: Math.min(...ys), w: Math.max(...v.rects.map((q) => q.x + q.w)) - Math.min(...xs), h: Math.max(...v.rects.map((q) => q.y + q.h)) - Math.min(...ys) };
    v.text = v.text.trim().slice(0, 40);
    texts.push(v);
  }
  const issues = [];
  const add = (kind, id, msg) => issues.push({ kind, id, msg });
  const inter = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));

  // OVERLAP
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const A = texts[i], B = texts[j];
    if (A.cap || B.cap || A.el.contains(B.el) || B.el.contains(A.el)) continue;
    for (const a of A.rects) for (const b of B.rects) if (inter(a, b) > 0.15 * Math.min(a.w * a.h, b.w * b.h)) { add("OVERLAP", `${A.id} / ${B.id}`, `"${A.text}" overlaps "${B.text}"`); break; }
  }
  // COVERED: probe points inside each text rect; the topmost element must be the text's own element (or its child)
  for (const T of texts) {
    if (T.cap) continue;
    let hit = null;
    for (const q of T.rects) for (const [fx, fy] of [[0.15, 0.5], [0.5, 0.5], [0.85, 0.5]]) {
      const px = R.left + (q.x + q.w * fx) * sc, py = R.top + (q.y + q.h * fy) * sc;
      if (px < 0 || py < 0 || px > innerWidth || py > innerHeight) continue;
      // walk down the paint stack: the first thing that paints must be the text itself
      // (a full-frame layer that paints above the text = another scene on top: the text is simply not on screen)
      let first = null, hidden = false;
      for (const e of document.elementsFromPoint(px, py)) {
        if (T.el.contains(e) || e.contains(T.el)) break;
        if (visible(e) < 0.15 || e.closest(".cap")) continue;
        const cs = getComputedStyle(e);
        const paints = e.tagName === "IMG" || e.tagName === "VIDEO" || (cs.backgroundColor && !cs.backgroundColor.endsWith(", 0)") && cs.backgroundColor !== "transparent");
        const er = e.getBoundingClientRect();
        if (er.width * er.height > 0.45 * R.width * R.height) { if (paints) { hidden = true; break; } continue; }
        if (paints && !first) first = e;
      }
      if (first && !hidden) hit = first;
    }
    if (hit) add("COVERED", T.id, `"${T.text}" is covered by ${path(hit)}`);
  }
  // CROWDED: bordered boxes vs text that isn't inside them by a margin, or sits just outside
  const boxes = [...root.querySelectorAll("*")].filter((e) => {
    const cs = getComputedStyle(e);
    return parseFloat(cs.borderTopWidth) >= 2 && !cs.borderTopColor.endsWith(", 0)") && visible(e) > 0.3 && e.getBoundingClientRect().width > 60;
  }).map((e) => ({ el: e, id: path(e), b: norm(e.getBoundingClientRect()) }));
  for (const T of texts) {
    if (T.cap || t < 0.3) continue;
    const tb = T.box;
    for (const B of boxes) {
      const b = B.b;
      const cx = tb.x + tb.w / 2, cy = tb.y + tb.h / 2;
      if (B.el.contains(T.el) && cx > b.x && cx < b.x + b.w && cy > b.y && cy < b.y + b.h) {
        const pad = Math.min(tb.x - b.x, b.x + b.w - (tb.x + tb.w), tb.y - b.y, b.y + b.h - (tb.y + tb.h));
        if (pad < MIN_GAP && pad > -tb.h) add("CROWDED", T.id, `"${T.text}" is ${pad.toFixed(0)} px from the inside of ${B.id}`);
        continue;
      }
      if (T.el.contains(B.el) || B.el.contains(T.el)) continue;
      const hOverlap = Math.min(tb.x + tb.w, b.x + b.w) - Math.max(tb.x, b.x), vOverlap = Math.min(tb.y + tb.h, b.y + b.h) - Math.max(tb.y, b.y);
      const gapY = Math.max(b.y - (tb.y + tb.h), tb.y - (b.y + b.h)), gapX = Math.max(b.x - (tb.x + tb.w), tb.x - (b.x + b.w));
      if ((hOverlap > 0 && gapY < MIN_GAP) || (vOverlap > 0 && gapX < MIN_GAP && gapX > -1)) {
        if (inter(tb, b) > 0.5 * tb.w * tb.h) continue;                       // drawn over it on purpose (a label on a card)
        add("CROWDED", T.id, `"${T.text}" is ${Math.max(gapX, gapY).toFixed(0)} px from ${B.id}`);
      }
    }
  }
  // SAFE + OFFFRAME (frame 0 = the cover template, exempt)
  for (const T of texts) {
    const b = T.box;
    const out = b.x + b.w <= 0 || b.y + b.h <= 0 || b.x >= 1080 || b.y >= 1920;
    if (out) continue;                                                      // fully off-frame = not on screen
    const off = b.x < 0 || b.y < 0 || b.x + b.w > 1080 || b.y + b.h > 1920;
    if (off) { add("OFFFRAME", T.id, `"${T.text}" is cut by the frame edge`); continue; }
    if (t < 0.3) continue;
    if (b.y < SAFE_TOP || b.y + b.h > SAFE_BOTTOM) add("SAFE", T.id, `"${T.text}" outside y ${SAFE_TOP}-${SAFE_BOTTOM} (y ${b.y.toFixed(0)}-${(b.y + b.h).toFixed(0)})`);
    if (b.x + b.w > RAIL_X && b.y + b.h > RAIL_Y) add("SAFE", T.id, `"${T.text}" under the right rail (x ${(b.x + b.w).toFixed(0)}, y ${(b.y + b.h).toFixed(0)})`);
  }
  // SMALL: screenshot text size
  for (const img of root.querySelectorAll("img[data-text-px]")) {
    if (visible(img) < 0.3) continue;
    const r = img.getBoundingClientRect(); if (!img.naturalWidth || r.width < 10) continue;
    const px = (+img.dataset.textPx) * (r.width / sc) / img.naturalWidth;
    if (px < MIN_TEXT_PX) add("SMALL", path(img), `screenshot text renders ${px.toFixed(0)} px (< ${MIN_TEXT_PX})`);
  }
  return issues;
}

const open = new Map(), found = [];
const MIN_SAMPLES = 3;      // an issue must hold this many samples in a row (0.6 s at 0.2 s) — fly-ins and cuts are shorter
const flush = (key, until) => { const o = open.get(key); if (o.n >= MIN_SAMPLES) found.push({ ...o, until }); open.delete(key); };
for (let t = from; t <= to + 1e-6; t = +(t + STEP).toFixed(3)) {
  await page.evaluate(async (t) => { await window.__player.renderSeek(t); if (window.__hfWaitForSeekCompletion) await window.__hfWaitForSeekCompletion(); }, t);
  await page.waitForTimeout(30);
  const issues = await page.evaluate(inspect, [t, { MIN_GAP, MIN_TEXT_PX, SAFE_TOP, SAFE_BOTTOM, RAIL_X, RAIL_Y }]);
  const now = new Set();
  for (const i of issues) {
    const key = `${i.kind}|${i.id}`; now.add(key);
    const o = open.get(key);
    if (o) { o.n++; o.last = t; } else open.set(key, { ...i, from: t, last: t, n: 1 });
  }
  for (const key of [...open.keys()]) if (!now.has(key)) flush(key, open.get(key).last);
}
for (const key of [...open.keys()]) flush(key, open.get(key).last);
await browser.close();

found.sort((a, b) => a.from - b.from);
for (const f of found) console.log(`${f.kind.padEnd(9)} ${f.from.toFixed(1)}-${f.until.toFixed(1)}s  ${f.msg}  [${f.id}]`);
console.log(`${(to - from).toFixed(1)}s checked every ${STEP}s: ${found.length ? `FAIL (${found.length})` : "PASS"}`);
process.exit(found.length ? 1 : 0);
