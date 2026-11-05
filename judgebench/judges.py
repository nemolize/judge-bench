"""LLM judges. A verdict is exactly "YES" or "NO"; anything else is None (no answer)."""
import json
import math
import subprocess
import time
import urllib.request

OLLAMA = "http://localhost:11434"
CLAUDE_MODEL = "claude-haiku-5-5"
CLAUDE_SYSTEM = "You are a strict classifier. Output exactly one word: YES or NO."


def _post(path, payload, timeout=300):
    req = urllib.request.Request(OLLAMA + path, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.load(res)


class OllamaJudge:
    def __init__(self, model):
        self.model = model
        self.name = model.replace(":", "_")

    def ask(self, prompt):
        t0 = time.perf_counter()
        res = _post("/api/chat", {
            "model": self.model, "stream": False, "think": False, "logprobs": True, "top_logprobs": 10,
            "messages": [{"role": "user", "content": prompt}],
            "options": {"num_predict": 1, "temperature": 0},
        })
        dt = time.perf_counter() - t0
        first = res["logprobs"][0]
        verdict = first["token"] if first["token"] in ("YES", "NO") else None
        lp = {c["token"]: c["logprob"] for c in first["top_logprobs"]}
        p_yes = None
        if "YES" in lp and "NO" in lp:
            p_yes = 1 / (1 + math.exp(lp["NO"] - lp["YES"]))
        return {"verdict": verdict, "p_yes": p_yes, "latency_s": dt}

    def loaded_bytes(self):
        for m in _post_get("/api/ps").get("models", []):
            if m["name"] == self.model:
                return m["size"]
        return None


def _post_get(path):
    with urllib.request.urlopen(OLLAMA + path, timeout=30) as res:
        return json.load(res)


class ClaudeJudge:
    name = "claude_haiku"

    def ask(self, prompt):
        t0 = time.perf_counter()
        cmd = ["claude", "-p", "--model", CLAUDE_MODEL, "--tools", "", "--no-session-persistence",
               "--disable-slash-commands", "--setting-sources", "", "--system-prompt", CLAUDE_SYSTEM, prompt]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300, check=True)
        lines = res.stdout.strip().splitlines()
        first = lines[0].strip() if lines else ""
        return {"verdict": first if first in ("YES", "NO") else None, "p_yes": None, "latency_s": time.perf_counter() - t0}

    def loaded_bytes(self):
        return None


def make(name):
    return ClaudeJudge() if name == "claude_haiku" else OllamaJudge(name)
