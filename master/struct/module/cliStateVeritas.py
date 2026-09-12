# ==========================================================================
# EXISTENZ  master/struct/module/cliStateVeritas.py
# Cryptographic Validation and Security Gate Enforcement Engine
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzConfig, existenzPublicKeys

def execute(args, error_handler, repo_root: str):
    """
    Executes project-agnostic cryptographic consensus checking [MODE: VERITAS].
    Supports composite workspace checks via circle='all' to prevent value dropouts.
    """
    error_handler.print("Initiating universal cryptographic verification pass [MODE: VERITAS]...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    if not os.path.exists(manifest_target_path):
        error_handler.print("Veritas barrier error: manifest.json database tracking ledger missing.", level="error", exit_code=33)

    # Ingest existing tracking configurations from the filesystem
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)
    stored_manifest_signatures = manifest_data.get("signatures", {})

    # Import structural matrices directly from your active integrity tables
    from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeyStatus

    circle_to_glue_map = {
        "dist":   "CircleDist",
        "tools":  "CircleTools",
        "build":  "CircleBuild",
        "master": "CircleMaster"
    }

    active_circle_arg = str(args.circle).strip().lower()
    
    # FIXED: Support composite workspace checks by dynamically looping over all active rings sequentially
    if active_circle_arg == "all":
        circles_to_verify = ["dist", "tools", "build", "master"]
    else:
        circles_to_verify = [active_circle_arg]

    # ==========================================================================
    # PHASE 1: LOOP-DRIVEN CONSENSUS CHECK FOR DESIGNATED TRACKS
    # ==========================================================================
    for current_circle in circles_to_verify:
        glue_key = circle_to_glue_map.get(current_circle)
        if not glue_key or glue_key not in existenzIntegrityGlue:
            error_handler.print(f"Veritas aborted: unresolved circle target: {current_circle}", level="error", exit_code=34)

        # FIXED: Extract the raw bitmask integer weight precisely from index 1 of the metadata tuple configuration
        circle_bitmask_weight = existenzIntegrityGlue[glue_key][1]

        # FIXED: Cleared out the duplicated string syntax fragment
        req_env = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT)
        req_pfm = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM)
        req_dev = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
        req_psn = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)


        missing_keys = []
        if req_env and "Environment" not in stored_manifest_signatures: missing_keys.append("Environment")
        if req_pfm and "Platform" not in stored_manifest_signatures:    missing_keys.append("Platform")
        if req_dev and "Developer" not in stored_manifest_signatures:   missing_keys.append("Developer")
        if req_psn and "Personal" not in stored_manifest_signatures:    missing_keys.append("Personal")

        if missing_keys:
            error_handler.print("=" * 90, level="local")
            error_handler.print(f" [!!!] VERITAS SECURITY GUARD FAULT: REJECTING downstream BUILD [!!!]", level="local")
            error_handler.print(f"       Circle Ring [{current_circle.upper()}] requires missing private signatures: {missing_keys}", level="local")
            error_handler.print(f"       Further cross-language artifact building is explicitly BLOCKED.", level="local")
            error_handler.print("=" * 90, level="local")
            sys.exit(62)

        # 2. VERIFY DATA CONTINUITY (LIVE CRAWL VS SIGNED MANIFEST ENVELOPE)
        manifest_circle_block = manifest_data.get("signatures.circle", {})
        signed_envelope_hash = manifest_circle_block.get(f"hash.{current_circle}", "")
        
        manifest_paths = existenzLocations["manifest"]
        live_folder_files = engineSigningLibrary.gather_folder_files(manifest_paths.get(current_circle, current_circle), repo_root)
        live_computed_hash = engineSigningLibrary.calculate_aggregate_circle_hash(live_folder_files)

        if live_computed_hash != signed_envelope_hash:
            error_handler.print("=" * 90, level="local")
            error_handler.print(f" [!!!] VERITAS FRAUD INTERCEPT: DATA CORRUPTION DETECTED [!!!]", level="local")
            error_handler.print(f"       Track [{current_circle.upper()}] has code state changes since signature stamp!", level="local")
            error_handler.print(f"       Manifest expected: {signed_envelope_hash}", level="local")
            error_handler.print(f"       Live Filesystem:   {live_computed_hash}", level="local")
            error_handler.print("=" * 90, level="local")
            sys.exit(65)

    # ==========================================================================
    # PHASE 2: MATHEMATICAL ASYMMETRIC VERIFICATION PASS (100% OK)
    # ==========================================================================
    payload_to_verify = {
        "commit":                  manifest_data.get("commit"),
        "existentialCoreVersion":  manifest_data.get("existentialCoreVersion"),
        "files.build":             manifest_data.get("files.build", {}),
        "files.dist":              manifest_data.get("files.dist", {}),
        "files.master":            manifest_data.get("files.master", {}),
        "files.tools":             manifest_data.get("files.tools", {}),
        "public_keys":             manifest_data.get("public_keys", {}),
        "signatures.circle":       manifest_data.get("signatures.circle", {})
    }
    
    serialized_manifest_body = json.dumps(
        payload_to_verify,
        sort_keys=True,
        ensure_ascii=True,
        separators=(',', ':')
    ).encode('utf-8')

    public_key_map = {}
    for item in existenzPublicKeys:
        public_key_map[item] = item

    for identity, signature_hex in stored_manifest_signatures.items():
        if identity not in public_key_map:
            continue
            
        pub_ssh_str = public_key_map[identity]
        try:
            public_key_bytes = pub_ssh_str.encode('utf-8')
            public_key_obj = serialization.load_ssh_public_key(public_key_bytes)
            
            # Mathematical signature validation
            public_key_obj.verify(bytes.fromhex(signature_hex), serialized_manifest_body)
            error_handler.print(f"  [+] Cryptographic Verification PASSED for identity role: [{identity}]", level="notice")
        except Exception as crypto_fail:
            error_handler.print("=" * 90, level="local")
            error_handler.print(f" [!!!] VERITAS ASYMMETRIC FAILURE: CRYPTOGRAPHIC SIGNATURE BAD [!!!]", level="local")
            error_handler.print(f"       Mathematical validation failed for key role: [{identity}]", level="local")
            error_handler.print(f"       Details: {crypto_fail}", level="local")
            error_handler.print("=" * 90, level="local")
            sys.exit(67)

    # ==========================================================================
    # PHASE 3: DENSE HIERARCHY BOX STRUCTURE RENDERING
    # ==========================================================================
    sig_database = {}
    if os.path.exists(json_signatures_path):
        try:
            with open(json_signatures_path, "r", encoding="utf-8") as js_in:
                sig_database = json.load(js_in).get("existentialToken", {})
        except Exception:
            pass

    active_tree_rules = existenzSignatures.existentialCore
    pushed_matrix_rows = []
    
    tree_session_hashes = {
        "existentialCoreMagicHash": sig_database.get("MagicCheck_hash", "UNKNOWN"),
        "existentialCoreCheckHash": sig_database.get("CoreCheck_hash", "UNSIGNED"),
    }
    for rule_row in active_tree_rules:
        label = str(rule_row)
        inner_glue = rule_row
        live_hash = sig_database.get(f"{label}_hash", "")
        
        rebuilt_row = [
            label,
            inner_glue,
            live_hash,
            inner_glue,
            inner_glue,
            rule_row
        ]
        pushed_matrix_rows.append(rebuilt_row)
        
        tree_session_hashes[f"existential{label}Hash"] = live_hash
        tree_session_hashes[f"{label.lower()}_sign"] = sig_database.get(f"{label}_sign", "00000000")

    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, tree_session_hashes, pushed_matrix_rows)

    error_handler.print("[+] SUCCESS: All multi-signature verification rings cleared. Veritas unblocks the track.", level="notice")
    
    # Progress cleanly down to your dynamic next step loop calculator
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
