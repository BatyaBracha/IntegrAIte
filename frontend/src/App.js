import { useCallback, useEffect, useRef, useState } from 'react';
import './App.css';

import BotSummary from './components/BotSummary';
import InterviewForm from './components/InterviewForm';
import PlaygroundChat from './components/PlaygroundChat';
import StatusToasts from './components/StatusToasts';
import SnippetPanel from './components/SnippetPanel';
import { createBlueprint, fetchSessionState, fetchSnippet, sendPlaygroundMessage } from './services/api';
import { getOrCreateSessionId, setSessionId } from './utils/session';

function App() {
  // Theme state: 'dark' (night) or 'light' (day)
  const [theme, setTheme] = useState('dark');

  // Toggle theme handler
  const toggleTheme = () => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  const [blueprint, setBlueprint] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const [snippet, setSnippet] = useState(null);
  const [isSnippetLoading, setIsSnippetLoading] = useState(false);
  const [toasts, setToasts] = useState([]);
  const sessionIdRef = useRef(getOrCreateSessionId());
  const [sessionInput, setSessionInput] = useState(() => sessionIdRef.current);
  const [isSessionRefreshing, setIsSessionRefreshing] = useState(false);
  const toastTimers = useRef({});

  const dismissToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
    if (toastTimers.current[id]) {
      clearTimeout(toastTimers.current[id]);
      delete toastTimers.current[id];
    }
  }, []);

  const pushToast = useCallback(
    (type, message, ttl = 4500) => {
      const id =
        (typeof crypto !== 'undefined' && crypto.randomUUID && crypto.randomUUID()) ||
        `${Date.now()}-${Math.random().toString(16).slice(2, 6)}`;
      setToasts((prev) => [...prev, { id, type, message }]);
      if (typeof window !== 'undefined') {
        toastTimers.current[id] = window.setTimeout(() => dismissToast(id), ttl);
      }
    },
    [dismissToast]
  );

  useEffect(
    () => () => {
      Object.values(toastTimers.current).forEach((timer) => clearTimeout(timer));
    },
    []
  );

  const loadSessionState = useCallback(async (sessionId) => {
    const state = await fetchSessionState(sessionId);
    setBlueprint(state.blueprint || null);
    setChatHistory(state.history || []);
    setSnippet((current) => {
      if (!state.blueprint) {
        return null;
      }
      return current?.bot_id === state.blueprint.bot_id ? current : null;
    });
    return state;
  }, []);

  useEffect(() => {
    loadSessionState(sessionIdRef.current).catch((error) => {
      console.warn('Failed to restore session state', error);
    });
  }, [loadSessionState]);

  const handleCopySessionId = useCallback(async () => {
    const currentId = sessionIdRef.current;
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(currentId);
      } else {
        const tempInput = document.createElement('input');
        tempInput.value = currentId;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
      }
      pushToast('success', 'Session ID copied.');
    } catch (error) {
      console.warn('Failed to copy session ID', error);
      pushToast('error', 'Could not copy session ID');
    }
  }, [pushToast]);

  const handleSessionInputChange = (event) => {
    setSessionInput(event.target.value);
  };

  const handleSessionSubmit = async (event) => {
    event.preventDefault();
    const nextId = sessionInput.trim();
    if (!nextId) {
      pushToast('error', 'Session ID cannot be empty.');
      return;
    }
    if (nextId === sessionIdRef.current) {
      pushToast('info', 'Already on that session.');
      return;
    }

    setIsSessionRefreshing(true);
    try {
      setSessionId(nextId);
      sessionIdRef.current = nextId;
      setSessionInput(nextId);
      await loadSessionState(nextId);
      pushToast('success', 'Session restored.');
    } catch (error) {
      pushToast('error', error.message || 'Failed to load that session');
    } finally {
      setIsSessionRefreshing(false);
    }
  };

  const handleInterviewSubmit = async (payload) => {
    setIsGenerating(true);
    pushToast('info', 'Generating a bespoke bot blueprint…');
    try {
      const response = await createBlueprint(payload, sessionIdRef.current);
      setBlueprint(response);
      setChatHistory([]);
      setSnippet(null);
      pushToast('success', `Blueprint ready for ${response.bot_name}. Jump into the playground!`);
    } catch (error) {
      pushToast('error', error.message || 'Failed to create blueprint');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSendMessage = async (message) => {
    if (!blueprint) return;
    setIsSending(true);
    pushToast('info', 'Messaging your new bot persona…');
    try {
      const reply = await sendPlaygroundMessage(blueprint.bot_id, sessionIdRef.current, message);
      setChatHistory((prev) => [
        ...prev,
        { role: 'user', content: message },
        { role: 'assistant', content: reply.reply ?? reply },
      ]);
      pushToast('success', 'Reply received. Keep iterating!');
    } catch (error) {
      pushToast('error', error.message || 'Playground request failed');
    } finally {
      setIsSending(false);
    }
  };

  const handleSnippetRequest = async (language) => {
    if (!blueprint) return;
    setIsSnippetLoading(true);
    pushToast('info', 'Preparing code snippet…');
    try {
      const payload = await fetchSnippet(blueprint.bot_id, language);
      setSnippet(payload);
      pushToast('success', 'Snippet ready. Drop it into your stack.');
    } catch (error) {
      pushToast('error', error.message || 'Failed to generate snippet');
    } finally {
      setIsSnippetLoading(false);
    }
  };

  return (
    <div className={`app-shell${theme === 'light' ? ' light-theme' : ''}`}>
      <button
        onClick={toggleTheme}
        className="theme-toggle-btn chat-header"
        aria-label="Toggle day/night mode"
        title={theme === 'dark' ? 'Switch to Day Mode' : 'Switch to Night Mode'}
      >
        {theme === 'dark' ? 'Day' : 'Night'}
      </button>
      <main>
        <section className="hero">
          <div>
            <p className="eyebrow">From Zero to AI Hero</p>
            <h1>Spin up a boutique AI agent in minutes</h1>
            <p>
              Answer three intent-driven questions, test the persona instantly, and export production-ready code snippets.
              Crafted for founders who need momentum now.
            </p>
          </div>
          <div className="hero-card">
            <p className="muted">Session</p>
            <div className="session-id-row">
              <p className="session-id">{sessionIdRef.current}</p>
              <button
                type="button"
                className="session-copy-btn"
                aria-label="Copy session ID"
                onClick={handleCopySessionId}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" role="presentation" aria-hidden="true">
                  <rect x="7" y="7" width="12" height="12" rx="2" stroke="currentColor" fill="none" strokeWidth="2" />
                  <rect x="5" y="5" width="12" height="12" rx="2" stroke="currentColor" fill="none" strokeWidth="2" opacity="0.6" />
                </svg>
              </button>
            </div>
            <p className="tiny">Use this session ID to keep the Playground context synced.</p>
            <form className="session-form" onSubmit={handleSessionSubmit}>
              <label htmlFor="session-id-input">Restore an existing session</label>
              <div className="session-form__controls">
                <input
                  id="session-id-input"
                  value={sessionInput}
                  onChange={handleSessionInputChange}
                  placeholder="Paste a session ID"
                  autoComplete="off"
                />
                <button type="submit" disabled={isSessionRefreshing}>
                  {isSessionRefreshing ? 'Loading…' : 'Load'}
                </button>
              </div>
            </form>
          </div>
        </section>

        <section className="workspace">
          <div className="panel">
            <header className="panel-header">
              <div>
                <p className="eyebrow">01 · Interview</p>
                <h2>Describe your business</h2>
              </div>
              <p className="muted">Gemini translates your answers into a structured system prompt.</p>
            </header>
            <InterviewForm onSubmit={handleInterviewSubmit} isSubmitting={isGenerating} />
          </div>

          <div className="panel highlight">
            <header className="panel-header">
              <div>
                <p className="eyebrow">Blueprint</p>
                <h2>Persona snapshot</h2>
              </div>
            </header>
            <BotSummary blueprint={blueprint} />
          </div>
        </section>

        <section className="workspace">
          <div className="panel wide">
            <PlaygroundChat
              blueprint={blueprint}
              history={chatHistory}
              onSend={handleSendMessage}
              isSending={isSending}
            />
          </div>

          <div className="panel">
            <SnippetPanel
              blueprint={blueprint}
              snippet={snippet}
              onRequestSnippet={handleSnippetRequest}
              isLoading={isSnippetLoading}
            />
          </div>
        </section>
      </main>
      <StatusToasts toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}

export default App;
