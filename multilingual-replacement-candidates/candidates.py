"""Five-language replacement candidates anchored to original system prompts."""
import hashlib
import json
from functools import lru_cache
from pathlib import Path
ROOT = Path(__file__).resolve().parent
LANGUAGES = ('fr', 'es', 'zh', 'ko', 'ja')

def _jsonl(path):
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

@lru_cache(maxsize=1)
def lexicon():
    return {row['unit_id']: row for row in _jsonl(ROOT / 'data/lexicon.jsonl')}

@lru_cache(maxsize=1)
def prompts():
    return {row['prompt_id']: row for row in _jsonl(ROOT / 'data/prompts.jsonl')}

@lru_cache(maxsize=80)
def units(prompt_id):
    if prompt_id not in prompts():
        raise ValueError('Unknown prompt_id; use LR01–LR40 or FC01–FC40')
    row = json.loads((ROOT / 'data/units_by_prompt' / f'{prompt_id}.json').read_text(encoding='utf-8'))
    text = prompts()[prompt_id]['system_prompt']
    if hashlib.sha256(text.encode()).hexdigest() != row['system_sha256']:
        raise ValueError('Source prompt changed; original spans are invalid')
    return row['units']

def iter_candidates(prompt_id, languages=LANGUAGES, kinds=('word', 'phrase'),
                    include_protected=False, include_identity=False):
    """Stream candidate records; metadata is not itself a model input."""
    if isinstance(languages, str):
        languages = (languages,)
    if not set(languages) <= set(LANGUAGES):
        raise ValueError('Unsupported language')
    for unit in units(prompt_id):
        entry = lexicon()[unit['unit_id']]
        if unit['kind'] not in kinds or (unit['protected'] and not include_protected):
            continue
        if entry['identity_retained'] and not include_identity:
            continue
        for lang in languages:
            for variant, replacement in enumerate(entry['translations'][lang]):
                if replacement == unit['text'] and not include_identity:
                    continue
                yield dict(unit, prompt_id=prompt_id, language=lang,
                           variant=variant, replacement=replacement,
                           lookup_form=entry['lookup_form'],
                           uses_lemma_form=entry['uses_lemma_form'])

def apply_selection(prompt_id, selections, allow_protected=False, allow_identity=False):
    """Rebuild from the original prompt; reject overlapping word/phrase edits.

    Each selection is {unit_index, language, variant (default 0)}.
    Keep selections in original-span coordinates during iterative search.
    """
    original = prompts()[prompt_id]['system_prompt']
    source_units = units(prompt_id)
    edits = []
    for selection in selections:
        index = selection['unit_index']
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(source_units):
            raise ValueError('Invalid unit_index')
        unit = source_units[index]
        if unit['protected'] and not allow_protected:
            raise ValueError('Protected unit; explicitly enable allow_protected to replace it')
        entry = lexicon()[unit['unit_id']]
        if entry['identity_retained'] and not allow_identity:
            raise ValueError('Identifier/fragment has no asserted foreign translation')
        lang = selection['language']
        variant = selection.get('variant', 0)
        if lang not in LANGUAGES:
            raise ValueError('Unsupported language')
        choices = entry['translations'][lang]
        if not isinstance(variant, int) or isinstance(variant, bool) or not 0 <= variant < len(choices):
            raise ValueError('Invalid variant index')
        a, b = unit['start'], unit['end']
        if original[a:b] != unit['text']:
            raise ValueError('Span does not match source prompt')
        edits.append((a, b, choices[variant]))
    edits.sort()
    for left, right in zip(edits, edits[1:]):
        if right[0] < left[1]:
            raise ValueError('Overlapping selections; choose either a phrase or its constituent words')
    result = original
    for a, b, replacement in reversed(edits):
        result = result[:a] + replacement + result[b:]
    return result

def replace_once(prompt_id, unit_index, language, variant=0,
                 allow_protected=False, allow_identity=False):
    return apply_selection(prompt_id, [{'unit_index': unit_index,
                           'language': language, 'variant': variant}],
                           allow_protected=allow_protected,
                           allow_identity=allow_identity)
