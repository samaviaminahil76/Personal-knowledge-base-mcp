from mcp.server.fastmcp import FastMCP
from core import (
    search_notes as _search,
    get_document as _get,
    list_sources as _list,
    ingest_document as _ingest,
)

mcp = FastMCP("Personal Knowledge Base")


@mcp.tool()
def search_notes(user_id: str, query: str, top_k: int = 5) -> dict:
    """Semantic search over a user's indexed personal documents. Returns ranked chunks and citations."""
    return _search(user_id, query, top_k)


@mcp.tool()
def get_document(user_id: str, doc_id: str) -> dict:
    """Fetch the full indexed context for a document ID."""
    return _get(user_id, doc_id)


@mcp.tool()
def list_sources(user_id: str) -> dict:
    """List documents indexed for a user."""
    return _list(user_id)


@mcp.tool()
def ingest_document(user_id: str, path: str) -> dict:
    """Index a PDF, Markdown, or text document into the user's knowledge base."""
    return _ingest(user_id, path)


if __name__ == "__main__":
    mcp.run(transport="stdio")