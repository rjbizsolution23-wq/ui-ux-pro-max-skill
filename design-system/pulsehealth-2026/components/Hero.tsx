'use client';

import React, { useEffect, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Layers, Sparkles, ShieldCheck, ArrowRight, Sun, Moon } from 'lucide-react';

export default function PulseHealth2026Hero() {
  const targetRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: targetRef,
    offset: ['start start', 'end start'],
  });

  const yLayer1 = useTransform(scrollYProgress, [0, 1], ['0%', '20%']);
  const yLayer2 = useTransform(scrollYProgress, [0, 1], ['0%', '-15%']);
  const yLayer3 = useTransform(scrollYProgress, [0, 1], ['0%', '-30%']);

  return (
    <div ref={targetRef} className="relative min-h-screen bg-[#08090E] text-white overflow-hidden selection:bg-indigo-500 selection:text-white">
      
      {/* Ambient Light Orbs (Depth 0.10) */}
      <motion.div style={{ y: yLayer1 }} className="fixed -top-40 -left-40 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />
      <motion.div style={{ y: yLayer1 }} className="fixed top-1/2 -right-40 w-96 h-96 bg-cyan-500/15 rounded-full blur-[140px] pointer-events-none" />

      {/* Floating Glass Nav */}
      <header className="fixed top-4 inset-x-0 z-50 max-w-5xl mx-auto px-4">
        <nav className="rounded-full px-6 py-3.5 flex items-center justify-between bg-white/[0.06] backdrop-blur-2xl border border-white/10 shadow-2xl">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center">
              <Layers className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-lg">PulseHealth 2026</span>
          </div>

          <button className="rounded-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 px-5 py-2 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-lg shadow-emerald-500/20 cursor-pointer">
            Deploy 2026 <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </nav>
      </header>

      {/* Parallax Hero Content */}
      <main className="relative z-10 pt-36 pb-24 max-w-5xl mx-auto px-4 text-center">
        <motion.div style={{ y: yLayer2 }} className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/[0.05] border border-white/10 backdrop-blur-xl text-xs text-slate-300 mb-8">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>August 2026 Multi-Agent Intelligence Engine</span>
        </motion.div>

        <motion.h1 style={{ y: yLayer3 }} className="text-5xl sm:text-7xl font-extrabold tracking-tight mb-6 leading-tight">
          Architect the Future with 
          <span className="bg-gradient-to-r from-indigo-400 via-cyan-300 to-emerald-400 bg-clip-text text-transparent">
            Liquid Glass
          </span>
        </motion.h1>

        <p className="text-lg text-slate-300 max-w-2xl mx-auto mb-10">
          Flawless multi-agent design orchestration. Generating W3C DTCG tokens, fluid clamp scales, and production code.
        </p>

        {/* Interactive Glass Showcase Card */}
        <motion.div
          whileHover={{ y: -6, rotateX: 3, rotateY: -3 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          className="rounded-3xl p-8 text-left bg-white/[0.05] backdrop-blur-2xl border border-white/15 shadow-[0_20px_50px_rgba(0,0,0,0.6),inset_0_1px_1px_rgba(255,255,255,0.3)]"
        >
          <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-6">
            <span className="font-mono text-xs text-slate-400">multi-agent-bus://react.runtime</span>
            <span className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
              <ShieldCheck className="w-4 h-4" /> 100% WCAG 2.2 AAA Validated
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
            <div className="bg-black/40 rounded-2xl p-4 border border-white/5">
              <p className="text-slate-500 text-[10px] uppercase mb-1">Agent 01: Strategy</p>
              <p className="text-indigo-300 font-semibold">Liquid Chromatic 2026</p>
            </div>
            <div className="bg-black/40 rounded-2xl p-4 border border-white/5">
              <p className="text-slate-500 text-[10px] uppercase mb-1">Agent 02: Tokens</p>
              <p className="text-cyan-300 font-semibold">W3C DTCG Spec</p>
            </div>
            <div className="bg-black/40 rounded-2xl p-4 border border-white/5">
              <p className="text-slate-500 text-[10px] uppercase mb-1">Agent 03: QA Audit</p>
              <p className="text-emerald-300 font-semibold">WCAG 2.2 AAA</p>
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}
