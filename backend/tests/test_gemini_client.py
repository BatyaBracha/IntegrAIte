from types import SimpleNamespace

import pytest
from google.api_core import exceptions as google_exceptions

from app.services import gemini_client
from app.services.exceptions import MissingConfigurationError


@pytest.fixture(autouse=True)
def reset_client():
    gemini_client._client = None
    yield
    gemini_client._client = None


def _stub_settings(models, api_key="test-key"):
    class _Settings:
        gemini_api_key = api_key

        def __init__(self, preferred):
            self._preferred = preferred

        @property
        def preferred_models(self):
            return self._preferred

    return _Settings(models)


def test_generate_with_fallback_returns_first_success(monkeypatch):
    fake_response = SimpleNamespace(text="ok")

    class FakeModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, model, contents):
            self.calls.append((model, contents))
            return fake_response

    fake_client = SimpleNamespace(models=FakeModels())
    monkeypatch.setattr(gemini_client, "_ensure_client", lambda: fake_client)
    monkeypatch.setattr(gemini_client, "settings", _stub_settings(["gemini-a"]))

    response, used_model = gemini_client.generate_with_fallback("prompt")

    assert response.text == "ok"
    assert used_model == "gemini-a"
    assert fake_client.models.calls == [("gemini-a", "prompt")]


def test_generate_with_fallback_retries_on_quota(monkeypatch):
    fake_response = SimpleNamespace(text="second")

    class FakeModels:
        def __init__(self):
            self.calls = []

        def generate_content(self, model, contents):
            self.calls.append(model)
            if len(self.calls) == 1:
                raise google_exceptions.ResourceExhausted("quota")
            return fake_response

    fake_client = SimpleNamespace(models=FakeModels())
    monkeypatch.setattr(gemini_client, "_ensure_client", lambda: fake_client)
    monkeypatch.setattr(gemini_client, "settings", _stub_settings(["gemini-a", "gemini-b"]))

    response, used_model = gemini_client.generate_with_fallback("hello")

    assert response.text == "second"
    assert used_model == "gemini-b"
    assert fake_client.models.calls == ["gemini-a", "gemini-b"]


def test_generate_with_fallback_raises_when_no_models(monkeypatch):
    monkeypatch.setattr(gemini_client, "settings", _stub_settings([], api_key="test-key"))

    with pytest.raises(MissingConfigurationError, match="No Gemini models"):
        gemini_client.generate_with_fallback("prompt")
