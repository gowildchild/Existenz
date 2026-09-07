# ==========================================================================
# EXISTENZ  master/struct/module/cliStateSign.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzConfig

def execute(args, error_handler, repo_root: str):
    """
    Executes bitmask-driven asymmetric signature updates against tracking circles.
    Supports individual targets or composite workspace updates via circle='all'.
    """
    error_handler.print("Initiating bitmask-driven asymmetric multi-signature execution...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    config_target_path = os.path.abspath(os.path.join(repo_root, args.config))
    
    if not os.path.exists(manifest_target_path):
        error_handler.print("Manifest database tracking ledger missing. Run manifest stage first.", level="error", exit_code=33)

    # 1. Ingest consolidated tracking payload structures from file destination
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)

    # Load local configuration private key paths from disk template
    config_paths = {}
    if os.path.exists(config_target_path):
        try:
            with open(config_target_path, "r", encoding="utf-8") as cf:
                config_paths = json.load(cf).get("private_key_paths", {})
        except Exception:
            pass

    # 2. Extract your live bitmask definitions out of your active integrity glue file
    from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeysHandler, existenzIntegrityKeyStatus, existenzSteps
    from existentialSignatures import existentialToken

    # Map your target circle name directly to its corresponding glue key element
    circle_to_glue_map = {
        "dist":   "CircleDist",
        "tools":  "CircleTools",
        "build":  "CircleBuild",
        "master": "CircleMaster"
    }

    active_circle_arg = str(args.circle).strip().lower()
    
    # FIXED: Extract individual target circles dynamically to enable composite workspace signing via 'all'
    if active_circle_arg == "all":
        circles_to_process = ["dist", "tools", "build", "master"]
    else:
        circles_to_process = [active_circle_arg]

    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    if "signatures" not in manifest_data:
        manifest_data["signatures"] = {}

    # 3. RUN ITERATIVE SIGNING TRACK FOR ALL SPECIFIED VALIDATION RINGS
    for current_circle in circles_to_process:
        glue_key = circle_to_glue_map.get(current_circle)
        if not glue_key or glue_key not in existenzIntegrityGlue:
            error_handler.print(f"Skipping unresolved circle identifier: {current_circle}", level="warning")
            continue

        # Extract the exact bitmask status profile value straight from your entry tuple index 1
        circle_bitmask_weight = existenzIntegrityGlue[glue_key][1]

        # DYNAMIC BITMASK MATCHING GATES: Determine exactly what keys have permissions for this circle
        req_env = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT)
        req_pfm = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM)
        req_dev = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
        req_psn = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)

        # Compile the canonical sorting layout matching your cross-language byte payload specifications
        payload_to_sign = {
            "commit":                  manifest_data.get("commit"),
            "existentialCoreVersion":  manifest_data.get("existentialCoreVersion"),
            "files.build":             manifest_data.get("files.build", {}),
            "files.dist":              manifest_data.get("files.dist", {}),
            "files.master":            manifest_data.get("files.master", {}),
            "files.tools":             manifest_data.get("files.tools", {}),
            "public_keys":             manifest_data.get("public_keys", {}),
            "signatures.circle":       manifest_data.get("signatures.circle", {})
        }
        
        # Serialize payload to safe zero-whitespace bytes for signing consistency
        serialized_manifest_body = json.dumps(
            payload_to_sign,
            sort_keys=True,
            ensure_ascii=True,
            separators=(',', ':')
        ).encode('utf-8')

        # 4. Map identities queue straight to their required loop environment prefixes and file paths
        identities_queue = [
            ("Environment", req_env, "SIGN_EXISTENZ_AUDIT_",     None),
            ("Platform",    req_pfm, "SIGN_EXISTENZ_PLATFORM_",  config_paths.get("Platform")),
            ("Developer",   req_dev, "SIGN_EXISTENZ_DEVELOPER_", config_paths.get("Developer")),
            ("Personal",    req_psn, "SIGN_EXISTENZ_PERSONAL_",  config_paths.get("Personal"))
        ]
        for identity, is_required, env_prefix, local_key_path in identities_queue:
            if not is_required:
                continue
                
            error_handler.print(f" [*] Bitmask match active for identity role: [{identity}] on circle: [{current_circle}]", level="info")
            private_key_object = None

            # A. LOCAL OPERATION TRACK: Load from file system using your config paths if active
            if local_key_path:
                expanded_path = os.path.expanduser(local_key_path)
                if os.path.exists(expanded_path):
                    try:
                        private_key_object = engineSigningLibrary.load_private_key(
                            identity=identity,
                            path=expanded_path,
                            error_handler=error_handler,
                            repo_github_flag=is_github_runner
                        )
                    except Exception as file_err:
                        error_handler.print(f"  [!] Failed loading local key profile from path: {file_err}", level="warning")

            if not private_key_object:
                # FIXED: Skip cloud environment checks completely if running locally offline
                if not is_github_runner:
                    error_handler.print(f"  [ ] Environment cloud variables unavailable locally. Skipping track: [{identity}].", level="warning")
                    continue

                env_loader = engineSigningLibrary.visualMixEngineEnvironment(
                    error_handler=error_handler,
                    repo_github_flag=is_github_runner,
                    post=env_prefix,
                    namespace=identity.lower()
                )
                try:
                    secret_env_map = env_loader.load_secret_key()
                    private_key_object = secret_env_map.get("_OBJECT")
                except Exception:
                    raise

            # C. EXECUTE CRYPTOGRAPHIC STAMP IF KEY IS LOADED
            if private_key_object:
                try:
                    # Stamp global manifest database envelope signature
                    signature_bytes = private_key_object.sign(serialized_manifest_body)
                    manifest_data["signatures"][identity] = signature_bytes.hex()
                    error_handler.print(f"  [+] Cryptographically signed manifest ledger block: [{identity}]", level="notice")
                    
                    # Stamp the individual circle target tracking signature path inside signatures.circle
                    hash_key = f"hash.{current_circle}"
                    sign_key = f"sign.{current_circle}"
                    
                    # Look up the dynamic aggregate hash of the active track loop
                    target_circle_hash = manifest_data.get("signatures.circle", {}).get(hash_key, "")
                    
                    if target_circle_hash:
                        # Generate the explicit cryptographic signature for this individual track payload
                        circle_sig_bytes = private_key_object.sign(target_circle_hash.encode('utf-8'))
                        manifest_data["signatures.circle"][sign_key] = circle_sig_bytes.hex()
                        error_handler.print(f"  [+] Stamped circle verification ring signature: [{sign_key}]", level="notice")

                except Exception as sig_err:
                    error_handler.print(f"Failed to compile signature for role [{identity}]: {sig_err}", level="error", exit_code=64)
            else:
                error_handler.print(f"  [ ] Skipping signature for [{identity}]: Private key asset not loaded.", level="warning")

    # 5. Flush signed ledger updates straight back to the file system destination
    if str(args.run).strip().lower() != "dry":
        try:
            with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
                json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
            error_handler.print("[+] SUCCESS: Asymmetric signatures written to manifest tracking registries.", level="notice")
        except Exception as e:
            error_handler.print(f"Failed to record signature tokens to file: {e}", level="error", exit_code=32)

    # Move smoothly into your dynamic pipeline routing step calculator
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
   
