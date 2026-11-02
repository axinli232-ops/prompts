# 去掉分类任务提示的版本

80 条 system prompt 原文不变；每条仍有 150 条 user query，共 12,000 条。

## 本次处理
去除 Classify this review、Please categorize the following、Which category fits、What sentiment 等分类任务前缀，以及能安全识别的尾部分类提问，保留待判断的原始内容。
分类范围：全部 LR，以及 FC01/FC02/FC04/FC05/FC30/FC38。
其他格式控制任务的正常请求，如写故事、拟信、生成计划，保留其任务含义。
FC01 的文件元数据和判定规则、FC30 的预设标签集是完成任务所需的数据，因此保留，以免删除后缺少必要输入。

无法安全提取待判断内容的元问题和去前缀后重复的条目，共 187 条，已放入 removed_or_merged_queries.jsonl；从既有同任务合成池补充 187 条，使各 system 保持 150 条且无完全重复。

## 文件和来源
两个分组 JSONL 各 40 条 system；on_topic_user_prompts 为每条 system 的完整 150 条列表。
all_pairs_12000.jsonl 为展开后的配对；index.html 为阅读版。
user_prompt 为本次处理后的输入，raw_user_prompt 为处理前文本；query_edit 说明处理方式。
origin 表示来源，原数据集来源的 query 可能已经删去了任务提示，不应再声称全部 query 与原数据集逐字一致；source_text_unchanged 可用于判断。
本版本保留原数据来源 489 条、合成来源 11511 条；所有被替换或合并的旧条目可在修改记录中找回。
新增数据仍未经过独立相关性标注或目标模型运行验证；去掉前缀也不代表语义上完全去掉了所有任务线索。
scenario_family 可帮助按基础情景分组，避免训练测试之间泄漏相近变体。
