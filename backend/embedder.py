"""
embedder.py — OpenAI embeddings and cosine-similarity ranking.

- Batch-embeds a list of texts using text-embedding-3-small.
- Ranks stored chunks against a query embedding using cosine similarity.
- Detects low-confidence retrieval when the best score is below LOW_CONFIDENCE_THRESHOLD.
"""

from __future__ import annotations

import math
import os
from typing import Any

from openai import AsyncOpenAI

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
LOW_CONFIDENCE_THRESHOLD = 0.30   # below this → "no supporting evidence found"
WEAK_EVIDENCE_THRESHOLD = 0.50    # below this → "weak evidence" warning

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return one embedding vector per input text."""
    if not texts:
        return []
    response = await get_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    # Sort by index so order is guaranteed
    items = sorted(response.data, key=lambda d: d.index)
    return [item.embedding for item in items]


def rank_chunks(
    chunks: list[dict[str, Any]],
    query_embedding: list[float],
    top_k: int = 6,
) -> tuple[list[dict[str, Any]], str]:
    """
    Rank chunks by cosine similarity to the query embedding.

    Returns:
        ranked_chunks: top-k chunks, each with a 'score' key added.
        confidence: one of 'strong' | 'weak' | 'none'
    """
    scored = [
        {**chunk, "score": _cosine(chunk["embedding"], query_embedding)}
        for chunk in chunks
    ]
    scored.sort(key=lambda c: c["score"], reverse=True)
    top = scored[:top_k]

    best_score = top[0]["score"] if top else 0.0
    if best_score < LOW_CONFIDENCE_THRESHOLD:
        confidence = "none"
    elif best_score < WEAK_EVIDENCE_THRESHOLD:
        confidence = "weak"
    else:
        confidence = "strong"

    return top, confidence


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
