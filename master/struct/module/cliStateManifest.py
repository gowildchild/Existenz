# ========================================================================== 
# EXISTENZ  master/struct/module/cliStateManifest.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import sys 
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzMeta, existenzPublicKeys

def execute(args, error_handler, repo_root: str):
    """
    Executes progressive  directory scanning and manifest file cataloging.
    Preserves untouched signature tracks while consolidating live cryptographic layers.
    """
    error_handler.print(" [M] Initiating file scan for manifest.json", level="notice")
    
    # Extract the true master destination configurations from your metadata layout maps
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    error_handler.print(f" [M] {manifest_target_path}", level="info")

    # Load existing manifest ledger blocks to allow partial circle preservation
    old_data = {}
    if os.path.exists(manifest_target_path):
        try:
            with open(manifest_target_path, "r", encoding="utf-8") as mf:
                old_data = json.load(mf)
        except Exception:
            pass

    # Extract target directories from your live meta locations matrix
    manifest_paths = existenzLocations["manifest"]
    
    files_dist   = {}
    files_tools  = {}
    files_build  = {}
    files_master = {}

    # Gather frozen data tracks from the old ledger to support incremental updates
    old_dist_bucket   = old_data.get("files.dist", {})
    old_tools_bucket  = old_data.get("files.tools", {})
    old_build_bucket  = old_data.get("files.build", {})
    old_master_bucket = old_data.get("files.master", {})

    # Evaluate target requirements based on your runtime argument parameters
    active_circle = str(args.circle).strip().lower()
    git_commit_sha = engineSigningLibrary.resolve_live_git_commit(repo_root)

    if active_circle == "master":
        error_handler.print(" [S] SCOPE:MASTER <- RE-SIGN -> Except Tools and Dist", level="info")
        files_master.update(engineSigningLibrary.gather_folder_files(manifest_paths["master"], repo_root))
        files_build.update(engineSigningLibrary.gather_folder_files(manifest_paths["build"], repo_root))
        files_tools.update(old_tools_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "tools":
        error_handler.print(" [S] SCOPE:TOOLS <- RE-SIGN -> Except Master, Build and Dist", level="info")
        files_tools.update(engineSigningLibrary.gather_folder_files(manifest_paths["tools"], repo_root))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "dist":
        error_handler.print(" [S] SCOPE:DIST <- RE-SIGN -> Except Master, Build and Tools", level="info")
        files_dist.update(engineSigningLibrary.gather_folder_files(manifest_paths["dist"], repo_root))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_tools.update(old_tools_bucket)
        
    else: # Full global baseline overwrite ("circleall" or default fallback configuration)
        error_handler.print(" [S] SCOPE:ALL <- OVERWRITE -> Baseline ALL", level="info")
        files_dist.update(engineSigningLibrary.gather_folder_files(manifest_paths["dist"], repo_root))
        files_tools.update(engineSigningLibrary.gather_folder_files(manifest_paths["tools"], repo_root))
        files_build.update(engineSigningLibrary.gather_folder_files(manifest_paths["build"], repo_root))
        files_master.update(engineSigningLibrary.gather_folder_files(manifest_paths["master"], repo_root))

    # 2. Build Unified Public Keys Map Record Dictionary 1:1 out of your tuple profiles
    public_keys_registry = {}
    for key_meta in existenzPublicKeys:
        name, pub_str, _, _, _, _ = key_meta
        public_keys_registry[name] = pub_str

    # 3. Extract raw circle hashes and build your precise dot-separated token map layout
    hash_dist   = engineSigningLibrary.calculate_aggregate_circle_hash(files_dist)
    hash_tools  = engineSigningLibrary.calculate_aggregate_circle_hash(files_tools)
    hash_build  = engineSigningLibrary.calculate_aggregate_circle_hash(files_build)
    hash_master = engineSigningLibrary.calculate_aggregate_circle_hash(files_master)

    old_circle_block = old_data.get("signatures.circle", {})

    signatures_circle_registry = {
        "hash.dist":   hash_dist,
        "hash.tools":  hash_tools,
        "hash.build":  hash_build,
        "hash.master": hash_master,
        
        "sign.dist":   old_circle_block.get("sign.dist", ""),
        "sign.tools":  old_circle_block.get("sign.tools", ""),
        "sign.build":  old_circle_block.get("sign.build", ""),
        "sign.master": old_circle_block.get("sign.master", "")
    }

    # Run bitmask-driven verification check to warn on signature drifts
    from engineSigningStruct import existenzIntegrityGlue, existenzIntegrityKeyStatus

    circle_to_glue_map = {
        "dist":   "CircleDist",
        "tools":  "CircleTools",
        "build":  "CircleBuild",
        "master": "CircleMaster"
    }

    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    master_changed = (hash_master != old_circle_block.get("hash.master", ""))
    build_changed  = (hash_build != old_circle_block.get("hash.build", ""))

    # ==========================================================================
    # MODIFIED AREA START: FORENSIC FILE DRIFT ANALYSIS GRID PASS
    # ==========================================================================
    if (master_changed or build_changed) and is_github_runner:
        changed_items = ""
        if master_changed and build_changed:
            changed_items = "MASTER & BUILD"
        elif master_changed:
            changed_items = "MASTER"
        elif build_changed:
            changed_items = "BUILD"
            
        drift_details = [
            "Unsigned changes detected in MASTER CORE code!",
            "File system update is blocked till fully signed with private keys!",
            f"Changed {changed_items}"
        ]

        # Scan for changed or added files inside the master ring
        old_master_files = old_data.get("files.master", {})
        for file_path, current_hash in files_master.items():
            old_hash = old_master_files.get(file_path)
            if old_hash != current_hash:
                drift_details.append(f" [➔] DRIFT FILE: {file_path}")
                drift_details.append(f"     From: {old_hash or 'NEW_ASSET_NONE'}")
                drift_details.append(f"     To:   {current_hash}")

        # Scan for missing or dropped files inside the master ring
        for file_path, old_hash in old_master_files.items():
            if file_path not in files_master:
                drift_details.append(f" [➔] DROPPED FILE: {file_path}")
                drift_details.append(f"     From: {old_hash}")
                drift_details.append(f"     To:   DELETION_ASSET_NONE")

        error_handler.notice(
            level="error",
            message="* * * MASTER CHANGE INTERCEPTION! * * *",
            details=drift_details,
            exit_code=65
        )

    for target_c, glue_key in circle_to_glue_map.items():
        current_hash = signatures_circle_registry.get(f"hash.{target_c}")
        old_hash = old_circle_block.get(f"hash.{target_c}", "")
        has_signature = bool(signatures_circle_registry.get(f"sign.{target_c}", ""))

        if current_hash != old_hash or not has_signature:
            # FIXED: Target index 1 coordinate to extract raw bitmask integers safely out of glue records
            bitmask_weight = existenzIntegrityGlue[glue_key][1] if glue_key in existenzIntegrityGlue else 0
            
            needed_keys = []
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM):  needed_keys.append("Platform")
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER): needed_keys.append("Developer")
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL):  needed_keys.append("Personal")

            if needed_keys:
                core_drift_details = [
                    "Unsigned changes detected in MASTER CORE code!",
                    "File system update is blocked till fully signed with private keys!",
                    f"From {old_hash or 'BLANK_START'} -> {current_hash}"
                ]
                
                # Fetch target bucket dynamically based on active iteration ring loop
                target_bucket_key = f"files.{target_c}"
                old_bucket_files = old_data.get(target_bucket_key, {})
                live_bucket_files = locals().get(f"files_{target_c}", {})
                
                # Scan internal file properties inside current active sub-ring
                for file_path, current_f_hash in live_bucket_files.items():
                    old_f_hash = old_bucket_files.get(file_path)
                    if old_f_hash != current_f_hash:
                        core_drift_details.append(f" [➔] DRIFTING FILE: {file_path}")
                        core_drift_details.append(f"     From: {old_f_hash or 'NEW_ASSET_NONE'}")
                        core_drift_details.append(f"     To:   {current_f_hash}")

                error_handler.notice(
                    level="warning",
                    message=f"* * * CORE CHANGE INTERCEPTION IN [{target_c.upper()}] * * *",
                    details=core_drift_details
                )
    # ==========================================================================
    # MODIFIED AREA END
    # ==========================================================================

    manifest_data = {
        "existentialCoreVersion": existenzMeta.HEADER["VERSION"].decode(),
        "commit": git_commit_sha,
        "public_keys": public_keys_registry,
        "files.dist": files_dist,
        "files.tools": files_tools,
        "files.build": files_build,
        "files.master": files_master,
        "signatures.circle": signatures_circle_registry,
        "signatures": old_data.get("signatures", {})
    }

    # Bypasses direct file saves if strategy is set to dry simulation
    if str(args.run).strip().lower() == "dry":
        error_handler.print("DRY-MODE prevents writing to disk!", level="notice")
        return

    # 4. Serialize layout straight to root path destination with sorted attributes
    try:
        with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
            json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
        error_handler.print(" [+] Manifest consolidated succesfully", level="notice")
    except Exception as e:
        error_handler.print(f" FAILURE writing to manifest: {e}", level="error", exit_code=32)

    # 5. Transition seamlessly straight to your bitmask-driven step calculation handler loop
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
