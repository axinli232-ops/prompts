"""Load indexed train/test records and join preserved system/query metadata."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def _read(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def iter_examples(prompt_id=None, split="train", root=None):
    if split not in {"train", "test"}:
        raise ValueError("split must be train or test")
    base = Path(root) if root is not None else ROOT
    prompts = {p["prompt_id"]: p for p in _read(base / "data/prompts.jsonl")}
    if prompt_id is not None and prompt_id not in prompts:
        raise ValueError("Unknown prompt_id")
    cache = {}
    for ref in _read(base / "data" / f"{split}.jsonl"):
        pid = ref["prompt_id"]
        if prompt_id is not None and pid != prompt_id:
            continue
        if pid not in cache:
            cache[pid] = {q["query_id"]: q for q in _read(base / "data/by_prompt" / f"{pid}.jsonl")}
        q = cache[pid][ref["query_id"]]
        yield dict(q, system_prompt=prompts[pid]["system_prompt"])

def to_messages(example):
    return [{"role": "system", "content": example["system_prompt"]},
            {"role": "user", "content": example["user_prompt"]}]
