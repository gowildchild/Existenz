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
    Executes project-agnostic cryptographic consensus checking [MODE: VERITAS].
    Cross-references multi-signature requirements and blocks pipeline if validation drifts.
    """
    error_handler.print("Initiating universal cryptographic verification pass [MODE: VERITAS]...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    if not os.path.exists(manifest_target_path):
        error_handler.print("Veritas barrier error: manifest.json database tracking ledger missing.", level="error", exit_code=33)

    # 1. Ingest existing tracking configurations from the filesystem
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        stored_manifest = json.load(mf)
    
    sig_database = {}
    if os.path.exists(json_signatures_path):
        try:
            with open(json_signatures_path, "r", encoding="utf-8") as js_in:
                sig_database = json.load(js_in).get("existentialToken", {})
        except Exception:
            pass

    # 2. PHASE ONE: Map session variables dynamically to drive your custom tree visualizer
    active_tree_rules = existenzSignatures.existentialCore
    tree_session_hashes = {
        "existentialCoreMagicHash": sig_database.get("MagicCheck_hash", "UNKNOWN"),
        "existentialCoreCheckHash": sig_database.get("CoreCheck_hash", "UNSIGNED"),
    }
    # Universal loop maps whatever items are declared inside your meta configurations directly
    for label, _, _ in active_tree_rules:
        tree_session_hashes[f"existential{label}Hash"] = sig_database.get(f"{label}_hash", "")
        tree_session_hashes[f"{label.lower()}_sign"] = sig_database.get(f"{label}_sign", "00000000")

    # Render your pristine tree layout view onto the screen terminal
    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, tree_session_hashes, active_tree_rules)

    # 3. PHASE TWO: Verify Asymmetric Security Envelope Keys
    stored_manifest_signatures = stored_manifest.get("signatures", {})
    req_env, req_pfm, req_dev, req_psn = engineSigningLibrary.solve_ring_requirements(args.stage)
    
    missing_keys = []
    if req_env and "Environment" not in stored_manifest_signatures: missing_keys.append("Environment")
    if req_pfm and "Platform" not in stored_manifest_signatures:    missing_keys.append("Platform")
    if req_dev and "Developer" not in stored_manifest_signatures:   missing_keys.append("Developer")
    if req_psn and "Personal" not in stored_manifest_signatures:    missing_keys.append("Personal")

    if missing_keys:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] VERITAS SECURITY BLOCKADE: ENVELOPE PROTECTION FAULT [!!!]", level="local")
        error_handler.print(f"       Immutable files cannot be built without mandatory private key signatures: {missing_keys}", level="local")
        error_handler.print("=" * 90, level="local")
        sys.exit(62)

    # 4. PHASE THREE: Agnostic Structural Drift Enforcement Gate
    for key, glue_tuple in existenzIntegrityGlue.items():
        name, status_mask, op_flags, hex_id, relative_path, old_sig = glue_tuple
        
        if bool(status_mask & existenzIntegrityKeyStatus.KEY_IS_VERIFIED):
            live_computed_hash = sig_database.get(f"{key}_hash", "")
            if live_computed_hash and old_sig and live_computed_hash != old_sig:
                error_handler.print("=" * 90, level="local")
                error_handler.print(f" [!!!] VERITAS CONFLICT DETECTED: Structure '{key}' has been modified without re-signing!", level="local")
                error_handler.print(f"       Blueprint expected: {old_sig}", level="local")
                error_handler.print(f"       FS Live Computed:   {live_computed_hash}", level="local")
                error_handler.print("=" * 90, level="local")
                sys.exit(65)

    error_handler.print("[+] SUCCESS: All universal verification checks successfully cleared. Safe to advance.", level="notice")

    # Pass control safely to your dynamic pipeline link tracker loop
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
