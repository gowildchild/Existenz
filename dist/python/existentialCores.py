# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
# Version: v0.76.15 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

import sys
from existentialCoreCheck import existentialCoreCheck, existentialCoreCheckVersion
from single.existentialCore import existentialCore
# UPDATED: Import the new shadow vacuum structure right into the runtime module
from single.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal, existentialCoreThreatShadowVacuum

def _execute_existenz_platform_autocheck():
    """Internal zero-trust gatekeeper. Automatically fires upon import."""
    if not existentialCoreCheck.check_integrity_legal():
        print("[-] CRITICAL ERROR: existentialCoreThreatLegal corruption detected!", file=sys.stderr)
        sys.exit(1)
        
    # NEW: Actively catch any runtime drift or corruption inside the shadow vacuum layers
    if hasattr(existentialCoreCheck, 'check_integrity_vacuum') and not existentialCoreCheck.check_integrity_vacuum():
        print("[-] CRITICAL ERROR: existentialCoreThreatShadowVacuum corruption detected!", file=sys.stderr)
        sys.exit(1)

    pristine_vector = existentialCore.CANARY_S_STATE
    if not existentialCoreCheck.check_integrity(pristine_vector):
        print("[-] CRITICAL ERROR: existentialCoreCheck issue detected!", file=sys.stderr)
        sys.exit(1)

_execute_existenz_platform_autocheck()
__all__ = ['existentialCore', 'existentialCoreThreat', 'existentialCoreThreatLegal', 'existentialCoreThreatShadowVacuum', 'existentialCoreCheck', 'existentialCoreCheckVersion']
