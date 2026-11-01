"""Validate frozen exports, splits and checksums using the standard library."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return [json.loads(line) for line in (ROOT / path).read_text(encoding="utf-8").splitlines() if line]

def check(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    prompts = read("data/prompts.jsonl")
    check(len(prompts) == 40, "Expected 40 prompts")
    prompt_map = {p["prompt_id"]: p for p in prompts}
    check(set(prompt_map) == {f"short_{i:02d}" for i in range(1, 41)}, "Invalid prompt IDs")
    canonical = {}
    split_texts = {"train": set(), "test": set()}
    film_groups = {"train": set(), "test": set()}
    for pool in ("general", "text", "film"):
        for split, size in (("train", 100), ("test", 50)):
            rows = read(f"data/queries/{pool}/{split}.jsonl")
            check(len(rows) == size, f"Wrong pool count: {pool}/{split}")
            for row in rows:
                qid = row["query_id"]
                check(qid not in canonical, f"Duplicate query ID: {qid}")
                check(row["split"] == split, "Incorrect canonical split")
                check(qid.startswith(pool + "_"), "Incorrect pool ID")
                check(bool(row["user_prompt"].strip()), "Empty user input")
                canonical[qid] = row
                split_texts[split].add(row["user_prompt"])
                if pool == "film":
                    film_groups[split].add(qid.rsplit("_", 1)[0])
    check(len(canonical) == 450, "Expected 450 canonical queries")
    check(len({r["user_prompt"] for r in canonical.values()}) == 450, "Duplicate canonical text")
    check(not split_texts["train"] & split_texts["test"], "Exact-text train/test overlap")
    check(not film_groups["train"] & film_groups["test"], "Film group train/test overlap")
    check(len(film_groups["train"]) == 20 and len(film_groups["test"]) == 10, "Wrong film split")
    all_rows = []
    for split, size in (("train", 4000), ("test", 2000)):
        rows = read(f"data/{split}.jsonl")
        check(len(rows) == size, f"Wrong combined {split} count")
        expected_size = 100 if split == "train" else 50
        check(Counter(r["prompt_id"] for r in rows) == Counter({p: expected_size for p in prompt_map}), "Wrong per-prompt count")
        for row in rows:
            p = prompt_map[row["prompt_id"]]
            q = canonical[row["query_id"]]
            check(row["split"] == q["split"] == split, "Inconsistent split")
            check(row["system_prompt"] == p["system_prompt"], "Changed system prompt")
            check(row["user_prompt"] == q["user_prompt"], "Changed user input")
            check(row["query_id"].startswith(p["query_pool"] + "_"), "Wrong query pool")
        all_rows.extend(rows)
    check(len({(r["prompt_id"], r["query_id"]) for r in all_rows}) == 6000, "Duplicate pair")
    for pid in prompt_map:
        rows = read(f"data/by_prompt/{pid}.jsonl")
        expected = [r for r in all_rows if r["prompt_id"] == pid]
        key = lambda r: (r["split"], r["query_id"])
        check(sorted(rows, key=key) == sorted(expected, key=key), f"By-prompt export differs: {pid}")
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    actual_paths = {str(p.relative_to(ROOT)) for p in (ROOT / "data").rglob("*.jsonl")}
    check(actual_paths == set(manifest["files_sha256"]), "Manifest file list differs")
    for path, expected_hash in manifest["files_sha256"].items():
        check(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected_hash, f"Checksum differs: {path}")
    print("PASS: 40 prompts; 4,000 train + 2,000 test pairs; 450 unique queries; fixed splits and checksums verified.")

if __name__ == "__main__":
    main()
