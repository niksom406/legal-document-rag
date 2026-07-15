"use client";

import React from "react";
import { type Chunk, type Confidence } from "@/lib/api";

interface ConfidenceBadgeProps {
  confidence: Confidence;
}

const CONFIG: Record<Confidence, { label: string; className: string }> = {
  strong: { label: "Strong evidence", className: "badge-strong" },
  weak: { label: "Weak evidence", className: "badge-weak" },
  none: { label: "No supporting evidence found", className: "badge-none" },
};

export function ConfidenceBadge({ confidence }: ConfidenceBadgeProps) {
  const { label, className } = CONFIG[confidence];
  return <span className={`confidence-badge ${className}`}>{label}</span>;
}
