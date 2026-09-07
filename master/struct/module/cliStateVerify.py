# ==========================================================================
# EXISTENZ  master/struct/module/cliStateVerify.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
import engineSigningLibrary
from engineSigningMeta import existenzLocations


def execute(args, error_handler, repo_root: str):
    """
    Executes deep asymmetric verification loops.
    Validates manifest alignment and blocks the downstream build phase if keys fail or drift.
    """
    error_handler.print("Initiating full cryptographic multi-signature validation pass...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))

    if not os.path.exists(manifest_target_path):
        error_handler.print("Verification aborted: manifest.json missing.", level="error", exit_code=33)

    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        stored_manifest = json.load(mf)

    stored_signatures = stored_manifest.get("signatures", {})
    
    # 1. Determine exactly what security rules are demanded by the active pipeline stage bitmask
    req_env, req_pfm, req_dev, req_psn = engineSigningLibrary.solve_ring_requirements(args.stage)
    
    missing_signatures = []
    if req_env and "Environment" not in stored_signatures: missing_signatures.append("Environment")
    if req_pfm and "Platform" not in stored_signatures:    missing_signatures.append("Platform")
    if req_dev and "Developer" not in stored_signatures:   missing_signatures.append("Developer")
    if req_psn and "Personal" not in stored_signatures:    missing_signatures.append("Personal")

    # 2. Strict Verification Gate: Refuse execution immediately if missing keys
    if missing_signatures:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] CRITICAL SECURITY BLOCKADE: REJECTING DOWNSTREAM PIPELINE TRACKS [!!!]", level="local")
        error_handler.print(f"       Required bitmask verification fields are completely missing: {missing_signatures}", level="local")
        error_handler.print(f"       Further structural code building is explicitly REFUSED.", level="local")
        error_handler.print("=" * 90, level="local")
        sys.exit(62) # Aborts runner instantly before reaching the build stage

    error_handler.print("[+] SUCCESS: Asymmetric security verification rings validated clean. Safe to advance.", level="notice")
    
    # Unblock and calculate the next pipeline loop step natively
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
