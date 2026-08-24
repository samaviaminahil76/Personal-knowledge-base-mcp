import argparse
from pathlib import Path
from core import ingest_document

parser = argparse.ArgumentParser()
parser.add_argument("--user", default="demo")
parser.add_argument("--path", required=True)
args = parser.parse_args()

p = Path(args.path)
paths = [p] if p.is_file() else [x for x in p.rglob("*") if x.suffix.lower() in {".pdf", ".md", ".txt"}]
for f in paths:
    try:
        print(ingest_document(args.user, str(f)))
    except Exception as e:
        print(f"FAILED {f}: {e}")
