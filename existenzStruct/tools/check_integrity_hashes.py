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
        existentialCoreThreatLegal,
        existentialCoreThreatSignatures 
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
    core_structure_signature = hmac.new(existentialCoreCheckMagic, core_structure_payload, hashlib.sha256).hexdigest()
    core_structure_sign = core_structure_signature[:8]
    
    # 2. MACHINE THREAT LAYER (The Attack Vectors & Canaries)
    threat_structure = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()))
    threat_structure_payload = threat_structure.encode('utf-8')
    threat_structure_signature = hmac.new(existentialCoreCheckMagic, threat_structure_payload, hashlib.sha256).hexdigest()
    threat_structure_sign = threat_structure_signature[:8]
    
    # 3. FORENSIC TRANSLATION LAYER (The International Human Rights Map)
    threat_legal_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
    threat_legal_structure_payload = threat_legal_structure.encode('utf-8')
    threat_legal_structure_signature = hmac.new(existentialCoreCheckMagic, threat_legal_structure_payload, hashlib.sha256).hexdigest()
    threat_legal_structure_sign = threat_legal_structure_signature[:8]

    # 4. UNIFIED THREAT STRUCTURES LAYER (Threat + Legal Fused Boundary Lock)
    threat_structures = f"{threat_structure}||{threat_legal_structure}"
    threat_structures_payload = threat_structures.encode('utf-8')
    threat_structures_signature = hmac.new(existentialCoreCheckMagic, threat_structures_payload, hashlib.sha256).hexdigest()
    threat_structures_sign = threat_structures_signature[:8]

    # 5. MASTER PLATFORM CHECK STRUCTURES LAYER (Core + Combined ThreatStructures)
    check_structures = f"{core_structure}||{threat_structures}"
    check_structures_payload = check_structures.encode('utf-8')
    check_structures_signature = hmac.new(existentialCoreCheckMagic, check_structures_payload, hashlib.sha256).hexdigest()
    check_structures_sign = check_structures_signature[:8]
    
    # --- DIAGNOSTIC LOGS ALIGNED TO YOUR EXACT VARIABLES ---
    print("[*] Stage 1: Evaluating core layout structure...")
    print("------------------------------------------------------------------")  
    print(f"  [>] existentialCoreCheckMagic        : {existentialCoreCheckMagic}")
    print(f"  [>] existentialCoreCheckSignature    : {existentialCoreCheckSignature}")
    print("------------------------------------------------------------------")
    print("[*] ANTI-COLLISION SUPPLY-CHAIN LOCKS COPY & PASTE INSTRUCTIONS:")
    print("------------------------------------------------------------------")
    print(f"  Inside existentialCore.py       -> existentialCoreSign = 0x{core_structure_sign}")
    print(f"                                  -> existentialCoreSignature = \"{core_structure_signature}\"")
    print(f"  Inside existentialCoreThreat.py ->- class existentialCoreThreatSignatures:")
    print(f"                                     -> existentialCoreThreatSign                = 0x{threat_structure_sign}")
    print(f"                                     -> existentialCoreThreatSignature           = \"{threat_structure_signature}\"")
    print(f"                                     -> existentialCoreThreatLegalSign           = 0x{threat_legal_structure_sign}")
    print(f"                                     -> existentialCoreThreatLegalSignature      = \"{threat_legal_structure_signature}\"")
    print(f"                                     -> existentialCoreThreatStructuresSign      = 0x{threat_structures_sign}")
    print(f"                                     -> existentialCoreThreatStructuresSignature = \"{threat_structures_signature}\"")
    print(f"  Inside existentialCoreCheck.py  -> existentialCoreCheckSign = 0x{check_structures_sign}")
    print(f"                                  -> existentialCoreCheckSignature = \"{existentialCoreCheckSignature}\"")
    print("==================================================================")
        
    validation_topology = (
        ("Core", core_structure_sign, core_structure_signature, existentialCoreSign, existentialCoreSignature),
        ("CoreThreat", threat_structure_sign, threat_structure_signature, existentialCoreThreatSignatures.existentialCoreThreatSign, existentialCoreThreatSignatures.existentialCoreThreatSignature),
        ("CoreThreatLegal", threat_legal_structure_sign, threat_legal_structure_signature, existentialCoreThreatSignatures.existentialCoreThreatLegalSign, existentialCoreThreatSignatures.existentialCoreThreatLegalSignature),
        ("CoreThreatStruct", threat_structures_sign, threat_structures_signature, existentialCoreThreatSignatures.existentialCoreThreatStructuresSign, existentialCoreThreatSignatures.existentialCoreThreatStructuresSignature)
    )

    for layer, live_sign, live_sig, frozen_sign, frozen_sig in validation_topology:
        # Tier A Verification: Fast-Path Short Anchor Check
        if not hmac.compare_digest(live_sign, hex(frozen_sign)[2:]):
            print(f"  [-] CRITICAL ALERT: {layer} short sign definition mismatch!")
            return False
        # Tier B Verification: Deep 256-Bit Anti-Tampering Firewall
        if not hmac.compare_digest(live_sig, frozen_sig):
            print(f"  [-] CRITICAL ALERT: {layer} structural collision attack or alteration detected!")
            return False
            
    print("  [+] Passed: Hierarchical fast-path and deep 256-bit locks verified clean.")

    # --- STAGE 2: SEQUENCE ALIGNMENT ---
    print("[*] Stage 2: Auditing global signature string alignment...")
    short_sign_hex = hex(existentialCoreCheckSign)[2:]
    
    # RULE 1: The Short Sign must be the EXACT tail of the Long Signature
    if not existentialCoreCheckSignature.endswith(short_sign_hex):
        print("  [-] CRITICAL ALERT: Architectural misalignment inside existentialCoreCheck.py!")
        print(f"      config Sign parameter (Tail) : {short_sign_hex}")
        print(f"      config Signature whole string: {existentialCoreCheckSignature}")
        print("      [!] Error: The Sign integer must match the literal end of the Signature string.")
        return False
        
    # RULE 2: The calculated live token from Stage 1 must match that exact tail
    if hmac.compare_digest(check_structures_sign, short_sign_hex):
        print(f"  [+] Passed: Unified sequence signature string verified clean (Tail: 0x{check_structures_sign}).")
    else:
        print("  [-] CRITICAL ALERT: Live layout tracking chain token drift exposed!")
        print(f"      Expected Suffix inside file  : {short_sign_hex}")
        print(f"      Calculated from live memory  : {check_structures_sign}")
        print(f"      [=] Action Required          : Update existentialCoreCheckSignature to end with '{check_structures_sign}'")
        return False

    # --- STAGE 3: SYMMETRY HANDSHAKE ---
    print("[*] Stage 3: Cross-examining three-way absolute system symmetry...")
    if hmac.compare_digest(check_structures_sign, hex(existentialCoreCheckSign)[2:]):
        print(f"  [+] Passed: 1:1 Symmetrical Handshake verified absolute (0x{check_structures_sign}).")
    else:
        print("  [-] CRITICAL ALERT: System desynchronization detected between core layers!")
        return False

    print("==================================================================")
    print("[+] SUCCESS: Cryptographic environment verified and locked.")
    return True

if __name__ == "__main__":
    secure = verify_structural_hashes()
    sys.exit(0 if secure else 1)
