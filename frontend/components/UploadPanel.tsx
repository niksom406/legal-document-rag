"use client";

import React, { useRef, useState } from "react";
import { apiUpload, type UploadResponse } from "@/lib/api";
import { ChunkVisualizer } from "./ChunkVisualizer";

interface UploadPanelProps {
  onUploadSuccess: (data: UploadResponse) => void;
}

export function UploadPanel({ onUploadSuccess }: UploadPanelProps) {
  const [status, setStatus] = useState<"idle" | "uploading" | "done" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [docInfo, setDocInfo] = useState<UploadResponse | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function processFiles(files: File[]) {
    const invalid = files.find(f => f.type !== "application/pdf");
    if (invalid) {
      setErrorMsg(`Only PDF files are supported. Found: ${invalid.name}`);
      setStatus("error");
      return;
    }

    setStatus("uploading");
    setErrorMsg(null);

    try {
      const data = await apiUpload(files);
      setDocInfo(data);
      setStatus("done");
      onUploadSuccess(data);
    } catch (err: unknown) {
      setErrorMsg(err instanceof Error ? err.message : "Upload failed.");
      setStatus("error");
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(e.target.files || []);
    if (files.length > 0) processFiles(files);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) processFiles(files);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(true);
  }

  return (
    <aside className="upload-panel">
      {/* Logo / Brand */}
      <div className="brand">
        <div className="brand-logo">A</div>
        <div>
          <div className="brand-name">ABC</div>
          <div className="brand-tagline">Matter Assistant</div>
        </div>
      </div>

      <hr className="divider" />

      {/* Upload area */}
      <h2 className="panel-section-title">Upload Matter PDF</h2>

      <div
        className={`drop-zone ${dragOver ? "drop-zone--over" : ""} ${status === "uploading" ? "drop-zone--loading" : ""}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={() => setDragOver(false)}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          multiple

          className="sr-only"
          onChange={handleFileChange}
          disabled={status === "uploading"}
        />
        {status === "uploading" ? (
          <div className="drop-zone-content">
            <div className="spinner" />
            <p>Extracting text, chunking, and embedding…</p>
          </div>
        ) : (
          <div className="drop-zone-content">
            <div className="upload-icon">📄</div>
            <p className="drop-primary">Drop PDFs here</p>
            <p className="drop-secondary">or click to browse multiple files</p>
          </div>
        )}
      </div>

      {status === "error" && errorMsg && (
        <p className="upload-error">{errorMsg}</p>
      )}

      {/* Document info */}
      {docInfo && status === "done" && (
        <div className="doc-info">
          <div className="doc-info-icon">✅</div>
          <div>
            <div className="doc-name">
              {docInfo.files.map((f, i) => (
                <div key={i}>{f.name}</div>
              ))}
            </div>
            <p className="doc-meta">
              {docInfo.page_count} pages · {docInfo.chunk_count} chunks indexed
            </p>
          </div>
        </div>
      )}

      {docInfo && status === "done" && (
        <ChunkVisualizer uploadData={docInfo} />
      )}

      <hr className="divider" />

      {/* Safety notice */}
      <div className="safety-notice">
        <p className="safety-title">🔒 Safety Controls Active</p>
        <ul className="safety-list">
          <li>Read-only — no writes to any system</li>
          <li>Answers grounded in document only</li>
          <li>Every claim cites its source passage</li>
          <li>All actions require human approval</li>
        </ul>
      </div>
    </aside>
  );
}
