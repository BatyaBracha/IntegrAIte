import { fireEvent, render, screen } from '@testing-library/react';
import SnippetPanel from '../SnippetPanel';

const blueprint = {
  bot_id: 'bot-123',
};

describe('SnippetPanel', () => {
  it('disables action button until blueprint exists', () => {
    render(<SnippetPanel blueprint={null} snippet={null} onRequestSnippet={jest.fn()} isLoading={false} />);
    expect(screen.getByRole('button', { name: /Create a blueprint first/i })).toBeDisabled();
  });

  it('invokes callback with selected language', () => {
    const onRequestSnippet = jest.fn();
    render(
      <SnippetPanel
        blueprint={blueprint}
        snippet={null}
        onRequestSnippet={onRequestSnippet}
        isLoading={false}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /JavaScript/i }));
    fireEvent.click(screen.getByRole('button', { name: /Generate snippet/i }));

    expect(onRequestSnippet).toHaveBeenCalledWith('js');
  });

  it('renders snippet payload', () => {
    const snippet = {
      language: 'py',
      instructions: 'copy me',
      code: 'print("hello")',
    };

    render(
      <SnippetPanel blueprint={blueprint} snippet={snippet} onRequestSnippet={jest.fn()} isLoading={false} />
    );

    expect(screen.getByText(snippet.instructions)).toBeInTheDocument();
    expect(screen.getByText(snippet.code)).toBeInTheDocument();
  });
});
