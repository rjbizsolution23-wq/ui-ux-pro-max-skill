#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Comprehensive Test Suite for UI/UX Pro Max v3.0
Tests BM25 Search, Design Tokens, Multi-Agent Pipeline, MCP Server, and QA Validation.
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Add scripts directory
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"))

from core import search, search_stack, detect_domain, CSV_CONFIG
from tokens import DesignTokenEngine
from multi_agent.pipeline import MultiAgentPipeline
from multi_agent.protocol import PipelineStage
from mcp_server import create_tool_definitions, handle_tool_call


class TestCoreSearch(unittest.TestCase):
    def test_domain_detection(self):
        self.assertEqual(detect_domain("frosted glass blur"), "style")
        self.assertEqual(detect_domain("multi-plane scroll parallax"), "animation")
        self.assertEqual(detect_domain("w3c dtcg tokens"), "token")
        self.assertEqual(detect_domain("fintech color palette"), "color")
        self.assertEqual(detect_domain("modern serif font pairing"), "typography")

    def test_search_styles(self):
        res = search("Liquid Chromatic Glass", "style", 3)
        self.assertIn("results", res)
        self.assertGreaterEqual(res["count"], 1)
        first = res["results"][0]
        self.assertIn("Style Category", first)
        self.assertIn("Effects & Animation", first)

    def test_search_animations(self):
        res = search("parallax", "animation", 2)
        self.assertGreaterEqual(res["count"], 1)
        self.assertIn("CSS Implementation", res["results"][0])

    def test_search_tokens(self):
        res = search("glass", "token", 2)
        self.assertGreaterEqual(res["count"], 1)
        self.assertIn("W3C Token Path", res["results"][0])

    def test_search_stack(self):
        res = search_stack("responsive layout", "html-tailwind", 2)
        self.assertIn("results", res)
        self.assertGreaterEqual(res["count"], 1)


class TestDesignTokens(unittest.TestCase):
    def setUp(self):
        self.engine = DesignTokenEngine(
            brand_primary="#6366F1",
            brand_secondary="#06B6D4",
            brand_cta="#10B981"
        )

    def test_w3c_dtcg_schema(self):
        tokens = self.engine.generate_w3c_tokens()
        self.assertEqual(tokens.get("$schema"), "https://design-tokens.github.io/community-group/format/")
        self.assertIn("color", tokens)
        self.assertIn("typography", tokens)
        self.assertIn("glass", tokens)
        self.assertIn("parallax", tokens)
        self.assertIn("motion", tokens)

    def test_css_variables_export(self):
        css = self.engine.export_css_variables()
        self.assertIn("--color-primary: #6366F1;", css)
        self.assertIn("--glass-blur: 24px;", css)
        self.assertIn("--parallax-d1: 0.10;", css)
        self.assertIn(".dark", css)

    def test_tailwind_v4_export(self):
        tw = self.engine.export_tailwind_v4_theme()
        self.assertIn("@theme", tw)
        self.assertIn("--color-primary: #6366F1;", tw)
        self.assertIn("--ease-spring:", tw)

    def test_typescript_tokens_export(self):
        ts = self.engine.export_typescript_tokens()
        self.assertIn("export const designTokens =", ts)
        self.assertIn("export type DesignTokens =", ts)


class TestMultiAgentPipeline(unittest.TestCase):
    def test_pipeline_execution_and_handover(self):
        pipeline = MultiAgentPipeline()
        ctx = pipeline.run("Build a high-conversion AI SaaS platform with liquid glass and parallax", "Synapse AI")

        # Verify session & stages
        self.assertTrue(ctx.session_id.startswith("sess_"))
        self.assertEqual(ctx.stage_status[PipelineStage.INGESTION], "COMPLETED")
        self.assertEqual(ctx.stage_status[PipelineStage.STRATEGY], "COMPLETED")
        self.assertEqual(ctx.stage_status[PipelineStage.TOKEN_ARCHITECTURE], "COMPLETED")
        self.assertEqual(ctx.stage_status[PipelineStage.LAYOUT_ARCHITECTURE], "COMPLETED")
        self.assertEqual(ctx.stage_status[PipelineStage.COMPONENT_ENGINEERING], "COMPLETED")
        self.assertEqual(ctx.stage_status[PipelineStage.QA_VERIFICATION], "COMPLETED")

        # Verify artifacts
        self.assertIn("supervisor_brief", ctx.artifacts)
        self.assertIn("strategy_profile", ctx.artifacts)
        self.assertIn("token_registry", ctx.artifacts)
        self.assertIn("layout_architecture", ctx.artifacts)
        self.assertIn("code_bundle", ctx.artifacts)
        self.assertIn("qa_audit_report", ctx.artifacts)

        # Verify message bus communication
        self.assertEqual(len(ctx.message_bus), 6)
        senders = [m.sender for m in ctx.message_bus]
        self.assertEqual(senders, [
            "Supervisor_Agent",
            "Strategy_Agent",
            "Token_Architect_Agent",
            "Layout_Architect_Agent",
            "Component_Engineer_Agent",
            "QA_Validation_Agent"
        ])

        # Verify QA scorecard
        qa = ctx.get_artifact("qa_audit_report")
        self.assertEqual(qa["overall_status"], "APPROVED")
        self.assertEqual(qa["compliance_score"], "100/100")


class TestMCPServer(unittest.TestCase):
    def test_tools_listing(self):
        tools = create_tool_definitions()
        tool_names = [t["name"] for t in tools]
        self.assertIn("run_multi_agent_design_pipeline", tool_names)
        self.assertIn("generate_design_tokens", tool_names)
        self.assertIn("search_ui_intelligence", tool_names)
        self.assertIn("audit_ui_accessibility", tool_names)

    def test_mcp_tokens_call(self):
        res = handle_tool_call("generate_design_tokens", {"brand_primary": "#4F46E5"})
        self.assertIn("w3c_dtcg", res)
        self.assertIn("css_variables", res)

    def test_mcp_pipeline_call(self):
        res = handle_tool_call("run_multi_agent_design_pipeline", {"prompt": "Fintech dashboard with dark glass"})
        self.assertIn("markdown_documentation", res)
        self.assertIn("telemetry", res)
        self.assertIn("qa_verdict", res)


if __name__ == "__main__":
    unittest.main()
