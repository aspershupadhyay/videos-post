// Renders scripts/cover.html to assets/shots/cover.png (frame 0 of the film) and renders/cover.png (the post's cover).
//   NODE_PATH=$(npm root -g) node scripts/make_cover.mjs
import { createRequire } from "module";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const P = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto("file://" + path.join(P, "scripts/cover.html"));
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
const boxes = await p.evaluate(() => ["k", "g", "h", "sub", "ph", "wm"].map((id) => { const r = document.getElementById(id).getBoundingClientRect(); return [id, Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }));
console.log(JSON.stringify(boxes));
await p.screenshot({ path: path.join(P, "assets/shots/cover.png") });
fs.mkdirSync(path.join(P, "renders"), { recursive: true });
fs.copyFileSync(path.join(P, "assets/shots/cover.png"), path.join(P, "renders/cover.png"));
await b.close();
