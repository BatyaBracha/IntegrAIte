import { render, screen } from '@testing-library/react';
import App from './App';

test('renders hero headline and interview button', () => {
  render(<App />);
  expect(screen.getByText(/Spin up a boutique AI agent in minutes/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /Generate Blueprint/i })).toBeInTheDocument();
});
