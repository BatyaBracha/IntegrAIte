const API_BASE = process.env.REACT_APP_API_BASE ?? 'http://localhost:8000/api/v1';

async function handleResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const detail = (payload && payload.detail) || payload || 'Request failed';
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }

  return payload;
}

async function request(path, options = {}) {
  const defaults = {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  };
  alert(`${API_BASE}${path}`, "API_BASE", API_BASE, "path", path);
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: defaults.headers,
  });

  return handleResponse(response);
}

export function createBlueprint(payload) {
  return request('/bots/blueprint', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function sendPlaygroundMessage(botId, sessionId, message) {
  return request(`/bots/${botId}/playground`, {
    method: 'POST',
    headers: {
      'X-Session-ID': sessionId,
    },
    body: JSON.stringify({ content: message }),
  });
}

export function fetchSnippet(botId, language) {
  return request(`/bots/${botId}/snippet?lang=${language}`, {
    method: 'GET',
  });
}
