import { fireEvent, render, screen } from '@testing-library/react';
import PlaygroundChat from '../PlaygroundChat';

const blueprint = {
  bot_id: 'bot-123',
  bot_name: 'Flower Muse',
  language: 'he',
};

const history = [
  { role: 'user', content: 'יש לכם זר לילדה?' },
  { role: 'assistant', content: 'כן! ממליצה על ורדים צהובים.' },
];

describe('PlaygroundChat', () => {
  it('renders existing history and metadata', () => {
    render(<PlaygroundChat blueprint={blueprint} history={history} onSend={jest.fn()} isSending={false} />);

    expect(screen.getByText('Flower Muse')).toBeInTheDocument();
    expect(screen.getByText(history[0].content)).toBeInTheDocument();
    expect(screen.getByText(history[1].content)).toBeInTheDocument();
  });

  it('calls onSend with trimmed message', () => {
    const onSend = jest.fn();
    render(<PlaygroundChat blueprint={blueprint} history={[]} onSend={onSend} isSending={false} />);

    fireEvent.change(screen.getByPlaceholderText(/Ask the bot/i), { target: { value: ' שלום  ' } });
    fireEvent.submit(screen.getByTestId('chat-form'));

    expect(onSend).toHaveBeenCalledWith('שלום');
  });
});
