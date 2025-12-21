import { createBlueprint, fetchSnippet, sendPlaygroundMessage } from '../api';

const mockResponse = (payload, { ok = true, contentType = 'application/json' } = {}) => ({
  ok,
  headers: {
    get: () => contentType,
  },
  json: jest.fn(() => Promise.resolve(payload)),
  text: jest.fn(() => Promise.resolve(payload)),
});

describe('API client', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
    global.alert = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('posts interview payload and returns parsed JSON', async () => {
    const payload = { bot_id: 'bot-1' };
    global.fetch.mockResolvedValue(mockResponse(payload));

    const result = await createBlueprint({ business_name: 'Cafe' });

    expect(result).toEqual(payload);
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/bots/blueprint',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ business_name: 'Cafe' }),
      })
    );
  });

  it('attaches session header when sending playground message', async () => {
    global.fetch.mockResolvedValue(mockResponse({ reply: 'ok' }));

    await sendPlaygroundMessage('bot-1', 'sess-9', 'hello');

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/bots/bot-1/playground',
      expect.objectContaining({
        headers: expect.objectContaining({ 'X-Session-ID': 'sess-9' }),
        method: 'POST',
      })
    );
  });

  it('throws formatted error details for non-OK responses', async () => {
    global.fetch.mockResolvedValue(mockResponse({ detail: 'Boom' }, { ok: false }));

    await expect(fetchSnippet('bot-1', 'py')).rejects.toThrow('Boom');
  });
});
