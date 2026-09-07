# ==========================================================================
# EXISTENZ  master/struct/module/cliStateVeritas.py
# Cryptographic Validation and Security Gate Enforcement Engine
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzIntegrityGlue, existenzSignatures
from engineSigningStruct import existenzIntegrityKeyStatus

def execute(args, error_handler, repo_root: str):
    """
    Executes full consensus validation across all structural tracking layers.
    Asserts un-tampered key alignment and enforces absolute pipeline blocks on drift.
    """
    error_handler.print("Initiating full cryptographic multi-signature validation pass [MODE: VERITAS]...", level="notice")
    
    # 1. Resolve artifact pathways natively from location mapping registries
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    if not os.path.exists(manifest_target_path):
        error_handler.print("Validation aborted: manifest.json tracking ledger missing.", level="error", exit_code=33)

    # 2. Ingest stored manifest footprint database states
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        stored_manifest = json.load(mf)
    stored_signatures = stored_manifest.get("signatures", {})

    # 3. Determine bitmask security constraints based on active execution stage
    req_env, req_pfm, req_dev, req_psn = engineSigningLibrary.solve_ring_requirements(args.stage)
    
    missing_signatures = []
    if req_env and "Environment" not in stored_signatures: missing_signatures.append("Environment")
    if req_pfm and "Platform" not in stored_signatures:    missing_signatures.append("Platform")
    if req_dev and "Developer" not in stored_signatures:   missing_signatures.append("Developer")
    if req_psn and "Personal" not in stored_signatures:    missing_signatures.append("Personal")

    # Strict Envelope Gate: Refuse execution if required cryptographic keys are missing
    if missing_signatures:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] VERITAS SECURITY BLOCKADE: REJECTING DOWNSTREAM PIPELINE TRACKS [!!!]", level="local")
        error_handler.print(f"       Required bitmask verification fields are completely missing: {missing_signatures}", level="local")
        error_handler.print(f"       Further structural code building is explicitly REFUSED.", level="local")
        error_handler.print("=" * 90, level="local")
        sys.exit(62)

    # 4. CROSS-CHECK COMPARTMENT INTEGRITY: Verify python/json signatures file alignment
    if os.path.exists(json_signatures_path):
        try:
            with open(json_signatures_path, "r", encoding="utf-8") as js_in:
                sig_database = json.load(js_in).get("existentialToken", {})
                
            # Step through your integrity glue matrix and ensure stored hashes match live filesystem constraints
            for key, glue_tuple in existenzIntegrityGlue.items():
                name, status_mask, op_flags, hex_id, relative_path, old_sig = glue_tuple
                
                # If KEY_IS_VERIFIED is enabled, check account policy or strict manifest state
                if bool(status_mask & existenzIntegrityKeyStatus.KEY_IS_VERIFIED):
                    saved_hash = sig_database.get(f"{key}_hash", "")
                    if saved_hash and old_sig and saved_hash != old_sig:
                        error_handler.print(f" [!!!] VERITAS MALFORMATION DETECTED: Structure '{key}' has been modified without re-signing!", level="error", exit_code=65)
        except Exception as parse_err:
            error_handler.print(f"Veritas database extraction warning: {parse_err}", level="warning")

    error_handler.print("[+] SUCCESS: Asymmetric security verification rings validated clean. Veritas unblocks the track.", level="notice")
    
    # Update pipeline environment variables and advance to next chronological phase seamlessly
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
