import { getOrCreateSessionId } from './session';

describe('getOrCreateSessionId', () => {
  afterEach(() => {
    window.localStorage.clear();
  });

  it('returns existing session id from storage', () => {
    window.localStorage.setItem('integrAIte-session-id', 'existing-id');
    expect(getOrCreateSessionId()).toBe('existing-id');
  });

  it('generates and stores a new id when missing', () => {
    const originalCrypto = global.crypto;
    global.crypto = { randomUUID: jest.fn(() => 'generated-id') };

    const id = getOrCreateSessionId();

    expect(id).toBe('generated-id');
    expect(window.localStorage.getItem('integrAIte-session-id')).toBe('generated-id');

    global.crypto = originalCrypto;
  });

  it('falls back when window is undefined', () => {
    const originalWindow = global.window;
    Reflect.deleteProperty(global, 'window');

    const id = getOrCreateSessionId();

    expect(typeof id).toBe('string');
    expect(id).toMatch(/-/);

    global.window = originalWindow;
  });
});
