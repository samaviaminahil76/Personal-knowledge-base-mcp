# Personal Knowledge-Base MCP Server

A recruiter-ready MCP server that exposes semantic search over a real, personally-owned document corpus.

## Problem

Keyword search misses semantically related information when the wording differs. This project indexes personal notes with embeddings and exposes reusable retrieval tools through the Model Context Protocol.

## What it ships

- **FastMCP server** with 3 callable tools:
  - `search_notes(user_id, query, top_k)` — ranked chunks + source citations
  - `get_document(user_id, doc_id)` — full indexed document context
  - `list_sources(user_id)` — indexed sources
- PDF/Markdown/TXT ingestion and overlap-aware chunking
- `sentence-transformers/all-MiniLM-L6-v2` embeddings
- Qdrant vector storage with per-user collections
- Similarity threshold with explicit `no_confident_match`
- FastAPI multi-user web demo with signup/login, upload and search
- Hand-labeled retrieval evaluation script

## Architecture

See [`architecture.md`](architecture.md).

## Quick start

### 1. Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Qdrant Cloud

Create a free Qdrant Cloud cluster, copy its URL/API key, and create `.env` from `.env.example`.

```env
QDRANT_URL=https://YOUR-CLUSTER.qdrant.io
QDRANT_API_KEY=YOUR_KEY
```

### 3. Add your real corpus

Put 2–5 of your own semester notes in `corpus/`, then:

```bash
python ingest.py --user demo --path corpus
```

### 4. Run the web demo

```bash
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000`.

### 5. Run the MCP server

```bash
python server.py
```

For Claude Desktop, add the server command to the MCP configuration using the absolute path to `server.py` and the same Python interpreter from your virtual environment.

Example shape:

```json
{
  "mcpServers": {
    "personal-knowledge-base": {
      "command": "C:\\PATH\\TO\\.venv\\Scripts\\python.exe",
      "args": ["C:\\PATH\\TO\\personal-knowledge-base-mcp\\server.py"]
    }
  }
}
```

## Retrieval quality

Create a small hand-labeled set in `evaluation_queries.json`, with each query mapped to the correct `doc_id`, then run:

```bash
python evaluate.py --user demo
```

Report the actual measured Precision@k in your final README. Do not fabricate the number.

## Demo

See [`demo_script.md`](demo_script.md) for a 5-minute live demo sequence.

## Tech stack

Python · FastMCP · Qdrant Cloud · Sentence Transformers · FastAPI · SQLite · PDF/Markdown/TXT

## Why this is useful

The MCP layer is protocol-level: the same retrieval capability can be called by Claude Desktop or another MCP-compatible client instead of being locked into a custom chatbot UI.

## Limitations

This is a fellowship/demo implementation. Authentication is intentionally basic; production deployments should add secure sessions, password hashing, authorization middleware, rate limits, encrypted storage, and stronger tenant isolation.
