import argparse
import itertools
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from candidates import iter_candidates, replace_once
p = argparse.ArgumentParser()
p.add_argument('--prompt-id', required=True)
p.add_argument('--languages', nargs='+', default=['fr', 'es', 'zh', 'ko', 'ja'])
p.add_argument('--kind', choices=['word', 'phrase', 'both'], default='both')
p.add_argument('--limit', type=int)
p.add_argument('--include-protected', action='store_true')
p.add_argument('--include-identity', action='store_true')
p.add_argument('--include-text', action='store_true')
a = p.parse_args()
if a.limit is not None and a.limit < 0: p.error('--limit must be nonnegative')
kinds = ('word', 'phrase') if a.kind == 'both' else (a.kind,)
rows = iter_candidates(a.prompt_id, a.languages, kinds,
                      include_protected=a.include_protected,
                      include_identity=a.include_identity)
if a.limit is not None: rows = itertools.islice(rows, a.limit)
for r in rows:
    if a.include_text:
        r['candidate_system_prompt'] = replace_once(a.prompt_id, r['unit_index'],
            r['language'], r['variant'], a.include_protected, a.include_identity)
    print(json.dumps(r, ensure_ascii=False))
