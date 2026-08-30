#!/usr/bin/env bash
# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
# Version: v0.76.15 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

source existentialCoreCheck.sh
if ! check_integrity "$existentialCore_CANARY_S_STATE"; then exit 1; fi
