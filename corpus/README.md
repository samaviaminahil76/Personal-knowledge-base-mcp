# Personal Knowledge Base MCP Server

An MCP server that provides semantic search over my personal semester notes using embeddings and Qdrant.

## Problem

Keyword search can miss relevant information when the wording of a query differs from the wording in the source document. This project uses semantic vector search to retrieve relevant knowledge by meaning.

## Architecture

PDF / Markdown / TXT
        ↓
Text Extraction
        ↓
Chunking
        ↓
Sentence Transformers
        ↓
Qdrant Vector Database
        ↓
FastMCP Server
        ↓
MCP Client

## MCP Tools

### search_notes
Performs semantic search and returns ranked chunks with similarity scores and source citations.

### get_document
Retrieves the complete indexed context for a document using its document ID.

### list_sources
Lists all documents indexed for a user.

## Corpus

The project uses my personally created semester notes:

`Samavia_Semester_Notes.md`

The document contains 9 indexed chunks covering topics including:

- Introduction & Intelligent Agents
- Problem Solving by Search
- Knowledge Representation & Logic
- Machine Learning & Probabilistic Reasoning

## Technology Stack

- Python
- FastMCP
- Qdrant Cloud
- Sentence Transformers
- all-MiniLM-L6-v2
- FastMCP STDIO transport

## Retrieval

The system uses cosine similarity with a configurable confidence threshold of 0.35. Queries below the threshold return `no_confident_match` instead of forcing an irrelevant result.

Example:

Query: `What is an intelligent agent?`

Top result:

- Source: `Samavia_Semester_Notes.md`
- Chunk: `0`
- Similarity: `0.6372`

## Evaluation

A hand-labeled test set of 5 queries was used to evaluate whether the system retrieved a relevant chunk.

Result:

**5/5 queries returned a relevant result — 100% query-level retrieval success.**

## Demo

The MCP server was tested through an MCP client and successfully exposed:

- `search_notes`
- `get_document`
- `list_sources`

Screenshots of the live tool calls are included in the project documentation.

## Future Work

- Multi-user web interface
- User authentication
- Document upload UI
- Search history
- FastAPI backend
- Remote HTTP deployment