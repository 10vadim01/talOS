from __future__ import annotations
import requests, logging

_LOG = logging.getLogger("talos.llm")

class OllamaClient:
    def __init__(self, ip: str, port: int, model: str = "devstral"):
        self.url   = f"http://{ip}:{port}/api/generate"
        self.model = model

    def generate(self, prompt: str, *, stop: list[str] | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if stop:
            payload["stop"] = stop
        try:
            resp = requests.post(self.url, json=payload, timeout=60)
            resp.raise_for_status()
        except Exception as exc:
            _LOG.error("Ollama request failed: %s", exc)
            return ""
        data = resp.json()
        return data.get("response", "")