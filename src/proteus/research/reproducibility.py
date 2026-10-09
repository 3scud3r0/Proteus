"""Stable SHA-256 fingerprint of a JSON-compatible configuration."""
import hashlib
import json

def fingerprint(config: dict) -> str:
    return hashlib.sha256(json.dumps(config,sort_keys=True,separators=(",",":")).encode()).hexdigest()
