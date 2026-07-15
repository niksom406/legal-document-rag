"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { type Chunk } from "@/lib/api";

// Load PDF viewer client-side only (PDF.js requires browser APIs)
const PDFViewer = dynamic(
  () => import("./PDFViewer").then((m) => ({ default: m.PDFViewer })),
  { ssr: false, loading: () => <div className="pdf-loading"><div className="spinner" /><p>Loading viewer…</p></div> }
);

interface CitationSidebarProps {
  citations: Chunk[];
  activeCitationId: string | null;
  fileUrls: Record<string, string>;
  onCitationClick: (id: string) => void;
}

export function CitationSidebar({
  citations,
  activeCitationId,
  fileUrls,
  onCitationClick,
}: CitationSidebarProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const activeCitation = citations.find((c) => c.id === activeCitationId) ?? null;

  // Auto-switch document when citation is clicked
  useEffect(() => {
    if (activeCitation?.file_name) {
      setSelectedFile(activeCitation.file_name);
    }
  }, [activeCitation]);

  // Default to first file if none selected
  const files = Object.keys(fileUrls);
  const currentFile = (selectedFile && files.includes(selectedFile)) ? selectedFile : (files[0] ?? null);
  const currentFileUrl = currentFile ? fileUrls[currentFile] : null;

  // Filter citations passed to PDFViewer to only those belonging to currentFile
  const currentFileCitations = citations.filter((c) => c.file_name === currentFile);

  return (
    <aside className="citation-sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <h2 className="sidebar-title">
          Document Viewer
          {citations.length > 0 && (
            <span className="citation-count">{citations.length} citations</span>
          )}
        </h2>

        {/* Document selector */}
        {files.length > 0 && (
          <div className="document-tabs">
            {files.map((file) => (
              <button
                key={file}
                className={`doc-tab ${file === currentFile ? "doc-tab--active" : ""}`}
                onClick={() => setSelectedFile(file)}
                title={file}
              >
                {file.length > 25 ? file.slice(0, 22) + "..." : file}
              </button>
            ))}
          </div>
        )}

        {/* Citation pills row (for current file) */}
        {currentFileCitations.length > 0 && (
          <div className="citation-pill-row">
            {currentFileCitations.map((c) => (
              <button
                key={c.id}
                className={`citation-pill ${c.id === activeCitationId ? "citation-pill--active" : ""}`}
                onClick={() => onCitationClick(c.id)}
                title={`Pages ${c.page_start}–${c.page_end}: ${c.text.slice(0, 80)}…`}
              >
                {c.id}
                <span className="citation-pill-page">p.{c.page_start}</span>
              </button>
            ))}
          </div>
        )}

        {/* Active citation excerpt */}
        {activeCitation && (
          <div className="active-citation-excerpt">
            <div className="excerpt-header">
              <span className="excerpt-chip">{activeCitation.id}</span>
              <span className="excerpt-page">
                {activeCitation.file_name}, Page {activeCitation.page_start}
                {activeCitation.page_end !== activeCitation.page_start && `–${activeCitation.page_end}`}
              </span>
              <span className="excerpt-label">highlighted below ↓</span>
            </div>
            <p className="excerpt-text">{activeCitation.text.slice(0, 200)}{activeCitation.text.length > 200 ? "…" : ""}</p>
          </div>
        )}
      </div>

      <div className="pdf-panel">
        {currentFileUrl ? (
          <PDFViewer
            fileUrl={currentFileUrl}
            activeCitation={activeCitation?.file_name === currentFile ? activeCitation : null}
            allCitations={currentFileCitations}
            onCitationClick={onCitationClick}
          />
        ) : (
          <div className="sidebar-empty">
            <div className="sidebar-empty-icon">📄</div>
            <p>Upload a matter PDF to see it here.</p>
            <p className="sidebar-empty-sub">
              After asking a question, click any{" "}
              <code>[C1]</code> citation to jump to that passage and highlight it in the document.
            </p>
          </div>
        )}
      </div>
    </aside>
  );
}
