# ABC Matter RAG Demo

Upload a conveyancing matter PDF, ask questions, and get cited answers grounded in the retrieved chunks. Click a citation to see the exact section used.

## Try it (recruiter)

1. Open the deployed frontend URL (Vercel).
2. Upload a matter PDF (sample files are in `sample_documents/`).
3. Ask a question, then click citations to inspect the source chunks.

**Note:** The free backend may sleep after idle time — the first request can take ~30–60 seconds.

## Local development

Requirements: Node.js 22+, Python 3.11+, OpenAI API key.

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set OPENAI_API_KEY
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
# .env.local should contain:
# NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:3000

## Deploy

- **Backend:** Render (`render.yaml`) — set `OPENAI_API_KEY` and `CORS_ORIGINS` (your Vercel URL).
- **Frontend:** Vercel — set `NEXT_PUBLIC_API_URL` to the Render service URL.

## Notes

- Narrow demo for uploaded matter PDFs (not connected to a case management system).
- Citations are chunk-based; sessions are in-memory and clear on server restart.
- Image-only PDFs without selectable text may extract poorly.
