# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76g | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

import sys
from existentialCoreCheck import existentialCoreCheck, existentialCoreCheckVersion
from single.existentialCore import existentialCore
from single.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal

def _execute_existenz_platform_autocheck():
    """Internal zero-trust gatekeeper. Automatically fires upon import."""
    if not existentialCoreCheck.check_integrity_legal():
        print("[-] CRITICAL ERROR: Threat Legal Map corruption detected!", file=sys.stderr)
        sys.exit(1)
    pristine_vector = existentialCore.CANARY_S_STATE
    if not existentialCoreCheck.check_integrity(pristine_vector):
        print("[-] CRITICAL ERROR: Foundational Kernel or Checklist mismatch!", file=sys.stderr)
        sys.exit(1)

_execute_existenz_platform_autocheck()
__all__ = ['existentialCore', 'existentialCoreThreat', 'existentialCoreCheck', 'existentialCoreCheckVersion']
