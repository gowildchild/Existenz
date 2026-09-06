# ==========================================================================
# EXISTENZ master/struct/visualMixEngineCrypto.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# ==========================================================================
import os
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def calculate_sha256(data: bytes) -> str:
    """Calculates the absolute SHA256 checksum string for raw binary blocks."""
    return hashlib.sha256(data).hexdigest()

def calculate_file_sha256(file_path: str) -> str:
    """Safely streams a file from disk to generate a uniform SHA256 signature."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def calculate_md5(data: bytes) -> str:
    """Calculates the absolute MD5 checksum string for raw binary blocks."""
    return hashlib.md5(data).hexdigest()

def calculate_file_md5(file_path: str) -> str:
    """Calculates a deterministic 7-character MD5 hash of any target disk asset."""
    try:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()[:7]
    except Exception:
        return "ERROR"

def deserialize_ssh_private_key(key_bytes: bytes, password_bytes: bytes = None) -> ed25519.Ed25519PrivateKey:
    """Natively deserializes an OpenSSH private key asset using explicit password strings."""
    return serialization.load_ssh_private_key(key_bytes, password=password_bytes)
