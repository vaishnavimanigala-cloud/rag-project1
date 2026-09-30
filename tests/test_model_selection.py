from core.model_selector import select_ollama_model


def test_select_qwen_when_available(monkeypatch):
    class FakeResponse:
        ok = True

        def json(self):
            return {"models": [{"name": "qwen2.5:7b"}, {"name": "llama3.2:3b"}]}

    monkeypatch.setattr("core.model_selector.requests.get", lambda *args, **kwargs: FakeResponse())
    model = select_ollama_model()
    assert "qwen" in model.lower()


def test_select_llama_when_qwen_missing(monkeypatch):
    class FakeResponse:
        ok = True

        def json(self):
            return {"models": [{"name": "llama3.2:3b"}]}

    monkeypatch.setattr("core.model_selector.requests.get", lambda *args, **kwargs: FakeResponse())
    model = select_ollama_model()
    assert "llama" in model.lower()


def test_no_model_returns_none(monkeypatch):
    class FakeResponse:
        ok = True

        def json(self):
            return {"models": [{"name": "mistral:7b"}]}

    monkeypatch.setattr("core.model_selector.requests.get", lambda *args, **kwargs: FakeResponse())
    model = select_ollama_model()
    assert model is None
