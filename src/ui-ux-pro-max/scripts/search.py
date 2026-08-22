#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max - August 2026 Multi-Agent Design Intelligence System
Usage:
    python search.py "<query>" [--domain <domain>] [--stack <stack>] [--max-results 3]
    python search.py "<query>" --agent [-p "Project Name"] [--stack react] [--persist]
    python search.py "<query>" --design-system [-p "Project Name"] [-f markdown|ascii] [--persist]
    python search.py --tokens [-p "Project Name"] [--primary "#6366F1"] [--format css|w3c|tailwind|ts|all]
    python search.py --mcp
    python search.py --serve [--port 8080]
"""

import argparse
import sys
import io
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system
from tokens import DesignTokenEngine
from multi_agent.pipeline import MultiAgentPipeline

# Force UTF-8 for stdout/stderr to handle emojis on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_output(result):
    """Format results for consumption (token-optimized)"""
    if "error" in result:
        return f"Error: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max Stack Guidelines")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max Search Results")
        output.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Source:** {result['file']} | **Found:** {result['count']} results\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Result {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI/UX Pro Max - August 2026 Design System & Multi-Agent Engine")
    parser.add_argument("query", nargs="?", default="", help="Search query or prompt")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Stack-specific search")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Multi-Agent Mode
    parser.add_argument("--agent", "-a", action="store_true", help="Run full August 2026 multi-agent design pipeline")
    
    # Design system generation
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate complete design system recommendation")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name for design system output")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown", "json", "css", "tailwind", "ts", "w3c", "all"], default="all", help="Output format")
    
    # Tokens generation
    parser.add_argument("--tokens", action="store_true", help="Generate W3C DTCG design tokens & theme files")
    parser.add_argument("--primary", type=str, default="#6366F1", help="Primary brand hex color")
    parser.add_argument("--secondary", type=str, default="#06B6D4", help="Secondary brand hex color")
    parser.add_argument("--cta", type=str, default="#10B981", help="CTA accent hex color")
    
    # MCP server mode
    parser.add_argument("--mcp", action="store_true", help="Start Model Context Protocol (MCP) JSON-RPC server")
    
    # Live Studio Server
    parser.add_argument("--serve", action="store_true", help="Start live interactive August 2026 Design Studio web app & REST API")
    parser.add_argument("--port", type=int, default=8080, help="Port for live studio server (default: 8080)")
    
    # Persistence (Master + Overrides pattern)
    parser.add_argument("--persist", action="store_true", help="Save design system to design-system/MASTER.md & token files")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override file in design-system/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory for persisted files")

    args = parser.parse_args()

    # Mode 1: MCP Server
    if args.mcp:
        from mcp_server import run_stdio_server
        run_stdio_server()
        sys.exit(0)

    # Mode 2: Live Studio Web Server
    if args.serve:
        from studio_server import run_studio_server
        run_studio_server(port=args.port)
        sys.exit(0)

    # Mode 3: Multi-Agent Pipeline
    if args.agent:
        pipeline = MultiAgentPipeline()
        ctx = pipeline.run(args.query, project_name=args.project_name, target_stack=args.stack)
        
        if args.persist:
            saved = pipeline.persist(ctx, base_dir=args.output_dir)
            print("=" * 65)
            print("✨ August 2026 Multi-Agent Pipeline Execution Complete")
            print("=" * 65)
            for k, v in saved.items():
                print(f"  📄 [{k.upper()}]: {v}")
            print("=" * 65)
            print("")

        if args.json or args.format == "json":
            print(json.dumps({
                "session_id": ctx.session_id,
                "project_name": ctx.project_name,
                "stack": ctx.target_stack,
                "artifacts": ctx.artifacts,
                "telemetry": [m.to_dict() for m in ctx.message_bus]
            }, indent=2, ensure_ascii=False))
        else:
            print(pipeline.format_markdown(ctx))
        sys.exit(0)

    # Mode 4: Tokens Generator
    if args.tokens:
        engine = DesignTokenEngine(
            brand_primary=args.primary,
            brand_secondary=args.secondary,
            brand_cta=args.cta,
            heading_font="Plus Jakarta Sans",
            body_font="Inter"
        )
        if args.format == "css":
            print(engine.export_css_variables())
        elif args.format == "tailwind":
            print(engine.export_tailwind_v4_theme())
        elif args.format == "ts":
            print(engine.export_typescript_tokens())
        elif args.format == "w3c" or args.format == "json" or args.json:
            print(json.dumps(engine.generate_w3c_tokens(), indent=2, ensure_ascii=False))
        else:
            print("/* CSS Custom Properties */")
            print(engine.export_css_variables())
            print("\n/* Tailwind v4 @theme */")
            print(engine.export_tailwind_v4_theme())
            print("\n/* TypeScript Tokens */")
            print(engine.export_typescript_tokens())
        sys.exit(0)

    # Mode 5: Design System
    if args.design_system:
        # Check if we should route through multi-agent pipeline for rich 2026 specs
        if args.format == "markdown":
            pipeline = MultiAgentPipeline()
            ctx = pipeline.run(args.query, project_name=args.project_name, target_stack=args.stack)
            if args.persist:
                pipeline.persist(ctx, base_dir=args.output_dir)
            print(pipeline.format_markdown(ctx))
        else:
            result = generate_design_system(
                args.query, 
                args.project_name, 
                args.format,
                persist=args.persist,
                page=args.page,
                output_dir=args.output_dir
            )
            print(result)
        sys.exit(0)

    # Mode 6: Stack Search
    if args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
        sys.exit(0)

    # Mode 7: Domain Search
    if args.query:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    else:
        parser.print_help()
