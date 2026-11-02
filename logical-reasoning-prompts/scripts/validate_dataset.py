"""Validate imported prompt text, indexed splits and per-prompt family isolation."""
from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]
def read(path):
 return [json.loads(s) for s in (ROOT/path).read_text(encoding='utf-8').splitlines() if s]
def check(c,m):
 if not c:raise ValueError(m)
def main():
 prompts=read('data/prompts.jsonl');check(len(prompts)==40,'Expected 40 prompts')
 check(len({p['prompt_id'] for p in prompts})==40,'Duplicate prompt ID')
 expected=set();counts=collections.Counter();all_rows=[]
 for p in prompts:
  pid=p['prompt_id'];check(hashlib.sha256(p['system_prompt'].encode()).hexdigest()==p['system_sha256'],f'System changed: {pid}')
  rows=read(f'data/by_prompt/{pid}.jsonl');check(len(rows)==150,f'Wrong query count: {pid}')
  check(len({q['query_id'] for q in rows})==150,f'Duplicate query ID: {pid}')
  check(len({q['user_prompt'] for q in rows})==150,f'Duplicate query text: {pid}')
  check(collections.Counter(q['split'] for q in rows)=={'train':100,'test':50},f'Wrong split: {pid}')
  groups={s:{q['split_group'] for q in rows if q['split']==s} for s in ('train','test')}
  check(not groups['train']&groups['test'],f'Family split across train/test: {pid}')
  for q in rows:
   check(q['prompt_id']==pid,'Wrong prompt mapping')
   check(q['user_prompt'].endswith('\n\nAnswer in English'),'Missing English suffix')
   expected.add((pid,q['query_id'],q['split']));counts[q['split']]+=1;all_rows.append(q)
 actual=[]
 for split in ('train','test'):
  refs=read(f'data/{split}.jsonl');check(len(refs)==(4000 if split=='train' else 2000),'Wrong index size')
  for r in refs:
   check(r['split']==split,'Wrong index split');actual.append((r['prompt_id'],r['query_id'],r['split']))
 check(len(actual)==len(set(actual))==6000,'Duplicate index entry')
 check(set(actual)==expected,'Index and canonical queries differ')
 m=json.loads((ROOT/'manifest.json').read_text());paths={str(p.relative_to(ROOT)) for p in (ROOT/'data').rglob('*.jsonl')}
 check(paths==set(m['files_sha256']),'Manifest file list differs')
 for path,digest in m['files_sha256'].items():check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,f'Checksum differs: {path}')
 check(dict(collections.Counter(q['origin'] for q in all_rows))==m['origin_counts'],'Origin counts differ')
 print('PASS: 40 unchanged system prompts; 4,000 train + 2,000 test queries; English suffix; per-prompt family isolation; consistent indices and checksums.')
if __name__=='__main__':main()
