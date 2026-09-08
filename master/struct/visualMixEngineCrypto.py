# ========================================================================== 
# EXISTENZ master/struct/visualMixEngineCrypto.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# ==========================================================================
import os
import hashlib
import getpass
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

def load_private_key(identity: str, path: str, error_handler, repo_github: bool) -> ed25519.Ed25519PrivateKey:
    """Manages secure key disk fetching, interactive passphrase challenges, and parsing."""
    if repo_github:
        error_handler.notice(
            level="error",
            message="GitHub CI is not supposed to sign with a private key!",
            exit_code=4  # visualmixErrorHandler.ERR_MISSING_LOCAL
        )

    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        error_handler.notice(
            level="error",
            message=f"Key file missing at: {expanded_path}",
            exit_code=63  # visualmixErrorHandler.ERR_MISSING_KEY
        )

    with open(expanded_path, "rb") as k_file:
        key_data = k_file.read()

    try:
        return serialization.load_ssh_private_key(key_data, password=None)
    except Exception as e:
        err_str = str(e).lower()
        if any(w in err_str for w in ["password", "unsupported", "encrypted", "passphrase"]):
            error_handler.notice(
                level="local",
                message=f"[SECURITY] Private key for manifest identity '{identity}' is password-protected."
            )
            pwd = getpass.getpass(f"   Enter interactive pass-phrase for [{identity}]: ").encode('utf-8')
            try:
                return serialization.load_ssh_private_key(key_data, password=pwd)
            except Exception as e:
                error_handler.notice(
                    level="error",
                    message=f"Invalid password entry or corrupt key format: {e}",
                    exit_code=66  # visualmixErrorHandler.ERR_KEY_VALUE
                )
        else:
            error_handler.notice(
                level="error",
                message=f"Corrupt key format: {e}",
                exit_code=67  # visualmixErrorHandler.ERR_KEY_FORMAT
            )

def deserialize_ssh_private_key(key_bytes: bytes, password_bytes: bytes = None) -> ed25519.Ed25519PrivateKey:
    """Natively deserializes an OpenSSH private key asset using explicit password strings."""
    return serialization.load_ssh_private_key(key_bytes, password=password_bytes)
