# ==========================================================================
# EXISTENZ  master/struct/engineSigningLibrary.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import visualMixEngineCrypto
import os
import sys
import json
import argparse
import hashlib
import getpass
import time
from enum import IntFlag
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from typing import Dict, Any

from engineSigningMeta import existenzLocations, existenzMeta
# Added missing existenzIntegrityKeyStatus registration dependency entry
from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeysHandler, existenzIntegrityKeyStatus
from existenzSignatures import existentialToken

from visualMixEngineLogging import visualmixErrorHandler

INT_VERSION = "v0.76.16"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Initialize global diagnostic loop interceptor
error_handler = visualmixErrorHandler(custom_post="_ERR")

def compute_sha256(file_path: str) -> str:
    """Redirects file streaming straight through your uniform crypto engine helper."""
    return visualMixEngineCrypto.calculate_file_sha256(file_path)


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
    """Invokes the consolidated global cryptography library handler."""
    return visualMixEngineCrypto.load_private_key(identity, path, error_handler, REPO_GITHUB)


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
        skeleton = {}  # Fixed critical missing dictionary variable instantiation

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

        # 4. Attempt Cryptographic instantiation checks via decoupled engine library
        try:
            pvt_bytes = raw_pvt_key.strip().encode('utf-8')
            parsed_private_key = visualMixEngineCrypto.deserialize_ssh_private_key(
                pvt_bytes,
                password_bytes=password_bytes
            )
            print("\033[1;32m  [+] Cryptographic Validation: Key parsing loop verified successfully!\033[0m")
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
        error_handler.notice(
            level="info", 
            message=f"engineSigningLibrary.py: [{REPO_GITHUB}]"
        )
                
    else:
        print("[!] Local execution skipped. This test routine targets GitHub Actions environment contexts.")
