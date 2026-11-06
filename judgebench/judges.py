"""LLM judges. A verdict is exactly "YES" or "NO"; anything else is None (no answer)."""
import json
import math
import os
import subprocess
import time
import urllib.error
import urllib.request

from .common import ROOT

OLLAMA = "http://localhost:11434"
CLAUDE_MODEL = "claude-haiku-5-5"
CLAUDE_SYSTEM = "You are a strict classifier. Output exactly one word: YES or NO."


def _post(path, payload, timeout=300):
    req = urllib.request.Request(OLLAMA + path, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.load(res)


def verdict_from(sampled, logprobs):
    """YES when its probability beats NO's; the sampled token only decides when one of the two is missing."""
    if "YES" in logprobs and "NO" in logprobs:
        p_yes = 1 / (1 + math.exp(logprobs["NO"] - logprobs["YES"]))
        return {"verdict": "YES" if p_yes >= 0.5 else "NO", "p_yes": p_yes}
    return {"verdict": sampled if sampled in ("YES", "NO") else None, "p_yes": None}


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
        lp = {c["token"]: c["logprob"] for c in first["top_logprobs"]}
        return {**verdict_from(first["token"], lp), "latency_s": dt}

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
    hosted = True

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


QUESTIONS = json.loads((ROOT / "prompts" / "decisions.json").read_text(encoding="utf-8"))
RETRIES = 4


def _decide_request(url, key, payload):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, json.dumps(payload).encode(), headers)
        try:
            with urllib.request.urlopen(req, timeout=300) as res:
                return json.load(res)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == RETRIES - 1:
                raise
            time.sleep(2 ** (attempt + 1))


class DecisionsJudge:
    """A decision model asked one yes/no question about the text; YES when its probability is at least 0.5."""

    decisions = True

    def __init__(self, name, model, url, key_env, kind, hosted):
        self.name, self.model, self.url, self.key_env, self.kind, self.hosted = name, model, url, key_env, kind, hosted

    def _payload(self, q, text):
        if self.kind == "predicate":
            instructions = f"{q['instructions']}（はい: {q['true']}／いいえ: {q['false']}）"
            return {"model": self.model, "input": text,
                    "questions": [{"type": "predicate", "name": "q", "instructions": instructions}]}
        return {"model": self.model, "state": text, "questions": {"q": {
            "type": "noul", "instructions": q["instructions"], "criteria": {"true": q["true"], "false": q["false"]}}}}

    def decide(self, task, text):
        t0 = time.perf_counter()
        res = _decide_request(self.url, os.environ.get(self.key_env), self._payload(QUESTIONS[task], text))
        dt = time.perf_counter() - t0
        answers = res["answers"]
        ans = answers[0] if isinstance(answers, list) else answers["q"]
        p = ans.get("probability", ans.get("noul"))
        return {"verdict": None if p is None else ("YES" if p >= 0.5 else "NO"), "p_yes": p, "latency_s": dt}

    def loaded_bytes(self):
        if self.hosted:
            return None
        for m in _post_get("/api/ps").get("models", []):
            if m["name"].startswith(self.model):
                return m["size"]
        return None


DECISION_JUDGES = {
    "jev": ("jev-1.14.0", "https://api.typesafe.ai/v1/systemone", "TYPESAFE_API_KEY", "noul", True),
    "clef_flash": ("clef-flash", OLLAMA + "/v1/systemone", "", "noul", False),
    "gpt_6_luna": ("gpt-6-luna", "https://api.openai.com/v1/decisions", "OPENAI_API_KEY", "predicate", True),
}


def make(name):
    if name in DECISION_JUDGES:
        model, url, key_env, kind, hosted = DECISION_JUDGES[name]
        return DecisionsJudge(name, model, url, key_env, kind, hosted)
    return ClaudeJudge() if name == "claude_haiku" else OllamaJudge(name)
