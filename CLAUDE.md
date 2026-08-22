# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rick Jefferson Design is an AI-powered design intelligence and multi-agent orchestration system providing searchable databases of 73+ UI styles, 96 color palettes, 57 font pairings, W3C DTCG design tokens, 2026 animation patterns, and UX guidelines. It works as a skill/workflow for AI coding assistants, an MCP server, a CLI tool, and a live web design studio.

## Commands

### 1. Multi-Agent Design Orchestration
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --agent [-p "Project Name"] [--stack <stack>] [--persist]
```

### 2. Design Tokens Generator (W3C DTCG Standard)
```bash
python3 src/ui-ux-pro-max/scripts/search.py --tokens --primary "#6366F1" --secondary "#06B6D4" --cta "#10B981" [-f css|tailwind|ts|w3c|all]
```

### 3. BM25 Intelligence Search
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

Available domains: `style`, `animation`, `token`, `color`, `typography`, `chart`, `landing`, `product`, `ux`, `agent`, `icons`, `react`, `web`

### 4. Stack Search
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```
Available stacks: `html-tailwind` (default), `react`, `nextjs`, `astro`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

### 5. Universal MCP Server
```bash
python3 src/ui-ux-pro-max/scripts/search.py --mcp
```

### 6. Live Interactive Design Studio
```bash
python3 src/ui-ux-pro-max/scripts/search.py --serve [--port 8080]
```

---

## Architecture

```
src/ui-ux-pro-max/                # Source of Truth
├── data/                         # Canonical CSV databases
│   ├── styles.csv                # 73+ UI styles (including August 2026 styles)
│   ├── animations.csv            # 2026 motion, parallax, and shader tokens
│   ├── design-tokens.csv         # W3C DTCG standard token registry
│   ├── agent-rules.csv           # Multi-agent handover & validation gates
│   ├── colors.csv, typography.csv, products.csv, charts.csv, ...
│   └── stacks/                   # Stack-specific guidelines
├── scripts/
│   ├── search.py                 # Master CLI entry point
│   ├── core.py                   # BM25 + regex hybrid search engine
│   ├── tokens.py                 # W3C DTCG token generator & exporter
│   ├── mcp_server.py             # Model Context Protocol JSON-RPC server
│   ├── studio_server.py          # Live Design Studio web workbench & REST API
│   ├── design_system.py          # Design system generation & persistence
│   └── multi_agent/              # Hierarchical Multi-Agent System
│       ├── protocol.py           # Message bus, envelopes, and context
│       ├── supervisor_agent.py   # Intent parsing & DAG coordinator
│       ├── strategy_agent.py     # August 2026 trend & style specialist
│       ├── token_agent.py        # Design Token Architect
│       ├── layout_agent.py       # Bento 3.0 & Parallax Layout Architect
│       ├── engineering_agent.py  # Component & Motion Engineer
│       ├── qa_agent.py           # A11y, Performance & QA Validation
│       └── pipeline.py           # Master Multi-Agent Pipeline Runner
└── templates/
    ├── base/                     # Base templates (skill-content.md, quick-reference.md)
    └── platforms/                # Platform configs (claude.json, cursor.json, ...)

cli/                              # CLI installer (rick-jefferson-design / uipro on npm)
├── src/
│   ├── commands/                 # init, agent, tokens, design, mcp, serve, update
│   └── utils/                    # template rendering, github, logger
└── assets/                       # Bundled assets synced from src/
```

## Sync Rules

**Source of Truth:** `src/ui-ux-pro-max/`

When modifying files:

1. **Data & Scripts** - Edit in `src/ui-ux-pro-max/`:
   - `data/*.csv` and `data/stacks/*.csv`
   - `scripts/*.py` and `scripts/multi_agent/*.py`
   - Changes automatically available via symlinks in `.claude/`, `.shared/`

2. **Templates** - Edit in `src/ui-ux-pro-max/templates/`:
   - `base/skill-content.md` - Common SKILL.md content
   - `base/quick-reference.md` - Quick reference section
   - `platforms/*.json` - Platform-specific configs

3. **CLI Assets & Build** - Run sync and build:
   ```bash
   cp -r src/ui-ux-pro-max/data/* cli/assets/data/
   cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
   cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/
   cd cli && npm run build
   ```

4. **Reference Folders** - The CLI generates these from templates during `uipro init`.

## Prerequisites

Python 3.x and Node.js (for CLI packaging)
