import argparse
import itertools
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dataset import iter_examples, to_messages

parser = argparse.ArgumentParser()
parser.add_argument("--prompt-id", default="FC01")
parser.add_argument("--split", choices=["train", "test"], default="train")
parser.add_argument("--limit", type=int, default=2)
args = parser.parse_args()
if args.limit < 0:
    parser.error("--limit must be nonnegative")
for row in itertools.islice(iter_examples(args.prompt_id, args.split), args.limit):
    print(json.dumps({"prompt_id": row["prompt_id"], "query_id": row["query_id"],
                      "messages": to_messages(row)}, ensure_ascii=False))
