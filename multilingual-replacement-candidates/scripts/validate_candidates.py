import hashlib
import json
import re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from candidates import ROOT, LANGUAGES, prompts, units, lexicon, iter_candidates, replace_once, apply_selection

def check(condition,message):
    if not condition:raise ValueError(message)

def main():
    ps=prompts();lex=lexicon();check(len(ps)==80,'Expected 80 prompts')
    check(set(ps)=={f'{prefix}{i:02d}' for prefix in ('LR','FC') for i in range(1,41)},'Wrong prompt IDs')
    words={r['english'] for r in lex.values() if r['kind']=='word'}
    check(len(words)==1759,'Expected 1759 word forms')
    check(len([r for r in lex.values() if r['kind']=='phrase'])==85,'Expected 85 phrase entries')
    for r in lex.values():
        check(set(r['translations'])==set(LANGUAGES),'Missing language')
        for lang,values in r['translations'].items():
            check(bool(values) and all(isinstance(v,str) and v.strip() for v in values),'Empty candidate')
            check(len(values)==len(set(values)),'Duplicate candidate')
    expected_words=set();word_occurrences=0;phrase_occurrences=0;overlap_checked=False
    for pid,p in ps.items():
        text=p['system_prompt'];check(hashlib.sha256(text.encode()).hexdigest()==p['system_sha256'],'Source hash differs')
        source=ROOT.parent/p['source_path']
        if source.exists():
            original=next(json.loads(s) for s in source.read_text().splitlines() if json.loads(s)['prompt_id']==pid)
            check(original['system_prompt']==text,'Original system prompt differs')
        spans=units(pid);expected=[m.span() for m in re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)?",text)]
        actual=[(u['start'],u['end']) for u in spans if u['kind']=='word'];check(actual==expected,'Missing or reordered word span')
        check(apply_selection(pid,[])==text,'Empty selection changed text')
        for i,u in enumerate(spans):
            check(u['unit_index']==i,'Wrong unit index');check(text[u['start']:u['end']]==u['text'],'Wrong character span')
            check(text.encode()[u['byte_start']:u['byte_end']].decode()==u['text'],'Wrong byte span')
            entry=lex[u['unit_id']];check(entry['english']==u['text'].lower(),'Wrong lexicon mapping')
            if u['kind']=='word':word_occurrences+=1;expected_words.add(u['text'].lower())
            else:phrase_occurrences+=1
        for c in iter_candidates(pid):
            out=replace_once(pid,c['unit_index'],c['language'],c['variant'])
            expected_text=text[:c['start']]+c['replacement']+text[c['end']:]
            check(out==expected_text,'Replacement changed unrelated text')
        protected=next((u for u in spans if u['protected']),None)
        if protected:
            try:replace_once(pid,protected['unit_index'],'fr')
            except ValueError:pass
            else:raise ValueError('Protected replacement was not rejected')
        if not overlap_checked:
            phrase=next((u for u in spans if u['kind']=='phrase' and not u['protected']),None)
            word=next((u for u in spans if phrase and u['kind']=='word' and not u['protected'] and phrase['start']<=u['start']<u['end']<=phrase['end']),None)
            if word:
                try:apply_selection(pid,[{'unit_index':phrase['unit_index'],'language':'fr'},{'unit_index':word['unit_index'],'language':'zh'}])
                except ValueError:overlap_checked=True
                else:raise ValueError('Overlapping edits accepted')
    check(overlap_checked,'No overlapping-edit check performed')
    check(expected_words==words,'Word dictionary and source vocabulary differ')
    check(word_occurrences==8136 and phrase_occurrences==297,'Coverage counts differ')
    manifest=json.loads((ROOT/'manifest.json').read_text())
    actual_paths={str(p.relative_to(ROOT)) for p in (ROOT/'data').rglob('*') if p.is_file()}
    check(actual_paths==set(manifest['data_files_sha256']),'Manifest file list differs')
    for name,digest in manifest['data_files_sha256'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Checksum differs: '+name)
    print('PASS: 80 unchanged prompts; 1,759 word forms; 85 phrase entries; 5 languages; 8,136 word + 297 phrase spans; exact replacements, protection checks, overlap rejection and checksums.')
if __name__=='__main__':main()
