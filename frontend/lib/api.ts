/**
 * lib/api.ts — typed API client for the FastAPI backend.
 */

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ── Types ─────────────────────────────────────────────────────────────────────

export interface Chunk {
  id: string;
  file_name: string;
  page_start: number;
  page_end: number;
  text: string;
  char_count: number;
  score?: number;
}

export interface UploadResponse {
  session_id: string;
  files: { name: string; url: string }[];
  page_count: number;
  chunk_count: number;
  chunks: Chunk[];
}

export type Confidence = "strong" | "weak" | "none";

export interface ChatResponse {
  answer: string;
  confidence: Confidence;
  citations: Chunk[];
  retrieved: Chunk[];
}

export interface HealthResponse {
  ok: boolean;
  has_api_key: boolean;
  chat_model: string;
  embedding_model: string;
}

// ── API helpers ───────────────────────────────────────────────────────────────

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error((body as { detail?: string }).detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function apiHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BASE}/api/health`);
  return handleResponse<HealthResponse>(res);
}

export async function apiUpload(files: File[]): Promise<UploadResponse> {
  const form = new FormData();
  for (const f of files) {
    form.append("files", f);
  }
  const res = await fetch(`${BASE}/api/upload`, { method: "POST", body: form });
  return handleResponse<UploadResponse>(res);
}

export async function apiChat(
  sessionId: string,
  question: string
): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, question }),
  });
  return handleResponse<ChatResponse>(res);
}

export function pdfUrl(fileUrl: string): string {
  return `${BASE}${fileUrl}`;
}
