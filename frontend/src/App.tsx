import { FormEvent, useState } from "react";
import { BookOpen, Download, LoaderCircle, Search, Sparkles } from "lucide-react";

type ResearchResult = {
  search_results: string;
  scraped_content: string;
  report: string;
  critique: string;
};

const tabs = [
  ["sources", "Sources"],
  ["notes", "Notes"],
  ["report", "Report"],
  ["review", "Review"],
] as const;

function App() {
  const [topic, setTopic] = useState("");
  const [numResults, setNumResults] = useState(5);
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof tabs)[number][0]>("report");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runResearch(event: FormEvent) {
    event.preventDefault();
    if (!topic.trim()) {
      setError("Add a research question to begin.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic.trim(), num_results: numResults }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "Research could not be completed.");
      setResult(body as ResearchResult);
      setActiveTab("report");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Research could not be completed.");
    } finally {
      setLoading(false);
    }
  }

  function downloadReport() {
    if (!result) return;
    const blob = new Blob([result.report], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "research-report.md";
    link.click();
    URL.revokeObjectURL(link.href);
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark"><Sparkles size={16} /></span> Research lab</div>
        <nav>
          <a className="nav-link active"><Search size={16} /> New research</a>
          <a className="nav-link"><BookOpen size={16} /> Source library</a>
          <a className="nav-link"><span className="nav-dot" /> Saved reports</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="eyebrow">Workflow</div>
          <p>Find signal, understand context, and make evidence easier to act on.</p>
          <div className="pipeline-mini">
            <span /><span /><span /><span />
          </div>
          <small>Search · Extract · Write · Review</small>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar"><span className="status-dot" /> Workspace / New research <span className="topbar-date">Private session</span></header>
        <section className="hero">
          <div className="hero-kicker"><span /> Evidence, distilled</div>
          <h1>What should we<br /><em>focus on?</em></h1>
          <p className="hero-copy">A calm space to search, synthesize, and pressure-test the ideas that matter.</p>
          <form onSubmit={runResearch} className="research-form">
            <textarea value={topic} onChange={(event) => setTopic(event.target.value)} placeholder="Ask a question worth exploring..." rows={3} />
            <div className="form-footer">
              <label>Depth <input type="range" min="1" max="10" value={numResults} onChange={(event) => setNumResults(Number(event.target.value))} /><strong>{numResults} sources</strong></label>
              <button type="submit" disabled={loading}>{loading ? <><LoaderCircle className="spin" size={17} /> Researching...</> : <><span>Start research</span><span className="button-arrow">↗</span></>}</button>
            </div>
          </form>
          {error && <p className="error-message">{error}</p>}
        </section>

        {result ? (
          <section className="results-panel">
            <div className="results-heading"><div><div className="eyebrow">Research complete</div><h2>Your briefing</h2></div><button className="download-button" onClick={downloadReport}><Download size={15} /> Export markdown</button></div>
            <div className="tabs">{tabs.map(([id, label]) => <button key={id} className={activeTab === id ? "tab active" : "tab"} onClick={() => setActiveTab(id)}>{label}<span>{id === "sources" ? numResults : id === "review" ? "AI" : ""}</span></button>)}</div>
            <article className="result-card"><div className="result-meta">{tabs.find(([id]) => id === activeTab)?.[1]}</div><div className="result-copy">{result[activeTab === "sources" ? "search_results" : activeTab === "notes" ? "scraped_content" : activeTab === "review" ? "critique" : "report"]}</div></article>
          </section>
        ) : (
          <section className="empty-state"><div className="empty-icon"><BookOpen size={20} /></div><div><strong>Your research will appear here</strong><p>Sources, notes, a clear report, and a critical review — all in one place.</p></div></section>
        )}
      </main>
    </div>
  );
}

export default App;
