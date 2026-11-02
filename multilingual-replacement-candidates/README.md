# 五语词级／短语级替换候选

供提示词混淆的离散候选搜索使用，覆盖仓库中的 **LR01–LR40 与 FC01–FC40，共80条原始 system prompt**。

| 内容 | 数量 |
| --- | ---: |
| 不同英文词形 | 1,759 |
| 英文词语出现次数 | 8,136 |
| 精选常用短语词条 | 85 |
| 短语在这80条prompt中的匹配次数 | 297 |
| 使用词元候选的英文词形 | 312 |
| 目标语言 | 法语、西班牙语、简体中文、韩语、日语 |

这些是 **AI生成的孤立词汇／短语候选**，不是80条prompt的整句翻译，也不是已通过语义等价或utility验证的混淆结果。一个词的候选可含多个词，例如 `sentiment → 情感倾向`。多义词有部分备选义项，尚未逐处按上下文消歧。法语、西语的性数、动词变位，以及中日韩语序不会因单词替换而自动调整；后续须由你的搜索目标和模型打分选择。

## 文件

- `data/lexicon.jsonl`：共享词典，每行一个英文词形或短语，`translations` 包含 `fr/es/zh/ko/ja` 五个列表。
- `data/prompts.jsonl`：80条未修改的原始system prompt、来源及SHA-256。
- `data/units_by_prompt/LR01.json` 等80个文件：每处单词／短语在原prompt中的精确范围、词典ID、保护标记。
- `data/coverage.json`：完整覆盖统计及每条prompt的数量。
- `data/languages.json`：语言代码表。
- `candidates.py`：候选遍历、单点替换、多点重建接口。
- `scripts/list_candidates.py`：输出供GPU评分程序读取的候选JSONL。
- `scripts/apply_candidate.py`：应用一个指定候选并输出完整prompt。
- `scripts/validate_candidates.py`：词典覆盖、五语字段、字符／字节范围、保护标记、重叠处理和校验和验证。

## 词形与词元

每个不同英文词形都有自己的词典记录；其中312个词形共用相应词元的翻译候选，例如某些复数或进行时形式采用单数／原形候选，并标记 `uses_lemma_form: true`，不声称已还原原文语法。`lookup_form` 明确记录其查词形式；常见派生词、易错词和部分助动词另外提供了独立词条。

缩写、标识符或非词汇碎片中没有可靠外文译法的条目，会原样保留并标记 `identity_retained: true`，不将其宣称为五种不同的翻译；默认不进入替换迭代。85个短语是精选词组，不是所有可能n-gram的穷举。

## 位置与保护标记

`start/end` 是Python字符串的Unicode字符索引，右端不含；`byte_start/byte_end` 是UTF-8字节范围，二者均不是模型token位置。原prompt中的标点、数字、空格、大小写保留不变。

代码、URL、占位符、引号内字面量、标记和疑似固定输出标签会被启发式标记为 `protected`；仍保留词典候选，但默认跳过。保护规则可能有误判，不能代替对任务约束的审查；必要时可显式启用 `include_protected` / `allow_protected`。

## 快速使用（Python 3.9+，无第三方依赖）

```bash
cd multilingual-replacement-candidates
python scripts/validate_candidates.py
python scripts/list_candidates.py --prompt-id LR01 --languages fr es zh ko ja --limit 10
python scripts/list_candidates.py --prompt-id LR01 --kind word --languages zh --include-text --limit 5
```

列表输出中的 `unit_index` 对应该prompt的候选位置，使用它进行替换：

```bash
python scripts/apply_candidate.py --prompt-id LR01 --unit-index 0 --language fr
```

实际执行前应从候选列表选择有效位置；受保护项需要明确加入 `--allow-protected`。

```python
from candidates import iter_candidates, replace_once, apply_selection

for c in iter_candidates('LR01', languages=('fr', 'es', 'zh', 'ko', 'ja')):
    candidate_prompt = replace_once('LR01', c['unit_index'], c['language'], c['variant'])
    # 用你的目标tokenizer重新编码完整candidate_prompt，再在GPU上打分。
    # score = utility_loss(candidate_prompt, train_queries)

# 连续搜索时，保存原始位置上的选择，再从原文重建每个候选：
selected = []  # 每项为 {unit_index, language, variant}
current_prompt = apply_selection('LR01', selected)
```

短语与组成单词的范围可能重叠，不能同时替换；接口会拒绝重叠选择。选中的外文长度可能改变，不要拿第一次替换前的字符位置去切割已修改的文本，也不要沿用英语的token索引；应保留原文位置上的选择，逐次从原文重建并重新tokenize。

## 实验衔接

只修改system prompt。原有三类数据目录、user queries及其 `Answer in English` 后缀、100/50划分均不在此次修改范围。优化使用训练query，测试query保持持出。本目录不调用模型或占用GPU，也未提供模型评分结果。

数据来源是本仓库80条LR/FC system prompt；词汇候选由AI生成，未经过独立多语人工审校或自动翻译质量评测。覆盖率验证只确认候选存在、映射完整、替换实现正确，不证明语义或任务性能保持。
