# Role Control Prompts 40

40 role/style-control system prompts, each paired with 150 English user inputs: **100 train + 50 test**.

## Dataset at a glance

| Item | Count |
| --- | ---: |
| System prompts | 40 |
| Training prompt–query pairs | 4,000 |
| Test prompt–query pairs | 2,000 |
| Unique user inputs | 450 |

The 6,000 pairs are **not 6,000 distinct queries**: 36 prompts share a 150-input general pool; `short_23`, `short_24`, and `short_28` share a 150-input text pool; `short_35` uses a separate 150-input film pool. Every pool has a fixed 100/50 split. Shared inputs always stay in the same split across prompts. Film queries are grouped by film: 20 training titles and 10 test titles, with five questions per title.

User inputs do not name the target role, accent, style, output sentence count, or grammatical person. They consist of natural questions, situations, or source text. General inputs are individually authored; the film pool uses five question patterns across 30 films. These queries are AI-generated synthetic data, not queries copied from TruthfulQA or the USENIX paper.

## Files

- `data/train.jsonl`, `data/test.jsonl`: self-contained experiment records, including both system and user text.
- `data/prompts.jsonl`: the 40 system prompts, source metadata, Notion snapshot URLs, and pool assignments.
- `data/queries/<pool>/<split>.jsonl`: the 450 canonical user inputs and fixed splits.
- `data/by_prompt/short_XX.jsonl`: all 150 paired records for one prompt; filter the `split` field.
- `dataset.py`: dependency-free Python loader and chat-message builder.
- `examples/read_dataset.py`: minimal example that does not call a model.
- `scripts/validate_dataset.py`: counts, uniqueness, split consistency, export consistency, and SHA-256 checks.
- `manifest.json`: metadata and checksums for data files.

## Quick start

Python 3.9+; no third-party packages required.

```bash
python scripts/validate_dataset.py
python examples/read_dataset.py --prompt-id short_01 --split train --limit 2
```

```python
from dataset import iter_examples, to_messages

for example in iter_examples(prompt_id="short_01", split="train"):
    messages = to_messages(example)
    # Send messages to your chosen model using your own client.
    # For obfuscation, replace only messages[0]["content"].
```

A JSONL record contains `prompt_id`, `query_id`, `split`, `system_prompt`, and `user_prompt`. IDs, split labels, and source metadata are not model inputs. `to_messages` puts the system and user text into separate messages. No target answers or model responses are supplied.

## Experiment protocol

Use the 100 training inputs per prompt to optimize the obfuscated prompt. Keep the 50 test inputs held out from optimization and prompt selection. Evaluate original, blank, and obfuscated conditions on the same test inputs and generation settings. Do not interpret output similarity alone as a verified measure of task correctness or style compliance.

Do not independently shuffle or re-split each prompt: that would place identical queries in different splits across prompt conditions. This split prevents exact-text overlap, but semantic near-duplicates have not undergone independent human review.

## Prompt-specific notes

- `short_11` literally contains `{{topic}}`, as in its source. The default loader preserves it. Choose and document a consistent topic-substitution policy before running an experiment; do not provide extra topic information only to one condition.
- `short_28` requests preservation of tone, pacing, and emotional resonance but does not define a transformation operation. Define the intended task and scoring before treating it as a transformation benchmark.
- The collection includes role/task prompts as well as direct style controls. It is not a set of 40 independent pure styles.
- Prompts, splits, and user inputs were exported from the current Notion pages on 2026-11-01. Model utility and style compliance have not been validated.

## Sources and reuse

The first seven system prompts are attributed to Appendix A of *Prompt Obfuscation for Large Language Models*, USENIX Security 2025: https://www.usenix.org/system/files/usenixsecurity25-pape.pdf

The remaining prompts are complete short prompts or verbatim excerpts from prompts.chat. Each record retains its source URL and source type. The prompts.chat source URLs refer to the revision used during selection. Synthetic user inputs were generated separately for this collection.

No blanket license is asserted over third-party prompt text; see `SOURCE_NOTES.md` and the original sources for reuse terms.
