# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76g | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

package existentialCores;
use strict;
use warnings;
use existentialCoreCheck;
use single::existentialCore;
if (!existentialCoreCheck::check_integrity($existentialCore::existentialCore{'CANARY_S_STATE'})) { die; }
1;
