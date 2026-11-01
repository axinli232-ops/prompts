"""Read the frozen dataset without modifying prompts or splits."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def iter_examples(prompt_id=None, split="train", root=None):
    """Yield records from train or test; preserve original query and system text."""
    if split not in {"train", "test"}:
        raise ValueError("split must be train or test")
    if prompt_id is not None and prompt_id not in {f"short_{i:02d}" for i in range(1, 41)}:
        raise ValueError("Unknown prompt_id")
    base = Path(root) if root is not None else ROOT
    with (base / "data" / f"{split}.jsonl").open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if prompt_id is None or record["prompt_id"] == prompt_id:
                yield record

def to_messages(example):
    """Keep metadata out of model input; preserve unresolved source placeholders."""
    return [{"role": "system", "content": example["system_prompt"]},
            {"role": "user", "content": example["user_prompt"]}]
