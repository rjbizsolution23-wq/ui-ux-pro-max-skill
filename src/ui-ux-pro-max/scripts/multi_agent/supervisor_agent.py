#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Supervisor Agent - Intent Decomposition, DAG Routing & Delivery Orchestration
"""

import re
from typing import Dict, Any
from .protocol import PipelineStage, AgentMessage, PipelineContext


class SupervisorAgent:
    """Master orchestrator that directs the multi-agent design pipeline."""

    def __init__(self, name: str = "Supervisor_Agent"):
        self.name = name

    def execute(self, ctx: PipelineContext) -> AgentMessage:
        ctx.update_stage(PipelineStage.INGESTION, "RUNNING")
        
        prompt = ctx.user_prompt.lower()
        
        # 1. Detect Stack
        stack = ctx.target_stack or "html-tailwind"
        if "react" in prompt:
            stack = "react"
        elif "next" in prompt:
            stack = "nextjs"
        elif "vue" in prompt:
            stack = "vue"
        elif "svelte" in prompt:
            stack = "svelte"
        elif "swiftui" in prompt:
            stack = "swiftui"
        elif "flutter" in prompt:
            stack = "flutter"
        elif "compose" in prompt:
            stack = "jetpack-compose"
        ctx.target_stack = stack

        # 2. Extract Project Intent & Domain
        is_dark_mode_requested = any(kw in prompt for kw in ["dark", "oled", "night", "black"])
        is_glassmorphism_requested = any(kw in prompt for kw in ["glass", "frosted", "blur", "translucent", "specular"]) or True
        is_parallax_requested = any(kw in prompt for kw in ["parallax", "scroll", "depth", "spring", "tilt", "3d", "multi-plane"]) or True
        
        execution_plan = {
            "project_name": ctx.project_name,
            "target_stack": stack,
            "theme_preference": "dark" if is_dark_mode_requested else "adaptive_light_dark",
            "required_capabilities": [
                "August 2026 Liquid Chromatic Glassmorphism",
                "GPU-Accelerated Multi-Plane Parallax Scroll",
                "Inertial Pointer Tilt Micro-interactions",
                "Spatial Bento 3.0 Modular Layout",
                "W3C DTCG Standard Design Tokens",
                "WCAG 2.2 AAA Contrast & Accessibility Fallbacks"
            ],
            "dag_pipeline": [
                "Strategy_Agent",
                "Token_Architect_Agent",
                "Layout_Architect_Agent",
                "Component_Engineer_Agent",
                "QA_Validation_Agent"
            ]
        }

        ctx.set_artifact("supervisor_brief", execution_plan)
        ctx.update_stage(PipelineStage.INGESTION, "COMPLETED")

        msg = AgentMessage(
            sender=self.name,
            recipient="Strategy_Agent",
            stage=PipelineStage.INGESTION,
            message_type="HANDOVER",
            payload=execution_plan,
            confidence_score=0.98,
            reasoning_logs=[
                f"Parsed prompt: '{ctx.user_prompt}'",
                f"Resolved target tech stack: {stack}",
                f"Formulated execution DAG with August 2026 glassmorphic and parallax directives."
            ]
        )
        ctx.emit(msg)
        return msg
