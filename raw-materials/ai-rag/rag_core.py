"""
Universal RAG Pipeline — Reference Implementation
Software Factory Raw Material: ai-rag

Provides chunking, retrieval, and prompt augmentation components
ready to wire into any FastAPI service or agent tool.
"""
from __future__ import annotations
import math
import os
from typing import Any, Dict, List, Optional


# ── Chunking ─────────────────────────────────────────────────────────────────

def chunk_documents(
    docs: List[str],
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Dict[str, Any]]:
    """
    Split documents into overlapping chunks with metadata.

    Args:
        docs: list of raw document strings
        chunk_size: approximate chars per chunk
        overlap: chars of overlap between consecutive chunks

    Returns:
        list of dicts: {text, doc_index, chunk_index, char_start, char_end}
    """
    chunks = []
    for doc_idx, doc in enumerate(docs):
        start = 0
        chunk_idx = 0
        while start < len(doc):
            end = min(start + chunk_size, len(doc))
            chunks.append({
                "text": doc[start:end],
                "doc_index": doc_idx,
                "chunk_index": chunk_idx,
                "char_start": start,
                "char_end": end,
            })
            chunk_idx += 1
            if end == len(doc):
                break
            start += chunk_size - overlap
    return chunks


# ── Embedding ─────────────────────────────────────────────────────────────────

def embed_query(
    text: str,
    model: str = "text-embedding-3-small",
    _client=None,
) -> List[float]:
    """
    Embed text using OpenAI or a local model.

    Falls back to a deterministic hash-based mock when
    OPENAI_API_KEY is unset — safe for unit tests.

    Args:
        text: string to embed
        model: OpenAI embedding model name
        _client: optional pre-built OpenAI client (for DI in tests)

    Returns:
        list of floats (1536-dim for text-embedding-3-small)
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Deterministic mock: hash chars mod 1, 1536-dim
        dim = 1536
        seed = [ord(c) for c in text]
        vec = [(((seed[i % len(seed)] * (i + 1)) % 256) / 255.0) for i in range(dim)]
        # Normalize
        mag = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / mag for x in vec]

    client = _client
    if client is None:
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("pip install openai to use real embeddings")

    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def embed_chunks(chunks: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
    """Embed all chunks in-place, adding an 'embedding' key."""
    for chunk in chunks:
        chunk["embedding"] = embed_query(chunk["text"], **kwargs)
    return chunks


# ── Retrieval ─────────────────────────────────────────────────────────────────

def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a)) or 1e-10
    mag_b = math.sqrt(sum(x * x for x in b)) or 1e-10
    return dot / (mag_a * mag_b)


def retrieve(
    query: str,
    corpus: List[Dict[str, Any]],
    top_k: int = 5,
    score_threshold: float = 0.0,
) -> List[Dict[str, Any]]:
    """
    Retrieve the top-k most similar chunks from a pre-embedded corpus.

    Args:
        query: query string (will be embedded internally)
        corpus: list of chunk dicts that must already have 'embedding' keys
        top_k: number of results to return
        score_threshold: minimum cosine similarity to include

    Returns:
        sorted list of (chunk + similarity_score) dicts, best first
    """
    if not corpus:
        return []
    query_vec = embed_query(query)
    scored = []
    for chunk in corpus:
        emb = chunk.get("embedding")
        if not emb:
            continue
        score = _cosine_similarity(query_vec, emb)
        if score >= score_threshold:
            scored.append({**chunk, "similarity_score": round(score, 6)})
    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored[:top_k]


# ── Prompt Augmentation ───────────────────────────────────────────────────────

DEFAULT_TEMPLATE = """\
Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I don't know."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""


def augment_prompt(
    query: str,
    retrieved: List[Dict[str, Any]],
    template: Optional[str] = None,
    max_context_chars: int = 4000,
) -> str:
    """
    Build a RAG-augmented prompt from a query and retrieved chunks.

    Args:
        query: the user query
        retrieved: ordered list of retrieved chunks (from retrieve())
        template: optional custom template with {context} and {query} placeholders
        max_context_chars: cap context size to avoid token overflow

    Returns:
        Complete prompt string ready for LLM inference
    """
    template = template or DEFAULT_TEMPLATE
    context_parts = []
    total_chars = 0
    for chunk in retrieved:
        text = chunk.get("text", "")
        if total_chars + len(text) > max_context_chars:
            remaining = max_context_chars - total_chars
            if remaining > 100:
                context_parts.append(text[:remaining] + "…")
            break
        context_parts.append(text)
        total_chars += len(text)
    context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant context found."
    return template.format(context=context, query=query)


# ── Pipeline ──────────────────────────────────────────────────────────────────

def run_rag_pipeline(
    query: str,
    docs: List[str],
    top_k: int = 5,
    chunk_size: int = 500,
    overlap: int = 50,
) -> Dict[str, Any]:
    """
    End-to-end RAG pipeline: chunk → embed → retrieve → augment.

    Args:
        query: user question
        docs: list of raw document strings
        top_k: number of chunks to retrieve
        chunk_size: chars per chunk
        overlap: overlap between chunks

    Returns:
        dict with keys: prompt, retrieved_chunks, chunk_count
    """
    chunks = chunk_documents(docs, chunk_size=chunk_size, overlap=overlap)
    embedded_chunks = embed_chunks(chunks)
    retrieved = retrieve(query, embedded_chunks, top_k=top_k)
    prompt = augment_prompt(query, retrieved)
    return {
        "prompt": prompt,
        "retrieved_chunks": retrieved,
        "chunk_count": len(chunks),
        "retrieved_count": len(retrieved),
    }
