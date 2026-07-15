# ABC Matter RAG Demo

Upload a conveyancing matter PDF, ask questions, and get cited answers grounded in the retrieved chunks. Click a citation to see the exact section used.

## Try it (recruiter)

**Live demo:** https://legal-document-rag.vercel.app

1. Open the link above.
2. Upload a matter PDF (samples in `sample_documents/`).
3. Ask a question, then click citations to inspect the source chunks.

API: https://legal-rag-api.vercel.app

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

Both apps are on Vercel:

- **Frontend:** set `NEXT_PUBLIC_API_URL` to the API URL.
- **Backend:** set `OPENAI_API_KEY` and `CORS_ORIGINS` (frontend URL). `render.yaml` remains as an alternate host option.

## Notes

- Narrow demo for uploaded matter PDFs (not connected to a case management system).
- Citations are chunk-based; sessions are in-memory and clear on server restart.
- Image-only PDFs without selectable text may extract poorly.
