import { useCallback, useEffect, useRef, useState } from 'react';
import './App.css';

import BotSummary from './components/BotSummary';
import InterviewForm from './components/InterviewForm';
import PlaygroundChat from './components/PlaygroundChat';
import StatusToasts from './components/StatusToasts';
import SnippetPanel from './components/SnippetPanel';
import { createBlueprint, fetchSnippet, sendPlaygroundMessage } from './services/api';
import { getOrCreateSessionId } from './utils/session';

function App() {
  const [blueprint, setBlueprint] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const [snippet, setSnippet] = useState(null);
  const [isSnippetLoading, setIsSnippetLoading] = useState(false);
  const [toasts, setToasts] = useState([]);
  const toastTimers = useRef({});
  const sessionIdRef = useRef(getOrCreateSessionId());

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

  const handleInterviewSubmit = async (payload) => {
    setIsGenerating(true);
    pushToast('info', 'Generating a bespoke bot blueprint…');
    try {
      const response = await createBlueprint(payload);
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
    <div className="app-shell">
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
            <p className="session-id">{sessionIdRef.current}</p>
            <p className="tiny">Use this session ID to keep the Playground context synced.</p>
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
