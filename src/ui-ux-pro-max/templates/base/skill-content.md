# {{TITLE}}

{{DESCRIPTION}}
{{QUICK_REFERENCE}}
## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## August 2026 Multi-Agent Architecture & Design Intelligence

UI/UX Pro Max operates via a **Hierarchical Multi-Agent Pipeline** that coordinates 6 specialized agents:

1. **Supervisor Agent**: Intent decomposition, DAG planning, and delivery orchestration.
2. **Strategy Agent**: August 2026 visual trend synthesis, style priority (Liquid Chromatic Glass 2026, Bento 3.0, Parallax), and anti-pattern defense.
3. **Token Architect Agent**: Generates W3C DTCG standard tokens, OKLCH high-gamut scales, fluid clamp() typography, and Tailwind v4 themes.
4. **Layout Architect Agent**: Structures 12-column Bento 3.0 grids and 4-plane hardware-accelerated parallax depth planes.
5. **Component Engineer Agent**: Synthesizes production-ready components with sub-pixel specular borders and spring physics.
6. **QA Validation Agent**: Audits WCAG 2.2 AAA text contrast (7:1+), zero cumulative layout shifts (CLS), and prefers-reduced-motion safety.

---

## How to Use This {{SKILL_OR_WORKFLOW}}

When user requests UI/UX work (design, build, create, implement, review, fix, improve, tokens, parallax, glassmorphism), follow this workflow:

### Mode 1: Multi-Agent Design Orchestration (RECOMMENDED)

Execute the end-to-end multi-agent pipeline for complete tokens, layout, code, and QA:

```bash
python3 {{SCRIPT_PATH}} "<product_type> <style_keywords> <requirements>" --agent [-p "Project Name"] [--stack <stack>] [--persist]
```

**Example:**
```bash
python3 {{SCRIPT_PATH}} "luxury fintech SaaS dashboard with liquid glass and parallax" --agent -p "Apex Wealth" --persist
```

This command automatically:
1. Coordinates the 6 specialized agents on the typed message bus.
2. Generates W3C DTCG standard design tokens (`design-system/<slug>/tokens/tokens.json`).
3. Generates CSS Custom Properties and Tailwind v4 `@theme` directives (`design-system/<slug>/tokens/theme.css`).
4. Emits production-ready component code (`design-system/<slug>/components/index.html` & `Hero.tsx`).
5. Persists `design-system/<slug>/MASTER.md` as the Global Source of Truth.

### Mode 2: Design Tokens Generator (W3C DTCG & Tailwind v4)

Generate mathematically sound design tokens with high-gamut OKLCH palettes and fluid typography:

```bash
python3 {{SCRIPT_PATH}} --tokens --primary "#6366F1" --secondary "#06B6D4" --cta "#10B981" [--format css|tailwind|ts|w3c]
```

### Mode 3: Domain & Stack Intelligence Searches

Query the BM25 intelligence database across 10 specialized domains:

```bash
python3 {{SCRIPT_PATH}} "<keyword>" --domain <domain> [-n <max_results>]
```

| Domain | Focus | Example |
|---|---|---|
| `style` | 73+ UI styles with 2026 specs | `python3 {{SCRIPT_PATH}} "liquid glass 2026" --domain style` |
| `animation` | 2026 Parallax, spring easing, shaders | `python3 {{SCRIPT_PATH}} "scroll parallax" --domain animation` |
| `token` | W3C DTCG Token paths & variables | `python3 {{SCRIPT_PATH}} "glass tokens" --domain token` |
| `color` | 96 industry color palettes | `python3 {{SCRIPT_PATH}} "fintech dark" --domain color` |
| `typography` | 57 font pairings & clamp equations | `python3 {{SCRIPT_PATH}} "modern sans" --domain typography` |
| `landing` | 27 landing page conversion patterns | `python3 {{SCRIPT_PATH}} "bento showcase" --domain landing` |
| `ux` | 99 UX rules & anti-patterns | `python3 {{SCRIPT_PATH}} "prefers-reduced-motion" --domain ux` |
| `agent` | Multi-agent rules & handover gates | `python3 {{SCRIPT_PATH}} "validation gate" --domain agent` |

### Mode 4: Universal Model Context Protocol (MCP) Server

Connect any MCP-compatible AI assistant (Cursor, Claude Desktop, Windsurf, Cline, Zed):

```bash
python3 {{SCRIPT_PATH}} --mcp
```

### Mode 5: Live Interactive Design Studio & Web Workbench

Launch the visual design studio and REST API:

```bash
python3 {{SCRIPT_PATH}} --serve --port 8080
```

---

## August 2026 Core Rules for Flawless UI

### 1. Liquid Chromatic Glassmorphism
- **Backdrop Filter**: `backdrop-filter: blur(24px) saturate(190%)`.
- **Specular Inset Highlight**: `box-shadow: 0 20px 40px -15px rgba(0,0,0,0.5), inset 0 1px 1px 0 rgba(255,255,255,0.4)`.
- **Contrast**: Calculate background luminance to guarantee minimum 7:1 ratio (WCAG 2.2 AAA).

### 2. GPU-Accelerated Multi-Plane Parallax
- **Layers**: 4 discrete depth channels (0.10 ambient, 0.25 badges, 0.50 cards, 0.85 foreground pointer tilt).
- **CSS Scroll Timelines**: Use `animation-timeline: scroll()` or spring requestAnimationFrame with `translate3d`.
- **Reduced Motion**: Strictly provide `@media (prefers-reduced-motion: reduce) { transform: none; }`.

### 3. Icon & Structural Integrity
- **No Emojis as Icons**: Strictly use vectorized SVG icons from Lucide / Heroicons with 24x24 viewBox.
- **Cursor Pointer**: Add `cursor-pointer` to all clickable interactive cards, buttons, and badges.
- **Zero CLS**: Use fixed aspect ratios (`aspect-[16/9]`, `aspect-square`) or explicit min-height on all containers.
