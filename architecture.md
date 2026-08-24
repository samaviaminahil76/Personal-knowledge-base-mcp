# Architecture

```text
                    ┌─────────────────────┐
                    │ Claude Desktop /     │
                    │ MCP-compatible client│
                    └──────────┬──────────┘
                               │ JSON-RPC / STDIO
                               ▼
                    ┌─────────────────────┐
                    │ FastMCP server      │
                    │ 3 tools             │
                    │ search_notes        │
                    │ get_document        │
                    │ list_sources        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Retrieval core      │
                    │ chunk → embed →      │
                    │ cosine search →      │
                    │ threshold            │
                    └──────┬──────────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
        Sentence Transformers      Qdrant Cloud
        all-MiniLM-L6-v2           per-user collections
```

The web demo uses FastAPI and calls the same retrieval functions as the MCP tools.
