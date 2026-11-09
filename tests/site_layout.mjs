// Loads every page of the website (the landing page, the examples page,
// and the Hindi and Tamil landing pages) at phone, tablet, and desktop sizes in Chromium
// and WebKit (the engine behind Safari) and fails if the page is wider
// than the screen, if a phone lays it out at the wrong width (the page
// gets zoomed out), or if the page throws a script error.
//
// Needs Playwright:  npm install --no-save playwright@1.63.0
//                    npx playwright install --with-deps chromium webkit
// Run from the repo root:  node tests/site_layout.mjs

import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium, webkit } = require("playwright");

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const pages = ["index.html", "examples.html", "hi/index.html", "ta/index.html"].map((p) => ({
  name: p,
  url: pathToFileURL(path.join(root, "docs", ...p.split("/"))).href,
}));

const sizes = [
  { name: "phone 320", width: 320, height: 640, mobile: true },
  { name: "phone 360", width: 360, height: 740, mobile: true },
  { name: "phone 390", width: 390, height: 844, mobile: true },
  { name: "phone 412", width: 412, height: 915, mobile: true },
  { name: "tablet 768", width: 768, height: 1024, mobile: true },
  { name: "desktop 1280", width: 1280, height: 900, mobile: false },
];

const engines = [["chromium", chromium], ["webkit", webkit]];
const only = process.env.SITE_ENGINES ? process.env.SITE_ENGINES.split(",") : null;

let failures = 0;
for (const [engineName, engine] of engines) {
  if (only && !only.includes(engineName)) continue;
  let browser;
  try {
    browser = await engine.launch();
  } catch (err) {
    console.log(`SKIP ${engineName}: not installed (${err.message.split("\n")[0]})`);
    if (process.env.CI) failures++;
    continue;
  }
  for (const page of pages) {
  for (const size of sizes) {
    const options = { viewport: { width: size.width, height: size.height }, hasTouch: size.mobile, reducedMotion: "reduce" };
    // Firefox has no mobile mode; Chromium and WebKit both do.
    if (size.mobile) options.isMobile = true;
    const context = await browser.newContext(options);
    const tab = await context.newPage();
    const errors = [];
    tab.on("pageerror", (e) => errors.push(e.message));
    await tab.goto(page.url);
    await tab.waitForTimeout(300);
    const r = await tab.evaluate(() => {
      const vw = window.innerWidth;
      const wide = [];
      for (const el of document.querySelectorAll("body *")) {
        const box = el.getBoundingClientRect();
        if (!box.width) continue;
        let clipped = false;
        for (let a = el.parentElement; a; a = a.parentElement) {
          if (/hidden|clip|auto|scroll/.test(getComputedStyle(a).overflowX)) { clipped = true; break; }
        }
        if (!clipped && (box.right > vw + 1 || box.left < -1)) {
          wide.push(el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).join(".") : ""));
        }
      }
      return { vw, scrollWidth: document.documentElement.scrollWidth, wide: [...new Set(wide)].slice(0, 5) };
    });
    const problems = [];
    if (r.scrollWidth > r.vw + 1) problems.push(`page is ${r.scrollWidth}px wide on a ${r.vw}px screen`);
    if (size.mobile && r.vw !== size.width) problems.push(`laid out at ${r.vw}px instead of ${size.width}px, so the phone zooms the page out`);
    if (r.wide.length) problems.push(`sticks out of the screen: ${r.wide.join(", ")}`);
    if (errors.length) problems.push(`script errors: ${errors.join(" | ")}`);
    if (problems.length) {
      failures++;
      console.log(`FAIL ${engineName} ${page.name} ${size.name}: ${problems.join("; ")}`);
    } else {
      console.log(`ok   ${engineName} ${page.name} ${size.name}`);
    }
    await context.close();
  }
  }
  await browser.close();
}

if (failures) {
  console.log(`\n${failures} problem(s) found.`);
  process.exit(1);
}
console.log("\nEvery page fits every screen size.");
