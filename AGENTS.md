# AGENTS.md

Guidance for AI coding agents (Claude Code, Cursor, Copilot, ZCode, etc.) working in this repository.

## What this repo is

A single agent skill — `excalidraw` — that renders hand-drawn style diagrams using the real Excalidraw engine. It is distributed via the [skills](https://github.com/vercel-labs/skills) ecosystem (`npx skills add xiaoshuai1024/excalidraw-skill`) and installs into 70+ different agents' skill directories automatically.

## Repository layout

```
skills/excalidraw/        # the skill itself (this is what skills CLI installs)
  SKILL.md                # agent-facing instructions: when to use, how to build a scene
  scripts/
    render.py             # the renderer — the core of the skill
    render_template.html  # browser page that loads Excalidraw and exports to SVG
    install.sh            # one-time dependency installer (playwright + chromium)
  references/
    element-templates.md  # JSON templates for each element type
    examples/             # working .excalidraw scenes + a generator script
examples/                 # demo diagrams: gen-diagrams.py / gen-all-diagrams.py
                          #   + diagrams/ + all/ (scene JSONs) + output/ (rendered svg/png)
test/                     # integration tests + post-render checks
  render.test.mjs         #   run: node test/render.test.mjs
  check.mjs               #   run: node test/check.mjs <scene.excalidraw> <rendered.svg>
assets/diagram.{svg,png}  # rendered example shown in the README
```

The skill lives entirely under `skills/excalidraw/`. The repo root holds metadata, docs, tests, and rendered assets — none of it is installed into agents.

## How rendering works (important context)

`render.py` drives headless Chromium (via Playwright) which loads the official `@excalidraw/excalidraw` package from a CDN and calls `exportToSvg`. This is NOT a reimplementation of Excalidraw — it uses the real engine, so the hand-drawn look (rough.js jitter, Virgil font) is identical to excalidraw.com.

Key technical facts (these are non-obvious and load-bearing — do not "simplify" them without testing):

1. **CDN URL must be a single bundled module.** `render_template.html` tries CDNs in order: jsdelivr `+esm` (primary), esm.sh `?bundle`, skypack. The query (`+esm` / `?bundle`) is mandatory — without it, Excalidraw's many sub-imports become dozens of cascading CDN requests that blow past any timeout.
2. **`exportToSvg` takes an OBJECT** `{elements, appState, files}`, not positional args. Positional args silently return an empty 40x40 canvas in Excalidraw 0.18.
3. **`restore()` + `convertToExcalidrawElements()` are required** before export — hand-authored scenes miss fields the renderer needs, and text elements get dropped without this normalization.
4. **The Virgil font only exists inside exported SVGs** — it is not available in the bare page. `measureText` in the page falls back to serif (wrong metrics). Any text-positioning logic must account for this.

## Testing changes

```bash
node test/render.test.mjs
```

11 integration tests, fail-fast. They invoke `render.py` as a subprocess and assert on exit codes, output files, and SVG content. **Run these after any change to `render_template.html` or `render.py`** — the rendering pipeline is fragile and a "harmless" edit can silently break text rendering or produce an empty canvas.

## Making changes

- Edits to the skill go under `skills/excalidraw/`. Do not put skill code at the repo root.
- After editing, re-render the README example so `assets/diagram.{svg,png}` stays current:
  ```bash
  python3 skills/excalidraw/scripts/render.py skills/excalidraw/references/examples/cicd-microservice.excalidraw --output assets/diagram
  ```
- The `.excalidraw` example files have `seed: null` — the renderer injects random seeds. Do not hardcode seeds in examples.
- Keep the SKILL.md generic — no project/brand-specific colors or examples.
