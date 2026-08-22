#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max - August 2026 Live Design Studio & REST API Server
Provides an interactive web workbench, live multi-agent visualizer, 2026 glassmorphic sandbox,
design token inspector, and REST API for any software.
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from core import search, search_stack, CSV_CONFIG, _load_csv, DATA_DIR
from tokens import DesignTokenEngine
from multi_agent.pipeline import MultiAgentPipeline


STUDIO_HTML = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UI/UX Pro Max — August 2026 Multi-Agent Design Studio</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
            body: ['"Inter"', 'sans-serif'],
          },
          colors: {
            brand: {
              primary: '#6366F1',
              secondary: '#06B6D4',
              cta: '#10B981',
              darkBg: '#08090E',
              darkSurface: '#121420',
            }
          }
        }
      }
    }
  </script>

  <style>
    :root {
      --glass-blur: 24px;
      --glass-sat: 190%;
      --glass-bg: rgba(18, 20, 32, 0.75);
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-specular: rgba(255, 255, 255, 0.40);
      --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
    }

    body {
      background-color: #08090E;
      color: #F8FAFC;
    }

    .glass-panel {
      background: var(--glass-bg);
      backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat));
      -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat));
      border: 1px solid var(--glass-border);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 1px 0 var(--glass-specular);
    }

    .ambient-glow {
      background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.20) 0%, rgba(6, 182, 212, 0.10) 40%, transparent 70%);
    }

    .tilt-box {
      transform-style: preserve-3d;
      perspective: 1000px;
      transition: transform 300ms var(--ease-spring);
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.3);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-brand-primary selection:text-white">

  <!-- Ambient Light Header -->
  <div class="fixed inset-x-0 top-0 h-96 ambient-glow pointer-events-none z-0"></div>

  <!-- Top App Navigation -->
  <header class="relative z-20 border-b border-white/10 glass-panel px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
        <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
      </div>
      <div>
        <h1 class="font-bold text-base tracking-tight flex items-center gap-2">
          UI/UX Pro Max 
          <span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">August 2026 Release</span>
        </h1>
        <p class="text-xs text-slate-400">Multi-Agent Design System Studio & Universal Integration Hub</p>
      </div>
    </div>

    <!-- Mode Tabs -->
    <div class="flex items-center gap-1 bg-black/40 p-1 rounded-xl border border-white/10 text-xs font-medium text-slate-300">
      <button onclick="switchTab('agent')" id="tab-agent" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 text-white font-semibold transition-all">Multi-Agent Pipeline</button>
      <button onclick="switchTab('glass')" id="tab-glass" class="px-3.5 py-1.5 rounded-lg hover:text-white transition-all">Glass & Parallax Lab</button>
      <button onclick="switchTab('tokens')" id="tab-tokens" class="px-3.5 py-1.5 rounded-lg hover:text-white transition-all">Design Tokens</button>
      <button onclick="switchTab('search')" id="tab-search" class="px-3.5 py-1.5 rounded-lg hover:text-white transition-all">Intelligence Search</button>
    </div>

    <!-- Action Tools -->
    <div class="flex items-center gap-3 text-xs">
      <div class="font-mono text-slate-400 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        MCP Server: Active
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="relative z-10 flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">

    <!-- TAB 1: MULTI-AGENT PIPELINE -->
    <section id="view-agent" class="space-y-6">
      <!-- Prompt Input Panel -->
      <div class="glass-panel rounded-2xl p-6">
        <label class="block text-sm font-semibold text-white mb-2">Multi-Agent Design Prompt</label>
        <div class="flex flex-col sm:flex-row gap-3">
          <input id="agentPrompt" type="text" value="Build a high-conversion luxury fintech SaaS landing page with dark liquid glassmorphism and 3D parallax layers" 
                 class="flex-1 bg-black/50 border border-white/15 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 font-sans" />
          
          <select id="agentStack" class="bg-black/50 border border-white/15 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
            <option value="html-tailwind">HTML + Tailwind v4</option>
            <option value="react">React + Next.js</option>
            <option value="vue">Vue 3 + Tailwind</option>
            <option value="svelte">Svelte 5 Runes</option>
            <option value="swiftui">SwiftUI 6</option>
            <option value="flutter">Flutter</option>
          </select>

          <button onclick="runAgentPipeline()" id="runBtn" class="rounded-xl bg-brand-cta hover:bg-emerald-400 text-slate-950 px-6 py-3 font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition-all cursor-pointer">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            <span>Run Pipeline</span>
          </button>
        </div>
      </div>

      <!-- Pipeline Telemetry & Message Bus -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left: Stage Telemetry (4 cols) -->
        <div class="lg:col-span-4 glass-panel rounded-2xl p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-white/10 pb-3">
            <h2 class="font-bold text-sm text-white flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-indigo-400"></span> Agent Stage Telemetry
            </h2>
            <span id="telemetryStatus" class="font-mono text-[11px] text-emerald-400">Ready</span>
          </div>

          <div id="stageList" class="space-y-2.5 text-xs font-mono">
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">1. Ingestion & Routing</span>
              <span class="text-emerald-400 font-semibold">Supervisor</span>
            </div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">2. Trend & Anti-Patterns</span>
              <span class="text-indigo-400 font-semibold">Strategy</span>
            </div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">3. W3C DTCG Token Engine</span>
              <span class="text-cyan-400 font-semibold">Token Arch</span>
            </div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">4. Bento 3.0 & Parallax Stack</span>
              <span class="text-purple-400 font-semibold">Layout Arch</span>
            </div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">5. Component Synthesis</span>
              <span class="text-amber-400 font-semibold">Engineer</span>
            </div>
            <div class="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
              <span class="text-slate-300">6. WCAG 2.2 AAA Audit</span>
              <span class="text-emerald-400 font-semibold">QA Validator</span>
            </div>
          </div>
        </div>

        <!-- Right: Message Bus & Artifact Output (8 cols) -->
        <div class="lg:col-span-8 glass-panel rounded-2xl p-6 space-y-4">
          <div class="flex items-center justify-between border-b border-white/10 pb-3">
            <h2 class="font-bold text-sm text-white">Agent Output & Generated Artifacts</h2>
            <div class="flex gap-2">
              <button onclick="copyGeneratedCode()" class="px-3 py-1 bg-white/10 hover:bg-white/20 text-xs rounded-lg font-mono text-slate-300 transition-colors">Copy Code</button>
              <button onclick="copyTokens()" class="px-3 py-1 bg-white/10 hover:bg-white/20 text-xs rounded-lg font-mono text-slate-300 transition-colors">Copy Tokens</button>
            </div>
          </div>

          <div id="outputDisplay" class="bg-black/60 rounded-xl p-4 font-mono text-xs text-slate-300 h-96 overflow-y-auto border border-white/5 leading-relaxed">
            <p class="text-slate-500">// Pipeline ready. Click "Run Pipeline" to trigger the multi-agent design orchestration.</p>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 2: GLASS & PARALLAX LAB -->
    <section id="view-glass" class="hidden space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Controls (4 cols) -->
        <div class="lg:col-span-4 glass-panel rounded-2xl p-6 space-y-5">
          <h2 class="font-bold text-base text-white border-b border-white/10 pb-3">2026 Liquid Glass & Parallax Shader Controls</h2>
          
          <div>
            <div class="flex justify-between text-xs text-slate-300 mb-1.5">
              <span>Backdrop Blur Radius</span>
              <span id="valBlur" class="font-mono text-indigo-400">24px</span>
            </div>
            <input id="sliderBlur" type="range" min="4" max="60" value="24" class="w-full accent-indigo-500" oninput="updateGlassShader()" />
          </div>

          <div>
            <div class="flex justify-between text-xs text-slate-300 mb-1.5">
              <span>Backdrop Saturation</span>
              <span id="valSat" class="font-mono text-indigo-400">190%</span>
            </div>
            <input id="sliderSat" type="range" min="100" max="300" value="190" class="w-full accent-indigo-500" oninput="updateGlassShader()" />
          </div>

          <div>
            <div class="flex justify-between text-xs text-slate-300 mb-1.5">
              <span>Specular Inset Border Opacity</span>
              <span id="valSpec" class="font-mono text-indigo-400">0.45</span>
            </div>
            <input id="sliderSpec" type="range" min="10" max="90" value="45" class="w-full accent-indigo-500" oninput="updateGlassShader()" />
          </div>

          <div>
            <div class="flex justify-between text-xs text-slate-300 mb-1.5">
              <span>Parallax Depth Multiplier</span>
              <span id="valDepth" class="font-mono text-indigo-400">0.85x</span>
            </div>
            <input id="sliderDepth" type="range" min="10" max="150" value="85" class="w-full accent-indigo-500" oninput="updateGlassShader()" />
          </div>

          <div class="pt-4 border-t border-white/10">
            <button onclick="resetGlassShader()" class="w-full py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-mono text-slate-400 transition-colors">Reset to 2026 Golden Ratio</button>
          </div>
        </div>

        <!-- Live Interactive Preview Canvas (8 cols) -->
        <div class="lg:col-span-8 glass-panel rounded-2xl p-8 relative overflow-hidden min-h-[460px] flex items-center justify-center">
          
          <!-- Background Moving Gradient Orbs -->
          <div class="absolute -top-10 -left-10 w-64 h-64 bg-indigo-500/30 rounded-full blur-[80px] pointer-events-none"></div>
          <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-cyan-500/25 rounded-full blur-[90px] pointer-events-none"></div>

          <!-- Interactive Tilt Card -->
          <div id="interactiveCard" class="tilt-box glass-panel rounded-3xl p-8 max-w-md w-full relative z-10 border border-white/20 shadow-2xl cursor-pointer">
            <div class="flex items-center justify-between mb-6">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center text-white font-bold text-sm">
                2026
              </div>
              <span class="font-mono text-xs text-emerald-400 bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-500/30">
                Specular Shader Active
              </span>
            </div>

            <h3 class="text-2xl font-extrabold text-white mb-2">Liquid Chromatic Glass</h3>
            <p class="text-sm text-slate-300 leading-relaxed mb-6">
              Sub-pixel 1px specular lighting reflections with multi-plane spring depth rendering. Zero cumulative layout shift.
            </p>

            <div class="flex items-center justify-between pt-4 border-t border-white/10 text-xs font-mono text-slate-400">
              <span>Depth: <strong id="cardDepthIndicator" class="text-indigo-300">0.85</strong></span>
              <span class="text-emerald-400 font-semibold">WCAG 2.2 AAA (16.8:1)</span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- TAB 3: DESIGN TOKENS -->
    <section id="view-tokens" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-6">
        <h2 class="font-bold text-base text-white mb-4">W3C DTCG Standard Design Tokens (August 2026)</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-black/40 rounded-xl p-4 border border-white/10">
            <p class="text-xs text-slate-400 mb-1 font-mono">High-Gamut OKLCH Primary</p>
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-lg bg-indigo-500 shadow-md"></div>
              <span class="font-mono text-xs text-indigo-300">oklch(0.55 0.24 260)</span>
            </div>
          </div>
          <div class="bg-black/40 rounded-xl p-4 border border-white/10">
            <p class="text-xs text-slate-400 mb-1 font-mono">High-Conversion CTA</p>
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-lg bg-emerald-500 shadow-md"></div>
              <span class="font-mono text-xs text-emerald-300">oklch(0.65 0.22 145)</span>
            </div>
          </div>
          <div class="bg-black/40 rounded-xl p-4 border border-white/10">
            <p class="text-xs text-slate-400 mb-1 font-mono">Fluid Typography Clamp</p>
            <span class="font-mono text-xs text-cyan-300">clamp(2.5rem, 1.8rem + 3.5vw, 5.5rem)</span>
          </div>
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>Tailwind v4 @theme & CSS Custom Properties</span>
            <button onclick="copyTokenBlock()" class="text-indigo-400 hover:underline">Copy All</button>
          </div>
          <pre id="tokenPre" class="bg-black/60 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto border border-white/5"></pre>
        </div>
      </div>
    </section>

    <!-- TAB 4: INTELLIGENCE SEARCH -->
    <section id="view-search" class="hidden space-y-6">
      <div class="glass-panel rounded-2xl p-6">
        <label class="block text-sm font-semibold text-white mb-2">BM25 Hybrid Intelligence Search</label>
        <div class="flex gap-3 mb-4">
          <input id="searchQuery" type="text" placeholder="Search styles, tokens, animations, landing patterns, charts, stacks..." 
                 class="flex-1 bg-black/50 border border-white/15 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-sans" />
          
          <select id="searchDomain" class="bg-black/50 border border-white/15 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
            <option value="">Auto-Detect Domain</option>
            <option value="style">Styles (73+)</option>
            <option value="animation">Animations (2026)</option>
            <option value="token">Design Tokens</option>
            <option value="color">Colors (96)</option>
            <option value="typography">Typography (57)</option>
            <option value="landing">Landing Patterns</option>
            <option value="product">Products</option>
            <option value="ux">UX Guidelines</option>
            <option value="agent">Agent Rules</option>
          </select>

          <button onclick="performSearch()" class="rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 font-semibold text-sm transition-all cursor-pointer">
            Search
          </button>
        </div>

        <div id="searchResults" class="bg-black/60 rounded-xl p-4 font-mono text-xs text-slate-300 min-h-64 max-h-96 overflow-y-auto border border-white/5">
          <p class="text-slate-500">// Type a query to search the BM25 design intelligence database.</p>
        </div>
      </div>
    </section>

  </main>

  <script>
    let currentPipelineData = null;

    function switchTab(tab) {
      ['agent', 'glass', 'tokens', 'search'].forEach(t => {
        document.getElementById(`view-${t}`).classList.add('hidden');
        document.getElementById(`tab-${t}`).classList.remove('bg-indigo-600', 'text-white', 'font-semibold');
      });
      document.getElementById(`view-${tab}`).classList.remove('hidden');
      document.getElementById(`tab-${tab}`).classList.add('bg-indigo-600', 'text-white', 'font-semibold');
    }

    async function runAgentPipeline() {
      const prompt = document.getElementById('agentPrompt').value;
      const stack = document.getElementById('agentStack').value;
      const btn = document.getElementById('runBtn');
      const out = document.getElementById('outputDisplay');
      const status = document.getElementById('telemetryStatus');

      btn.disabled = true;
      btn.innerHTML = 'Orchestrating...';
      status.innerText = 'Running 6 Agents...';
      status.className = 'font-mono text-[11px] text-amber-400 animate-pulse';

      out.innerHTML = '<p class="text-indigo-400">⚡ Dispatching supervisor envelope to message bus...</p>';

      try {
        const resp = await fetch('/api/pipeline', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt, stack })
        });
        const data = await resp.json();
        currentPipelineData = data;

        let logHtml = '';
        logHtml += `<p class="text-emerald-400 font-bold">✅ Pipeline Execution Finished in 6 Stages [Session: ${data.session_id}]</p>\\n`;
        logHtml += `<p class="text-slate-400">QA Verdict: <span class="text-white font-semibold">${data.qa_verdict.verdict}</span> (Score: ${data.qa_verdict.compliance_score})</p>\\n<br/>`;
        
        logHtml += `<p class="text-indigo-300 font-bold">// AGENT MESSAGE BUS TELEMETRY:</p>\\n`;
        data.telemetry.forEach(msg => {
          logHtml += `<p class="text-slate-400">[<span class="text-indigo-400">${msg.sender}</span> &rarr; <span class="text-cyan-400">${msg.recipient}</span>] (${msg.stage}): <span class="text-slate-200">${msg.reasoning[0]}</span></p>\\n`;
        });

        logHtml += `<br/><p class="text-emerald-300 font-bold">// PRODUCTION CODE GENERATED (${stack}):</p>\\n`;
        logHtml += `<pre class="text-slate-300 mt-2">${escapeHtml(data.markdown_documentation.slice(0, 1500))}...</pre>`;

        out.innerHTML = logHtml;
        status.innerText = 'Completed (100%)';
        status.className = 'font-mono text-[11px] text-emerald-400';
      } catch (err) {
        out.innerHTML = `<p class="text-rose-400">Error running pipeline: ${err.message}</p>`;
        status.innerText = 'Error';
        status.className = 'font-mono text-[11px] text-rose-400';
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg><span>Run Pipeline</span>`;
      }
    }

    function escapeHtml(text) {
      return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function copyGeneratedCode() {
      if (currentPipelineData && currentPipelineData.markdown_documentation) {
        navigator.clipboard.writeText(currentPipelineData.markdown_documentation);
        alert('Design System Markdown and Code copied to clipboard!');
      } else {
        alert('Run the pipeline first to generate code.');
      }
    }

    function copyTokens() {
      fetch('/api/tokens', { method: 'POST', body: JSON.stringify({}) })
        .then(r => r.json())
        .then(data => {
          navigator.clipboard.writeText(JSON.stringify(data.w3c_dtcg, null, 2));
          alert('W3C DTCG Tokens JSON copied to clipboard!');
        });
    }

    // Glass Shader Live Playground
    function updateGlassShader() {
      const blur = document.getElementById('sliderBlur').value;
      const sat = document.getElementById('sliderSat').value;
      const spec = document.getElementById('sliderSpec').value / 100;
      const depth = (document.getElementById('sliderDepth').value / 100).toFixed(2);

      document.getElementById('valBlur').innerText = blur + 'px';
      document.getElementById('valSat').innerText = sat + '%';
      document.getElementById('valSpec').innerText = spec;
      document.getElementById('valDepth').innerText = depth + 'x';
      document.getElementById('cardDepthIndicator').innerText = depth;

      const card = document.getElementById('interactiveCard');
      card.style.backdropFilter = `blur(${blur}px) saturate(${sat}%)`;
      card.style.webkitBackdropFilter = `blur(${blur}px) saturate(${sat}%)`;
      card.style.boxShadow = `0 20px 50px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px 0 rgba(255, 255, 255, ${spec})`;
    }

    function resetGlassShader() {
      document.getElementById('sliderBlur').value = 24;
      document.getElementById('sliderSat').value = 190;
      document.getElementById('sliderSpec').value = 45;
      document.getElementById('sliderDepth').value = 85;
      updateGlassShader();
    }

    // 3D Pointer tilt on interactive card
    const card = document.getElementById('interactiveCard');
    if (card) {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        const depthMul = parseFloat(document.getElementById('sliderDepth').value) / 100;
        card.style.transform = `perspective(1000px) rotateX(${(y / (rect.height / 2)) * -10 * depthMul}deg) rotateY(${(x / (rect.width / 2)) * 10 * depthMul}deg) translateZ(12px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0)';
      });
    }

    // Token view loader
    fetch('/api/tokens', { method: 'POST', body: JSON.stringify({}) })
      .then(r => r.json())
      .then(data => {
        document.getElementById('tokenPre').innerText = data.tailwind_v4 + '\\n\\n' + data.css_variables;
      });

    function copyTokenBlock() {
      const text = document.getElementById('tokenPre').innerText;
      navigator.clipboard.writeText(text);
      alert('Tokens copied to clipboard!');
    }

    // Search
    async function performSearch() {
      const q = document.getElementById('searchQuery').value;
      const domain = document.getElementById('searchDomain').value;
      const out = document.getElementById('searchResults');
      out.innerHTML = '<p class="text-indigo-400">Searching BM25 index...</p>';

      const url = `/api/search?q=${encodeURIComponent(q)}` + (domain ? `&domain=${encodeURIComponent(domain)}` : '');
      const resp = await fetch(url);
      const data = await resp.json();

      let html = `<p class="text-emerald-400 font-bold mb-3">Found ${data.count} results in domain [${data.domain}]:</p>`;
      data.results.forEach((row, i) => {
        html += `<div class="p-3 mb-2 rounded-lg bg-white/5 border border-white/10">`;
        html += `<p class="text-indigo-300 font-bold mb-1">Result ${i+1}</p>`;
        for (let [k, v] of Object.entries(row)) {
          html += `<p class="text-slate-300"><span class="text-slate-500">${k}:</span> ${escapeHtml(String(v))}</p>`;
        }
        html += `</div>`;
      });
      out.innerHTML = html;
    }
  </script>
</body>
</html>"""


class StudioHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(STUDIO_HTML.encode("utf-8"))
            return

        elif path == "/api/search":
            q = query.get("q", [""])[0]
            domain = query.get("domain", [None])[0]
            stack = query.get("stack", [None])[0]

            if stack:
                res = search_stack(q, stack)
            else:
                res = search(q, domain)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/styles":
            styles_file = DATA_DIR / "styles.csv"
            styles_data = _load_csv(styles_file) if styles_file.exists() else []
            res = {
                "domain": "style",
                "count": len(styles_data),
                "results": styles_data
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        data = json.loads(body.decode("utf-8")) if body else {}

        if parsed.path == "/api/pipeline":
            prompt = data.get("prompt", "High conversion SaaS")
            stack = data.get("stack", "html-tailwind")
            project_name = data.get("project_name")

            pipeline = MultiAgentPipeline()
            ctx = pipeline.run(prompt, project_name=project_name, target_stack=stack)

            resp = {
                "session_id": ctx.session_id,
                "project_name": ctx.project_name,
                "markdown_documentation": pipeline.format_markdown(ctx),
                "telemetry": [m.to_dict() for m in ctx.message_bus],
                "qa_verdict": ctx.get_artifact("qa_audit_report"),
                "artifacts": list(ctx.artifacts.keys())
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        elif parsed.path == "/api/tokens":
            engine = DesignTokenEngine(
                brand_primary=data.get("primary", "#6366F1"),
                brand_secondary=data.get("secondary", "#06B6D4"),
                brand_cta=data.get("cta", "#10B981")
            )
            resp = {
                "w3c_dtcg": engine.generate_w3c_tokens(),
                "css_variables": engine.export_css_variables(),
                "tailwind_v4": engine.export_tailwind_v4_theme(),
                "typescript": engine.export_typescript_tokens()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


def run_studio_server(port=8080):
    server = HTTPServer(("0.0.0.0", port), StudioHandler)
    print(f"🚀 UI/UX Pro Max August 2026 Design Studio active at http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_studio_server(port)
