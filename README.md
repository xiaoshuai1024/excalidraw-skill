# excalidraw-skill

> A 64-type diagram skill for AI coding agents. Hand-drawn style via Excalidraw engine. SVG + PNG.

[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![install](https://img.shields.io/badge/npx-skills%20add%20xiaoshuai1024%2Fexcalidraw--skill-2ea44f)](#install)

## What it draws

Every diagram type is rendered with the real Excalidraw engine — hand-drawn aesthetic, Virgil font, rough.js jitter. SVG stays editable (drag back into excalidraw.com).

![demo](assets/diagram.png)

**64 diagram types, 26 working examples.** The skill knows the professional notation for all of them:

| Category | Types | Examples |
|---|---|---|
| **UML Structure** | Class, Component, Deployment, Package, Composite Structure, Object | 5 |
| **UML Behavior** | Use Case, Activity, State Machine, Sequence, Communication, Interaction Overview, Timing | 3 |
| **Business** | Flowchart, BPMN, Data Flow Diagram | 1 |
| **Architecture** | Business Architecture, C4 Model, Deployment, System Landscape, 4+1 Views | 3 |
| **Data** | ER Diagram (Crow's Foot), Entity Lifecycle | 1 |
| **R&D Management** | RACI Matrix, Impact-Effort Matrix, Risk Matrix, Stakeholder Map, Value Stream Map, Kanban, Gantt, Burndown, Burnup, Org Chart | 6 |
| **DDD** | Event Storming, Context Map, Domain Architecture, Aggregate Design | 2 |
| **DevOps/SRE** | Git Branch Strategy, Alert Escalation, Technology Radar, NFR Tree, Capacity Planning | 3 |
| **API/Integration** | API Call Flow, Message Flow, OpenAPI Map | 1 |
| **Product** | User Journey Map, Kano Model, Business Model Canvas, Persona Card, Feature Tree, Competitive Matrix | 2 |
| **Security** | STRIDE Threat Model, Attack Surface | 1 |
| **Infrastructure** | Network Topology, CI/CD Pipeline | 1 |
| **Testing/Quality** | FMEA Fault Tree, Fishbone Diagram | 0 |
| **Other** | Mindmap, Decision Tree, Wardley Map, Empathy Map, Story Map, Service Blueprint, State Transition Matrix | 1 |

Full notation reference: [`references/all-diagram-types.md`](references/all-diagram-types.md).

## Install

```bash
npx skills add xiaoshuai1024/excalidraw-skill
```

Supports 72 agent types (Claude Code, Cursor, ZCode, OpenCode, Copilot, etc.). The installer interactively asks which agent(s) to install to. Or specify directly:

```bash
npx skills add xiaoshuai1024/excalidraw-skill --agent claude
npx skills add xiaoshuai1024/excalidraw-skill --agent claude,cursor,opencode
```

One-time setup (Playwright + Chromium, ~150MB):

```bash
bash skills/excalidraw/scripts/install.sh
```

## Usage

### With an agent

Install the skill, then just ask:

```
Draw a payment sequence diagram with activation boxes
Draw an ER diagram for an e-commerce system with Crow's Foot notation
Make a RACI matrix for our onboarding feature
Show me a Kano model analysis for our product features
```

The agent generates `.excalidraw` scene JSON and calls the renderer.

### CLI

```bash
python3 skills/excalidraw/scripts/render.py diagram.excalidraw
# → diagram.svg + diagram.png

python3 skills/excalidraw/scripts/render.py diagram.excalidraw --format svg
python3 skills/excalidraw/scripts/render.py diagram.excalidraw --scale 4
```

| Option | Effect |
|---|---|
| `--format svg\|png\|both` | Output format (default both) |
| `--output PATH` | Output path stem (no extension) |
| `--scale N` | PNG resolution (default 2, SVG is always vector) |
| `--keep-seed` | Preserve seeds for reproducible renders |

## How it works

```
.excalidraw (scene JSON)
  → headless Chromium loads @excalidraw/excalidraw (multi-CDN fallback)
  → restore() + convertToExcalidrawElements() normalizes the scene
  → exportToSvg() renders with the real engine
  → SVG file + PNG screenshot
```

Not a reimplementation — this is the real Excalidraw engine (rough.js, Virgil font, all visual details identical to excalidraw.com).

## Examples

Generated examples under `test/output/` (10 diagrams) and `test/all/output/` (16 diagrams), each with `.excalidraw` source + `.svg` + `.png`.

| File | Type |
|---|---|
| `test/diagrams/01-business-architecture.excalidraw` | 3-layer business architecture |
| `test/diagrams/02-deployment-architecture.excalidraw` | K8s deployment topology |
| `test/diagrams/03-flowchart.excalidraw` | Registration flowchart |
| `test/diagrams/04-sequence-diagram.excalidraw` | Payment sequence (UML) |
| `test/diagrams/05-er-diagram.excalidraw` | ER with Crow's Foot |
| `test/diagrams/06-state-machine.excalidraw` | Order state machine (UML) |
| `test/diagrams/07-mindmap.excalidraw` | Product planning mindmap |
| `test/diagrams/08-network-topology.excalidraw` | Network topology |
| `test/diagrams/09-user-journey.excalidraw` | User journey map |
| `test/diagrams/10-component-diagram.excalidraw` | Component diagram |
| `test/all/37-raci-matrix.excalidraw` | RACI matrix |
| `test/all/38-impact-effort-matrix.excalidraw` | Impact-effort prioritization |
| `test/all/39-risk-matrix.excalidraw` | Risk matrix |
| `test/all/40-stakeholder-map.excalidraw` | Stakeholder map |
| `test/all/41-value-stream-map.excalidraw` | Value stream map |
| `test/all/42-kanban-board.excalidraw` | Kanban board |
| `test/all/44-event-storming.excalidraw` | Event Storming (DDD) |
| `test/all/45-context-map.excalidraw` | Context Map (DDD) |
| `test/all/48-git-branch-strategy.excalidraw` | Git Flow |
| `test/all/50-system-landscape.excalidraw` | System landscape |
| `test/all/51-technology-radar.excalidraw` | Technology radar |
| `test/all/53-nfr-quality-tree.excalidraw` | NFR quality tree |
| `test/all/55-api-service-interaction.excalidraw` | API call flow |
| `test/all/58-kano-model.excalidraw` | Kano model |
| `test/all/60-business-model-canvas.excalidraw` | Business Model Canvas |
| `test/all/63-stride-threat-model.excalidraw` | STRIDE threat model |

## Repo structure

```
skills/excalidraw/           # skill body (installed by npx skills add)
  SKILL.md                   # agent instructions
  scripts/
    render.py                # core renderer
    render_template.html     # browser page
    install.sh               # dependency installer
  references/
    all-diagram-types.md     # 64 diagram types + notation reference
    element-templates.md     # JSON templates per element type
    examples/                # working .excalidraw scenes
test/                        # generators + output
  gen-diagrams.py            # generates 10 diagrams
  gen-all-diagrams.py        # generates 16 more
  render.test.mjs            # 11 integration tests
  diagrams/                  # scene JSONs (10)
  all/                       # scene JSONs (16)
assets/                      # README demo image
```

## License

MIT
