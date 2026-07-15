"""
main.py — ABC RAG demo backend (FastAPI).

Routes:
  GET  /api/health                        — API key + model status
  POST /api/upload                        — Upload PDF, chunk, embed, return session
  POST /api/chat                          — Ask a question, get cited answer
  GET  /api/session/{session_id}/chunks   — Return all chunks for a session
  GET  /uploads/{filename}                — Serve uploaded PDFs

Sessions are stored in-memory (sufficient for a demo; replace with a DB for production).
"""

from __future__ import annotations

import os
import re
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import AsyncOpenAI
from pydantic import BaseModel

from chunker import extract_chunks_from_bytes
from embedder import embed_texts, rank_chunks

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
# Vercel Functions only allow writes under /tmp
UPLOADS_DIR = (
    Path("/tmp/uploads")
    if os.getenv("VERCEL")
    else Path(__file__).parent / "uploads"
)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Comma-separated list; defaults keep local Next.js ports working.
_CORS_DEFAULT = "http://localhost:3000,http://localhost:3001"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _CORS_DEFAULT).split(",")
    if origin.strip()
]

SYSTEM_PROMPT = """You are a cautious internal conveyancing assistant for ABC staff.

Rules you must follow without exception:
1. Answer ONLY from the retrieved matter context provided below. Do not use general legal knowledge or invented facts.
2. Cite every material claim inline using the chunk ID provided, e.g. [C1] or [C3].
3. If evidence is missing, say clearly: "No supporting evidence was found in the uploaded document for this question."
4. If evidence is weak or partial, label your answer: "Based on limited evidence —"
5. If two sources conflict, show both with their dates/chunk IDs and flag the conflict explicitly.
6. Never give a definitive legal conclusion. Always frame suggestions as: "This may warrant review by a fee earner."
7. Suggested next actions must be explicitly labelled as: "Suggested actions (for staff review only):"

Your audience is conveyancing paralegals and fee earners. Be concise and precise."""

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="ABC RAG Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id → session dict
sessions: dict[str, dict[str, Any]] = {}


def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "has_api_key": bool(os.getenv("OPENAI_API_KEY")),
        "chat_model": CHAT_MODEL,
        "embedding_model": EMBEDDING_MODEL,
    }


# ── Upload ────────────────────────────────────────────────────────────────────

@app.post("/api/upload")
async def upload_pdf(files: list[UploadFile] = File(...)):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="OPENAI_API_KEY is not set. Add it to backend/.env before uploading.",
        )

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    session_id = str(uuid.uuid4())
    all_chunks = []
    file_info_list = []
    total_pages = 0

    for pdf in files:
        if pdf.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"Only PDF files are supported. File {pdf.filename} is not a PDF.")

        pdf_bytes = await pdf.read()
        if not pdf_bytes:
            continue

        chunks = extract_chunks_from_bytes(pdf_bytes, pdf.filename or "unknown.pdf")
        if chunks:
            all_chunks.extend(chunks)

        # Persist PDF
        file_id = str(uuid.uuid4())
        stored_name = f"{file_id}.pdf"
        stored_path = UPLOADS_DIR / stored_name
        stored_path.write_bytes(pdf_bytes)
        
        pages_in_file = max((c.page_end for c in chunks), default=0) if chunks else 0
        total_pages += pages_in_file

        file_info_list.append({
            "name": pdf.filename,
            "url": f"/uploads/{stored_name}",
        })

    if not all_chunks:
        raise HTTPException(
            status_code=400,
            detail="No readable text was extracted from any of the uploaded PDFs."
        )

    # Re-assign chunk IDs globally across all files (C1, C2...)
    for i, chunk in enumerate(all_chunks, start=1):
        chunk.id = f"C{i}"

    # Embed all chunks
    texts = [c.text for c in all_chunks]
    embeddings = await embed_texts(texts)
    indexed_chunks = [
        {**c.to_dict(), "embedding": embeddings[i]}
        for i, c in enumerate(all_chunks)
    ]

    sessions[session_id] = {
        "id": session_id,
        "files": file_info_list,
        "created_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "page_count": total_pages,
        "chunks": indexed_chunks,
    }

    return {
        "session_id": session_id,
        "files": file_info_list,
        "page_count": total_pages,
        "chunk_count": len(indexed_chunks),
        "chunks": [
            {k: v for k, v in c.items() if k != "embedding"}
            for c in indexed_chunks
        ],
    }


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/api/chat")
async def chat(body: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="OPENAI_API_KEY is not set.",
        )

    session = sessions.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Please upload a PDF first.")

    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Embed query and rank chunks
    [question_embedding] = await embed_texts([question])
    ranked_chunks, confidence = rank_chunks(session["chunks"], question_embedding, top_k=6)

    # Build context block for the LLM
    context_parts = [
        f"[{c['id']}] Pages {_fmt_pages(c['page_start'], c['page_end'])}\n{c['text']}"
        for c in ranked_chunks
    ]
    context = "\n\n".join(context_parts)

    client = get_openai_client()
    completion = await client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Retrieved matter context:\n{context}\n\n"
                    "Answer with inline citations using only the provided chunk IDs."
                ),
            },
        ],
    )

    answer = (completion.choices[0].message.content or "").strip()
    if not answer:
        answer = "I could not produce an answer from the retrieved context."

    # Extract which citation IDs appear in the answer
    cited_ids = list(dict.fromkeys(re.findall(r"\[(C\d+)\]", answer)))

    # Map to full chunk data (excluding embedding)
    id_to_chunk = {c["id"]: c for c in ranked_chunks}
    citation_chunks = [
        id_to_chunk[cid]
        for cid in cited_ids
        if cid in id_to_chunk
    ] or ranked_chunks[:3]

    def strip_embedding(c: dict) -> dict:
        return {k: v for k, v in c.items() if k != "embedding"}

    return {
        "answer": answer,
        "confidence": confidence,   # "strong" | "weak" | "none"
        "citations": [strip_embedding(c) for c in citation_chunks],
        "retrieved": [
            {**strip_embedding(c), "score": round(c["score"], 4)}
            for c in ranked_chunks
        ],
    }


# ── Session chunks ────────────────────────────────────────────────────────────

@app.get("/api/session/{session_id}/chunks")
async def get_chunks(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "session_id": session_id,
        "files": session["files"],
        "page_count": session["page_count"],
        "chunk_count": len(session["chunks"]),
        "chunks": [
            {k: v for k, v in c.items() if k != "embedding"}
            for c in session["chunks"]
        ],
    }


# ── Serve uploaded PDFs ───────────────────────────────────────────────────────

@app.get("/uploads/{filename}")
async def serve_upload(filename: str):
    path = UPLOADS_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path, media_type="application/pdf")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_pages(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}–{end}"
