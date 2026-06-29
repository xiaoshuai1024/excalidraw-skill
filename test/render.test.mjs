#!/usr/bin/env node
/**
 * Test suite for the Excalidraw render pipeline.
 *
 * Run:  node test/render.test.mjs
 *
 * These are black-box integration tests: they invoke scripts/render.py as a
 * subprocess and assert on its exit code, stdout, and the files it produces.
 * They do NOT import render.py directly, because the whole point is to verify
 * the CLI contract that users (and agents) rely on.
 *
 * The first failing test stops the suite (fail-fast) so you get the most
 * actionable error. Set RENDER_BIN to point at a different python if needed.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, rmSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const SKILL = join(ROOT, "skills", "excalidraw");
const RENDER = join(SKILL, "scripts", "render.py");
const FIXTURE = join(SKILL, "references", "examples", "flowchart.excalidraw");
const TMP = join(ROOT, ".test-tmp");

const PYTHON = process.env.PYTHON || "python3";

let passed = 0;
let failed = 0;

function run(args, { expectFail = false } = {}) {
  try {
    const out = execFileSync(PYTHON, [RENDER, ...args], {
      cwd: ROOT,
      encoding: "utf-8",
      timeout: 180000,
      stdio: ["ignore", "pipe", "pipe"],
    });
    if (expectFail) {
      throw new Error(`expected failure but render succeeded:\n${out}`);
    }
    return out;
  } catch (e) {
    if (expectFail) return (e.stderr || "") + (e.stdout || "");
    throw new Error(
      `render failed unexpectedly:\n${e.stderr || ""}\n${e.stdout || ""}`
    );
  }
}

function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  PASS  ${name}`);
  } catch (e) {
    failed++;
    console.error(`  FAIL  ${name}`);
    console.error(`        ${e.message.split("\n")[0]}`);
    if (process.env.NO_FAIL_FAST !== "1") {
      console.error(`\nStopping (fail-fast). ${passed} passed, ${failed} failed.`);
      process.exit(1);
    }
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

// --- setup ------------------------------------------------------------------
if (existsSync(TMP)) rmSync(TMP, { recursive: true, force: true });
mkdirSync(TMP, { recursive: true });

const out = (n) => join(TMP, n);

console.log("Excalidraw render pipeline — integration tests\n");

// --- tests ------------------------------------------------------------------

test("rejects a non-existent input file", () => {
  run([out("nope.excalidraw")], { expectFail: true });
});

test("rejects malformed JSON", () => {
  const bad = out("bad.excalidraw");
  writeFileSync(bad, "{ this is not json");
  const err = run([bad], { expectFail: true });
  assert(/invalid JSON/i.test(err), `expected 'invalid JSON' in error, got: ${err}`);
});

test("rejects a scene with no elements array", () => {
  const empty = out("no-elements.excalidraw");
  writeFileSync(empty, JSON.stringify({ type: "excalidraw" }));
  run([empty], { expectFail: true });
});

test("rejects an empty elements array", () => {
  const empty = out("empty-elements.excalidraw");
  writeFileSync(
    empty,
    JSON.stringify({ type: "excalidraw", elements: [] })
  );
  run([empty], { expectFail: true });
});

test("renders default (both SVG + PNG) from the example fixture", () => {
  run([FIXTURE, "--output", out("both")]);
  assert(existsSync(out("both.svg")), "missing both.svg");
  assert(existsSync(out("both.png")), "missing both.png");
});

test("produces an SVG with real content (not the empty 40x40 failure case)", () => {
  const svg = readFileSync(out("both.svg"), "utf-8");
  assert(/<path/.test(svg), "SVG has no <path> elements");
  assert(svg.length > 2000, `SVG suspiciously small (${svg.length} bytes)`);
  // The fixture has 4 text labels: Start, Validate, OK?, Save.
  assert(/Start/.test(svg), "SVG missing 'Start' text");
});

test("--format svg produces only SVG (no PNG)", () => {
  run([FIXTURE, "--format", "svg", "--output", out("svgonly")]);
  assert(existsSync(out("svgonly.svg")), "missing svgonly.svg");
  assert(!existsSync(out("svgonly.png")), "should NOT have produced a PNG");
});

test("--format png produces only PNG (no SVG)", () => {
  run([FIXTURE, "--format", "png", "--output", out("pngonly")]);
  assert(existsSync(out("pngonly.png")), "missing pngonly.png");
  assert(!existsSync(out("pngonly.svg")), "should NOT have produced an SVG");
});

test("--scale changes PNG file size (higher scale = larger file)", () => {
  run([FIXTURE, "--format", "png", "--scale", "1", "--output", out("s1")]);
  run([FIXTURE, "--format", "png", "--scale", "4", "--output", out("s4")]);
  const s1 = statSize(out("s1.png"));
  const s4 = statSize(out("s4.png"));
  assert(s4 > s1 * 2, `scale=4 PNG (${s4}) should be much larger than scale=1 (${s1})`);
});

test("randomizes seed each run (two renders differ)", () => {
  run([FIXTURE, "--format", "svg", "--output", out("r1")]);
  run([FIXTURE, "--format", "svg", "--output", out("r2")]);
  const h1 = md5(readFileSync(out("r1.svg"), "utf-8"));
  const h2 = md5(readFileSync(out("r2.svg"), "utf-8"));
  assert(h1 !== h2, "two renders produced identical SVG — seed not randomized");
});

test("printed output is the file path(s)", () => {
  const stdout = run([FIXTURE, "--format", "svg", "--output", out("pathout")]);
  assert(/pathout\.svg/.test(stdout), `stdout should name the output path, got: ${stdout}`);
});

function statSize(p) {
  return readFileSync(p).length;
}
// tiny md5 (good enough for "are these different") — uses node crypto
function md5(s) {
  return createHash("md5").update(s).digest("hex");
}

// --- summary ----------------------------------------------------------------
console.log(`\n${passed} passed, ${failed} failed.`);
process.exit(failed > 0 ? 1 : 0);
