// ==========================================================================
// EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
// Version: v0.76.15 | Github Deployment
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

#pragma once
#include <cstdlib>
#include "existentialCoreCheck.hpp"
namespace existentialCores {
    inline void _execute_existenz_platform_autocheck() {
        if (!existentialCoreCheck::existentialCoreCheck::check_integrity(existentialCore::CANARY_S_STATE)) { std::exit(1); }
    }
    struct AutoRun { AutoRun() { _execute_existenz_platform_autocheck(); } };
    static AutoRun __injector;
}
