# Raw Material: Universal Storage Backend

**Category:** Infrastructure | **Status:** REFERENCE | **Language:** Python

## What This Provides

An abstract `StorageBackend` interface with two concrete implementations:

- **`LocalStorageBackend`** — stores files in a local directory tree. No dependencies.
- **`S3StorageBackend`** — wraps boto3 for AWS S3. Requires `pip install boto3`.

A `get_backend()` factory function selects the backend from `STORAGE_BACKEND` env var.

## Key Interface

```python
backend = get_backend()

backend.upload("images/logo.png", open("logo.png", "rb"))
data = backend.download("images/logo.png")
backend.delete("images/logo.png")
keys = backend.list_keys(prefix="images/")
backend.upload_text("docs/readme.md", "# Hello")
text = backend.download_text("docs/readme.md")
```

## Switching Backends

```bash
# Local (default — no setup required)
STORAGE_BACKEND=local

# AWS S3
STORAGE_BACKEND=s3
S3_BUCKET=my-project-bucket
AWS_DEFAULT_REGION=us-east-1
```

## Wiring into FastAPI

```python
from fastapi import FastAPI, UploadFile
from raw_materials.storage.storage_core import get_backend

app = FastAPI()
storage = get_backend()

@app.post("/upload/{key:path}")
async def upload(key: str, file: UploadFile):
    content = await file.read()
    result = storage.upload(key, content)
    return result
```

## Testing with Local Backend

```python
from raw_materials.storage.storage_core import LocalStorageBackend

backend = LocalStorageBackend(base_dir="/tmp/test_storage")
backend.upload_text("test/hello.txt", "Hello World")
assert backend.download_text("test/hello.txt") == "Hello World"
assert "test/hello.txt" in backend.list_keys("test/")
backend.delete("test/hello.txt")
```
