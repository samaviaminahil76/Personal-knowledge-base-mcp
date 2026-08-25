# Personal Knowledge-Base MCP Server

A recruiter-ready Model Context Protocol (MCP) server that provides semantic search over a real, personally-owned document corpus.

The project combines an MCP server, Qdrant vector search, sentence-transformer embeddings, document ingestion, retrieval evaluation, and a lightweight multi-user web interface.

---

## Overview

Traditional keyword search can miss relevant information when the wording of a query differs from the wording used in a document.

This project solves that problem by converting documents into vector embeddings and storing them in Qdrant. Users can then search their knowledge base by meaning rather than exact keywords.

The retrieval functionality is exposed through the Model Context Protocol (MCP), allowing an MCP-compatible client to call the knowledge-base tools directly.

---

## Problem Statement

Static keyword search depends heavily on matching exact words.

For example, a document may contain:

> "Agents receive percepts from their environment and perform rational actions."

while a user searches:

> "What is an intelligent agent?"

A semantic retrieval system can recognize that these concepts are related even when the wording is different.

This project provides reusable semantic retrieval tools backed by a vector database rather than building a one-off chatbot.

---

## Goals

The project was designed to:

- Build a working MCP server exposing reusable retrieval tools.
- Index a real student-owned document corpus.
- Generate embeddings for document chunks.
- Store embeddings in Qdrant.
- Retrieve semantically relevant document chunks.
- Return ranked results with source citations.
- Support retrieving complete indexed documents.
- Provide a list of indexed sources.
- Return `no_confident_match` when a query falls below the similarity threshold.
- Provide measurable retrieval evaluation using hand-labeled queries.
- Provide a simple multi-user web demonstration.

---

## Key Features

### MCP Server

The FastMCP server exposes three callable tools:

#### `search_notes(user_id, query, top_k)`

Performs semantic search and returns ranked document chunks with:

- Rank
- Similarity score
- Document ID
- Source filename
- Chunk ID
- Retrieved text
- Source citation

#### `get_document(user_id, doc_id)`

Retrieves the full indexed document context associated with a document ID.

#### `list_sources(user_id)`

Lists the documents currently indexed for a user.

---

### Document Ingestion

The system supports:

- PDF
- Markdown (`.md`)
- TXT

Documents are processed into overlapping chunks before embeddings are generated.

---

### Semantic Embeddings

The project uses:

`sentence-transformers/all-MiniLM-L6-v2`

Each document chunk is converted into a vector representation.

The vectors are then stored and searched using Qdrant.

---

### Vector Database

The project uses **Qdrant Cloud** for vector storage and similarity search.

The system supports per-user isolation so that each user's indexed documents can be kept separate.

---

### Similarity Threshold

The retrieval system does not blindly return results for every query.

If the best matches do not meet the configured similarity threshold, the system returns:

```json
{
  "status": "no_confident_match",
  "query": "example query",
  "threshold": 0.35,
  "results": []
}
