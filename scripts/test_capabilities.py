#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.7.0",
#   "httpx>=0.27.0",
# ]
# ///
"""
Smoke test for AIproductfactory's Deep Research RRF Fusion, Deduplication,
Citation Velocity Scoring, and Pydantic Output Envelopes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path("skills/academic-data-search/scripts").resolve()))
from deep_research_engine import (
    Author,
    ResearchPaper,
    fuse_and_deduplicate,
    render_evidence_table,
)


def test_rrf_deduplication_and_scoring():
    openalex_mock = [
        ResearchPaper(
            paper_id="OA-1",
            title="Agentic Workflows and Long-Horizon Planning in LLM Systems",
            authors=[Author(name="Logesh V"), Author(name="A. Researcher")],
            year=2025,
            venue="NeurIPS",
            doi="10.1000/agentic.2025.01",
            url="https://doi.org/10.1000/agentic.2025.01",
            citation_count=85,
            sources=["OpenAlex"],
        ),
        ResearchPaper(
            paper_id="OA-2",
            title="Incremental Codebase Indexing with Vector Graphs",
            authors=[Author(name="B. Builder")],
            year=2024,
            venue="ICSE",
            doi="10.1000/coco.2024.02",
            citation_count=42,
            sources=["OpenAlex"],
        ),
    ]

    s2_mock = [
        # Duplicate of OA-1 with extra influential citations and PDF URL
        ResearchPaper(
            paper_id="S2-99",
            title="Agentic Workflows and Long-Horizon Planning in LLM Systems!",
            authors=[Author(name="Logesh V"), Author(name="A. Researcher")],
            year=2025,
            venue="NeurIPS",
            doi="10.1000/agentic.2025.01",
            pdf_url="https://arxiv.org/pdf/2501.00001.pdf",
            abstract="Full synthesis of long-horizon agentic execution.",
            citation_count=92,
            influential_citation_count=18,
            sources=["SemanticScholar"],
        ),
    ]

    arxiv_mock = [
        # Same title without DOI — should still deduplicate via normalized title
        ResearchPaper(
            paper_id="arXiv:2501.00001",
            title="Agentic Workflows and Long-Horizon Planning in LLM Systems",
            authors=[Author(name="Logesh V")],
            year=2025,
            venue="arXiv",
            url="https://arxiv.org/abs/2501.00001",
            sources=["arXiv"],
        )
    ]

    ranked, total_raw = fuse_and_deduplicate([openalex_mock, s2_mock, arxiv_mock], top_k=5)
    assert total_raw == 4, f"Expected 4 raw candidates, got {total_raw}"
    assert len(ranked) == 2, f"Expected 2 deduplicated papers, got {len(ranked)}"

    top = ranked[0]
    assert set(top.sources) == {"OpenAlex", "SemanticScholar", "arXiv"}, f"Sources not merged: {top.sources}"
    assert top.citation_count == 92, "Should retain max citation count across providers"
    assert top.influential_citation_count == 18, "Should retain influential citations"
    assert top.pdf_url == "https://arxiv.org/pdf/2501.00001.pdf", "Should merge open-access PDF URL"
    assert top.bibtex.startswith("@article{v2025_"), f"Unexpected BibTeX key: {top.bibtex}"

    md_table = render_evidence_table(ranked)
    assert "OpenAlex, SemanticScholar, arXiv" in md_table
    print("✅ Deep Research RRF fusion, DOI/title deduplication, and Pydantic contracts verified!")
    print("\nSample Generated Evidence Matrix:\n")
    print(md_table)


if __name__ == "__main__":
    test_rrf_deduplication_and_scoring()