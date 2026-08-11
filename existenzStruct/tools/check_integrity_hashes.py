#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (REPO tools / Check Hashes v0.76g)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/check_integrity_hashes.py
#

# This is not needed anymore once the structure is 100% validated and immutable
# import boot_guard

import hmac
import hashlib
import os
import sys

# 1. Locate the absolute repository root path on the remote virtual machine
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 2. Inject the project workspace root into Python's top-level search path
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    # --- FIXED: ABSOLUTE NAMESPACE IMPORTS ROUTED CORRECTLY ---
    from existenzStruct.existentialCoreCheck import (
        existentialCoreCheckMagic, 
        existentialCoreCheckSignature
    )
    from existenzStruct.master.existentialCore import (
        existentialCore,
        existentialCoreSignature
    )
    from existenzStruct.master.existentialCoreThreat import (
        existentialCoreThreat,
        existentialCoreThreatSignature,
        existentialCoreThreatLegal
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
    threat_meanings = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()))
    
    fused_blueprint = f"{core_meanings}||{threat_meanings}"
    payload_bytes = fused_blueprint.encode('utf-8')
    
    # Compute the live HMAC of the code layouts using your master hardware anchor
    computed_hash = hmac.new(existentialCoreCheckMagic, payload_bytes, hashlib.sha256).digest()
    live_token = computed_hash[:4].hex()
    
    print("[*] Stage 1: Evaluating core layout structure...")
    expected_core_link = hex(existentialCoreSignature)[2:]
    
    if hmac.compare_digest(live_token, expected_core_link):
        print(f"  [+] Passed: Core blueprints match compiled chain token (0x{live_token}).")
    else:
        print("  [-] CRITICAL ALERT: Structural definition drift detected inside master files!")
        print(f"      Expected Anchor token : 0x{expected_core_link}")
        print(f"      Calculated from data   : 0x{live_token}")
        return False

    # 2. Enforce structural validation over the Threat Legal Map dictionary content
    print("[*] Stage 2: Evaluating forensic threat legal translation mapping...")
    serialized_map = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
    map_bytes = serialized_map.encode('utf-8')
    
    computed_map_hash = hmac.new(existentialCoreCheckMagic, map_bytes, hashlib.sha256).digest()
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
    if existentialCoreCheckSignature.startswith(live_token):
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
