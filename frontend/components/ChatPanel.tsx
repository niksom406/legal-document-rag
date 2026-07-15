"use client";

import React, { useEffect, useRef, useState } from "react";
import { apiChat, type ChatResponse, type Chunk, type Confidence } from "@/lib/api";
import { ConfidenceBadge } from "./ConfidenceBadge";

interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  confidence?: Confidence;
  citations?: Chunk[];
}

interface ChatPanelProps {
  sessionId: string | null;
  onCitationsChange: (citations: Chunk[], activeCitationId: string | null) => void;
}

const SAMPLE_QUESTIONS = [
  "What are the outstanding mortgage conditions and how do they relate to the search results?",
  "Is there any issue with building regulations for the rear extension?",
  "What is the status of the Japanese knotweed enquiry and the related mortgage condition?",
  "Who is providing the gifted deposit and what AML documents are still missing?",
];

export function ChatPanel({ sessionId, onCitationsChange }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e?: React.FormEvent) {
    e?.preventDefault();
    const q = question.trim();
    if (!q || !sessionId || loading) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      text: q,
    };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setError(null);
    setLoading(true);

    // Reset citation panel
    onCitationsChange([], null);

    try {
      const data: ChatResponse = await apiChat(sessionId, q);

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: data.answer,
        confidence: data.confidence,
        citations: data.citations,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      onCitationsChange(data.citations, null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleCitationClick(citationId: string, citations: Chunk[]) {
    onCitationsChange(citations, citationId);
  }

  function useSampleQuestion(q: string) {
    setQuestion(q);
    textareaRef.current?.focus();
  }

  return (
    <section className="chat-panel">
      {/* Message history */}
      <div className="message-list">
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <div className="chat-empty-icon">⚖️</div>
            <h3>ABC Matter Assistant</h3>
            <p>
              Upload a matter PDF then ask anything about it. Every answer is
              grounded in the document and traceable to a specific passage.
            </p>
            {sessionId && (
              <>
                <p className="sample-label">Try a sample question:</p>
                <ul className="sample-questions">
                  {SAMPLE_QUESTIONS.map((sq) => (
                    <li key={sq}>
                      <button
                        className="sample-question-btn"
                        onClick={() => useSampleQuestion(sq)}
                      >
                        {sq}
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            onCitationClick={(cid) =>
              msg.citations && handleCitationClick(cid, msg.citations)
            }
          />
        ))}

        {loading && (
          <div className="message message--assistant">
            <div className="message-bubble message-bubble--assistant loading-bubble">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        )}

        {error && (
          <div className="chat-error">
            <strong>Error:</strong> {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className="chat-textarea"
          rows={2}
          placeholder={
            sessionId
              ? "Ask about this matter… (Enter to send, Shift+Enter for new line)"
              : "Upload a PDF to start asking questions"
          }
          value={question}
          disabled={!sessionId || loading}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="send-button"
          type="submit"
          disabled={!sessionId || loading || !question.trim()}
          aria-label="Send question"
        >
          {loading ? "…" : "Send"}
        </button>
      </form>

      {sessionId && (
        <p className="chat-disclaimer">
          Answers are grounded in the uploaded document only. All suggested actions require human review before being acted on.
        </p>
      )}
    </section>
  );
}

// ── Message bubble ─────────────────────────────────────────────────────────────

interface MessageBubbleProps {
  message: Message;
  onCitationClick: (citationId: string) => void;
}

function MessageBubble({ message, onCitationClick }: MessageBubbleProps) {
  const isUser = message.role === "user";

  // Parse suggested actions section out of the answer
  const suggestedActionsMatch = message.text.match(
    /Suggested actions \(for staff review only\):([\s\S]*?)(?=$|\n\n[^\s])/i
  );
  const suggestedActions = suggestedActionsMatch?.[1]?.trim() ?? null;
  const mainText = suggestedActionsMatch
    ? message.text.slice(0, suggestedActionsMatch.index).trim()
    : message.text;

  return (
    <div className={`message ${isUser ? "message--user" : "message--assistant"}`}>
      <div className={`message-bubble ${isUser ? "message-bubble--user" : "message-bubble--assistant"}`}>
        {isUser ? (
          <p>{message.text}</p>
        ) : (
          <>
            {message.confidence && (
              <div className="message-meta">
                <ConfidenceBadge confidence={message.confidence} />
              </div>
            )}
            <div className="message-text">
              {renderAnswerWithCitations(mainText, message.citations ?? [], onCitationClick)}
            </div>
            {suggestedActions && (
              <div className="suggested-actions">
                <span className="suggested-actions-label">
                  📋 Suggested actions (staff review only)
                </span>
                <p>{suggestedActions}</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function renderAnswerWithCitations(
  text: string,
  citations: Chunk[],
  onCitationClick: (id: string) => void
): React.ReactNode {
  const citationSet = new Set(citations.map((c) => c.id));
  const parts = text.split(/(\[C\d+\])/g);

  return (
    <span>
      {parts.map((part, i) => {
        const match = part.match(/^\[(C\d+)\]$/);
        if (match) {
          const id = match[1];
          return citationSet.has(id) ? (
            <button
              key={i}
              className="citation-pill"
              onClick={() => onCitationClick(id)}
              title={`Jump to source ${id}`}
            >
              {id}
            </button>
          ) : (
            <span key={i}>{part}</span>
          );
        }
        // Render newlines as <br />
        return (
          <span key={i}>
            {part.split("\n").map((line, j, arr) => (
              <React.Fragment key={j}>
                {line}
                {j < arr.length - 1 && <br />}
              </React.Fragment>
            ))}
          </span>
        );
      })}
    </span>
  );
}
