# Personal Knowledge-Base MCP Server

A recruiter-ready Model Context Protocol (MCP) server that provides semantic search over a real, personally-owned document corpus.

The project combines an MCP server, Qdrant vector search, sentence-transformer embeddings, document ingestion, retrieval evaluation, and a lightweight multi-user web interface.

---

## Overview

Traditional keyword search can miss relevant information when the wording of a query differs from the wording used in a document.

This project solves that problem by converting documents into vector embeddings and storing them in Qdrant. Users can then search their knowledge base by meaning rather than exact keywords.

The retrieval functionality is exposed through the Model Context Protocol (MCP), allowing MCP-compatible clients to call the knowledge-base tools directly.

This is a working retrieval system rather than a chatbot UI.

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

# Key Features

## 1. MCP Server

The FastMCP server exposes three callable tools.

### `search_notes(user_id, query, top_k)`

Performs semantic search and returns ranked document chunks containing:

- Rank
- Similarity score
- Document ID
- Source filename
- Chunk ID
- Retrieved text
- Source citation

Example:

```json
{
  "status": "ok",
  "query": "What is an intelligent agent?",
  "results": [
    {
      "rank": 1,
      "score": 0.6372,
      "doc_id": "23a876d6-e46d-4fc4-9701-d3b924896841",
      "source": "Samavia_Semester_Notes.md",
      "chunk_id": 0,
      "text": "Artificial Intelligence (AI) is the study of agents..."
    }
  ]
}
