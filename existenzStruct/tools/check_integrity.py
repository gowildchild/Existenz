#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (REPO tools / Check Hashes v0.76i)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/check_integrity.py
#
import hmac
import hashlib
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
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
        existentialCoreThreatShadowVacuum,
        existentialCoreThreatSignatures 
    )
except ImportError as e:
    print(f"[-] Execution Error: Missing structural components. {e}")
    sys.exit(1)

def verify_structural_hashes() -> bool:
    print("ExistenzIntegrityScan v0.76g")
    print("==================================================================")

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
    
    # 3a. FORENSIC TRANSLATION LAYER (The International Human Rights Map)
    threat_legal_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
    threat_legal_structure_payload = threat_legal_structure.encode('utf-8')
    threat_legal_structure_signature = hmac.new(existentialCoreCheckMagic, threat_legal_structure_payload, hashlib.sha256).hexdigest()
    threat_legal_structure_sign = threat_legal_structure_signature[:8]

    # 3b. FORENSIC TRANSLATION LAYER (The International Human Rights Map)
    threat_shadow_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatShadowVacuum.items()))
    threat_shadow_structure_payload = threat_shadow_structure.encode('utf-8')
    threat_shadow_structure_signature = hmac.new(existentialCoreCheckMagic, threat_shadow_structure_payload, hashlib.sha256).hexdigest()
    threat_shadow_structure_sign = threat_shadow_structure_signature[:8]    

    # 4. UNIFIED THREAT STRUCTURES LAYER (Threat + Legal Fused Boundary Lock)
    threat_structures = f"{threat_structure}||{threat_legal_structure}||{threat_shadow_structure}"
    threat_structures_payload = threat_structures.encode('utf-8')
    threat_structures_signature = hmac.new(existentialCoreCheckMagic, threat_structures_payload, hashlib.sha256).hexdigest()
    threat_structures_sign = threat_structures_signature[:8]

    # 5. MASTER PLATFORM CHECK STRUCTURES LAYER (Core + Combined ThreatStructures)
    check_structures = f"{core_structure}||{threat_structures}||{threat_shadow_structure}"
    check_structures_payload = check_structures.encode('utf-8')
    check_structures_signature = hmac.new(existentialCoreCheckMagic, check_structures_payload, hashlib.sha256).hexdigest()
    check_structures_sign = check_structures_signature[:8]
    
    print("[*] Stage 1: Evaluating core structure...")
    print("─" * 80)
    print(f"  [>] existentialCoreCheckMagic        : {existentialCoreCheckMagic}")
    print(f"  [>] existentialCoreCheckSignature    : {existentialCoreCheckSignature}")
    print("──┬ [ inside ] ───────────────────────────────────────────────────")
    print(f"  ├── existentialCore.py        ─┬─► existentialCoreSign                      = 0x{core_structure_sign}")
    print(f"  │                              └─► existentialCoreSignature                 = \"{core_structure_signature}\"")
    print(f"  ├── existentialCoreThreat.py ─┬► class existentialCoreThreatSignatures:")
    print(f"  │                             ├──► existentialCoreThreatSign                = 0x{threat_structure_sign}")
    print(f"  │                             ├──► existentialCoreThreatSignature           = \"{threat_structure_signature}\"")
    print(f"  │                             ├──► existentialCoreThreatLegalSign           = 0x{threat_legal_structure_sign}")
    print(f"  │                             ├──► existentialCoreThreatLegalSignature      = \"{threat_legal_structure_signature}\"")
    print(f"  │                             ├──► existentialCoreThreatShadowVacuumSign    = 0x{threat_shadow_structure_sign}")
    print(f"  │                             ├──► existentialCoreThreatShadowV..Signature  = \"{threat_shadow_structure_signature}\"")    
    print(f"  │                             ├──► existentialCoreThreatStructuresSign      = 0x{threat_structures_sign}")
    print(f"  │                             └──► existentialCoreThreatStructuresSignature = \"{threat_structures_signature}\"")
    print(f"  └── existentialCoreCheck.py   ─┬─► existentialCoreCheckSign                 = 0x{check_structures_sign}")
    print(f"                                 └─► existentialCoreCheckSignature            = \"{check_structures_signature}\"")
    print("==================================================================")

    master_system_anchor = f"{existentialCoreCheckSign:08x}"
    
    validation_topology = (
        ("Core",             core_structure_sign, core_structure_signature,   f"{existentialCoreSign:08x}", existentialCoreSignature),
        ("CoreThreat",       threat_structure_sign, threat_structure_signature, f"{existentialCoreThreatSignatures.existentialCoreThreatSign:08x}", existentialCoreThreatSignatures.existentialCoreThreatSignature),
        ("CoreThreatLegal",  threat_legal_structure_sign, threat_legal_structure_signature, f"{existentialCoreThreatSignatures.existentialCoreThreatLegalSign:08x}", existentialCoreThreatSignatures.existentialCoreThreatLegalSignature),
        ("CoreThreatShadow", threat_shadow_structure_sign, threat_shadow_structure_signature, f"{existentialCoreThreatSignatures.existentialCoreThreatShadowVacuumSign:08x}", existentialCoreThreatSignatures.existentialCoreThreatShadowVacuumSignature),
        ("CoreThreatStruct", threat_structures_sign, threat_structures_signature, f"{existentialCoreThreatSignatures.existentialCoreThreatStructuresSign:08x}", existentialCoreThreatSignatures.existentialCoreThreatStructuresSignature),
        ("CoreCheck",        check_structures_sign, check_structures_signature, master_system_anchor, existentialCoreCheckSignature)
    )

    for layer, live_sign, live_sig, frozen_sign_str, frozen_sig in validation_topology:
        # Tier A Verification: Fast-Path Short Anchor Check
        if not hmac.compare_digest(live_sign, frozen_sign_str):
            print(f"  [-] CRITICAL ALERT: {layer} short sign definition mismatch!")
            print(f"      Expected inside code: 0x{frozen_sign_str}")
            print(f"      Live calculated data: 0x{live_sign}")
            return False
            
        # Tier B Verification: Deep 256-Bit Anti-Tampering Firewall
        if not hmac.compare_digest(live_sig, frozen_sig):
            print(f"  [-] CRITICAL ALERT: {layer} structural alteration or code injection exposed!")
            print(f"      Expected inside code: \"{frozen_sig}\"")
            print(f"      Live calculated data: \"{live_sig}\"")
            return False

    if not hmac.compare_digest(check_structures_sign, master_system_anchor):
        print("  [-] CRITICAL ALERT: Global system desynchronization / alignment failure exposed!")
        print(f"      Master Check Anchor : 0x{master_system_anchor}")
        print(f"      Live platform state : 0x{check_structures_sign}")
        return False
            
    print("  [+] Passed: Symmetrical fast-path, prefix alignment, and deep 256-bit locks verified clean.")
    print("==================================================================")
    print("[+] SUCCESS: Cryptographic environment verified and locked.")
    return True


if __name__ == "__main__":
    secure = verify_structural_hashes()
    sys.exit(0 if secure else 1)

