const STORAGE_KEY = 'integrAIte-session-id';

function fallbackUuid() {
  return `${Date.now().toString(16)}-${Math.random().toString(16).slice(2, 10)}`;
}

export function getOrCreateSessionId() {
  if (typeof window === 'undefined') {
    return fallbackUuid();
  }

  const existing = window.localStorage.getItem(STORAGE_KEY);
  if (existing) {
    return existing;
  }

  const id = (window.crypto?.randomUUID && window.crypto.randomUUID()) || fallbackUuid();
  window.localStorage.setItem(STORAGE_KEY, id);
  return id;
}
