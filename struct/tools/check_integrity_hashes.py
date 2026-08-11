#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (REPO tools / Check Hashes v0.76f)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: struct/tools/check_integrity_hashes.py
import hmac
import hashlib
import os
import sys

# 1. Locate the absolute repository root path on the remote virtual machine
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 2. Extract the direct path to your master blueprint folder
MASTER_PATH = os.path.join(REPO_ROOT, "struct", "master")

# 3. CRITICAL NAME-COLLISION FIX: Insert MASTER_PATH at position 0!
# This tells Python to prioritize looking for files inside your master/ directory
# BEFORE it scans any built-in system paths or name-blocked namespaces.
if MASTER_PATH not in sys.path:
    sys.path.insert(0, MASTER_PATH)

try:
    # We remove "struct.master." entirely from the import line.
    # Because master/ is now your primary search domain, Python directly links
    # to your neighbor file 'existentialCores.py' with zero conflicts.
    from existentialCores import (
        PLATFORM_ANCHOR_KEY, 
        SIGNATURE_CORE_EXISTENZ,
        existentialCore, 
        existentialCoreThreat
    )
except ImportError as e:
    print(f"[-] Execution Error: Missing structural components. {e}")
    sys.exit(1)

def verify_structural_hashes() -> bool:
    print("==================================================================")
    print("[*] LAUNCHING EXISTENZ INTEGRITY SCAN")
    print("==================================================================")
    
    # 1. Enforce strict matching on the multi-class layout sequence
    core_meanings = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCore.__members__.items()))
    threat_meanings = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()) if k != "THREAT_RIGHTS_LEGAL")
    
    fused_blueprint = f"{core_meanings}||{threat_meanings}"
    payload_bytes = fused_blueprint.encode('utf-8')
    
    # Compute the live HMAC of the code layouts using your master hardware anchor
    computed_hash = hmac.new(PLATFORM_ANCHOR_KEY, payload_bytes, hashlib.sha256).digest()
    live_token = computed_hash[:4].hex()
    
    print("[*] Stage 1: Evaluating core layout structure...")
    expected_core_link = hex(existentialCore.SIGN_CORES_CHAINED)[2:]
    
    if hmac.compare_digest(live_token, expected_core_link):
        print(f"  [+] Passed: Core blueprints match compiled chain token (0x{live_token}).")
    else:
        print("  [-] CRITICAL ALERT: Structural definition drift detected inside master files!")
        print(f"      Expected Anchor token : 0x{expected_core_link}")
        print(f"      Calculated from data   : 0x{live_token}")
        return False

    # 2. Enforce structural validation over the Threat Legal Map dictionary content
    print("[*] Stage 2: Evaluating forensic threat legal translation mapping...")
    serialized_map = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreat.THREAT_RIGHTS_LEGAL.items()))
    map_bytes = serialized_map.encode('utf-8')
    
    computed_map_hash = hmac.new(PLATFORM_ANCHOR_KEY, map_bytes, hashlib.sha256).digest()
    live_map_token = computed_map_hash[:4].hex()
    expected_map_link = hex(existentialCoreThreat.SIGN_THREAT_RIGHTS_LEGAL)[2:]
    
    if hmac.compare_digest(live_map_token, expected_map_link):
        print(f"  [+] Passed: Threat legal map matches compiled signature (0x{live_map_token}).")
    else:
        print("  [-] CRITICAL ALERT: Legal map dictionary modifications exposed!")
        print(f"      Expected Signature token: 0x{expected_map_link}")
        print(f"      Calculated from data     : 0x{live_map_token}")
        return False

    # 3. Verify validation against the file-global sequence signature
    print("[*] Stage 3: Auditing global signature string alignment...")
    if SIGNATURE_CORE_EXISTENZ.startswith(live_token):
        print("  [+] Passed: Global SIGNATURE_CORE_EXISTENZ string matches compiled components.")
    else:
        print("  [-] CRITICAL ALERT: Global signature variable string has been corrupted!")
        return False

    print("==================================================================")
    print("[+] SUCCESS: Cryptographic environment verified and locked.")
    return True

if __name__ == "__main__":
    secure = verify_structural_hashes()
    sys.exit(0 if secure else 1)

