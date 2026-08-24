# Personal Knowledge Corpus

This directory contains the real, student-owned document corpus used to
demonstrate the Personal Knowledge-Base MCP Server.

## Corpus Source

The corpus consists of my own semester notes created for studying
Artificial Intelligence and related university coursework.

### Included Document

- `Samavia_Semester_Notes.md` — personal semester notes covering:
  - Introduction to Artificial Intelligence
  - Intelligent Agents
  - Environment Types
  - Agent Architectures
  - Problem Solving by Search
  - Knowledge Representation and Logic
  - Machine Learning
  - Probabilistic Reasoning

## Why This Corpus

The project requirement is to demonstrate semantic retrieval on a real,
student-owned corpus rather than a generic tutorial or public benchmark
dataset.

These notes were selected because they contain multiple related AI concepts
that can be retrieved semantically even when the query wording differs from
the exact wording in the notes.

## Ingestion

The document is:

1. Read as Markdown/TXT content.
2. Split into overlapping chunks.
3. Converted into sentence embeddings using
   `sentence-transformers/all-MiniLM-L6-v2`.
4. Stored as vectors and metadata in Qdrant Cloud.
5. Retrieved using cosine-similarity semantic search.

## Current Indexed Source

| Document | Type | Chunks |
|---|---|---:|
| `Samavia_Semester_Notes.md` | Markdown | 9 |

## Example Semantic Query

**Query:**

> What is an intelligent agent?

The system retrieves the relevant section:

> Artificial Intelligence (AI) is the study of agents that receive percepts
> from the environment and perform rational actions to maximize their chance
> of success.

The result includes the document name, chunk number, similarity score,
and document ID for citation and traceability.

## Privacy

This corpus contains personal study notes and is included only as the
demonstration dataset for this fellowship project.