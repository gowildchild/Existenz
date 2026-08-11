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
    from existenzStruct.existentialCoreCheck import (
        existentialCoreCheckMagic, 
        existentialCoreCheckSignature
    )
    # --- FIXED: ADDED THE MISSING SIGN/SIGNATURE HOOK VARIABLES HERE ---
    from existenzStruct.master.existentialCore import (
        existentialCore,
        existentialCoreSign,
        existentialCoreSignature
    )
    from existenzStruct.master.existentialCoreThreat import (
        existentialCoreThreat, 
        existentialCoreThreatSign,
        existentialCoreThreatSignature, 
        existentialCoreThreatLegal
    )
    
except ImportError as e:
    print(f"[-] Execution Error: Missing structural components. {e}")
    sys.exit(1)

def verify_structural_hashes() -> bool:
    print("==================================================================")
    print("[*] ExistenzIntegrityScan v0.76g")
    print("==================================================================")
    
    # 1. Enforce strict matching on the multi-class layout sequence
    core_meanings = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCore.__members__.items()))
    threat_meanings = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()))
    
    fused_blueprint = f"{core_meanings}||{threat_meanings}"
    payload_bytes = fused_blueprint.encode('utf-8')
    
    # Compute the live HMAC of the code layouts using your master hardware anchor
    computed_hash = hmac.new(existentialCoreCheckMagic, payload_bytes, hashlib.sha256).digest()
    live_short_token = computed_hash[:4].hex()
    live_long_signature = hashlib.sha256(payload_bytes).hexdigest()
    
    print("[*] Stage 1: Evaluating core layout structure...")
    print(f"  [>] Calculated Short Token  : 0x{live_short_token}")
    print(f"  [>] Calculated Long Ledger  : {live_long_signature}")
    print("------------------------------------------------------------------")
    print("[*] FORENSIC COPY & PASTE CONFIGURATION BLOCKS:")
    print("------------------------------------------------------------------")
    print(f"  Inside existentialCore.py       -> existentialCoreSign = 0x{live_short_token}")
    print(f"  Inside existentialCore.py       -> existentialCoreSignature = \"{live_long_signature}\"")
    print(f"  Inside existentialCoreThreat.py -> existentialCoreThreatSign = 0x{live_short_token}")
    print(f"  Inside existentialCoreThreat.py -> existentialCoreThreatSignature = \"{live_long_signature}\"")
    print(f"  Inside existentialCoreCheck.py  -> existentialCoreCheckSignature = \"5beba3df6d44968d18641470c01eca1e{live_short_token}\"")
    print("==================================================================")
        
    expected_core_sign = hex(existentialCoreSign)[2:]
    if not hmac.compare_digest(live_short_token, expected_core_sign):
        print(f"  [-] CRITICAL ALERT: Short signature definition mismatch (0x{expected_core_sign})!")
        return False
    print("  [+] Passed: Fast-path short anchor validation verified clean.")
    
    # Tier B Verification: 256-bit collision firewall check
    if not hmac.compare_digest(live_long_signature, existentialCoreSignature):
        print("  [-] CRITICAL ALERT: Brute-force structural collision attack or alteration detected!")
        print(f"      Expected Long Ledger: {existentialCoreSignature}")
        print(f"      Calculated Live data: {live_long_signature}")
        return False
    print("  [+] Passed: Deep 256-bit long ledger identity verified clean. Collision risk is 0%.")
    
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
        return False

    # 3. Verify validation against the file-global sequence signature strings
    print("[*] Stage 3: Auditing global signature string alignment...")
    if existentialCoreCheckSignature.startswith(live_short_token) or existentialCoreCheckSignature.endswith(live_short_token):
        print("  [+] Passed: Global configuration signature verification clean.")
    else:
        print("  [-] CRITICAL ALERT: Global signature variable string has been corrupted or spoofed!")
        return False

    print("==================================================================")
    print("[+] SUCCESS: Cryptographic environment verified and locked.")
    return True

if __name__ == "__main__":
    secure = verify_structural_hashes()
    sys.exit(0 if secure else 1)
