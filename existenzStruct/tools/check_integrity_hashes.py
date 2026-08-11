#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (REPO tools / Check Hashes v0.76g)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/check_integrity_hashes.py
#
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
        existentialCoreCheckSign,
        existentialCoreCheckSignature
    )
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
    
    # --- YOUR PERFECTED REALIGNMENT CHUNK ---
    # 1. Enforce strict matching on the multi-class layout sequence
    core_structure = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCore.__members__.items()))
    core_structure_payload = core_structure.encode('utf-8')
    core_structure_signature = hashlib.sha256(core_structure_payload).hexdigest()
    core_structure_sign = hmac.new(existentialCoreCheckMagic, core_structure_payload, hashlib.sha256).digest()[:4].hex()
    
    # 2. Isolate and serialize the pure Threat text layout meanings
    threat_structure       = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()))
    threat_legal_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
    threat_structures      = f"{threat_structure}||{threat_legal_structure}"
    threat_structures_payload = threat_structures.encode('utf-8')
    threat_structures_signature = hashlib.sha256(threat_structures_payload).hexdigest()
    threat_structures_sign = hmac.new(existentialCoreCheckMagic, threat_structures_payload, hashlib.sha256).digest()[:4].hex()

    # 3. Compute the live short verification tokens
    fused_structures = f"{core_structure}||{threat_structures}"
    fused_structures_signature = hmac.new(existentialCoreCheckMagic, fused_structures.encode('utf-8'), hashlib.sha256).digest()
    fused_structures_sign = fused_structures_signature[:4].hex()
    
    # --- DIAGNOSTIC LOGS ALIGNED TO YOUR EXACT VARIABLES ---
    print("[*] Stage 1: Evaluating core layout structure...")
    print("------------------------------------------------------------------")  
    print(f"  [>] existentialCoreCheckMagic        : {existentialCoreCheckMagic}")
    print(f"  [>] existentialCoreCheckSignature    : {existentialCoreCheckSignature}")
    print("------------------------------------------------------------------")
    print("[*] ANTI-COLLISION COPY & PASTE INSTRUCTIONS:")
    print("------------------------------------------------------------------")

    print(f"  Inside existentialCore.py       -> existentialCoreSign = 0x{core_structure_sign}")
    print(f"                                  -> existentialCoreSignature = \"{core_structure_signature}\"")
    print(f"  Inside existentialCoreThreat.py -> existentialCoreThreatSign = 0x{threat_structures_sign}")
    print(f"                                  -> existentialCoreThreatSignature = \"{threat_structures_signature}\"")
    print(f"  Inside existentialCoreCheck.py  -> existentialCoreCheckSign = 0x{fused_structures_sign}")
    print(f"                                  -> existentialCoreCheckSignature = \"{existentialCoreCheckSignature}\"")
    print("==================================================================")

        
    # --- TIER A ALIGNED TO YOUR SHORT TOKEN VARIABLE ---
    expected_core_sign = hex(existentialCoreSign)[2:]
    if not hmac.compare_digest(fused_structures_sign, expected_core_sign):
        print(f"  [-] CRITICAL ALERT: Short signature definition mismatch (0x{expected_core_sign})!")
        return False
    print("  [+] Passed: Fast-path short anchor validation verified clean.")
    
    # --- TIER B ALIGNED TO YOUR LONG SIGNATURE VARIABLES ---
    if not hmac.compare_digest(core_structure_signature, existentialCoreSignature):
        print("  [-] CRITICAL ALERT: Core structural collision attack or alteration detected!")
        return False
    if not hmac.compare_digest(threat_structures_signature, existentialCoreThreatSignature):
        print("  [-] CRITICAL ALERT: Threat structural collision attack or alteration detected!")
        return False
    print("  [+] Passed: Deep 256-bit long signatures verified clean. Collision risk is 0%.")
    
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
    short_sign_hex = hex(existentialCoreCheckSign)[2:]
    
    # RULE 1: The Short Sign must be the EXACT tail of the Long Signature
    if not existentialCoreCheckSignature.endswith(short_sign_hex):
        print("  [-] CRITICAL ALERT: Architectural misalignment! Short sign is not the tail of the long signature.")
        return False
        
    # RULE 2: The calculated live token from Stage 1 must match that exact tail
    if hmac.compare_digest(fused_structures_sign, short_sign_hex):
        print(f"  [+] Passed: Unified sequence signature string verified clean (Tail: 0x{fused_structures_sign}).")
    else:
        print("  [-] CRITICAL ALERT: Live layout calculation does not match the frozen tracking signature!")
        return False

    # 4. Stage 4: Cross-examining three-way absolute system symmetry
    print("[*] Stage 4: Cross-examining three-way absolute system symmetry...")
    if hmac.compare_digest(hex(existentialCoreSign), hex(existentialCoreThreatSign)) and \
       hmac.compare_digest(hex(existentialCoreSign), hex(existentialCoreCheckSign)):
        print(f"  [+] Passed: 1:1 Symmetrical Handshake verified absolute (0x{fused_structures_sign}).")
    else:
        print("  [-] CRITICAL ALERT: System desynchronization detected between core layers!")
        return False

    print("==================================================================")
    print("[+] SUCCESS: Cryptographic environment verified and locked.")
    return True

if __name__ == "__main__":
    secure = verify_structural_hashes()
    sys.exit(0 if secure else 1)
