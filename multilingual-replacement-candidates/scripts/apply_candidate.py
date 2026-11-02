import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from candidates import replace_once
p = argparse.ArgumentParser()
p.add_argument('--prompt-id', required=True)
p.add_argument('--unit-index', type=int, required=True)
p.add_argument('--language', choices=['fr', 'es', 'zh', 'ko', 'ja'], required=True)
p.add_argument('--variant', type=int, default=0)
p.add_argument('--allow-protected', action='store_true')
p.add_argument('--allow-identity', action='store_true')
a = p.parse_args()
sys.stdout.write(replace_once(a.prompt_id, a.unit_index, a.language,
                             a.variant, a.allow_protected, a.allow_identity))
