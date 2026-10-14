---
name: academic-data-search
description: High-capability multi-source academic and technical deep research engine with parallel OpenAlex, Semantic Scholar, and arXiv retrieval, DOI/Title deduplication, Reciprocal Rank Fusion (RRF), citation-velocity scoring, and BibTeX generation.
---

# Academic Data Search & Deep Research Synthesis (`v2.0`)

## Overview
This skill upgrades standard single-endpoint literature search into a **multi-source deep research pipeline**:
1. **Parallel Async Retrieval:** Queries **OpenAlex**, **Semantic Scholar**, and **arXiv** concurrently.
2. **Cross-Source Deduplication:** Normalizes DOIs and titles to merge duplicate records while preserving the highest citation counts, influential citation metrics, abstracts, and Open-Access PDF links.
3. **Hybrid Ranking (RRF + Citation Velocity + Recency Decay):** Ranks papers using Reciprocal Rank Fusion across providers combined with log-normalized annual citation velocity ($\frac{\text{ citations } + 2 \times \text{ influential}}{\text{ age}}$) and recency weighting.
4. **Structured Output Contract:** Emits a deterministic JSON envelope (`ResearchSynthesisEnvelope`) containing a ready-to-render Markdown Evidence Matrix and formatted BibTeX citations.

## Quick Execution (Isolated via `uv`)
```bash
uv run skills/academic-data-search/scripts/deep_research_engine.py "agentic workflows long horizon planning" --top-k 10
```