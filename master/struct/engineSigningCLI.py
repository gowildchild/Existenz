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
import engineSigningLibrary

INT_VERSION = "v0.76.16"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)




def main():
    parser = argparse.ArgumentParser(description="Existenz SHA256 Manifest")
    parser.add_argument("-stage", "--stage", "-step", "--step", choices=["sign", "verify", "manifest"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-override", "--override", choices=["update", "recreate", "retry"], required=True, help="Manifest operation override.")
    parser.add_argument("-circle", "--circle", choices=["dist","tools","build","master","all"], default="all", help="Select circle")
    parser.add_argument("-bitmask","--bitmask", help="Select BitMask")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes.")
    parser.add_argument("-o", "--output", default=MANIFEST_OUTPUT, help="Path to your manifest file.")
    args = parser.parse_args()

    print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐")
    print(f"│ VisualMIX Signing CLI {INT_VERSION}     by Gunther Voet │")
    print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘")
    print(f"  [*] Operational: -stage {args.stage} -c {args.circle} -o {MANIFEST_OUTPUT}")

if __name__ == "__main__":
    # Test stub trigger when run directly in your workflow file
    if REPO_GITHUB:
        env_prefix = "SIGN_EXISTENZ_AUDIT_"
        if "dist" in args.stage:
            env_prefix = "SIGN_EXISTENZ_DIST_"
        elif "tools" in args.stage or "build" in args.stage:
            env_prefix = "SIGN_EXISTENZ_BUILD_"
        env_prefix = "SIGN_EXISTENZ_AUDIT_"

#        error_handler.notice(
#            level="info", 
#            message=f"Initializing environmental profile validation using prefix matching: [{env_prefix}]"
#        )
        
        env_agent = visualMixEngineEnvironment(
            post=env_prefix,
            conf=None
        )
#            namespace=f"EXISTENZ-{args.stage.upper()}"

        env_token_matrix = env_agent.load_secret_key()
        live_signing_key = env_token_matrix.get("_OBJECT")
        
    else:
        print("[!] Local execution skipped. This test routine targets GitHub Actions environment contexts.")
