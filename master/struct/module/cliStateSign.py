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
    Executes asymmetric multi-signature compilation against the manifest.
    Ingests loop-driven environment variables and configuration file paths cleanly.
    """
    error_handler.print("Initiating asymmetric multi-signature routines...", level="notice")
    
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    config_target_path = os.path.abspath(os.path.join(repo_root, args.config))
    
    if not os.path.exists(manifest_target_path):
        error_handler.print("Manifest. Execute manifest stage first.", level="error", exit_code=33)

    # 1. Ingest consolidated tracking payload structures from file destination
    with open(manifest_target_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)

    # Load local configuration private key paths if the file exists on disk
    config_paths = {}
    if os.path.exists(config_target_path):
        try:
            with open(config_target_path, "r", encoding="utf-8") as cf:
                config_paths = json.load(cf).get("private_key_paths", {})
        except Exception as ce:
            error_handler.print(f"Non-fatal configuration read warning: {ce}", level="warning")

    # 2. Compute the bitmask verification requirements for the active execution stage
    req_env, req_pfm, req_dev, req_psn = engineSigningLibrary.solve_ring_requirements(args.stage)
    
    # Compile the strict sorting layout matching your cross-language byte payload specifications
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

    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    if "signatures" not in manifest_data:
        manifest_data["signatures"] = {}

    # 3. Map identities queue straight to their required loop environment prefixes and file paths
    identities_queue = [
        ("Environment", req_env, "SIGN_EXISTENZ_AUDIT_",     None),
        ("Platform",    req_pfm, "SIGN_EXISTENZ_PLATFORM_",  config_paths.get("Platform")),
        ("Developer",   req_dev, "SIGN_EXISTENZ_DEVELOPER_", config_paths.get("Developer")),
        ("Personal",    req_psn, "SIGN_EXISTENZ_PERSONAL_",  config_paths.get("Personal"))
    ]

    for identity, is_required, env_prefix, local_key_path in identities_queue:
        if not is_required:
            continue
            
        error_handler.print(f" [*] Processing signing sequence for: [{identity}]", level="info")
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
                    error_handler.print(f"  [!] Failed loading local key from path: {file_err}", level="warning")

        # B. CLOUD PIPELINE TRACK: Fall back natively to your loop-driven environment loader if running on runner
        if not private_key_object:
            env_loader = engineSigningLibrary.visualMixEngineEnvironment(
                error_handler=error_handler,
                repo_github_flag=is_github_runner,
                post=env_prefix,
                namespace=identity.lower()
            )
            secret_env_map = env_loader.load_secret_key()
            private_key_object = secret_env_map.get("_OBJECT")

        # C. EXECUTE ASYMMETRIC SIGNATURE STAMP
        if private_key_object:
            try:
                signature_bytes = private_key_object.sign(serialized_manifest_body)
                manifest_data["signatures"][identity] = signature_bytes.hex()
                error_handler.print(f"  [+] Cryptographically signed manifest: [{identity}]", level="notice")
            except Exception as sig_err:
                error_handler.print(f"Failed to sign for role [{identity}]: {sig_err}", level="error", exit_code=64)
        else:
            error_handler.print(f"  [ ] Skipping signature for [{identity}]: Private key not loaded.", level="warning")

    # 4. Flush signed ledger updates straight back to the file system destination
    if str(args.run).strip().lower() != "dry":
        try:
            with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
                json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
            error_handler.print("[+] SUCCESS: Asymmetric signatures written to manifest.", level="notice")
        except Exception as e:
            error_handler.print(f"Failed towrite signatures to file: {e}", level="error", exit_code=32)

    # Move smoothly into your dynamic pipeline routing step calculator
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)

