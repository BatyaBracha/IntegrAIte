import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import App from './App';
import { createBlueprint, fetchSnippet, sendPlaygroundMessage } from './services/api';

jest.mock('./services/api', () => ({
  createBlueprint: jest.fn(),
  fetchSnippet: jest.fn(),
  sendPlaygroundMessage: jest.fn(),
}));

jest.mock('./components/InterviewForm', () => (props) => (
  <button
    type="button"
    onClick={() =>
      props.onSubmit({
        business_name: 'Cafe Luna',
        business_description: 'We roast beans and deliver daily.',
        desired_bot_role: 'Recommend blends fast',
        target_audience: 'Founders',
        preferred_tone: 'Bold',
        preferred_language: 'en',
      })
    }
  >
    Submit Interview
  </button>
));

jest.mock('./components/PlaygroundChat', () => (props) => (
  <button type="button" data-testid="send-chat" disabled={!props.blueprint} onClick={() => props.onSend('Ping')}>
    Send Playground Message
  </button>
));

jest.mock('./components/SnippetPanel', () => (props) => (
  <button
    type="button"
    data-testid="request-snippet"
    disabled={!props.blueprint}
    onClick={() => props.onRequestSnippet('py')}
  >
    Request Snippet
  </button>
));

jest.mock('./components/BotSummary', () => (props) => (
  <div data-testid="bot-summary">{props.blueprint ? props.blueprint.bot_id : 'no-bot'}</div>
));

jest.mock('./components/StatusToasts', () => ({ toasts }) => (
  <div data-testid="toasts">
    {toasts.map((toast) => (
      <span key={toast.id}>{toast.message}</span>
    ))}
  </div>
));

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders hero headline and interview button', () => {
    render(<App />);
    expect(screen.getByText(/Spin up a boutique AI agent in minutes/i)).toBeInTheDocument();
    expect(screen.getByText('Submit Interview')).toBeInTheDocument();
  });

  test('handles blueprint creation success and surfaces toast', async () => {
    createBlueprint.mockResolvedValue({
      bot_id: 'bot-900',
      bot_name: 'Luna',
      tagline: 't',
      tone: 'calm',
      language: 'en',
      knowledge_base: [],
      system_prompt: 'prompt',
      sample_questions: [],
      sample_responses: [],
    });

    render(<App />);
    fireEvent.click(screen.getByText('Submit Interview'));

    await waitFor(() => expect(createBlueprint).toHaveBeenCalled());
    expect(await screen.findByText(/Blueprint ready for Luna/)).toBeInTheDocument();
  });

  test('sends playground message once blueprint exists', async () => {
    createBlueprint.mockResolvedValue({
      bot_id: 'bot-77',
      bot_name: 'Muse',
      tagline: 't',
      tone: 'calm',
      language: 'en',
      knowledge_base: [],
      system_prompt: 'prompt',
      sample_questions: [],
      sample_responses: [],
    });
    sendPlaygroundMessage.mockResolvedValue({ reply: 'Response' });

    render(<App />);
    fireEvent.click(screen.getByText('Submit Interview'));
    await screen.findByText(/Blueprint ready for Muse/);
    fireEvent.click(screen.getByTestId('send-chat'));

    await waitFor(() => expect(sendPlaygroundMessage).toHaveBeenCalledWith('bot-77', expect.any(String), 'Ping'));
    expect(await screen.findByText(/Reply received/)).toBeInTheDocument();
  });

  test('shows snippet error toast when snippet generation fails', async () => {
    createBlueprint.mockResolvedValue({
      bot_id: 'bot-55',
      bot_name: 'Muse',
      tagline: 't',
      tone: 'calm',
      language: 'en',
      knowledge_base: [],
      system_prompt: 'prompt',
      sample_questions: [],
      sample_responses: [],
    });
    fetchSnippet.mockRejectedValue(new Error('No snippet today'));

    render(<App />);
    fireEvent.click(screen.getByText('Submit Interview'));
    await screen.findByText(/Blueprint ready for Muse/);
    fireEvent.click(screen.getByTestId('request-snippet'));

    expect(await screen.findByText(/No snippet today/)).toBeInTheDocument();
  });
});
