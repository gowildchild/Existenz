# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED GENESIS INITIALIZATION & IMPORT HUB)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# FILE: struct/existentialCoreImport.py
#
import sys
from struct.master.existentialCore import existentialCore
from struct.master.existentialCoreThreat import existentialCoreThreat
from struct.existentialCoreCheck import existentialCoreCheck, PLATFORM_VERSION

# ==========================================================================
# AUTOMATED RUNTIME INITIALIZATION AUTO-CHECK
# ==========================================================================
def _execute_existenz_platform_autocheck():
    """
    Internal zero-trust gatekeeper. Automatically fires upon import.
    Verifies legal map integrity and validates the structural system vector.
    """
    # 1. Enforce Legal Map Translation Integrity (HMAC-SHA256 Anchor Check)
    if not existentialCoreCheck.check_integrity_legal():
        print(f"[-] CRITICAL ERROR: Threat Legal Map corruption detected in {PLATFORM_VERSION}!", file=sys.stderr)
        print("[-] Platform Initialization aborted to protect digital sanctuary.", file=sys.stderr)
        sys.exit(1)

    # 2. Enforce Main Core Environmental Integrity (Pillar and Collision Checks)
    # Evaluates against the ideal pristine system state constant (0x055005f7)
    pristine_vector = existentialCore.CANARY_S_STATE
    if not existentialCoreCheck.check_integrity(pristine_vector):
        print(f"[-] CRITICAL ERROR: Foundational Kernel or Checklist mismatch in {PLATFORM_VERSION}!", file=sys.stderr)
        print("[-] Memory boundaries or master XOR parity flags have drifted.", file=sys.stderr)
        sys.exit(1)

# Execute the zero-trust sentinel block immediately on module loading
_execute_existenz_platform_autocheck()

# ==========================================================================
# EXPLICIT CLEAN EXPOSURE INTERFACE FOR EXTERNAL PACKETS
# ==========================================================================
# External apps only need to import from this file to access the whole ecosystem safely
__all__ = [
    'existentialCore',
    'existentialCoreThreat',
    'existentialCoreCheck',
    'PLATFORM_VERSION'
]
