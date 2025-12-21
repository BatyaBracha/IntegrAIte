import { fireEvent, render, screen } from '@testing-library/react';
import StatusToasts from '../StatusToasts';

describe('StatusToasts', () => {
  it('renders nothing when stack empty', () => {
    const { container } = render(<StatusToasts toasts={[]} onDismiss={jest.fn()} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders toast list and handles dismiss', () => {
    const handleDismiss = jest.fn();
    const toasts = [{ id: '1', type: 'info', message: 'Hello' }];

    render(<StatusToasts toasts={toasts} onDismiss={handleDismiss} />);

    fireEvent.click(screen.getByRole('button', { name: /Dismiss notification/i }));
    expect(handleDismiss).toHaveBeenCalledWith('1');
  });
});
