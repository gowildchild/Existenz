# ==========================================================================
# EXISTENZ  master/struct/engineSigningLibrary.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

import os
import sys
import json
import argparse
import hashlib
import getpass
from enum import IntFlag
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from typing import Dict, Any

from engineSigningMeta import existenzLocations, existenzMeta
from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeysHandler
from existenzSignatures import existentialToken

INT_VERSION = "v0.76.16"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class visualmixErrorHandler:
    """Handles script termination and formats logs cleanly for both Local and GitHub environments."""
    ERR_GENERAL          = 1
    ERR_ARGPARSE         = 2
    ERR_MISSING_CORE     = 4
    ERR_MISSING_LOCAL    = 8
    ERR_MISSING_CONFIG   = 16
    ERR_MISSING_FILE     = 32
    ERR_MISSING_MANIFEST = 33
    ERR_MISSING_SIGN     = 62
    ERR_MISSING_KEY      = 63
    ERR_KEY              = 64
    ERR_KEY_DRIFTING     = 65
    ERR_KEY_VALUE        = 66
    ERR_KEY_FORMAT       = 67
    ERR_KEY_EXCEPTION    = 68
    ERR_MISSING_EXECUTE  = 126
    ERR_MISSING_EXE      = 127
    ERR_UNKNOWN          = 254
    ERR_OUT_OF_RANGE     = 255
    
    ERR_MAP = {
        "error":   ("\033[1;31m[!] ERROR",   "::error", True),
        "warning": ("\033[1;33m[?] Warning", "::warning", True),
        "notice":  ("\033[1;36m[+] Notice",  "::notice", True),
        "debug":   ("\033[1;35m[-] Debug",   "::debug", True),
        "info":    ("\033[0;37m[ ] Info",    "  Info", True),
        "local":   ("\033[0;37m[ ] Local",   "", False)
    }
    
    def notice(self, level: str, message: str, exit_code: int = None, details: list = None):
        """Centralized logging method handling level logic and custom error codes."""
        notice_style, notice_github, notice_github_allowed = self.ERR_MAP.get(level, self.ERR_MAP["info"])
        if REPO_GITHUB:
            indent = " " * (len(level) + 2)
            if not notice_github_allowed:
                return

            no_details = level in ["info", "debug"] or not exit_code
            meta = "" if no_details else f" file=core_manifest.py::[Exit Code {exit_code}]"
            print(f"{notice_github}{meta}::{message}")
            if details:
                for line in details:
                    print(f"{indent}{line}")
        else:
            indent = " " * 10
            # FIXED: Wrapped in safe getter dict transformation to prevent lookup KeyErrors on arbitrary exit codes
            valid_err = {v: k for k, v in vars(self.__class__).items() if k.startswith("ERR_") and isinstance(v, int)}
            
            if exit_code:
                err_label = valid_err.get(exit_code, "ERR_UNKNOWN")
                full_err = f"{notice_style}_{err_label} ({exit_code})"
            else:
                full_err = f"{notice_style}"
                
            print(f"  {full_err}: {message}\033[0m")
            if details:
                for line in details:
                    print(f"{indent}{line}")

        if exit_code is not None:
            sys.exit(exit_code)

error_handler = visualmixErrorHandler()


def compute_sha256(file_path: str) -> str:
    """Computes a strict binary SHA-256 hash of a target file asset."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def gather_folder_files(folder_relative_path: str) -> dict:
    """Traverses a single target folder recursively to catalog all available file hashes."""
    file_matrix = {}
    full_folder_path = os.path.join(REPO_ROOT, folder_relative_path)

    if not os.path.exists(full_folder_path):
        return file_matrix

    for root, _, files in os.walk(full_folder_path):
        if "__pycache__" in root:
            continue

        for file in files:
            if file == "manifest.json" or file.endswith(".pyc"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, REPO_ROOT)
            rel_path = rel_path.replace("\\", "/")
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix


def load_private_key(identity: str, path: str) -> ed25519.Ed25519PrivateKey:
    """Natively reads an asymmetric OpenSSH private key, capturing password requirements explicitly."""
    if REPO_GITHUB:
        error_handler.notice(
            level="error",
            message="GitHub CI is not supposed to sign with a private key!",
            exit_code=visualmixErrorHandler.ERR_MISSING_LOCAL
        )

    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        error_handler.notice(
            level="error",
            message=f"Key file missing at: {expanded_path}",
            exit_code=visualmixErrorHandler.ERR_MISSING_KEY
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
                    exit_code=visualmixErrorHandler.ERR_KEY_VALUE
                )
        else:
            error_handler.notice(
                level="error",
                message=f"Corrupt key format: {e}",
                exit_code=visualmixErrorHandler.ERR_KEY_FORMAT
            )


def solve_ring_requirements(stage: str) -> tuple:
    """
    BITWISE ROUTINE ROUTER: Uses IntFlag bitmask matching to verify which keys are needed.
    Returns: (requires_platform, requires_developer, requires_personal)
    """
    # 1. Determine base existenzIntegrityKeysHandler ring weight
    ring_weight = existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT
    if "master" in stage:
        ring_weight = existenzIntegrityKeyStatus.KEY_PVT_PERSONAL
    elif "tools" in stage or "build" in stage:
        ring_weight = existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER

    platform_flag  = existenzIntegrityKeyStatus.SIGN_PVT_PLATFORM
    developer_flag = existenzIntegrityKeyStatus.SIGN_PVT_DEVELOPER
    personal_flag  = existenzIntegrityKeyStatus.SIGN_PVT_PERSONAL

    return (
        bool(ring_weight & platform_flag),
        bool(ring_weight & developer_flag),
        bool(ring_weight & personal_flag)
    )

class visualMixEngineEnvironment:
    def __init__(self, post:str="SIGN_EXISTENZ_AUDIT_", conf: Dict[str, Any] = None, namespace="visualMix"):
        self.post   = post
        self.conf   = conf or {}
        self.namespace = namespace

    def load_secret_key(self) -> Dict[str, Any]:
        """Loads file configurations smoothly matching extensions."""

        keys_pub = ["PUBLIC","FINGERPRINT"]
        keys_pvt = ["PRIVATE","PHRASE"]

        for key in (keys_pvt + keys_pub):
            conf_key = f"{self.post}{key.capitalize()}"
            env_key  = f"{self.post}{key}"

            if key == "FINGERPRINT":
	            env_fallback_value = os.environ.get(env_key, os.environ.get(f"{self.post}FINGERPRINT"))
            else:
                env_fallback_value = os.environ.get(env_key)
        
            skeleton[env_key] = self.conf.get(conf_key, env_fallback_value)


        time_key = f"{self.post}TIME"
        skeleton[time_key] = self.conf.get(time_key, os.environ.get(time_key, int(time.time())))
        
        raw_pvt_key = skeleton.get(f"{self.post}PRIVATE")
        env_pub_key = skeleton.get(f"{self.post}PUBLIC")
        env_finger  = skeleton.get(f"{self.post}FINGERPRINT")
        raw_phrase  = skeleton.get(f"{self.post}PHRASE")

        missing_fields = []
        if not raw_pvt_key: 
            missing_fields.append(f"{self.post}PRIVATE")
        if not env_pub_key: 
            missing_fields.append(f"{self.post}PUBLIC")
        if not env_finger:  
            missing_fields.append(f"{self.post}FINGERPRINT")
        
        if missing_fields:
            error_handler.notice(
                level="error",
                message=f"Loop-driven environment validation failed. Unresolved tracks: {missing_fields}",
                exit_code=visualmixErrorHandler.ERR_MISSING_KEY
            )

        clean_pub_display = env_pub_key.strip().split()[-1] if len(env_pub_key.strip().split()) > 1 else 'Custom Format'
        print(f"  [+] Ingest Namespace:      '{self.namespace}' Loop-Driven Tracker Block")
        print(f"  [+] Ingested Public Key:   '{clean_pub_display}'")
        print(f"  [+] Ingested Fingerprint:  {env_finger.strip()}")
        print(f"  [+] Private Key Payload:   Loaded ({len(raw_pvt_key.strip())} characters)")

        # 3. Handle asymmetric password protection mechanics
        password_bytes = None
        if raw_phrase and str(raw_phrase).strip():
            print(f"  [+] Key Protection State:  Encrypted passphrase token active")
            password_bytes = str(raw_phrase).strip().encode('utf-8')
        else:
            print(f"  [ ] Key Protection State:  Assuming plaintext unencrypted asset format")

        # 4. Attempt Cryptographic instantiation checks
        try:
            pvt_bytes = raw_pvt_key.strip().encode('utf-8')
            parsed_private_key = serialization.load_ssh_private_key(
                pvt_bytes,
                password=password_bytes
            )
            print("\033[1;32m  [+] Cryptographic Validation: Key parsing loop verified successfully!\033[0m")
            
            # Pass the running key pointer directly out of the tracking block safely
            skeleton["_OBJECT"] = parsed_private_key
            
        except Exception as crypto_fault:
            error_handler.notice(
                level="error",
                message=f"Failed to instantiate environment key: {crypto_fault}",
                exit_code=visualmixErrorHandler.ERR_KEY_FORMAT
            )

        return skeleton



if __name__ == "__main__":
    # Test stub trigger when run directly in your workflow file
    if REPO_GITHUB:
        env_prefix = "SIGN_EXISTENZ_AUDIT_"
        if "dist" in args.stage:
            env_prefix = "SIGN_EXISTENZ_DIST_"
        elif "tools" in args.stage or "build" in args.stage:
            env_prefix = "SIGN_EXISTENZ_BUILD_"

        error_handler.notice(
            level="info", 
            message=f"Initializing environmental profile validation using prefix matching: [{env_prefix}]"
        )
        
        env_agent = visualMixEngineEnvironment(
            post=env_prefix,
            conf=None, 
            namespace=f"EXISTENZ-{args.stage.upper()}"
        )

        env_token_matrix = env_agent.load_secret_key()
        live_signing_key = env_token_matrix.get("_OBJECT")
        
    else:
        print("[!] Local execution skipped. This test routine targets GitHub Actions environment contexts.")
