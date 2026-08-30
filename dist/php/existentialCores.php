<?php
// ==========================================================================
// EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
// Version: v0.76.15 | Github Deployment
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

namespace existentialCores;
use existentialCoreCheck\existentialCoreCheck;
use existentialCore\Layout;
function _execute_existenz_platform_autocheck() {
    if (!existentialCoreCheck::check_integrity(Layout::CANARY_S_STATE)) { exit(1); }
}
_execute_existenz_platform_autocheck();
