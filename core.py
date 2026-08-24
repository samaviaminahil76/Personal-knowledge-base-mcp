import os
import re
import uuid
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

load_dotenv()


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", "0.35")
)

client = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.getenv("QDRANT_API_KEY")
)

model = SentenceTransformer(MODEL_NAME)

VECTOR_SIZE = model.get_sentence_embedding_dimension()


# =========================================================
# COLLECTION HELPERS
# =========================================================

def collection_name(user_id: str) -> str:
    """Create a safe Qdrant collection name for a user."""

    safe = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        user_id
    )[:50]

    return f"pkb_{safe or 'demo'}"


def ensure_collection(user_id: str):
    """Create the user's collection if it doesn't exist."""

    name = collection_name(user_id)

    existing = {
        collection.name
        for collection in client.get_collections().collections
    }

    if name not in existing:
        client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

    return name


# =========================================================
# TEXT CHUNKING
# =========================================================

def chunk_text(
    text: str,
    chunk_size: int = 900,
    overlap: int = 150
):
    """Split document text into overlapping chunks."""

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text)
        )

        # Try to end at a word boundary
        if end < len(text):

            cut = text.rfind(
                " ",
                start + chunk_size - 120,
                end
            )

            if cut > start:
                end = cut

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(
            end - overlap,
            start + 1
        )

    return chunks


# =========================================================
# EMBEDDINGS
# =========================================================

def embed(texts):
    """Generate normalized embeddings."""

    return model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()


# =========================================================
# DOCUMENT INGESTION
# =========================================================

def ingest_document(
    user_id: str,
    path: str
):
    """Read a PDF/MD/TXT document and store its chunks."""

    from pypdf import PdfReader

    document_path = Path(path)

    if not document_path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    # -----------------------------
    # Read document
    # -----------------------------

    extension = document_path.suffix.lower()

    if extension == ".pdf":

        text = "\n".join(
            page.extract_text() or ""
            for page in PdfReader(
                str(document_path)
            ).pages
        )

    elif extension in {".md", ".txt"}:

        text = document_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    else:

        raise ValueError(
            "Only PDF, MD and TXT files are supported."
        )

    # -----------------------------
    # Create chunks
    # -----------------------------

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "No readable text found in the document."
        )

    # -----------------------------
    # Get collection
    # -----------------------------

    collection = ensure_collection(user_id)

    # -----------------------------
    # Generate embeddings
    # -----------------------------

    vectors = embed(chunks)

    # -----------------------------
    # Generate document ID
    # -----------------------------

    doc_id = str(uuid.uuid4())

    points = []

    # -----------------------------
    # Create Qdrant points
    # -----------------------------

    for chunk_id, (chunk, vector) in enumerate(
        zip(chunks, vectors)
    ):

        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),

                vector=vector,

                payload={
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                    "source": document_path.name,
                    "text": chunk
                }
            )
        )

    # -----------------------------
    # Store points
    # -----------------------------

    client.upsert(
        collection_name=collection,
        points=points,
        wait=True
    )

    return {
        "status": "ok",
        "doc_id": doc_id,
        "source": document_path.name,
        "chunks": len(chunks)
    }


# =========================================================
# SEMANTIC SEARCH
# =========================================================

def search_notes(
    user_id: str,
    query: str,
    top_k: int = 5
):
    """Search the user's indexed notes semantically."""

    if not query or not query.strip():

        return {
            "status": "error",
            "message": "Query cannot be empty.",
            "results": []
        }

    collection = ensure_collection(user_id)

    # Generate query embedding
    query_vector = embed([query])[0]

    # Search Qdrant
    hits = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=max(
            1,
            min(top_k, 20)
        ),
        with_payload=True,
        with_vectors=False
    ).points

    results = []

    for hit in hits:

        score = float(hit.score)

        if score < THRESHOLD:
            continue

        payload = hit.payload or {}

        results.append({
            "rank": len(results) + 1,
            "score": round(score, 4),
            "doc_id": payload.get("doc_id"),
            "source": payload.get("source"),
            "chunk_id": payload.get("chunk_id"),
            "text": payload.get("text"),
            "citation": (
                f"{payload.get('source')} "
                f"— chunk {payload.get('chunk_id')}"
            )
        })

    # No confident match
    if not results:

        return {
            "status": "no_confident_match",
            "query": query,
            "threshold": THRESHOLD,
            "results": []
        }

    return {
        "status": "ok",
        "query": query,
        "results": results
    }


# =========================================================
# GET COMPLETE DOCUMENT
# =========================================================

def get_document(
    user_id: str,
    doc_id: str
):
    """
    Retrieve all chunks belonging to a document.

    This intentionally does NOT use a Qdrant payload filter
    for doc_id. Instead, it scrolls through the collection
    and matches doc_id in Python.
    """

    collection = ensure_collection(user_id)

    # Get points from the collection
    points, _ = client.scroll(
        collection_name=collection,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )

    matching_payloads = []

    # Find chunks belonging to requested document
    for point in points:

        payload = point.payload or {}

        stored_doc_id = payload.get("doc_id")

        if str(stored_doc_id) == str(doc_id):

            matching_payloads.append(payload)

    # Document doesn't exist
    if not matching_payloads:

        return {
            "status": "not_found",
            "doc_id": doc_id
        }

    # Sort chunks in correct order
    matching_payloads.sort(
        key=lambda payload: payload.get(
            "chunk_id",
            0
        )
    )

    # Reconstruct document
    full_text = " ".join(
        payload.get("text", "")
        for payload in matching_payloads
    )

    return {
        "status": "ok",
        "doc_id": doc_id,
        "source": matching_payloads[0].get("source"),
        "full_text": full_text,
        "chunks": len(matching_payloads)
    }


# =========================================================
# LIST SOURCES
# =========================================================

def list_sources(user_id: str):
    """List all indexed documents for a user."""

    collection = ensure_collection(user_id)

    points, _ = client.scroll(
        collection_name=collection,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )

    documents = {}

    for point in points:

        payload = point.payload or {}

        doc_id = payload.get("doc_id")

        if not doc_id:
            continue

        if doc_id not in documents:

            documents[doc_id] = {
                "doc_id": doc_id,
                "source": payload.get("source"),
                "chunks": 0
            }

        documents[doc_id]["chunks"] += 1

    return {
        "status": "ok",
        "sources": list(
            documents.values()
        )
    }