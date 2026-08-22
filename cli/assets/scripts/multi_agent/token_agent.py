#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Architect Agent - W3C DTCG Design Token Generation, OKLCH Scales & Theme Export
"""

from typing import Dict, Any
from .protocol import PipelineStage, AgentMessage, PipelineContext
import sys
from pathlib import Path

# Import DesignTokenEngine from parent scripts
sys.path.insert(0, str(Path(__file__).parent.parent))
from tokens import DesignTokenEngine


class TokenArchitectAgent:
    """Architect agent responsible for synthesizing mathematically sound design tokens."""

    def __init__(self, name: str = "Token_Architect_Agent"):
        self.name = name

    def execute(self, ctx: PipelineContext) -> AgentMessage:
        ctx.update_stage(PipelineStage.TOKEN_ARCHITECTURE, "RUNNING")
        
        strategy = ctx.get_artifact("strategy_profile", {})
        colors = strategy.get("brand_colors", {})
        typo = strategy.get("typography", {})

        engine = DesignTokenEngine(
            brand_primary=colors.get("primary", "#6366F1"),
            brand_secondary=colors.get("secondary", "#06B6D4"),
            brand_cta=colors.get("cta", "#10B981"),
            bg_light=colors.get("bg_light", "#F8FAFC"),
            bg_dark=colors.get("bg_dark", "#0B0F19"),
            text_light=colors.get("text_light", "#0F172A"),
            text_dark=colors.get("text_dark", "#F8FAFC"),
            heading_font=typo.get("heading", "Plus Jakarta Sans"),
            body_font=typo.get("body", "Inter")
        )

        w3c_tokens = engine.generate_w3c_tokens()
        css_vars = engine.export_css_variables()
        tailwind_v4 = engine.export_tailwind_v4_theme()
        ts_tokens = engine.export_typescript_tokens()

        token_artifact = {
            "w3c_dtcg": w3c_tokens,
            "css_variables": css_vars,
            "tailwind_v4_theme": tailwind_v4,
            "typescript_tokens": ts_tokens,
            "color_scales": {
                "primary": colors.get("primary", "#6366F1"),
                "secondary": colors.get("secondary", "#06B6D4"),
                "cta": colors.get("cta", "#10B981"),
                "surface_dark": "#121420",
                "surface_light": "#FFFFFF"
            },
            "glass_recipes": {
                "card_light": "backdrop-filter: blur(24px) saturate(190%); background: rgba(255,255,255,0.72); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 20px 40px -15px rgba(0,0,0,0.08), inset 0 1px 1px 0 rgba(255,255,255,0.5);",
                "card_dark": "backdrop-filter: blur(24px) saturate(190%); background: rgba(18,20,32,0.68); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 20px 50px -10px rgba(0,0,0,0.6), inset 0 1px 1px 0 rgba(255,255,255,0.15);"
            },
            "parallax_depth_matrix": {
                "layer_1_ambient": 0.10,
                "layer_2_floating": 0.25,
                "layer_3_content": 0.50,
                "layer_4_foreground": 0.85
            }
        }

        ctx.set_artifact("token_registry", token_artifact)
        ctx.update_stage(PipelineStage.TOKEN_ARCHITECTURE, "COMPLETED")

        msg = AgentMessage(
            sender=self.name,
            recipient="Layout_Architect_Agent",
            stage=PipelineStage.TOKEN_ARCHITECTURE,
            message_type="HANDOVER",
            payload=token_artifact,
            confidence_score=0.99,
            reasoning_logs=[
                "Generated W3C DTCG standard design tokens.",
                "Computed 11-step perceptual tonal color ramps for primary, secondary, and CTA hues.",
                "Constructed fluid typography clamp scales for viewport range 320px - 1920px.",
                "Generated August 2026 specular glass recipes and 4-plane parallax depth factors."
            ]
        )
        ctx.emit(msg)
        return msg
