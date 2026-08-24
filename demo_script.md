# 5-minute demo script

1. Show the GitHub README and architecture.
2. Show Qdrant Cloud collection `pkb_demo` with vectors.
3. Run ingestion on 2–5 of your own semester-note PDFs/MD/TXT files.
4. Run the FastAPI web demo and search for a concept using different wording than the notes.
5. Show ranked chunks, similarity scores and source citations.
6. Open Claude Desktop with the MCP server connected.
7. Ask: `Search my notes for [your real question]. Use user_id "demo".`
8. Show the `search_notes` tool call and returned citations.
9. Call `list_sources` and then `get_document` for one returned doc_id.
10. Run the hand-labeled evaluation and record the real Precision@k result in the README.

Important: do not claim a fabricated corpus or fabricated evaluation number. Use your own notes and the measured result.
