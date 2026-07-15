"""
chunker.py — PDF text extraction and paragraph-level chunking.

Strategy (mirrors the document spec):
  - Extract text per page using pypdf (no heavy crypto dependency).
  - Split each page into paragraphs on blank lines.
  - Build chunks up to MAX_CHARS characters, then emit and start a new chunk
    that begins with the last OVERLAP_WORDS words of the previous chunk
    (so context is never cut dead at a boundary).
  - Each chunk carries: id, page_start, page_end, text, char_count.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass, field
from typing import Iterator

from pypdf import PdfReader

MAX_CHARS = 350       # approx token budget per chunk (~80 tokens at 4 chars/token)
OVERLAP_WORDS = 15    # words carried forward to next chunk for continuity


@dataclass
class Chunk:
    id: str
    file_name: str
    page_start: int
    page_end: int
    text: str
    char_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.char_count = len(self.text)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "text": self.text,
            "char_count": self.char_count,
        }


def extract_chunks_from_bytes(pdf_bytes: bytes, file_name: str) -> list[Chunk]:
    """Extract pages and chunk them. Returns an ordered list of Chunk objects."""
    pages = _extract_pages(pdf_bytes)
    return list(_chunk_pages(pages, file_name))


# ── Internal helpers ──────────────────────────────────────────────────────────


def _extract_pages(pdf_bytes: bytes) -> list[dict]:
    """Return a list of {page_number, text} dicts for pages that have text."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", raw).strip()
        if text:
            pages.append({"page_number": i, "text": text})
    return pages


def _chunk_pages(pages: list[dict], file_name: str) -> Iterator[Chunk]:
    """Yield chunks, maintaining ~MAX_CHARS limit with OVERLAP_WORDS overlap."""
    chunk_index = 1

    for page in pages:
        paragraphs = [
            re.sub(r"\s+", " ", p).strip()
            for p in re.split(r"\n+", page["text"])
            if p.strip()
        ]
        if not paragraphs:
            continue

        current_parts: list[str] = []
        current_len = 0
        page_num = page["page_number"]

        for para in paragraphs:
            if current_len + len(para) > MAX_CHARS and current_parts:
                # Emit current chunk
                chunk_text = "\n\n".join(current_parts)
                yield Chunk(
                    id=f"C{chunk_index}",
                    file_name=file_name,
                    page_start=page_num,
                    page_end=page_num,
                    text=chunk_text,
                )
                chunk_index += 1

                # Carry overlap words forward
                overlap = _tail_words(chunk_text, OVERLAP_WORDS)
                current_parts = [overlap, para] if overlap else [para]
                current_len = sum(len(p) for p in current_parts)
            else:
                current_parts.append(para)
                current_len += len(para)

        # Emit whatever remains on this page
        if current_parts:
            yield Chunk(
                id=f"C{chunk_index}",
                file_name=file_name,
                page_start=page_num,
                page_end=page_num,
                text="\n\n".join(current_parts),
            )
            chunk_index += 1


def _tail_words(text: str, n: int) -> str:
    """Return the last n words of text as a string."""
    words = text.split()
    return " ".join(words[-n:]) if len(words) >= n else " ".join(words)
