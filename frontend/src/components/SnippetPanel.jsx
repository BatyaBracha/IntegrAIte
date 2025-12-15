import { useState } from 'react';

const languages = [
  { value: 'py', label: 'Python' },
  { value: 'js', label: 'JavaScript' },
];

function SnippetPanel({ blueprint, snippet, onRequestSnippet, isLoading }) {
  const [selected, setSelected] = useState('py');

  const handleRequest = () => {
    onRequestSnippet(selected);
  };

  return (
    <div className="snippet-panel">
      <div className="snippet-header">
        <div>
          <p className="eyebrow">Deploy</p>
          <h3>Copy & embed</h3>
        </div>
        <div className="lang-switch">
          {languages.map((item) => (
            <button
              key={item.value}
              type="button"
              className={selected === item.value ? 'active' : ''}
              onClick={() => setSelected(item.value)}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      <p className="muted">
        Choose a language and we will generate an authenticated snippet that includes the persona instructions.
      </p>

      <button type="button" disabled={!blueprint || isLoading} onClick={handleRequest}>
        {!blueprint ? 'Create a blueprint first' : isLoading ? 'Generating snippet…' : 'Generate snippet'}
      </button>

      {snippet && (
        <div className="snippet-output">
          <div className="snippet-meta">
            <span>{snippet.language.toUpperCase()}</span>
            <small>{snippet.instructions}</small>
          </div>
          <pre>
            <code>{snippet.code}</code>
          </pre>
        </div>
      )}
    </div>
  );
}

export default SnippetPanel;
