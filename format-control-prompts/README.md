# Format Control Prompts

40 preserved system prompts, with 150 user queries each: **100 train + 50 test**, totaling 6,000 prompt–query pairs.

## Files and use

- `data/prompts.jsonl`: exact system prompts and preserved source metadata.
- `data/by_prompt/FC01.jsonl` through `FC40.jsonl`: 150 query records per prompt, including origin, edit history, scenario family and split.
- `data/train.jsonl`, `data/test.jsonl`: **indices** into the per-prompt files (4,000 / 2,000 entries); use the loader to join system and user text.
- `dataset.py`, `examples/read_dataset.py`: standard-library-only Python loader, compatible with the role-control loader's `iter_examples` / `to_messages` interface.
- `scripts/validate_dataset.py`: counts, exact duplicates, per-prompt family separation, index consistency, original system hashes, English suffix and file checksums.
- `provenance/`: original archive README, archive-wide manifest and historical removal log; historical removed entries are not model inputs.

```bash
cd format-control-prompts
python scripts/validate_dataset.py
python examples/read_dataset.py --prompt-id FC01 --split train --limit 2
```

```python
from dataset import iter_examples, to_messages
for record in iter_examples(prompt_id="FC01", split="test"):
    messages = to_messages(record)
    # Use your own model client; metadata is not sent to the model.
```

## Import and split policy

Imported from the user-supplied `prompts_80_queries_150_no_classification_prefix (1).zip` on 2026-11-02; the archive SHA-256 is recorded in `manifest.json`. All system prompts are preserved byte-for-byte. The current user input appends a blank line and `Answer in English` to the imported query; original `raw_user_prompt` and provenance fields remain historical reference data and are never used by `to_messages`.

The repository's `split` field is distinct from the upstream `source_split`. A deterministic subset-sum selection of complete `scenario_family` groups yields exactly 50 test queries per system prompt; records without a family are individual groups. Each prompt has disjoint family groups and exact query texts between train and test. Splits are defined per system prompt, not a guarantee of semantic or exact-text isolation across every different system prompt. Do not re-split or optimize on the held-out test inputs.

The imported `source_text_unchanged` is preserved as `imported_source_text_unchanged`; the current flag is false because the English suffix has been appended. `query_edit` still describes the archive edit; `repository_query_edit` describes this export's change. All other source metadata remains as supplied.

## Scope and provenance

The category labels and relevance flags come from the supplied archive, not a new task-quality assessment. The logical-reasoning category includes rule-based classification; it does not imply that every prompt requires complex multistep reasoning. Original dataset queries and synthetic extensions are distinguished by `origin`, with per-category counts in the manifest.

This export does not regenerate, paraphrase or add answers to the queries. It preserves task-relevant context such as FC01 file metadata/rules and FC30 label sets, as documented in the archive. No model-output, utility or independent relevance validation has been run. Consult each prompt's source URL and upstream reuse terms; no blanket license is asserted for third-party text.
