# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76g | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

package existentialCoreCheck;
use single::existentialCore;
sub check_integrity { return $_ == $existentialCore::existentialCore{"CANARY_S_STATE"}; }
1;
