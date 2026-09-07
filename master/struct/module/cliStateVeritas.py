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
    Executes absolute cryptographic validation (VERITAS).
    1. Asserts required keys are used based on glue bitmasks.
    2. Asserts data hashes have not drifted since signing.
    3. Graphically logs results and halts building on any signature fault.
    """
    error_handler.print("Initiating full cryptographic multi-signature validation pass [MODE: VERITAS]...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    if not os.path.exists(manifest_target_path):
        error_handler.print("Veritas boundary abort: manifest.json tracking ledger missing.", level="error", exit_code=33)

    # Ingest the active live manifest database mapping layer
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)
    stored_signatures = manifest_data.get("signatures", {})

    # Extract our structural arrays and bitmasks directly from your metadata layers
    from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeyStatus

    circle_to_glue_map = {
        "dist":   "CircleDist",
        "tools":  "CircleTools",
        "build":  "CircleBuild",
        "master": "CircleMaster"
    }

    active_circle_arg = str(args.circle).strip().lower()
    glue_key = circle_to_glue_map.get(active_circle_arg)
    
    if not glue_key or glue_key not in existenzIntegrityGlue:
        error_handler.print(f"Veritas aborted: unresolved active circle identifier: {active_circle_arg}", level="error", exit_code=34)

    # Direct Extraction Matching Your cliStateSign.py Logic Loop Layout
    circle_bitmask_weight = existenzIntegrityGlue[glue_key][1]

    # ==========================================================================
    # CHECK 1: VERIFY MANDATED BITMASK KEYS ARE PRESENT
    # ==========================================================================
    req_env = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT)
    req_pfm = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM)
    req_dev = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
    req_psn = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)

    missing_keys = []
    if req_env and "Environment" not in stored_signatures: missing_keys.append("Environment")
    if req_pfm and "Platform" not in stored_signatures:    missing_keys.append("Platform")
    if req_dev and "Developer" not in stored_signatures:   missing_keys.append("Developer")
    if req_psn and "Personal" not in stored_signatures:    missing_keys.append("Personal")

    if missing_keys:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] VERITAS CONSTRAINT VIOLATION: MANDATORY REJECTION [!!!]", level="local")
        error_handler.print(f"       Circle [{active_circle_arg.upper()}] requires missing private signatures: {missing_keys}", level="local")
        error_handler.print(f"       Further structural compilation is explicitly REFUSED.", level="local")
        error_handler.print("=" * 90, level="local")
        sys.exit(62)

    # ==========================================================================
    # CHECK 2: VERIFY DATA CONTINUITY (LIVE HASH VS MANIFEST RECORD)
    # ==========================================================================
    manifest_circle_block = manifest_data.get("signatures.circle", {})
    live_circle_hash = manifest_circle_block.get(f"hash.{active_circle_arg}", "")
    
    # Recalculate live files hashes to verify no file tampering took place since generation
    manifest_paths = existenzLocations["manifest"]
    live_fs_files = engineSigningLibrary.gather_folder_files(manifest_paths.get(active_circle_arg, active_circle_arg), repo_root)
    computed_live_hash = engineSigningLibrary.calculate_aggregate_circle_hash(live_fs_files)

    if computed_live_hash != live_circle_hash:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] VERITAS FILE CORRUPTION DETECTED: Circle [{active_circle_arg.upper()}] has data drift!", level="local")
        error_handler.print(f"       Manifest expected: {live_circle_hash}", level="local")
        error_handler.print(f"       Filesystem live:   {computed_live_hash}", level="local")
        error_handler.print(f"       Aborting pipeline execution to intercept supply-chain attack vector.", level="local")
        error_handler.print("=" * 90, level="local")
        sys.exit(65)

    # ==========================================================================
    # CHECK 3: ASYMMETRIC ED25519 CRYPTOGRAPHIC TRUTH VERIFICATION
    # ==========================================================================
    # Reassemble canonical signing payload matching your specification
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

    # Load matching public key strings out of your active tuple profiles
    public_key_map = {}
    for item in existenzPublicKeys:
        public_key_map[item[0]] = item[1]

    for identity, signature_hex in stored_signatures.items():
        if identity not in public_key_map:
            continue
            
        pub_ssh_str = public_key_map[identity]
        try:
            public_key_bytes = pub_ssh_str.encode('utf-8')
            public_key_obj = serialization.load_ssh_public_key(public_key_bytes)
            
            # Perform genuine mathematical verification
            public_key_obj.verify(bytes.fromhex(signature_hex), serialized_manifest_body)
            error_handler.print(f"  [+] Cryptographic Verification PASSED for identity role: [{identity}]", level="notice")
        except Exception as crypto_fail:
            error_handler.print("=" * 90, level="local")
            error_handler.print(f" [!!!] VERITAS CRYPTOGRAPHIC SIGNATURE FAILURE [!!!]", level="local")
            error_handler.print(f"       Mathematical validation failed for key role: [{identity}]", level="local")
            error_handler.print(f"       Error context details: {crypto_fail}", level="local")
            error_handler.print("=" * 90, level="local")
            sys.exit(67)

    # ==========================================================================
    # VISUAL RENDER: Output structural tree visualization matching data-dense matrix rows
    # ==========================================================================
    sig_database = {}
    if os.path.exists(json_signatures_path):
        try:
            with open(json_signatures_path, "r", encoding="utf-8") as js_in:
                sig_database = json.load(js_in).get("existentialToken", {})
        except Exception:
            pass

    tree_session_hashes = {
        "existentialCoreMagicHash": sig_database.get("MagicCheck_hash", "UNKNOWN"),
        "existentialCoreCheckHash": sig_database.get("CoreCheck_hash", "UNSIGNED"),
    }
    for label, _, _ in existenzSignatures.existentialCore:
        tree_session_hashes[f"existential{label}Hash"] = sig_database.get(f"{label}_hash", "")
        tree_session_hashes[f"{label.lower()}_sign"] = sig_database.get(f"{label}_sign", "00000000")

    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, tree_session_hashes, existenzSignatures.existentialCore)

    error_handler.print("[+] SUCCESS: All multi-signature verification rings cleared. Veritas unblocks the track.", level="notice")
    
    # Progress cleanly down to your dynamic next step loop calculator
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
