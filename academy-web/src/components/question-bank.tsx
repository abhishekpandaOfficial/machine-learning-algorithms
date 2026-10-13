"use client";

import { useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";

type Question = {
  id: string;
  title: string;
  difficulty: string;
  type: string;
  tags: string[];
  answer: string;
  example: string;
  pitfall: string;
  practice: string;
};

const difficulties = ["All levels", "Beginner", "Intermediate", "Advanced"];
const types = ["All types", "Concept", "Comparison", "Problem framing", "Problem solving", "Technique", "Data quality", "Algorithm", "Metric", "Validation design", "Debugging", "Scenario", "Incident response", "Decision making", "Capstone scenario", "Workflow", "Engineering"];

export default function QuestionBank({ questions }: { questions: Question[] }) {
  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState("All levels");
  const [type, setType] = useState("All types");
  const [expanded, setExpanded] = useState<string[]>([]);
  const [showAll, setShowAll] = useState(false);

  const filtered = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return questions.filter((question) => {
      const matchesQuery = !normalized || [
        question.id, question.title, question.type, question.difficulty,
        question.answer, question.example, question.pitfall, question.practice,
        ...question.tags,
      ].join(" ").toLowerCase().includes(normalized);
      return matchesQuery &&
        (difficulty === "All levels" || question.difficulty === difficulty) &&
        (type === "All types" || question.type === type);
    });
  }, [questions, query, difficulty, type]);

  const visible = showAll ? filtered : filtered.slice(0, 12);
  const allVisibleExpanded = visible.length > 0 && visible.every((question) => expanded.includes(question.id));

  function toggle(id: string) {
    setExpanded((current) => current.includes(id) ? current.filter((item) => item !== id) : [...current, id]);
  }

  return (
    <section className="bank" aria-label="Machine learning question bank">
      <div className="bank-toolbar">
        <label className="search-box">
          <span aria-hidden="true">⌕</span>
          <input value={query} onChange={(event) => { setQuery(event.target.value); setShowAll(false); }} placeholder="Search questions, concepts, tags…" aria-label="Search questions" />
          {query && <button type="button" className="clear-search" onClick={() => setQuery("")} aria-label="Clear search">×</button>}
        </label>
        <label className="filter-label"><span>Difficulty</span><select value={difficulty} onChange={(event) => { setDifficulty(event.target.value); setShowAll(false); }} aria-label="Filter by difficulty">{difficulties.map((item) => <option key={item}>{item}</option>)}</select></label>
        <label className="filter-label"><span>Question type</span><select value={type} onChange={(event) => { setType(event.target.value); setShowAll(false); }} aria-label="Filter by question type">{types.map((item) => <option key={item}>{item}</option>)}</select></label>
      </div>
      <div className="result-line"><span><b>{filtered.length}</b> questions found</span><button type="button" className="quiet-button" onClick={() => setExpanded(allVisibleExpanded ? [] : [...new Set([...expanded, ...visible.map((question) => question.id)])])}>{allVisibleExpanded ? "Collapse visible answers" : "Expand visible answers"}</button></div>
      {filtered.length === 0 ? (
        <div className="empty-state"><span>⌕</span><h3>No matching questions</h3><p>Try a broader keyword or reset your filters.</p><button type="button" onClick={() => { setQuery(""); setDifficulty("All levels"); setType("All types"); }}>Reset filters</button></div>
      ) : (
        <div className="question-list">
          {visible.map((question, index) => {
            const isExpanded = expanded.includes(question.id);
            return (
              <article className={`question-card ${isExpanded ? "is-expanded" : ""}`} key={question.id}>
                <button type="button" className="question-trigger" onClick={() => toggle(question.id)} aria-expanded={isExpanded} aria-controls={`answer-${question.id}`}>
                  <span className="question-number">{String(index + 1).padStart(2,"0")}</span>
                  <span className="question-heading"><span className="question-id">{question.id}</span><strong>{question.title}</strong><span className="tag-row">{question.tags.slice(0,3).map((tag) => <span className="tag" key={tag}>{tag}</span>)}</span></span>
                  <span className="question-meta"><span className={`difficulty-pill ${question.difficulty.toLowerCase()}`}>{question.difficulty}</span><span className="chevron">{isExpanded ? "−" : "+"}</span></span>
                </button>
                {isExpanded && <div className="answer-panel" id={`answer-${question.id}`}>
                  <div className="answer-block"><span className="answer-label">THE ANSWER</span><div className="markdown-body"><ReactMarkdown>{question.answer}</ReactMarkdown></div></div>
                  <div className="answer-grid">
                    <section><span className="answer-label"><span className="answer-dot mint-dot" /> PRACTICAL EXAMPLE</span><div className="markdown-body"><ReactMarkdown>{question.example}</ReactMarkdown></div></section>
                    <section><span className="answer-label"><span className="answer-dot amber-dot" /> WATCH OUT</span><div className="markdown-body"><ReactMarkdown>{question.pitfall}</ReactMarkdown></div></section>
                  </div>
                  <div className="practice-box"><span>↳ TRY IT</span><p>{question.practice}</p></div>
                </div>}
              </article>
            );
          })}
        </div>
      )}
      {filtered.length > 12 && <button type="button" className="load-more" onClick={() => setShowAll(!showAll)}>{showAll ? "Show fewer questions" : `Load all ${filtered.length} questions`} <span>{showAll ? "↑" : "↓"}</span></button>}
      <p className="bank-note">Question IDs are stable. New releases will expand this bank toward 1,200+ reviewed questions.</p>
    </section>
  );
}
