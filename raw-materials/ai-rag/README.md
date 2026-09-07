# Raw Material: AI RAG Pipeline

**Category:** AI/ML | **Status:** REFERENCE | **Language:** Python

## What This Provides

A complete, self-contained Retrieval-Augmented Generation (RAG) pipeline
ready to embed in any backend service. Works out-of-the-box with a
deterministic mock embedding (no API key needed for development/testing),
and upgrades seamlessly to real OpenAI embeddings by setting `OPENAI_API_KEY`.

## Key Functions

| Function | Description |
|---|---|
| `chunk_documents(docs, chunk_size, overlap)` | Split docs into overlapping chunks |
| `embed_query(text, model)` | Embed text (real or mock) |
| `embed_chunks(chunks)` | Embed an entire corpus in-place |
| `retrieve(query, corpus, top_k)` | Cosine-similarity retrieval |
| `augment_prompt(query, retrieved, template)` | Build RAG-augmented LLM prompt |
| `run_rag_pipeline(query, docs)` | End-to-end convenience wrapper |

## Quick Start

```python
from raw_materials.ai_rag.rag_core import run_rag_pipeline

result = run_rag_pipeline(
    query="What is the refund policy?",
    docs=["Our refund policy allows returns within 30 days...", "..."],
    top_k=3,
)
print(result["prompt"])
```

## Wiring into FastAPI

```python
from fastapi import FastAPI
from raw_materials.ai_rag.rag_core import run_rag_pipeline

app = FastAPI()

@app.post("/rag/query")
async def rag_query(query: str, docs: list[str]):
    return run_rag_pipeline(query, docs)
```

## Upgrading to Real Embeddings

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

No code changes required — the pipeline detects the key automatically.
