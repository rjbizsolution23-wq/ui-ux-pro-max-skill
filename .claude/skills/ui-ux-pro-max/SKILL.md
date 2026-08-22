---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 67 styles, 96 palettes, 57 font pairings, 25 charts, 13 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
---
# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 67 styles, 96 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks. Searchable database with priority-based recommendations.

## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference

### 1. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio for normal text
- `focus-states` - Visible focus rings on interactive elements
- `alt-text` - Descriptive alt text for meaningful images
- `aria-labels` - aria-label for icon-only buttons
- `keyboard-nav` - Tab order matches visual order
- `form-labels` - Use label with for attribute

### 2. Touch & Interaction (CRITICAL)

- `touch-target-size` - Minimum 44x44px touch targets
- `hover-vs-tap` - Use click/tap for primary interactions
- `loading-buttons` - Disable button during async operations
- `error-feedback` - Clear error messages near problem
- `cursor-pointer` - Add cursor-pointer to clickable elements

### 3. Performance (HIGH)

- `image-optimization` - Use WebP, srcset, lazy loading
- `reduced-motion` - Check prefers-reduced-motion
- `content-jumping` - Reserve space for async content

### 4. Layout & Responsive (HIGH)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Minimum 16px body text on mobile
- `horizontal-scroll` - Ensure content fits viewport width
- `z-index-management` - Define z-index scale (10, 20, 30, 50)

### 5. Typography & Color (MEDIUM)

- `line-height` - Use 1.5-1.75 for body text
- `line-length` - Limit to 65-75 characters per line
- `font-pairing` - Match heading/body font personalities

### 6. Animation (MEDIUM)

- `duration-timing` - Use 150-300ms for micro-interactions
- `transform-performance` - Use transform/opacity, not width/height
- `loading-states` - Skeleton screens or spinners

### 7. Style Selection (MEDIUM)

- `style-match` - Match style to product type
- `consistency` - Use same style across all pages
- `no-emoji-icons` - Use SVG icons, not emojis

### 8. Charts & Data (LOW)

- `chart-type` - Match chart type to data type
- `color-guidance` - Use accessible color palettes
- `data-table` - Provide table alternative for accessibility

## How to Use

Search specific domains using the CLI tool below.

---


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

## How to Use This Skill

When user requests UI/UX work (design, build, create, implement, review, fix, improve, tokens, parallax, glassmorphism), follow this workflow:

### Mode 1: Multi-Agent Design Orchestration (RECOMMENDED)

Execute the end-to-end multi-agent pipeline for complete tokens, layout, code, and QA:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <style_keywords> <requirements>" --agent [-p "Project Name"] [--stack <stack>] [--persist]
```

**Example:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "luxury fintech SaaS dashboard with liquid glass and parallax" --agent -p "Apex Wealth" --persist
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
python3 skills/ui-ux-pro-max/scripts/search.py --tokens --primary "#6366F1" --secondary "#06B6D4" --cta "#10B981" [--format css|tailwind|ts|w3c]
```

### Mode 3: Domain & Stack Intelligence Searches

Query the BM25 intelligence database across 10 specialized domains:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Domain | Focus | Example |
|---|---|---|
| `style` | 73+ UI styles with 2026 specs | `python3 skills/ui-ux-pro-max/scripts/search.py "liquid glass 2026" --domain style` |
| `animation` | 2026 Parallax, spring easing, shaders | `python3 skills/ui-ux-pro-max/scripts/search.py "scroll parallax" --domain animation` |
| `token` | W3C DTCG Token paths & variables | `python3 skills/ui-ux-pro-max/scripts/search.py "glass tokens" --domain token` |
| `color` | 96 industry color palettes | `python3 skills/ui-ux-pro-max/scripts/search.py "fintech dark" --domain color` |
| `typography` | 57 font pairings & clamp equations | `python3 skills/ui-ux-pro-max/scripts/search.py "modern sans" --domain typography` |
| `landing` | 27 landing page conversion patterns | `python3 skills/ui-ux-pro-max/scripts/search.py "bento showcase" --domain landing` |
| `ux` | 99 UX rules & anti-patterns | `python3 skills/ui-ux-pro-max/scripts/search.py "prefers-reduced-motion" --domain ux` |
| `agent` | Multi-agent rules & handover gates | `python3 skills/ui-ux-pro-max/scripts/search.py "validation gate" --domain agent` |

### Mode 4: Universal Model Context Protocol (MCP) Server

Connect any MCP-compatible AI assistant (Cursor, Claude Desktop, Windsurf, Cline, Zed):

```bash
python3 skills/ui-ux-pro-max/scripts/search.py --mcp
```

### Mode 5: Live Interactive Design Studio & Web Workbench

Launch the visual design studio and REST API:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py --serve --port 8080
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
