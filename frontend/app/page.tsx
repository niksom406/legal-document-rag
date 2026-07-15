"use client";

import React, { useState } from "react";
import { UploadPanel } from "@/components/UploadPanel";
import { ChatPanel } from "@/components/ChatPanel";
import { CitationSidebar } from "@/components/CitationSidebar";
import { type Chunk, type UploadResponse, pdfUrl } from "@/lib/api";

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [fileUrls, setFileUrls] = useState<Record<string, string>>({});
  const [citations, setCitations] = useState<Chunk[]>([]);
  const [activeCitationId, setActiveCitationId] = useState<string | null>(null);

  function handleUploadSuccess(data: UploadResponse) {
    setSessionId(data.session_id);
    const urls: Record<string, string> = {};
    data.files.forEach((f) => {
      urls[f.name] = pdfUrl(f.url);
    });
    setFileUrls(urls);
    setCitations([]);
    setActiveCitationId(null);
  }

  function handleCitationsChange(newCitations: Chunk[], activeId: string | null) {
    setCitations(newCitations);
    setActiveCitationId(activeId);
  }

  function handleCitationClick(id: string) {
    setActiveCitationId(id);
  }

  return (
    <div className="app-layout">
      <UploadPanel onUploadSuccess={handleUploadSuccess} />
      <ChatPanel
        sessionId={sessionId}
        onCitationsChange={handleCitationsChange}
      />
      <CitationSidebar
        citations={citations}
        activeCitationId={activeCitationId}
        fileUrls={fileUrls}
        onCitationClick={handleCitationClick}
      />
    </div>
  );
}
