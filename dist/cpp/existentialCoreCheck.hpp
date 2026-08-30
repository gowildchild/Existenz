// ==========================================================================
// EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
// Version: v0.76.15 | Github Deployment
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

#pragma once
#include "single/existentialCore.hpp"
namespace existentialCoreCheck {
class existentialCoreCheck {
public:
    static bool check_integrity(unsigned long s) { return s == existentialCore::CANARY_S_STATE; }
};
}
