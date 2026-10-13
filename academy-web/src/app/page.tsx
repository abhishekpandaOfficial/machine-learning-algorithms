import QuestionBank from "@/components/question-bank";
import questions from "@/data/questions.json";

export default function HomePage() {
  const total = questions.length;
  const scenarioCount = questions.filter((question) => question.type === "Scenario" || question.type === "Debugging" || question.type === "Decision making").length;

  return (
    <main className="site-shell">
      <header className="topbar">
        <a className="wordmark" href="/" aria-label="Machine Learning Knowledge Academy home">
          <span className="mark">ML</span>
          <span>Knowledge Academy</span>
        </a>
        <nav className="topnav" aria-label="Main navigation">
          <a href="#question-bank">Question bank</a>
          <a href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms" target="_blank" rel="noreferrer">GitHub ↗</a>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow"><span className="pulse" /> OPEN LEARNING PROJECT</p>
          <h1>Understand the model.<br /><span>Question every answer.</span></h1>
          <p className="hero-description">
            A hands-on machine learning knowledge base — from first principles to debugging,
            real-world scenarios, and production trade-offs.
          </p>
          <div className="hero-actions">
            <a className="primary-button" href="#question-bank">Explore the questions <span aria-hidden="true">→</span></a>
            <a className="text-link" href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms/tree/master/knowledge-bank" target="_blank" rel="noreferrer">Read the Markdown source ↗</a>
          </div>
          <div className="hero-meta"><span>✦ Beginner → Advanced</span><span>⌘ Markdown-first</span><span>◉ Colab-friendly</span></div>
        </div>
        <div className="hero-visual" aria-label="Learning roadmap illustration">
          <div className="orbit orbit-one" /><div className="orbit orbit-two" />
          <div className="core"><span>ML</span><small>LEARN / TEST / BUILD</small></div>
          <div className="float-card card-top"><span className="mini-icon violet">ƒ</span><span><b>Foundations</b><small>Build intuition</small></span><i>01</i></div>
          <div className="float-card card-right"><span className="mini-icon mint">↗</span><span><b>Experiments</b><small>Validate with data</small></span><i>02</i></div>
          <div className="float-card card-bottom"><span className="mini-icon amber">⌁</span><span><b>Real scenarios</b><small>Think like an engineer</small></span><i>03</i></div>
          <span className="spark spark-a">✳</span><span className="spark spark-b">✦</span>
        </div>
      </section>

      <section className="stats" aria-label="Academy statistics">
        <div><strong>{total.toString().padStart(2,"0")}</strong><span>Questions in release 01</span></div>
        <div><strong>05</strong><span>Learning tracks</span></div>
        <div><strong>{scenarioCount.toString().padStart(2,"0")}</strong><span>Applied scenarios</span></div>
        <div><strong>∞</strong><span>Room to grow</span></div>
      </section>

      <section className="section-intro" id="question-bank">
        <div><p className="eyebrow">THE QUESTION BANK</p><h2>Build understanding, <em>not just recall.</em></h2></div>
        <p>Search a concept, filter by difficulty, and expand an answer when you're ready. Each question includes an example, a pitfall to watch for, and a prompt to test your understanding.</p>
      </section>
      <QuestionBank questions={questions} />

      <footer className="footer">
        <a className="wordmark" href="#"><span className="mark">ML</span><span>Knowledge Academy</span></a>
        <p>Built for curious minds. Maintained in Markdown. Improved one experiment at a time.</p>
        <a href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms" target="_blank" rel="noreferrer">Open-source repository ↗</a>
      </footer>
    </main>
  );
}
