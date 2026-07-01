#!/usr/bin/env node
/**
 * Ink-density / blank-diagram check.
 *
 * Renders every scene in examples/diagrams/ + examples/all/ to PNG and measures
 * how much non-white "ink" each image contains. A diagram that comes out nearly
 * blank (e.g. boxes filled #ffffff on a white canvas, or connectors that never
 * became real elements) drops well below the threshold. This catches whole
 * classes of bugs that structural checks (check.mjs) cannot see, because it
 * looks at the actual pixels a user would see.
 *
 * Run:
 *   node test/check-ink.mjs                 # render-on-the-fly + measure all
 *   node test/check-ink.mjs <dir>           # measure pre-rendered PNGs in <dir>
 *   node test/check-ink.mjs --threshold 4   # override the blank threshold (ink%)
 *
 * Exit code 1 if any diagram is below threshold (fail-fast on the first one,
 * unless NO_FAIL_FAST=1). Rendering is the slow part (~40s/diagram via CDN);
 * point the first arg at a directory of existing PNGs to skip it.
 *
 * Zero third-party deps: PNG decoding uses only node:zlib + node:fs.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync, mkdtempSync, rmSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { inflateSync } from "node:zlib";
import { tmpdir } from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const SKILL = join(ROOT, "skills", "excalidraw");
const RENDER = join(SKILL, "scripts", "render.py");
const PYTHON = process.env.PYTHON || "python3";

// A diagram is "blank" below this ink %. Tuned so genuinely sparse-but-valid
// diagrams (burndown chart ~5%, kano axes) pass, while broken ones (~2%) fail.
const DEFAULT_THRESHOLD = 4;

// ── minimal dependency-free PNG decoder ─────────────────────────────────────
// Reads IHDR + all IDAT chunks, inflates, and reverses PNG row filters
// (None/Sub/Up/Average/Paeth) to recover raw pixel bytes. Returns grayscale
// ink ratio via luminance.
function pngInkRatio(path) {
  const buf = readFileSync(path);
  const SIG = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  if (buf.slice(0, 8).compare(SIG) !== 0) throw new Error(`${path}: not a PNG`);
  let off = 8;
  let width, height, colorType;
  const idat = [];
  while (off < buf.length) {
    const len = buf.readUInt32BE(off); off += 4;
    const type = buf.toString("ascii", off, off + 4); off += 4;
    const data = buf.slice(off, off + len); off += len + 4; // +4 CRC
    if (type === "IHDR") {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      colorType = data[9];
    } else if (type === "IDAT") {
      idat.push(data);
    } else if (type === "IEND") break;
  }
  const channels = colorType === 2 ? 3 : colorType === 6 ? 4 : 1; // RGB/RGBA/gray
  const bpp = channels;
  const stride = width * bpp;
  const raw = inflateSync(Buffer.concat(idat));
  const out = Buffer.alloc(stride * height);
  let prev = Buffer.alloc(stride);
  let p = 0;
  for (let y = 0; y < height; y++) {
    const f = raw[p++];
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? out[y * stride + x - bpp] : 0;
      const b = prev[x];
      const c = x >= bpp ? prev[x - bpp] : 0;
      let v = raw[p++];
      if (f === 1) v = (v + a) & 0xff;
      else if (f === 2) v = (v + b) & 0xff;
      else if (f === 3) v = (v + ((a + b) >> 1)) & 0xff;
      else if (f === 4) {
        const pp = a + b - c;
        const pa = Math.abs(pp - a), pb = Math.abs(pp - b), pc = Math.abs(pp - c);
        v = (v + (pa <= pb && pa <= pc ? a : pb <= pc ? b : c)) & 0xff;
      }
      out[y * stride + x] = v;
    }
    prev = out.subarray(y * stride, y * stride + stride);
  }
  // sample pixels (step to stay fast on large images)
  let dark = 0, total = 0;
  const step = Math.max(1, Math.floor((width * height) / 40000));
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      const i = (y * width + x) * bpp;
      const gray = channels >= 3
        ? out[i] * 0.299 + out[i + 1] * 0.587 + out[i + 2] * 0.114
        : out[i];
      total++;
      if (gray < 240) dark++;
    }
  }
  return dark / total;
}

// ── collect scenes ──────────────────────────────────────────────────────────
function scenes() {
  const dirs = [join(ROOT, "examples/diagrams"), join(ROOT, "examples/all")];
  const out = [];
  for (const d of dirs) {
    if (!existsSync(d)) continue;
    for (const f of readdirSync(d)) {
      if (f.endsWith(".excalidraw")) out.push(join(d, f));
    }
  }
  return out;
}

function renderPNG(scenePath, outStem) {
  execFileSync(PYTHON, [RENDER, scenePath, "--format", "png", "--output", outStem], {
    cwd: ROOT, encoding: "utf-8", timeout: 180000,
    stdio: ["ignore", "pipe", "pipe"],
  });
  return `${outStem}.png`;
}

// ── main ────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  let threshold = DEFAULT_THRESHOLD;
  let preDir = null;
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    if (rest[i] === "--threshold" && rest[i + 1]) {
      threshold = parseFloat(rest[++i]);
    } else if (!rest[i].startsWith("--")) {
      preDir = rest[i]; // positional: directory of pre-rendered PNGs
    }
  }
  return { threshold, preDir };
}

function main() {
  const { threshold, preDir } = parseArgs(process.argv);
  const list = scenes();
  if (list.length === 0) {
    console.error("No .excalidraw scenes found under examples/. Nothing to check.");
    process.exit(1);
  }
  console.log(`Ink-density check — ${list.length} scenes (threshold ${threshold}%)\n`);

  // Use a temp dir for render-on-the-fly, unless a pre-rendered dir was given.
  let workDir = preDir;
  let cleanup = null;
  if (!workDir) {
    workDir = mkdtempSync(join(tmpdir(), "excal-ink-"));
    cleanup = () => rmSync(workDir, { recursive: true, force: true });
  }

  let passed = 0, failed = 0;
  for (const scene of list) {
    const name = scene.split("/").pop().replace(".excalidraw", "");
    let pngPath;
    if (preDir) {
      pngPath = join(preDir, `${name}.png`);
      if (!existsSync(pngPath)) {
        console.log(`  SKIP  ${name} (no pre-rendered PNG in ${preDir})`);
        continue;
      }
    } else {
      const stem = join(workDir, name);
      try {
        pngPath = renderPNG(scene, stem);
      } catch (e) {
        console.error(`  FAIL  ${name} — render error: ${(e.stderr || e.message || "").toString().split("\n")[0]}`);
        failed++;
        if (process.env.NO_FAIL_FAST !== "1") break;
        continue;
      }
    }
    let ink;
    try {
      ink = pngInkRatio(pngPath) * 100;
    } catch (e) {
      console.error(`  FAIL  ${name} — PNG decode error: ${e.message}`);
      failed++;
      if (process.env.NO_FAIL_FAST !== "1") break;
      continue;
    }
    if (ink < threshold) {
      console.error(`  FAIL  ${name} — ink ${ink.toFixed(1)}% < ${threshold}% (likely blank/broken)`);
      failed++;
      if (process.env.NO_FAIL_FAST !== "1") {
        console.error(`\nStopping (fail-fast). ${passed} passed, ${failed} failed.`);
        if (cleanup) cleanup();
        process.exit(1);
      }
    } else {
      console.log(`  PASS  ${name} — ink ${ink.toFixed(1)}%`);
      passed++;
    }
  }

  if (cleanup) cleanup();
  console.log(`\n${passed} passed, ${failed} failed.`);
  process.exit(failed > 0 ? 1 : 0);
}

main();
