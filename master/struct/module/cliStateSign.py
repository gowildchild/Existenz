# ==========================================================================
# EXISTENZ  master/struct/module/cliStateSign.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzConfig, existenzMeta, existenzPublicKeys

def execute(args, error_handler, repo_root: str):
    """
    Executes asymmetric multi-signature compilation against the consolidated manifest.
    Ingests loop-driven environment secrets and locks down the verified ring keys.
    """
    error_handler.print("Initiating asymmetric multi-signature assembly routines...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    
    if not os.path.exists(manifest_target_path):
        error_handler.print("Manifest database tracking ledger missing. Execute manifest stage first.", level="error", exit_code=33)

    # 1. Ingest consolidated tracking payload structures from file destination
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)

    # 2. Compute the bitmask verification requirements for the active execution stage
    # Unpacks the full 4-identity signature state profile cleanly
    req_env, req_pfm, req_dev, req_psn = engineSigningLibrary.solve_ring_requirements(args.stage)
    
    # Assemble the canonical payload to sign using sorted parameters to avoid key order mutations
    payload_to_sign = {
        "commit":            manifest_data.get("commit"),
        "files.build":       manifest_data.get("files.build", {}),
        "files.dist":        manifest_data.get("files.dist", {}),
        "files.master":      manifest_data.get("files.master", {}),
        "files.tools":       manifest_data.get("files.tools", {}),
        "public_keys":       manifest_data.get("public_keys", {}),
        "signatures_circle": manifest_data.get("signatures_circle", {})
    }
    
    # Serialize payload to safe zero-whitespace bytes for signing consistency
    serialized_manifest_body = json.dumps(
        payload_to_sign,
        sort_keys=True,
        ensure_ascii=True,
        separators=(',', ':')
    ).encode('utf-8')

    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    if "signatures" not in manifest_data:
        manifest_data["signatures"] = {}

    # 3. Map identities queue straight to their required loop environment prefixes
    # Incorporates Environment (SIGN_EXISTENZ_AUDIT_) smoothly alongside your local keys
    identities_queue = [
        ("Environment", req_env, "SIGN_EXISTENZ_AUDIT_"),
        ("Platform",    req_pfm, "SIGN_EXISTENZ_PLATFORM_"),
        ("Developer",   req_dev, "SIGN_EXISTENZ_DEVELOPER_"),
        ("Personal",    req_psn, "SIGN_EXISTENZ_PERSONAL_")
    ]

    for identity, is_required, env_prefix in identities_queue:
        if not is_required:
            continue
            
        error_handler.print(f" [*] Processing signature sequence for identity role: [{identity}]", level="info")
        
        # Instantiate your environmental key loader engine natively
        env_loader = engineSigningLibrary.visualMixEngineEnvironment(
            error_handler=error_handler,
            repo_github_flag=is_github_runner,
            post=env_prefix,
            namespace=identity.lower()
        )
        
        try:
            secret_env_map = env_loader.load_secret_key()
            private_key_object = secret_env_map.get("_OBJECT")
            
            if private_key_object:
                # Sign the canonical body payload bytes using standard Ed25519 routines
                signature_bytes = private_key_object.sign(serialized_manifest_body)
                manifest_data["signatures"][identity] = signature_bytes.hex()
                error_handler.print(f"  [+] Cryptographically signed manifest ledger block: [{identity}]", level="notice")
            else:
                error_handler.print(f"  [!] Skipping signature for [{identity}]: Private key asset not loaded.", level="warning")
        except Exception as sig_err:
            error_handler.print(f"Failed to compile signature for role [{identity}]: {sig_err}", level="error", exit_code=64)

    # 4. Flush signed ledger updates straight back to the file system destination
    if str(args.run).strip().lower() != "dry":
        try:
            with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
                json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
            error_handler.print("[+] SUCCESS: Asymmetric signatures written to manifest tracking registries.", level="notice")
        except Exception as e:
            error_handler.print(f"Failed to record signature tokens to file: {e}", level="error", exit_code=32)

    # Move smoothly into your dynamic pipeline routing step calculator
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)

