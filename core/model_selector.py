import requests


def detect_ollama_models(model_url="http://localhost:11434"):
    try:
        response = requests.get(f"{model_url}/api/tags", timeout=3)
        if not response.ok:
            return []
        payload = response.json()
        models = payload.get("models", []) if isinstance(payload, dict) else []
        names = []
        for model in models:
            if isinstance(model, dict):
                name = model.get("name")
                if name:
                    names.append(str(name))
            elif model:
                names.append(str(model))
        return names
    except Exception:
        return []


def select_ollama_model(model_url="http://localhost:11434"):
    models = detect_ollama_models(model_url)
    if not models:
        return None

    normalized = [name.lower() for name in models]
    for name in normalized:
        if "qwen" in name:
            return next(model for model in models if "qwen" in model.lower())

    for name in normalized:
        if "llama" in name:
            return next(model for model in models if "llama" in model.lower())

    return None
