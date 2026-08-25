# Personal Knowledge-Base MCP Server

A recruiter-ready **Model Context Protocol (MCP) server** that provides semantic search over a real, personally-owned document corpus.

The project combines **FastMCP, Qdrant vector search, sentence-transformer embeddings, document ingestion, retrieval evaluation, FastAPI, SQLite authentication, and a multi-user web interface**.

---

## 1. Overview

Traditional keyword search can miss relevant information when the wording of a query differs from the wording used in a document.

This project solves that problem by converting documents into vector embeddings and storing them in **Qdrant**. Users can then search their knowledge base by meaning rather than exact keywords.

The retrieval functionality is exposed through the **Model Context Protocol (MCP)**, allowing an MCP-compatible client to call the knowledge-base tools directly.

The project is designed as a working, demo-able retrieval server rather than a chatbot application.

---

## 2. Problem Statement

Static keyword search depends heavily on matching exact words.

For example, a document may contain:

> "Agents receive percepts from their environment and perform rational actions."

while a user searches:

> "What is an intelligent agent?"

A semantic retrieval system can recognize that these concepts are related even when the wording is different.

This project provides reusable semantic retrieval tools backed by a vector database instead of building a one-off chatbot.

---

## 3. Goals

The project was designed to:

- Build a working MCP server exposing reusable retrieval tools.
- Index a real student-owned document corpus.
- Ingest PDF, Markdown, and TXT documents.
- Chunk documents before embedding.
- Generate semantic embeddings.
- Store embeddings in Qdrant.
- Retrieve semantically relevant document chunks.
- Return ranked results with source citations.
- Retrieve complete indexed document context.
- List indexed sources.
- Support per-user document isolation.
- Return `no_confident_match` for low-confidence queries.
- Measure retrieval quality using hand-labeled queries.
- Provide a lightweight multi-user web demonstration.
- Provide a live, connectable MCP server suitable for an MCP-compatible client.

---

## 4. Target Corpus

The project uses a real, student-owned corpus rather than a generic tutorial or Kaggle dataset.

The current demonstration corpus contains:

- `Samavia_Semester_Notes.md`

The notes contain Artificial Intelligence course material including:

- Intelligent Agents
- Environment Types
- Agent Architectures
- Search Algorithms
- Breadth-First Search
- A* Search
- Greedy Best-First Search
- Minimax
- Alpha-Beta Pruning
- Propositional Logic
- First-Order Logic
- Reinforcement Learning
- Bayes' Theorem
- Perceptrons
- Backpropagation

Additional personal documents can be uploaded through the web interface in PDF, Markdown, or TXT format.

---

## 5. Architecture

```text
                     ┌──────────────────────┐
                     │     MCP Client       │
                     │ Claude / MCP Client  │
                     └──────────┬───────────┘
                                │
                         MCP / JSON-RPC
                                │
                                ▼
                     ┌──────────────────────┐
                     │    FastMCP Server    │
                     │                      │
                     │  search_notes()      │
                     │  get_document()      │
                     │  list_sources()      │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │   Retrieval Core     │
                     │                      │
                     │ Chunking             │
                     │ Embeddings           │
                     │ Similarity Search    │
                     │ Threshold Filtering  │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    Qdrant Cloud      │
                     │   Vector Database    │
                     └──────────────────────┘


        ┌─────────────────────────────────────────┐
        │             Web Application             │
        │                                         │
        │  Sign Up / Login                        │
        │  Document Upload                        │
        │  Semantic Search                        │
        │  Source Listing                         │
        │  Search Results                         │
        └──────────────────┬──────────────────────┘
                           │
                           ▼
                    ┌───────────────┐
                    │   FastAPI     │
                    │   Backend     │
                    └───────┬───────┘
                            │
                            ▼
                     Retrieval Core
