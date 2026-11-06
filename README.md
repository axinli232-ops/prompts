# Prompts for Obfuscation Experiments

用于提示词混淆实验的 system prompts 与 user queries。

## 数据集

| 目录 | System prompts | 每条训练 / 测试 query | 配对总量 |
| --- | ---: | ---: | ---: |
| [role-control-prompts](role-control-prompts/) | 40 | 100 / 50 | 6,000 |
| [logical-reasoning-prompts](logical-reasoning-prompts/) | 40 | 100 / 50 | 6,000 |
| [format-control-prompts](format-control-prompts/) | 40 | 100 / 50 | 6,000 |

`role-control-prompts/` 提供原始 prompt、来源记录、固定数据划分、JSONL 文件、Python 读取示例和数据校验脚本。

36 个通用 prompt 共用一组150条 query；3个文本处理 prompt 共用另一组150条文本；1个电影相关 prompt 使用单独150条 query，共450条不同输入。

```bash
cd role-control-prompts
python scripts/validate_dataset.py
python examples/read_dataset.py --prompt-id short_01 --split train --limit 2
```

完整说明请查看 [数据集 README](role-control-prompts/README.md)。

新增两类保留上传压缩包中的 system prompt 和 query 来源记录，并按每条 prompt 内的完整 `scenario_family` 划分训练／测试集；所有实际 user query 末尾追加 `Answer in English`，读取方式见各目录 README。

## 多语替换候选

[逐条prompt的五语单词候选](multilingual-replacement-candidates/) 包含80份独立JSON文件（LR01–LR40、FC01–FC40）；每份按原文顺序逐词列出法语、西班牙语、中文、韩语、日语五个候选，直接写在对应单词下面，无需共享词典。

## Keyword Utilization

[keyword/](keyword/) 收录 PUPA 派生的 40 条英文个人背景提示词，每条配 100 条 train 和 50 条 test query，并含敏感/固定关键词标注及仅针对非敏感词的五语逐词替换候选。

