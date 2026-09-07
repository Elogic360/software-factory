"""
Universal Storage Backend — Reference Implementation
Software Factory Raw Material: storage

Abstract StorageBackend with LocalStorageBackend and S3StorageBackend
implementations. Factory function reads STORAGE_BACKEND env var.
"""
from __future__ import annotations
import abc
import io
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union


# ── Abstract Base ─────────────────────────────────────────────────────────────

class StorageBackend(abc.ABC):
    """Abstract storage backend. Implement upload/download/delete/list_keys."""

    @abc.abstractmethod
    def upload(self, key: str, data: Union[bytes, str, io.IOBase],
               metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Upload data to the given key. Returns upload metadata dict."""

    @abc.abstractmethod
    def download(self, key: str) -> bytes:
        """Download and return the raw bytes for a given key."""

    @abc.abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a key. Returns True on success, False if key did not exist."""

    @abc.abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """Return all keys starting with prefix."""

    def exists(self, key: str) -> bool:
        """Return True if key exists in storage."""
        return key in self.list_keys(prefix=key)

    def upload_text(self, key: str, text: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Convenience: upload a string as UTF-8 bytes."""
        return self.upload(key, text.encode(encoding))

    def download_text(self, key: str, encoding: str = "utf-8") -> str:
        """Convenience: download bytes and decode to string."""
        return self.download(key).decode(encoding)


# ── Local Filesystem ──────────────────────────────────────────────────────────

class LocalStorageBackend(StorageBackend):
    """
    Stores files in a local directory tree.
    Key maps to a relative file path: 'images/logo.png' → <base_dir>/images/logo.png
    """

    def __init__(self, base_dir: Union[str, Path] = "./storage_data"):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        # Sanitize key to prevent path traversal
        clean_key = key.lstrip("/").replace("..", "_")
        return self.base_dir / clean_key

    def upload(self, key: str, data: Union[bytes, str, io.IOBase],
               metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        target = self._path(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif isinstance(data, io.IOBase):
            data = data.read()
        target.write_bytes(data)
        stat = target.stat()
        return {"key": key, "size_bytes": stat.st_size, "backend": "local",
                "path": str(target)}

    def download(self, key: str) -> bytes:
        p = self._path(key)
        if not p.exists():
            raise FileNotFoundError(f"Key not found: {key}")
        return p.read_bytes()

    def delete(self, key: str) -> bool:
        p = self._path(key)
        if not p.exists():
            return False
        p.unlink()
        return True

    def list_keys(self, prefix: str = "") -> List[str]:
        results = []
        search_path = self._path(prefix) if prefix else self.base_dir
        if search_path.is_file():
            return [prefix]
        base = self.base_dir
        for f in base.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(base))
                if rel.startswith(prefix):
                    results.append(rel)
        return sorted(results)


# ── AWS S3 ────────────────────────────────────────────────────────────────────

class S3StorageBackend(StorageBackend):
    """
    AWS S3 storage backend using boto3.
    Reads credentials from env vars (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION) or from the standard ~/.aws/credentials file.
    """

    def __init__(self, bucket: Optional[str] = None, prefix: str = ""):
        self.bucket = bucket or os.environ.get("S3_BUCKET", "")
        self.prefix = prefix
        if not self.bucket:
            raise ValueError("S3_BUCKET env var or bucket parameter is required")
        try:
            import boto3  # type: ignore
            self._s3 = boto3.client("s3")
        except ImportError:
            raise ImportError("pip install boto3 to use S3StorageBackend")

    def _full_key(self, key: str) -> str:
        return f"{self.prefix}{key}" if self.prefix else key

    def upload(self, key: str, data: Union[bytes, str, io.IOBase],
               metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(data, bytes):
            data = io.BytesIO(data)
        extra_args: Dict[str, Any] = {}
        if metadata:
            extra_args["Metadata"] = metadata
        self._s3.upload_fileobj(data, self.bucket, self._full_key(key), ExtraArgs=extra_args or None)
        return {"key": key, "bucket": self.bucket, "backend": "s3"}

    def download(self, key: str) -> bytes:
        buf = io.BytesIO()
        self._s3.download_fileobj(self.bucket, self._full_key(key), buf)
        buf.seek(0)
        return buf.read()

    def delete(self, key: str) -> bool:
        try:
            self._s3.delete_object(Bucket=self.bucket, Key=self._full_key(key))
            return True
        except Exception:
            return False

    def list_keys(self, prefix: str = "") -> List[str]:
        full_prefix = self._full_key(prefix)
        paginator = self._s3.get_paginator("list_objects_v2")
        keys = []
        for page in paginator.paginate(Bucket=self.bucket, Prefix=full_prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if self.prefix:
                    key = key[len(self.prefix):]
                keys.append(key)
        return keys


# ── Factory Function ──────────────────────────────────────────────────────────

def get_backend(
    backend_type: Optional[str] = None,
    **kwargs: Any,
) -> StorageBackend:
    """
    Return a configured StorageBackend instance.
    Reads STORAGE_BACKEND env var ('local' or 's3'). Defaults to 'local'.

    Args:
        backend_type: 'local' or 's3' (overrides STORAGE_BACKEND env var)
        **kwargs: passed to the backend constructor

    Returns:
        StorageBackend instance

    Examples:
        get_backend()               # uses STORAGE_BACKEND env var
        get_backend('s3', bucket='my-bucket')
        get_backend('local', base_dir='/tmp/uploads')
    """
    backend = backend_type or os.environ.get("STORAGE_BACKEND", "local")
    if backend == "local":
        return LocalStorageBackend(**kwargs)
    elif backend == "s3":
        return S3StorageBackend(**kwargs)
    else:
        raise ValueError(f"Unknown STORAGE_BACKEND: {backend!r}. Choose 'local' or 's3'.")
