"use client";

/**
 * ChunkVisualizer.tsx
 *
 * Shows how the uploaded PDF was split into chunks:
 * - A visual "tape" of coloured blocks representing chunks by page
 * - Metadata: total chunks, avg size, overlap setting
 * - Expandable list to inspect each chunk's text
 */

import React, { useState } from "react";
import type { Chunk, UploadResponse } from "@/lib/api";

interface ChunkVisualizerProps {
  uploadData: UploadResponse;
}

const PAGE_COLORS = [
  "#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b",
  "#10b981", "#ef4444", "#06b6d4", "#f97316",
];

export function ChunkVisualizer({ uploadData }: ChunkVisualizerProps) {
  const [expanded, setExpanded] = useState(false);
  const [activeChunk, setActiveChunk] = useState<Chunk | null>(null);

  const { chunks, chunk_count, page_count } = uploadData;
  const avgSize = Math.round(chunks.reduce((s, c) => s + c.char_count, 0) / chunk_count);
  const maxSize = Math.max(...chunks.map((c) => c.char_count));

  return (
    <div className="chunk-viz">
      <button
        className="chunk-viz-toggle"
        onClick={() => setExpanded((v) => !v)}
      >
        <span className="chunk-viz-icon">🧩</span>
        <span>How chunking works</span>
        <span className="chunk-viz-arrow">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <div className="chunk-viz-body">
          {/* Stats row */}
          <div className="chunk-stats">
            <div className="chunk-stat">
              <span className="chunk-stat-val">{chunk_count}</span>
              <span className="chunk-stat-label">Chunks</span>
            </div>
            <div className="chunk-stat">
              <span className="chunk-stat-val">{page_count}</span>
              <span className="chunk-stat-label">Pages</span>
            </div>
            <div className="chunk-stat">
              <span className="chunk-stat-val">{avgSize}</span>
              <span className="chunk-stat-label">Avg chars</span>
            </div>
            <div className="chunk-stat">
              <span className="chunk-stat-val">45w</span>
              <span className="chunk-stat-label">Overlap</span>
            </div>
          </div>

          {/* How it works explanation */}
          <div className="chunk-explainer">
            <p className="chunk-explainer-title">📐 Chunking strategy</p>
            <ol className="chunk-steps">
              <li><strong>Extract</strong> text from each PDF page using pypdf</li>
              <li><strong>Split</strong> each page on blank lines into paragraphs</li>
              <li><strong>Accumulate</strong> paragraphs up to <code>900 chars</code></li>
              <li><strong>Emit</strong> a chunk, then carry <code>45 words</code> forward as overlap into the next chunk</li>
              <li><strong>Embed</strong> each chunk with <code>text-embedding-3-small</code></li>
              <li><strong>Rank</strong> by cosine similarity to the question at query time</li>
            </ol>
            <p className="chunk-why">
              The 45-word overlap ensures answers are never cut off at a paragraph
              boundary — context from the end of one chunk always appears at the
              start of the next.
            </p>
          </div>

          {/* Visual tape */}
          <p className="chunk-tape-label">Chunks across pages (click to inspect)</p>
          <div className="chunk-tape">
            {chunks.map((chunk) => {
              const pageColor = PAGE_COLORS[(chunk.page_start - 1) % PAGE_COLORS.length];
              const widthPct = Math.max(4, (chunk.char_count / maxSize) * 100);
              const isActive = activeChunk?.id === chunk.id;

              return (
                <button
                  key={chunk.id}
                  className={`chunk-block ${isActive ? "chunk-block--active" : ""}`}
                  style={{
                    width: `${widthPct}%`,
                    backgroundColor: isActive
                      ? "rgba(201,168,76,0.6)"
                      : `${pageColor}33`,
                    borderColor: isActive ? "#c9a84c" : pageColor,
                  }}
                  onClick={() => setActiveChunk(isActive ? null : chunk)}
                  title={`${chunk.id} · Page ${chunk.page_start} · ${chunk.char_count} chars`}
                >
                  <span className="chunk-block-id">{chunk.id}</span>
                </button>
              );
            })}
          </div>

          {/* Active chunk detail */}
          {activeChunk && (
            <div className="chunk-detail">
              <div className="chunk-detail-header">
                <span className="chunk-detail-id">{activeChunk.id}</span>
                <span className="chunk-detail-meta">
                  Page {activeChunk.page_start} · {activeChunk.char_count} chars
                </span>
                <button
                  className="chunk-detail-close"
                  onClick={() => setActiveChunk(null)}
                >
                  ×
                </button>
              </div>
              <pre className="chunk-detail-text">{activeChunk.text}</pre>
              {/* Show overlap visually */}
              <p className="chunk-overlap-note">
                ↩ The last ~45 words of this chunk are carried forward as context into the next chunk.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
