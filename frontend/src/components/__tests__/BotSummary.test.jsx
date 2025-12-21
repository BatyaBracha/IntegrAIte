import { render, screen } from '@testing-library/react';
import BotSummary from '../BotSummary';

const blueprint = {
  bot_id: 'bot-321',
  bot_name: 'Guide Bot',
  tagline: 'Helps you decide',
  tone: 'confident',
  language: 'en',
  knowledge_base: ['menu', 'policies'],
  system_prompt: 'Always explain the reasoning.',
  sample_questions: ['What should I buy?'],
  sample_responses: ['Try the deluxe plan.'],
};

describe('BotSummary', () => {
  it('renders placeholder when blueprint is missing', () => {
    render(<BotSummary blueprint={null} />);
    expect(
      screen.getByText(/Blueprint insights will appear here once the interview is complete/i)
    ).toBeInTheDocument();
  });

  it('renders blueprint details when available', () => {
    render(<BotSummary blueprint={blueprint} />);

    expect(screen.getByText(blueprint.bot_name)).toBeInTheDocument();
    expect(screen.getByText(blueprint.tagline)).toBeInTheDocument();
    expect(screen.getByText(blueprint.knowledge_base[0])).toBeInTheDocument();
    expect(screen.getByText(blueprint.sample_responses[0])).toBeInTheDocument();
  });
});
