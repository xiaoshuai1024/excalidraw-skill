#!/usr/bin/env node
/**
 * Post-render quality check. Verifies that every bound text label in a rendered
 * SVG is horizontally centered in its container box. Exits non-zero if any
 * label is off by more than the tolerance.
 *
 * Uses the SAME reliable method as the renderer's centering logic:
 *   offset = (first bound box's SVG text x) - (first bound box's scene cx)
 *   then every bound text's expected x = sceneCx + offset, compared to actual.
 *
 * Usage:
 *   node check.mjs <scene.excalidraw> <rendered.svg> [--tolerance 3]
 */
import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("Usage: node check.mjs <scene.excalidraw> <rendered.svg> [--tolerance N]");
  process.exit(2);
}
const scenePath = args[0];
const svgPath = args[1];
const tolIdx = args.indexOf("--tolerance");
const tolerance = tolIdx >= 0 ? parseFloat(args[tolIdx + 1]) : 3;

const scene = JSON.parse(readFileSync(scenePath, "utf-8"));
const svg = readFileSync(svgPath, "utf-8");

// tag residue check
const tagResidue = (svg.match(/\[\d+\]/g) || []).length;
if (tagResidue > 0) {
  console.error(`FAIL: ${tagResidue} centering tags "[N]" leaked into the SVG`);
  process.exit(1);
}

// Build element lookup
const els = {};
for (const e of scene.elements) {
  if (e && e.id) els[e.id] = e;
}

// Collect bound texts in scene order
const boundTexts = [];
for (const e of scene.elements) {
  if (!e || e.type !== "text" || !e.containerId) continue;
  const box = els[e.containerId];
  if (!box) continue;
  boundTexts.push({
    firstLine: (e.text || "").split("\n")[0].trim(),
    sceneCx: box.x + box.width / 2,
  });
}

if (boundTexts.length === 0) {
  console.log("OK (no bound text labels to check)");
  process.exit(0);
}

// Extract SVG middle-anchored texts in document order
const svgTextRe = /<text\s+x="([^"]+)"[^>]*text-anchor="middle"[^>]*>([^<]*)/g;
const svgTexts = [];
let m;
while ((m = svgTextRe.exec(svg)) !== null) {
  svgTexts.push({ x: parseFloat(m[1]), content: m[2].trim() });
}

// Compute offset from first bound box
const firstMid = svgTexts.find((t) => t.content.includes(boundTexts[0].firstLine));
if (!firstMid) {
  console.error(`FAIL: could not find first label "${boundTexts[0].firstLine}" in SVG`);
  process.exit(1);
}
const offset = firstMid.x - boundTexts[0].sceneCx;

// Check each bound text
let bad = 0;
let checked = 0;
let si = 0;
for (const bt of boundTexts) {
  const expected = bt.sceneCx + offset;
  // find matching svg text
  let found = null;
  while (si < svgTexts.length) {
    const st = svgTexts[si]; si++;
    if (bt.firstLine && (st.content.includes(bt.firstLine) || bt.firstLine.includes(st.content))) {
      found = st; break;
    }
  }
  if (!found) continue;
  const diff = found.x - expected;
  checked++;
  if (Math.abs(diff) > tolerance) {
    bad++;
    console.error(`  OFF: "${bt.firstLine}" expected x=${expected.toFixed(1)} got=${found.x.toFixed(1)} diff=${diff.toFixed(1)}`);
  }
}

if (bad > 0) {
  console.error(`\nFAIL: ${bad}/${checked} labels off by > ${tolerance}px. Re-render needed.`);
  process.exit(1);
}
console.log(`OK: ${checked}/${checked} labels centered (tolerance ${tolerance}px, offset ${offset.toFixed(1)})`);
process.exit(0);
