"use client";

/**
 * PDFViewer.tsx — Full PDF viewer with DOM-based precise citation highlighting.
 *
 * Approach:
 * - Render all pages with react-pdf (text layer enabled)
 * - When activeCitation changes, walk the actual DOM text layer of that page
 * - Concatenate all span text to find the exact location of the citation string
 * - Apply inline background highlights to matching spans
 * - Much more reliable than customTextRenderer (which processes spans independently)
 */

import React, { useCallback, useEffect, useRef, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import type { Chunk } from "@/lib/api";

import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

interface PDFViewerProps {
  fileUrl: string;
  activeCitation: Chunk | null;
  allCitations: Chunk[];
  onCitationClick: (id: string) => void;
}

export function PDFViewer({
  fileUrl,
  activeCitation,
  allCitations,
  onCitationClick,
}: PDFViewerProps) {
  const [numPages, setNumPages] = useState(0);
  const [containerWidth, setContainerWidth] = useState(400);
  const [renderedPages, setRenderedPages] = useState<Set<number>>(new Set());
  const containerRef = useRef<HTMLDivElement>(null);
  const pageRefs = useRef<Record<number, HTMLDivElement | null>>({});

  // Responsive width
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setContainerWidth(el.clientWidth - 16));
    ro.observe(el);
    setContainerWidth(el.clientWidth - 16);
    return () => ro.disconnect();
  }, []);

  // Scroll to active citation page
  useEffect(() => {
    if (!activeCitation) return;
    const el = pageRefs.current[activeCitation.page_start];
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [activeCitation]);

  // Apply DOM-based highlights whenever activeCitation or rendered pages change
  useEffect(() => {
    clearAllHighlights();
    if (!activeCitation) return;

    // Small delay so the text layer is fully painted
    const timer = setTimeout(() => {
      applyHighlight(activeCitation, pageRefs.current[activeCitation.page_start]);
    }, 150);

    return () => {
      clearTimeout(timer);
      clearAllHighlights();
    };
  }, [activeCitation, renderedPages]);

  function onDocumentLoadSuccess({ numPages: n }: { numPages: number }) {
    setNumPages(n);
  }

  function onPageRenderSuccess(pageNumber: number) {
    setRenderedPages((prev) => new Set([...prev, pageNumber]));
  }

  // Citations grouped by page
  const citationsByPage = React.useMemo(() => {
    const map: Record<number, Chunk[]> = {};
    for (const c of allCitations) {
      for (let p = c.page_start; p <= c.page_end; p++) {
        (map[p] ??= []).push(c);
      }
    }
    return map;
  }, [allCitations]);

  return (
    <div className="pdf-viewer-wrap" ref={containerRef}>
      <Document
        file={fileUrl}
        onLoadSuccess={onDocumentLoadSuccess}
        loading={<PDFLoading />}
        error={<PDFError />}
        className="pdf-document"
      >
        {Array.from({ length: numPages }, (_, i) => i + 1).map((pageNum) => {
          const pageCitations = citationsByPage[pageNum] ?? [];
          const isActivePage = activeCitation?.page_start === pageNum;

          return (
            <div
              key={pageNum}
              ref={(el) => { pageRefs.current[pageNum] = el; }}
              className={`pdf-page-wrap ${isActivePage ? "pdf-page-wrap--active" : ""}`}
            >
              {/* Page header bar */}
              <div className="pdf-page-label">
                <span>Page {pageNum}</span>
                {pageCitations.length > 0 && (
                  <span className="pdf-page-citation-pills">
                    {pageCitations.map((c) => (
                      <button
                        key={c.id}
                        className={`pdf-page-pill ${c.id === activeCitation?.id ? "pdf-page-pill--active" : ""}`}
                        onClick={() => onCitationClick(c.id)}
                        title={`Citation ${c.id} — click to highlight`}
                      >
                        {c.id}
                      </button>
                    ))}
                  </span>
                )}
              </div>

              <Page
                pageNumber={pageNum}
                width={containerWidth}
                renderTextLayer={true}
                renderAnnotationLayer={false}
                onRenderSuccess={() => onPageRenderSuccess(pageNum)}
                className={`pdf-page ${isActivePage ? "pdf-page--active" : ""}`}
              />
            </div>
          );
        })}
      </Document>
    </div>
  );
}

// ── DOM-based highlight helpers ───────────────────────────────────────────────

function clearAllHighlights() {
  document.querySelectorAll(".pdf-hl-span").forEach((el) => {
    (el as HTMLElement).style.backgroundColor = "";
    (el as HTMLElement).style.borderRadius = "";
    (el as HTMLElement).style.boxShadow = "";
    el.classList.remove("pdf-hl-span");
  });
}

function applyHighlight(citation: Chunk, pageEl: HTMLDivElement | null) {
  if (!pageEl) return;

  const textLayer = pageEl.querySelector(".react-pdf__Page__textContent");
  if (!textLayer) return;

  // Collect all leaf text spans
  const spans = Array.from(
    textLayer.querySelectorAll("span")
  ) as HTMLElement[];

  if (spans.length === 0) return;

  // Build a normalized string and a character map
  let normHaystack = "";
  const normToSpanIndex: number[] = [];

  for (let i = 0; i < spans.length; i++) {
    // Add a space to ensure spans don't meld if they shouldn't, 
    // though the alphanumeric filter below makes this less critical
    const text = (spans[i].textContent ?? "") + " ";
    for (let c = 0; c < text.length; c++) {
      const char = text[c].toLowerCase();
      if (char.match(/[a-z0-9]/)) {
        normHaystack += char;
        normToSpanIndex.push(i);
      }
    }
  }

  const citationNorm = citation.text.toLowerCase().replace(/[^a-z0-9]/g, "");

  if (citationNorm.length < 35) {
    const idx = normHaystack.indexOf(citationNorm);
    if (idx !== -1) {
      const highlightSpans = new Set<HTMLElement>();
      for (let k = idx; k < idx + citationNorm.length; k++) {
        if (k < normToSpanIndex.length) highlightSpans.add(spans[normToSpanIndex[k]]);
      }
      for (const el of highlightSpans) {
        el.style.backgroundColor = "rgba(201, 168, 76, 0.45)";
        el.style.borderRadius = "3px";
        el.style.boxShadow = "0 0 0 1px rgba(201,168,76,0.3)";
        el.classList.add("pdf-hl-span");
      }
      return;
    }
  } else {
    const needles: string[] = [];
    const offsets: number[] = [];
    for (let i = 0; i <= citationNorm.length - 25; i += 20) {
      needles.push(citationNorm.slice(i, i + 35));
      offsets.push(i);
    }

    const matches: { needleIndex: number; haystackIndex: number }[] = [];
    for (let i = 0; i < needles.length; i++) {
      let searchPos = 0;
      while (true) {
        const idx = normHaystack.indexOf(needles[i], searchPos);
        if (idx === -1) break;
        matches.push({ needleIndex: i, haystackIndex: idx });
        searchPos = idx + 1;
      }
    }

    if (matches.length > 0) {
      matches.sort((a, b) => a.haystackIndex - b.haystackIndex);
      const clusters: typeof matches[] = [];

      for (const m of matches) {
        let joined = false;
        for (const cluster of clusters) {
          const last = cluster[cluster.length - 1];
          const expectedDist = offsets[m.needleIndex] - offsets[last.needleIndex];
          const actualDist = m.haystackIndex - last.haystackIndex;
          
          if (m.needleIndex > last.needleIndex && actualDist > 0 && Math.abs(actualDist - expectedDist) < 35) {
            cluster.push(m);
            joined = true;
            break;
          }
        }
        if (!joined) {
          clusters.push([m]);
        }
      }

      clusters.sort((a, b) => b.length - a.length);
      const bestCluster = clusters[0];

      if (bestCluster.length > 0) {
        const first = bestCluster[0];
        const last = bestCluster[bestCluster.length - 1];
        
        const startIdx = Math.max(0, first.haystackIndex - offsets[first.needleIndex]);
        const endOffsetFromNeedle = citationNorm.length - offsets[last.needleIndex];
        const endIdx = Math.min(normHaystack.length, last.haystackIndex + endOffsetFromNeedle);

        const highlightSpans = new Set<HTMLElement>();
        for (let k = startIdx; k < endIdx; k++) {
          if (k >= 0 && k < normToSpanIndex.length) {
            highlightSpans.add(spans[normToSpanIndex[k]]);
          }
        }
        
        for (const el of highlightSpans) {
          el.style.backgroundColor = "rgba(201, 168, 76, 0.45)";
          el.style.borderRadius = "3px";
          el.style.boxShadow = "0 0 0 1px rgba(201,168,76,0.3)";
          el.classList.add("pdf-hl-span");
        }
        return;
      }
    }
  }

  // Fallback: highlight all spans on the active page (so user can at least see the page)
  for (const el of spans.slice(0, 30)) {
    el.style.backgroundColor = "rgba(201, 168, 76, 0.15)";
    el.style.borderRadius = "3px";
    el.classList.add("pdf-hl-span");
  }
}

// ── Loading / Error ───────────────────────────────────────────────────────────

function PDFLoading() {
  return (
    <div className="pdf-loading">
      <div className="spinner" />
      <p>Loading PDF…</p>
    </div>
  );
}

function PDFError() {
  return (
    <div className="pdf-error">
      <p>Could not load PDF. Ensure the backend server is running.</p>
    </div>
  );
}
