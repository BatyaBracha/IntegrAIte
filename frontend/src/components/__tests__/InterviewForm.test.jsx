import { fireEvent, render, screen } from '@testing-library/react';
import InterviewForm from '../InterviewForm';

describe('InterviewForm', () => {
  it('submits collected form values', () => {
    const handleSubmit = jest.fn();
    render(<InterviewForm onSubmit={handleSubmit} isSubmitting={false} />);

    fireEvent.change(screen.getByLabelText(/Business Name/i), { target: { value: 'Cafe Luna' } });
    fireEvent.change(screen.getByLabelText(/Describe your offering/i), {
      target: { value: 'We roast single-origin beans and deliver.' },
    });
    fireEvent.change(screen.getByLabelText(/What should the bot do/i), {
      target: { value: 'Recommend beans' },
    });
    fireEvent.change(screen.getByLabelText(/Target audience/i), { target: { value: 'Founders' } });
    fireEvent.change(screen.getByLabelText(/Preferred tone/i), { target: { value: 'Bold' } });
    fireEvent.change(screen.getByLabelText(/Language/i), { target: { value: 'en' } });

    fireEvent.submit(screen.getByRole('button', { name: /Generate Blueprint/i }));

    expect(handleSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        business_name: 'Cafe Luna',
        preferred_language: 'en',
        target_audience: 'Founders',
      })
    );
  });

  it('disables submit state while submitting', () => {
    render(<InterviewForm onSubmit={jest.fn()} isSubmitting />);
    expect(screen.getByRole('button', { name: /Designing your bot/i })).toBeDisabled();
  });
});
