"""Dataset registry: task name -> generator, and the prompt each task uses."""
from . import aitext, honorific, injection, secrets_task, style
from .common import DATA, UNCOMMITTED, digest, read_jsonl, write_jsonl

TASKS = {
    "honorific": honorific.generate,
    "aitext": aitext.generate,
    "style": style.generate,
    "secrets": secrets_task.generate,
    "injection_honorific": lambda: injection.generate("injection_honorific"),
    "injection_secrets": lambda: injection.generate("injection_secrets"),
}
PROMPT_TASK = {"injection_honorific": "honorific", "injection_secrets": "secrets"}


def path(task):
    return DATA / f"{task}.jsonl"


def build(task):
    items = TASKS[task]()
    write_jsonl(path(task), items)
    return items


def load(task):
    return read_jsonl(path(task)) if path(task).exists() else build(task)


def prompt_for(task, text):
    name = PROMPT_TASK.get(task, task)
    return (DATA.parent / "prompts" / f"{name}.txt").read_text(encoding="utf-8").replace("{text}", text.rstrip("\n"))


def manifest():
    return {t: {"items": len(items), "sha256": digest(items), "committed": t not in UNCOMMITTED}
            for t, items in ((t, f()) for t, f in TASKS.items())}
