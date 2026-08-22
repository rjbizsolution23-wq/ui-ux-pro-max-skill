#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Core - August 2026 BM25 search engine & design intelligence kernel
"""

import csv
import re
from pathlib import Path
from math import log
from collections import defaultdict

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style Category", "Keywords", "Best For", "Type", "AI Prompt Keywords", "Era/Origin", "CSS/Technical Keywords"],
        "output_cols": ["Style Category", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Performance", "Accessibility", "Framework Compatibility", "Complexity", "AI Prompt Keywords", "CSS/Technical Keywords", "Implementation Checklist", "Design System Variables"]
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Notes", "Border (Hex)"],
        "output_cols": ["Product Type", "Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Background (Hex)", "Text (Hex)", "Border (Hex)", "Notes"]
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Accessibility Notes", "Library Recommendation"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Color Guidance", "Accessibility Notes", "Library Recommendation", "Interactive Level"]
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["Pattern Name", "Keywords", "Conversion Optimization", "Section Order", "Recommended Effects"],
        "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Recommended Effects", "Conversion Optimization"]
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations", "Landing Page Pattern"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus", "Key Considerations"]
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform", "Do", "Don't"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"]
    },
    "icons": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Best For", "Library"],
        "output_cols": ["Category", "Icon Name", "Keywords", "Library", "Import Code", "Usage", "Best For", "Style"]
    },
    "animation": {
        "file": "animations.csv",
        "search_cols": ["Animation Pattern", "Category", "Trigger", "Best For", "August 2026 Specification", "CSS Implementation"],
        "output_cols": ["Animation Pattern", "Category", "Trigger", "CSS Implementation", "Spring/Timing Formula", "Parallax Depth", "Hardware Acceleration", "Accessibility Fallback", "Best For", "August 2026 Specification"]
    },
    "token": {
        "file": "design-tokens.csv",
        "search_cols": ["Token Category", "Token Name", "DTCG Type", "W3C Token Path", "CSS Variable", "August 2026 Description"],
        "output_cols": ["Token Category", "Token Name", "DTCG Type", "W3C Token Path", "CSS Variable", "Tailwind v4 Mapping", "Default Value", "Dark Mode Value", "August 2026 Description"]
    },
    "agent": {
        "file": "agent-rules.csv",
        "search_cols": ["Stage", "Agent Role", "Input Payload", "Output Artifact", "Validation Gate", "Handover Protocol"],
        "output_cols": ["Stage", "Agent Role", "Input Payload", "Output Artifact", "Validation Gate", "Failure Fallback", "Handover Protocol"]
    },
    "react": {
        "file": "react-performance.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "web": {
        "file": "web-interface.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    }
}

STACK_CONFIG = {
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "react": {"file": "stacks/react.csv"},
    "nextjs": {"file": "stacks/nextjs.csv"},
    "astro": {"file": "stacks/astro.csv"},
    "vue": {"file": "stacks/vue.csv"},
    "nuxtjs": {"file": "stacks/nuxtjs.csv"},
    "nuxt-ui": {"file": "stacks/nuxt-ui.csv"},
    "svelte": {"file": "stacks/svelte.csv"},
    "swiftui": {"file": "stacks/swiftui.csv"},
    "react-native": {"file": "stacks/react-native.csv"},
    "flutter": {"file": "stacks/flutter.csv"},
    "shadcn": {"file": "stacks/shadcn.csv"},
    "jetpack-compose": {"file": "stacks/jetpack-compose.csv"}
}

# Common columns for all stacks
_STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
    "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Lowercase, split, remove punctuation, filter short words"""
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from documents"""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ SEARCH FUNCTIONS ============
def _load_csv(filepath):
    """Load CSV and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    """Core search function using BM25"""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)

    # Build documents from search columns
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]

    # BM25 search
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)

    # Get top results with score > 0
    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})

    # If score was 0 for all, fallback to top items containing any substring
    if not results and data:
        q_tokens = [w for w in re.sub(r'[^\w\s]', ' ', query.lower()).split() if len(w) > 2]
        for row in data:
            row_text = " ".join(str(row.get(col, "")).lower() for col in search_cols)
            if any(t in row_text for t in q_tokens):
                results.append({col: row.get(col, "") for col in output_cols if col in row})
                if len(results) >= max_results:
                    break

    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "animation": ["animation", "parallax", "scroll", "motion", "spring", "inertial", "tilt", "shimmer", "cursor", "view transition", "stagger"],
        "token": ["token", "tokens", "dtcg", "w3c", "variable", "oklch", "scale", "spacing token", "color token", "radius token"],
        "agent": ["agent", "multi-agent", "pipeline", "handover", "orchestrator", "supervisor", "qa agent", "validation gate"],
        "color": ["color", "palette", "hex", "#", "rgb", "oklch", "hue", "theme"],
        "chart": ["chart", "graph", "visualization", "trend", "bar", "pie", "scatter", "heatmap", "funnel"],
        "landing": ["landing", "page", "cta", "conversion", "hero", "testimonial", "pricing", "section", "pattern"],
        "product": ["saas", "ecommerce", "e-commerce", "fintech", "healthcare", "gaming", "portfolio", "crypto", "dashboard", "b2b"],
        "style": ["style", "design", "ui", "minimalism", "glassmorphism", "neumorphism", "brutalism", "dark mode", "flat", "aurora", "bento", "prompt", "css", "spatial", "oled", "cyber"],
        "ux": ["ux", "usability", "accessibility", "wcag", "touch", "scroll", "animation", "keyboard", "navigation", "mobile", "a11y"],
        "typography": ["font", "typography", "heading", "serif", "sans", "google fonts", "clamp", "font pairing"],
        "icons": ["icon", "icons", "lucide", "heroicons", "symbol", "glyph", "pictogram", "svg icon"],
        "react": ["react", "next.js", "nextjs", "suspense", "memo", "usecallback", "useeffect", "rerender", "bundle", "waterfall", "barrel", "dynamic import", "rsc", "server component"],
        "web": ["aria", "focus", "outline", "semantic", "virtualize", "autocomplete", "form", "input type", "preconnect"]
    }

    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in domain_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    results = _search_csv(filepath, config["search_cols"], config["output_cols"], query, max_results)

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results
    }


def search_stack(query, stack, max_results=MAX_RESULTS):
    """Search stack-specific guidelines"""
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"}

    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]

    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}

    results = _search_csv(filepath, _STACK_COLS["search_cols"], _STACK_COLS["output_cols"], query, max_results)

    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results
    }
