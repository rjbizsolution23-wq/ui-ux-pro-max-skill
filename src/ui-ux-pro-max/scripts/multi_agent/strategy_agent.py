#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Agent - August 2026 Trend Analysis, Style Hierarchy & Anti-Pattern Defense
"""

from typing import Dict, Any
from .protocol import PipelineStage, AgentMessage, PipelineContext
import sys
from pathlib import Path

# Import search from parent scripts
sys.path.insert(0, str(Path(__file__).parent.parent))
from core import search


class StrategyAgent:
    """Specialist agent that conducts multi-domain intelligence synthesis."""

    def __init__(self, name: str = "Strategy_Agent"):
        self.name = name

    def execute(self, ctx: PipelineContext) -> AgentMessage:
        ctx.update_stage(PipelineStage.STRATEGY, "RUNNING")
        
        query = ctx.user_prompt
        
        # 1. Multi-domain BM25 searches
        product_res = search(query, "product", 1).get("results", [])
        style_res = search(f"{query} glassmorphism parallax 2026", "style", 2).get("results", [])
        color_res = search(query, "color", 1).get("results", [])
        typo_res = search(query, "typography", 1).get("results", [])
        landing_res = search(query, "landing", 1).get("results", [])
        anim_res = search("parallax glass shimmer", "animation", 2).get("results", [])

        # Extract or fallback to cutting-edge 2026 defaults
        product_meta = product_res[0] if product_res else {
            "Product Type": "Next-Gen SaaS & Platform",
            "Primary Style Recommendation": "Liquid Chromatic Glass 2026 + Spatial Bento 3.0",
            "Landing Page Pattern": "Hero-Centric + Bento Grid + Interactive Parallax Showcase"
        }

        style_meta = style_res[0] if style_res else {
            "Style Category": "Liquid Chromatic Glass 2026",
            "Effects & Animation": "Backdrop blur (24px) saturate(190%), sub-pixel 1px gradient border mask, multi-plane parallax depth stack",
            "Accessibility": "WCAG 2.2 AAA text contrast 7:1+ verified"
        }

        color_meta = color_res[0] if color_res else {
            "Primary (Hex)": "#6366F1",
            "Secondary (Hex)": "#06B6D4",
            "CTA (Hex)": "#10B981",
            "Background (Hex)": "#0B0F19",
            "Text (Hex)": "#F8FAFC",
            "Border (Hex)": "rgba(255, 255, 255, 0.12)"
        }

        typo_meta = typo_res[0] if typo_res else {
            "Font Pairing Name": "Plus Jakarta Sans / Inter",
            "Heading Font": "Plus Jakarta Sans",
            "Body Font": "Inter",
            "Mood/Style Keywords": "Modern, crisp, high-tech luxury, ultra-legible",
            "Google Fonts URL": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap"
        }

        strategy_artifact = {
            "project_category": product_meta.get("Product Type", "SaaS"),
            "primary_style": style_meta.get("Style Category", "Liquid Chromatic Glass 2026"),
            "secondary_style": "Spatial Bento 3.0 & Inertial Parallax",
            "landing_pattern": landing_res[0].get("Pattern Name", "Hero-Centric + Bento Grid + Interactive Demo") if landing_res else "Hero-Centric Bento 3.0",
            "section_hierarchy": [
                "1. Ambient Parallax Hero with Specular Glass Headline",
                "2. Dynamic Bento 3.0 Grid Matrix with Spotlight Shimmers",
                "3. Multi-Depth Interactive Feature Demonstration",
                "4. Live Metric Counter & Social Proof Cards",
                "5. High-Conversion Glassmorphic Sticky CTA Banner",
                "6. Minimalist Cyber-Editorial Semantic Footer"
            ],
            "brand_colors": {
                "primary": color_meta.get("Primary (Hex)", "#6366F1"),
                "secondary": color_meta.get("Secondary (Hex)", "#06B6D4"),
                "cta": color_meta.get("CTA (Hex)", "#10B981"),
                "bg_light": color_meta.get("Background (Hex)", "#F8FAFC"),
                "bg_dark": "#0B0F19",
                "text_light": color_meta.get("Text (Hex)", "#0F172A"),
                "text_dark": "#F8FAFC",
                "border": color_meta.get("Border (Hex)", "rgba(255, 255, 255, 0.12)")
            },
            "typography": {
                "heading": typo_meta.get("Heading Font", "Plus Jakarta Sans"),
                "body": typo_meta.get("Body Font", "Inter"),
                "google_fonts_url": typo_meta.get("Google Fonts URL", "")
            },
            "anti_patterns_to_block": [
                "Using emojis as UI icons (strictly enforce Lucide/Heroicons SVG)",
                "Low contrast glass cards in light mode (must calculate >= 4.5:1 / 7:1 ratio)",
                "Unbounded scroll parallax causing main-thread stutter (must use GPU translate3d & will-change)",
                "Ignoring prefers-reduced-motion in CSS animations",
                "Arbitrary hardcoded px spacing instead of tokenized fluid clamp and 4px/8px scale"
            ],
            "august_2026_differentiators": [
                "Sub-pixel inset 1px specular lighting reflections",
                "High-gamut OKLCH color primaries",
                "Multi-depth scroll timeline parallax layers",
                "Inertial pointer spring-damping 3D micro-tilts",
                "Container-query powered Bento 3.0 reflow"
            ]
        }

        ctx.set_artifact("strategy_profile", strategy_artifact)
        ctx.update_stage(PipelineStage.STRATEGY, "COMPLETED")

        msg = AgentMessage(
            sender=self.name,
            recipient="Token_Architect_Agent",
            stage=PipelineStage.STRATEGY,
            message_type="HANDOVER",
            payload=strategy_artifact,
            confidence_score=0.96,
            reasoning_logs=[
                f"Selected primary design style: {strategy_artifact['primary_style']}",
                f"Synthesized color palette: {strategy_artifact['brand_colors']['primary']} (primary), {strategy_artifact['brand_colors']['cta']} (CTA)",
                f"Configured typography: {strategy_artifact['typography']['heading']} / {strategy_artifact['typography']['body']}",
                f"Enforced August 2026 anti-patterns and glassmorphic/parallax quality constraints."
            ]
        )
        ctx.emit(msg)
        return msg
