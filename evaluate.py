import json, argparse
from core import search_notes

parser=argparse.ArgumentParser()
parser.add_argument("--user",default="demo")
parser.add_argument("--file",default="evaluation_queries.json")
args=parser.parse_args()

items=json.load(open(args.file,encoding="utf-8"))
correct=0
for item in items:
    res=search_notes(args.user,item["query"],item.get("top_k",5))["results"]
    returned={x["doc_id"] for x in res}
    ok=bool(returned & set(item["relevant_doc_ids"]))
    correct += ok
    print(("✓" if ok else "✗"), item["query"])
print(f"Precision@k (query-level): {correct/len(items):.2%}" if items else "No labeled queries.")
