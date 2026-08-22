#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max - Model Context Protocol (MCP) Server
Allows any MCP-compliant software (Cursor, Claude Desktop, Windsurf, Cline, Zed, LibreChat, AutoGen)
to interact with the August 2026 Multi-Agent Design System.
"""

import sys
import json
import io
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from core import search, search_stack
from tokens import DesignTokenEngine
from multi_agent.pipeline import MultiAgentPipeline


def create_tool_definitions():
    return [
        {
            "name": "run_multi_agent_design_pipeline",
            "description": "Execute the full August 2026 multi-agent design orchestration pipeline to produce complete design tokens, layout hierarchy, 2026 liquid glassmorphism + parallax components, and WCAG 2.2 AAA QA verification.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Natural language design request (e.g. 'Build a luxury fintech dashboard with dark glassmorphism and multi-depth parallax')"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Optional project name (e.g. 'Apex Finance')"
                    },
                    "stack": {
                        "type": "string",
                        "enum": ["html-tailwind", "react", "nextjs", "vue", "svelte", "swiftui", "flutter", "jetpack-compose", "shadcn"],
                        "description": "Target technology stack (default: html-tailwind)"
                    },
                    "persist": {
                        "type": "boolean",
                        "description": "Whether to persist design-system/MASTER.md and tokens to disk"
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "generate_design_tokens",
            "description": "Generate W3C DTCG standard design tokens, OKLCH high-gamut tonal color ramps, fluid clamp typography, and Tailwind v4 theme specifications.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "brand_primary": {"type": "string", "description": "Primary hex color (e.g. #6366F1)"},
                    "brand_secondary": {"type": "string", "description": "Secondary hex color (e.g. #06B6D4)"},
                    "brand_cta": {"type": "string", "description": "CTA accent color (e.g. #10B981)"},
                    "heading_font": {"type": "string", "description": "Heading font name (e.g. Plus Jakarta Sans)"},
                    "body_font": {"type": "string", "description": "Body font name (e.g. Inter)"},
                    "format": {
                        "type": "string",
                        "enum": ["w3c_json", "css_variables", "tailwind_v4", "typescript", "all"],
                        "description": "Output format"
                    }
                }
            }
        },
        {
            "name": "search_ui_intelligence",
            "description": "Search the BM25 design intelligence database across styles, colors, typography, charts, landing patterns, UX rules, and stack guidelines.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or topic"},
                    "domain": {
                        "type": "string",
                        "enum": ["style", "color", "typography", "chart", "landing", "product", "ux", "animation", "token", "agent"],
                        "description": "Search domain (auto-detected if omitted)"
                    },
                    "stack": {"type": "string", "description": "Specific tech stack search"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "audit_ui_accessibility",
            "description": "Run an automated WCAG 2.2 AAA & August 2026 quality audit for color contrast, reduced-motion fallbacks, GPU rendering, and layout stability.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "html_code": {"type": "string", "description": "HTML or component code to evaluate"}
                },
                "required": ["html_code"]
            }
        }
    ]


def handle_tool_call(name: str, arguments: dict) -> dict:
    if name == "run_multi_agent_design_pipeline":
        prompt = arguments.get("prompt", "")
        project_name = arguments.get("project_name")
        stack = arguments.get("stack", "html-tailwind")
        persist = arguments.get("persist", False)
        
        pipeline = MultiAgentPipeline()
        ctx = pipeline.run(prompt, project_name=project_name, target_stack=stack)
        
        output_files = {}
        if persist:
            output_files = pipeline.persist(ctx)
            
        return {
            "session_id": ctx.session_id,
            "project_name": ctx.project_name,
            "markdown_documentation": pipeline.format_markdown(ctx),
            "telemetry": [m.to_dict() for m in ctx.message_bus],
            "qa_verdict": ctx.get_artifact("qa_audit_report"),
            "persisted_files": output_files
        }

    elif name == "generate_design_tokens":
        engine = DesignTokenEngine(
            brand_primary=arguments.get("brand_primary", "#6366F1"),
            brand_secondary=arguments.get("brand_secondary", "#06B6D4"),
            brand_cta=arguments.get("brand_cta", "#10B981"),
            heading_font=arguments.get("heading_font", "Plus Jakarta Sans"),
            body_font=arguments.get("body_font", "Inter")
        )
        fmt = arguments.get("format", "all")
        if fmt == "w3c_json":
            return {"tokens": engine.generate_w3c_tokens()}
        elif fmt == "css_variables":
            return {"css": engine.export_css_variables()}
        elif fmt == "tailwind_v4":
            return {"tailwind": engine.export_tailwind_v4_theme()}
        elif fmt == "typescript":
            return {"typescript": engine.export_typescript_tokens()}
        else:
            return {
                "w3c_dtcg": engine.generate_w3c_tokens(),
                "css_variables": engine.export_css_variables(),
                "tailwind_v4": engine.export_tailwind_v4_theme(),
                "typescript": engine.export_typescript_tokens()
            }

    elif name == "search_ui_intelligence":
        query = arguments.get("query", "")
        domain = arguments.get("domain")
        stack = arguments.get("stack")
        if stack:
            return search_stack(query, stack)
        return search(query, domain)

    elif name == "audit_ui_accessibility":
        html_code = arguments.get("html_code", "")
        # Run QA agent audit
        from multi_agent.qa_agent import QAAgent
        from multi_agent.protocol import PipelineContext
        ctx = PipelineContext(session_id="audit_check", user_prompt="Audit", project_name="Audit", target_stack="html")
        ctx.set_artifact("code_bundle", {"html_tailwind": html_code})
        qa = QAAgent()
        qa.execute(ctx)
        return ctx.get_artifact("qa_audit_report", {})

    return {"error": f"Unknown tool: {name}"}


def run_stdio_server():
    """Run JSON-RPC MCP Server over standard input/output."""
    # Force UTF-8 for stdin/stdout
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stdin.encoding and sys.stdin.encoding.lower() != 'utf-8':
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "ui-ux-pro-max-mcp",
                            "version": "3.0.0"
                        }
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": create_tool_definitions()
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                tool_result = handle_tool_call(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(tool_result, indent=2, ensure_ascii=False)
                            }
                        ]
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
