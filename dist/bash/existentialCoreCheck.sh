#!/usr/bin/env bash
# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
# Version: v0.76.15 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

source single/existentialCore.sh
check_integrity() { [[ "$1" -eq "$existentialCore_CANARY_S_STATE" ]]; }
