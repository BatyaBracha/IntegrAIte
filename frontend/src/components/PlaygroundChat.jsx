import { useState } from 'react';

function PlaygroundChat({ blueprint, history, onSend, isSending }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!message.trim()) return;
    onSend(message.trim());
    setMessage('');
  };

  return (
    <div className="playground">
      <div className="chat-header">
        <div>
          <p className="eyebrow">Live Playground</p>
          <h3>{blueprint ? blueprint.bot_name : 'Waiting for blueprint'}</h3>
        </div>
        {blueprint && <span className="bot-language">{blueprint.language}</span>}
      </div>

      <div className="chat-window">
        {history.length === 0 && (
          <p className="muted">Send a message to experience the freshly minted persona.</p>
        )}
        {history.map((turn, index) => (
          <div key={`${turn.role}-${index}`} className={`chat-message ${turn.role}`}>
            <span>{turn.content}</span>
          </div>
        ))}
      </div>

      <form className="chat-input" onSubmit={handleSubmit} data-testid="chat-form">
        <input
          type="text"
          placeholder={blueprint ? 'Ask the bot anything about your business' : 'Generate a blueprint first'}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          disabled={!blueprint || isSending}
        />
        <button type="submit" disabled={!blueprint || isSending}>
          {isSending ? 'Thinking…' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default PlaygroundChat;
