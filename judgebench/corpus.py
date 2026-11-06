"""Text sources: the author's own Zenn prose and LLM-written passages on the same topics.

`extract_human` reads a checkout of the articles repo and writes data/human_prose.jsonl.
`generate_llm` asks `claude -p` for passages and writes data/llm_passages.jsonl; the output is
cached in the repo, so reruns of the benchmark read the cache and do not call the model again.
"""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .common import DATA, read_jsonl, write_jsonl

CHATGPT_RELEASE = "2022-11-30"
CJK = re.compile(r"[ぁ-んァ-ン一-龥]")
LLM_MODEL = "claude-haiku-5-5"

TOPICS = {
    "nvidia-kernel": "Linux カーネル更新後に NVIDIA ドライバのカーネルモジュール読み込みが失敗する問題",
    "manjaro-notes": "Manjaro Linux を日常利用するときの設定と備忘録",
    "wine-fonts": "Wine で日本語フォントを正しく表示させる設定",
    "aws-vault": "aws-vault でアクセスキーを安全に保存し MFA を扱う方法",
    "docker-rootless": "Docker を Rootless モードで利用する手順",
    "gpg-email": "GPG キーのメールアドレスを追加・削除する手順",
    "display-manager": "Light Display Manager が起動しないときのトラブルシューティング",
    "macos-ime": "macOS でテキストカーソル横の IME インジケータをオフにする方法",
}


def _prose_lines(text):
    text = re.sub(r"^---.*?---", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", ">", "|", "!", "http", ":::")):
            continue
        line = re.sub(r"^[-*]\s+|^\d+\.\s+", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line).replace("`", "")
        if len(CJK.findall(line)) >= 8:
            yield line


def extract_human(articles_dir, published_at):
    """published_at: {slug: 'YYYY-MM-DD'} read from the Zenn API by the caller."""
    out = []
    for path in sorted(Path(articles_dir).glob("*.md")):
        slug = path.stem
        for line in _prose_lines(path.read_text(encoding="utf-8")):
            for sent in re.split(r"(?<=[。！？])", line):
                sent = sent.strip()
                if 12 <= len(sent) <= 140 and sent[-1] in "。！？":
                    date = published_at[slug]
                    out.append({"slug": slug, "published": date, "pre_ai": date < CHATGPT_RELEASE, "text": sent})
    write_jsonl(DATA / "human_prose.jsonl", out)
    return out


def _ask(topic, n):
    prompt = (
        f"技術ブログの筆者として、次のテーマについて、です・ます調で1〜2文（合計30〜110字）の短い段落を{n}個書いてください。"
        f"1行に1つ、番号や記号は付けず、段落以外の文章は出力しないでください。\nテーマ: {topic}"
    )
    cmd = ["claude", "-p", "--model", LLM_MODEL, "--tools", "", "--no-session-persistence",
           "--disable-slash-commands", "--setting-sources", "", prompt]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300, check=True)
    return [ln.strip() for ln in res.stdout.splitlines() if CJK.search(ln) and ln.strip()[-1:] in "。！？"]


def generate_llm(per_topic=14):
    with ThreadPoolExecutor(max_workers=4) as pool:
        batches = list(pool.map(lambda kv: (kv[0], _ask(kv[1], per_topic)), TOPICS.items()))
    out = [{"topic": k, "text": t} for k, texts in batches for t in texts]
    write_jsonl(DATA / "llm_passages.jsonl", out)
    return out


SENTENCE_GENERATORS = {"claude_haiku": "claude-haiku-5-5", "gemma4_12b": "gemma4:12b", "qwen3.5_27b": "qwen3.5:27b"}


LENGTH_BANDS = [(20, 40), (40, 70), (70, 110)]


def _sentence_prompt(topic, n, band):
    lo, hi = band
    return (
        f"技術ブログの筆者として、次のテーマについて、です・ます調で、ちょうど1文（{lo}〜{hi}字）の文を{n}個書いてください。"
        f"1行に1文、番号や記号は付けず、複数の文を続けず、文以外は出力しないでください。\nテーマ: {topic}"
    )


def _ask_ollama(model, prompt):
    import json
    import urllib.request
    payload = {"model": model, "stream": False, "think": False, "messages": [{"role": "user", "content": prompt}],
               "options": {"temperature": 0.8, "num_predict": 2000}}
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as res:
        return json.load(res)["message"]["content"]


def _one_sentences(lines):
    out = []
    for ln in lines:
        ln = ln.strip().lstrip("-*・0123456789.)） ")
        parts = [x for x in re.split(r"(?<=[。！？])", ln) if x.strip()]
        if len(parts) == 1 and 20 <= len(ln) <= 110 and ln[-1:] in "。！？" and CJK.search(ln):
            out.append(ln)
    return out


def generate_sentences(per_band=10):
    """One-sentence passages from three generators, cached in data/llm_sentences.jsonl."""
    out = []
    for gen, model in SENTENCE_GENERATORS.items():
        for key, topic in TOPICS.items():
            for band in LENGTH_BANDS:
                prompt = _sentence_prompt(topic, per_band, band)
                if gen == "claude_haiku":
                    cmd = ["claude", "-p", "--model", model, "--tools", "", "--no-session-persistence",
                           "--disable-slash-commands", "--setting-sources", "", prompt]
                    text = subprocess.run(cmd, capture_output=True, text=True, timeout=300, check=True).stdout
                else:
                    text = _ask_ollama(model, prompt)
                out += [{"generator": gen, "topic": key, "text": t} for t in _one_sentences(text.splitlines())]
    write_jsonl(DATA / "llm_sentences.jsonl", out)
    return out


def human():
    return read_jsonl(DATA / "human_prose.jsonl")


def llm():
    return read_jsonl(DATA / "llm_passages.jsonl")


if __name__ == "__main__":
    if sys.argv[1:2] == ["generate-llm"]:
        print(len(generate_llm()))
    if sys.argv[1:2] == ["generate-sentences"]:
        print(len(generate_sentences()))
