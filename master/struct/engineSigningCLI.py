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

if __name__ == "__main__":
    # Test stub trigger when run directly in your workflow file
    if REPO_GITHUB:
        #env_prefix = "SIGN_EXISTENZ_AUDIT_"
        #if "dist" in args.stage:
        #    env_prefix = "SIGN_EXISTENZ_DIST_"
        #elif "tools" in args.stage or "build" in args.stage:
        #    env_prefix = "SIGN_EXISTENZ_BUILD_"
        env_prefix = "SIGN_EXISTENZ_AUDIT_"
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
