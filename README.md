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
