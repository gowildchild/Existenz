#!/usr/bin/env bash
# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76g | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

source existentialCoreCheck.sh
if ! check_integrity "$existentialCore_CANARY_S_STATE"; then exit 1; fi
