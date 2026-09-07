# ==========================================================================
# EXISTENZ  master/struct/module/cliStateSign.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import getpass
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzConfig
from engineSigningStruct import existenzIntegrityGlue, existenzIntegrityKeyStatus
def execute(args, error_handler, repo_root: str):
    """
    Executes bitmask-driven asymmetric signature updates against tracking circles.
    Prompts for key protection passphrases securely upfront to prevent input loops.
    """
    error_handler.print("Initiating bitmask-driven asymmetric multi-signature execution...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    config_target_path = os.path.abspath(os.path.join(repo_root, args.config))
    
    if not os.path.exists(manifest_target_path):
        error_handler.print("Manifest database tracking ledger missing. Run manifest stage first.", level="error", exit_code=33)

    # Ingest consolidated tracking payload structures from file destination
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

    circle_to_glue_map = {
        "dist":   "CircleDist",
        "tools":  "CircleTools",
        "build":  "CircleBuild",
        "master": "CircleMaster"
    }

    active_circle_arg = str(args.circle).strip().lower()
    if active_circle_arg == "all":
        circles_to_process = ["dist", "tools", "build", "master"]
    else:
        circles_to_process = [active_circle_arg]

    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    if "signatures" not in manifest_data:
        manifest_data["signatures"] = {}

    # ==========================================================================
    # SECURE UPFRONT PASSPHRASE ENTRY PASS (RUNS ONCE LOCALLY)
    # ==========================================================================
    passphrase_bytes = None
    if not is_github_runner:
        # Uses standard terminal hidden-mask input handlers to keep entries secure
        user_input = getpass.getpass("  [🔒] Enter Master Cryptographic Passphrase: ")
        if user_input.strip():
            passphrase_bytes = user_input.strip().encode('utf-8')

    # ==========================================================================
    # SESSION KEY CACHE - RETEINS UNLOCKED KEYS IN MEMORY
    # ==========================================================================
    private_keys_memory_cache = {}
    
    identities_blueprint = [
        ("Environment", "SIGN_EXISTENZ_AUDIT_",     None),
        ("Platform",    "SIGN_EXISTENZ_PLATFORM_",  config_paths.get("Platform")),
        ("Developer",   "SIGN_EXISTENZ_DEVELOPER_", config_paths.get("Developer")),
        ("Personal",    "SIGN_EXISTENZ_PERSONAL_",  config_paths.get("Personal"))
    ]

    error_handler.print(" [*] Pre-authenticating multi-signature identity layers...", level="info")
    for identity, env_prefix, local_key_path in identities_blueprint:
        private_key_object = None

        # Track A: Load local configuration paths offline from disk
        if local_key_path:
            expanded_path = os.expanduser(local_key_path) if hasattr(os, 'expanduser') else os.path.abspath(local_key_path)
            if os.path.exists(expanded_path):
                try:
                    # Ingests your private key bytes, matching it against your upfront passphrase natively
                    with open(expanded_path, "rb") as key_file:
                        key_bytes = key_file.read()
                    
                    from cryptography.hazmat.primitives import serialization
                    private_key_object = serialization.load_ssh_private_key(
                        key_bytes,
                        password=passphrase_bytes
                    )
                except Exception as file_err:
                    error_handler.print(f"  [!] Failed loading local key profile [{identity}]: {file_err}", level="warning")

        # Track B: Fall back to cloud pipeline environment loader if on runner
        if not private_key_object:
            if not is_github_runner:
                continue # Skip environment lookup silently if testing offline locally
                
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

        if private_key_object:
            # Commit instantiated key reference safely to our session cache registry
            private_keys_memory_cache[identity] = private_key_object

    # ==========================================================================
    # 2. RUN WORKSPACE SIGNING LOOPS USING CACHED PRIVATE KEYS
    # ==========================================================================
    for current_circle in circles_to_process:
        glue_key = circle_to_glue_map.get(current_circle)
        if not glue_key or glue_key not in existenzIntegrityGlue:
            continue

        # FIXED: Extract the raw bitmask integer weight precisely from index 1 of the metadata tuple configuration
        circle_bitmask_weight = existenzIntegrityGlue[glue_key][1]

        # Compute dynamic bitmask permissions for this target validation ring track loop
        req_env = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT)
        req_pfm = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM)
        req_dev = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
        req_psn = bool(circle_bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)

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
        
        serialized_manifest_body = json.dumps(
            payload_to_sign,
            sort_keys=True,
            ensure_ascii=True,
            separators=(',', ':')
        ).encode('utf-8')

        active_identities = [
            ("Environment", req_env),
            ("Platform",    req_pfm),
            ("Developer",   req_dev),
            ("Personal",    req_psn)
        ]

        for identity, is_required in active_identities:
            if not is_required:
                continue
                
            # Read pre-loaded keys straight out of memory context with ZERO extra prompts
            private_key_object = private_keys_memory_cache.get(identity)

            if private_key_object:
                try:
                    # Stamp global envelope signature metadata fields
                    signature_bytes = private_key_object.sign(serialized_manifest_body)
                    manifest_data["signatures"][identity] = signature_bytes.hex()
                    error_handler.print(f"  [+] Signed manifest envelope: [{identity}] on track [{current_circle}]", level="notice")
                    
                    hash_key = f"hash.{current_circle}"
                    sign_key = f"sign.{current_circle}"
                    target_circle_hash = manifest_data.get("signatures.circle", {}).get(hash_key, "")
                    
                    if target_circle_hash:
                        circle_sig_bytes = private_key_object.sign(target_circle_hash.encode('utf-8'))
                        manifest_data["signatures.circle"][sign_key] = circle_sig_bytes.hex()
                        error_handler.print(f"  [+] Stamped verification signature: [{sign_key}] via [{identity}]", level="notice")
                except Exception as sig_err:
                    error_handler.print(f"Failed compiling signature for [{identity}]: {sig_err}", level="error", exit_code=64)

    # 3. Flush updates back to disk ledger target destination
    if str(args.run).strip().lower() != "dry":
        try:
            with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
                json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
            error_handler.print("[+] SUCCESS: Asymmetric signatures successfully synchronized inside the manifest.", level="notice")
        except Exception as e:
            error_handler.print(f"Failed recording signatures to file: {e}", level="error", exit_code=32)

    # Progress Control Safely Down to Next Pipeline Phase
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
   
