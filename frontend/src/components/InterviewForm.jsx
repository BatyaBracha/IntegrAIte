import { useState } from 'react';

const INITIAL_FORM = {
  business_name: '',
  business_description: '',
  desired_bot_role: '',
  target_audience: '',
  preferred_tone: '',
  preferred_language: 'he',
};

const PLACEHOLDERS = {
  business_description: 'We craft vibrant bouquets and offer same-day delivery across the city.',
  desired_bot_role: 'Guide customers to the right bouquet and suggest greeting ideas.',
  target_audience: 'Busy professionals seeking last-minute gifts.',
  preferred_tone: 'Warm, celebratory, a dash of wit.',
};

function InterviewForm({ onSubmit, isSubmitting }) {
  const [form, setForm] = useState(INITIAL_FORM);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(form);
  };

  return (
    <form className="interview-form" onSubmit={handleSubmit}>
      <label>
        Business Name
        <input
          name="business_name"
          value={form.business_name}
          onChange={handleChange}
          placeholder="Florentine Atelier"
          required
        />
      </label>

      <label>
        Describe your offering
        <textarea
          name="business_description"
          value={form.business_description}
          onChange={handleChange}
          placeholder={PLACEHOLDERS.business_description}
          minLength={20}
          required
        />
      </label>

      <label>
        What should the bot do?
        <textarea
          name="desired_bot_role"
          value={form.desired_bot_role}
          onChange={handleChange}
          placeholder={PLACEHOLDERS.desired_bot_role}
          minLength={10}
          required
        />
      </label>

      <label>
        Target audience
        <input
          name="target_audience"
          value={form.target_audience}
          onChange={handleChange}
          placeholder={PLACEHOLDERS.target_audience}
        />
      </label>

      <label>
        Preferred tone
        <input
          name="preferred_tone"
          value={form.preferred_tone}
          onChange={handleChange}
          placeholder={PLACEHOLDERS.preferred_tone}
        />
      </label>

      <label>
        Language
        <select name="preferred_language" value={form.preferred_language} onChange={handleChange}>
          <option value="he">Hebrew</option>
          <option value="en">English</option>
          <option value="es">Spanish</option>
        </select>
      </label>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Designing your bot…' : 'Generate Blueprint'}
      </button>
    </form>
  );
}

export default InterviewForm;
