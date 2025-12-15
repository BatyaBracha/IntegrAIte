function InfoGroup({ label, children }) {
  return (
    <div className="info-group">
      <p className="info-label">{label}</p>
      <div className="info-content">{children}</div>
    </div>
  );
}

function BotSummary({ blueprint }) {
  if (!blueprint) {
    return (
      <div className="summary-placeholder">
        <p>Blueprint insights will appear here once the interview is complete.</p>
        <p className="muted">We will extract tone, knowledge base, sample scripts, and more.</p>
      </div>
    );
  }

  return (
    <div className="bot-summary">
      <header>
        <p className="bot-id">ID: {blueprint.bot_id}</p>
        <h3>{blueprint.bot_name}</h3>
        <p className="tagline">{blueprint.tagline}</p>
      </header>

      <InfoGroup label="Tone">
        <span>{blueprint.tone}</span>
      </InfoGroup>

      <InfoGroup label="Working language">
        <span>{blueprint.language}</span>
      </InfoGroup>

      <InfoGroup label="Knowledge base">
        <ul>
          {blueprint.knowledge_base.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </InfoGroup>

      <InfoGroup label="Sample questions">
        <ul>
          {blueprint.sample_questions.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </InfoGroup>

      <InfoGroup label="Sample responses">
        <ul>
          {blueprint.sample_responses.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </InfoGroup>

      <InfoGroup label="System prompt">
        <pre className="system-prompt">{blueprint.system_prompt}</pre>
      </InfoGroup>
    </div>
  );
}

export default BotSummary;
