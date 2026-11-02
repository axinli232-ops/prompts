# 80条prompt的逐词五语候选

每个JSON文件独立对应一条prompt，不需要读取其他文件或共享词典。

- `LR01.json`—`LR40.json`：40条logical reasoning prompt。
- `FC01.json`—`FC40.json`：40条format control prompt。
- 每个文件含完整 `system_prompt`，以及按原文顺序排列的 `words`。
- 每个单词直接携带5个候选：`fr`法语、`es`西班牙语、`zh`中文、`ko`韩语、`ja`日语。
- 同一个词出现多次时，每次分别列出；本版不含短语项，也不依赖外部词典ID。

```json
{
  "prompt_id": "示意",
  "system_prompt": "Your task",
  "words": [
    {
      "index": 0,
      "word": "Your",
      "start": 0,
      "end": 4,
      "candidates": {
        "fr": "votre",
        "es": "tu",
        "zh": "你的",
        "ko": "당신의",
        "ja": "あなたの"
      }
    },
    {
      "index": 1,
      "word": "task",
      "start": 5,
      "end": 9,
      "candidates": {
        "fr": "tâche",
        "es": "tarea",
        "zh": "任务",
        "ko": "작업",
        "ja": "タスク"
      }
    }
  ]
}
```

共80条原始prompt、8,136处英文词语；只解析system prompt，不处理user query。

`start/end`是原始Python字符串的字符位置，右端不含，不是token位置；标点、数字和空白不作为单词。GPU替换后应重新tokenize完整文本。多处替换应从原文按位置倒序应用，避免索引偏移。

候选沿用此前生成的五语词汇候选，尚未逐处验证语境、语法或utility；其中312个不同词形使用词元形式候选。JSON、CSV、名称和非词汇碎片等无可靠外文翻译的项目保留原样，不代表五种不同的译文。固定输出标签、格式键等是否替换由你的实验程序决定，本版没有默认跳过规则。

旧的共享词典、词组映射和辅助脚本已由这80份直接可读的文件取代；原有prompt与query数据目录未修改。
