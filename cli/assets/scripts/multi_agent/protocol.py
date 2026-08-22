#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Communication Protocol & Data Bus
Provides typed envelopes, artifacts store, telemetry, and pipeline lifecycle contracts.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid


class PipelineStage:
    INGESTION = "1_INGESTION"
    STRATEGY = "2_STRATEGY"
    TOKEN_ARCHITECTURE = "3_TOKEN_ARCHITECTURE"
    LAYOUT_ARCHITECTURE = "4_LAYOUT_ARCHITECTURE"
    COMPONENT_ENGINEERING = "5_COMPONENT_ENGINEERING"
    QA_VERIFICATION = "6_QA_VERIFICATION"
    DELIVERY = "7_DELIVERY"


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    stage: str
    message_type: str  # HANDOVER, QUERY, VALIDATION_PASS, VALIDATION_FAIL, TELEMETRY
    payload: Dict[str, Any]
    confidence_score: float = 1.0
    reasoning_logs: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.message_id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "recipient": self.recipient,
            "stage": self.stage,
            "type": self.message_type,
            "confidence": self.confidence_score,
            "reasoning": self.reasoning_logs,
            "payload": self.payload
        }


@dataclass
class PipelineContext:
    session_id: str
    user_prompt: str
    project_name: str
    target_stack: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Store for artifacts passed down the multi-agent pipeline
    artifacts: Dict[str, Any] = field(default_factory=dict)
    
    # Communication log of all messages exchanged
    message_bus: List[AgentMessage] = field(default_factory=list)
    
    # Stage status tracking
    stage_status: Dict[str, str] = field(default_factory=lambda: {
        PipelineStage.INGESTION: "PENDING",
        PipelineStage.STRATEGY: "PENDING",
        PipelineStage.TOKEN_ARCHITECTURE: "PENDING",
        PipelineStage.LAYOUT_ARCHITECTURE: "PENDING",
        PipelineStage.COMPONENT_ENGINEERING: "PENDING",
        PipelineStage.QA_VERIFICATION: "PENDING",
        PipelineStage.DELIVERY: "PENDING",
    })

    def emit(self, message: AgentMessage):
        self.message_bus.append(message)

    def set_artifact(self, key: str, value: Any):
        self.artifacts[key] = value

    def get_artifact(self, key: str, default: Any = None) -> Any:
        return self.artifacts.get(key, default)

    def update_stage(self, stage: str, status: str):
        self.stage_status[stage] = status

    def export_summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "project_name": self.project_name,
            "prompt": self.user_prompt,
            "stack": self.target_stack,
            "created_at": self.created_at,
            "stages": self.stage_status,
            "total_agent_exchanges": len(self.message_bus),
            "artifacts_generated": list(self.artifacts.keys())
        }
