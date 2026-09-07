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
    error_handler.print("Initiating repository file scan to manifest.json", level="notice")
    
    # Extract the true master destination configurations from your metadata layout maps
    manifest_filename = existenzLocations["engine"]["Manifest"]
    manifest_target_path = os.path.abspath(os.path.join(repo_root, manifest_filename))
    error_handler.print(f"  [REGISTRY TARGET] {manifest_target_path}", level="info")

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

    # 1. Surgical Ring Routing Mapped Straight to your Metadata Context Folders
    if active_circle == "master":
        error_handler.print("Re-signing Ring [MASTER & BUILD]. Preserving Tools and Dist tracks.", level="info")
        files_master.update(engineSigningLibrary.gather_folder_files(manifest_paths["master"], repo_root))
        files_build.update(engineSigningLibrary.gather_folder_files(manifest_paths["build"], repo_root))
        files_tools.update(old_tools_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "tools":
        error_handler.print("Re-signing Ring [TOOLS]. Preserving Master, Build, and Dist tracks.", level="info")
        files_tools.update(engineSigningLibrary.gather_folder_files(manifest_paths["tools"], repo_root))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "dist":
        error_handler.print("Re-signing Ring [DIST]. Preserving Master, Build, and Tools tracks.", level="info")
        files_dist.update(engineSigningLibrary.gather_folder_files(manifest_paths["dist"], repo_root))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_tools.update(old_tools_bucket)
        
    else: # Full global baseline overwrite ("circleall" or default fallback configuration)
        error_handler.print("Scoping Full Workspace - Baseline Overwrite.", level="info")
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

    # SECURITY HARDENING: Detect unauthorized modifications before writing out the manifest update
    is_github_runner = os.environ.get("GITHUB_ACTIONS") == "true"
    master_changed = (hash_master != old_circle_block.get("hash.master", ""))
    build_changed  = (hash_build != old_circle_block.get("hash.build", ""))

    if (master_changed or build_changed) and is_github_runner:
        error_handler.print("=" * 90, level="local")
        error_handler.print(f" [!!!] MANIFEST SECURITY INTERCEPT: REJECTING REMOTE OVERWRITE [!!!]", level="local")
        error_handler.print(f"       Unsigned changes detected in high-privilege tracks on remote public runner.", level="local")
        error_handler.print(f"       Master Changed: {master_changed} | Build Changed: {build_changed}", level="local")
        error_handler.print(f"       File system update is BLOCKED until signed locally via private keys.", level="local")
        error_handler.print("=" * 90, level="local")
        error_handler.notice(level="error", message=f"MANIFEST ESCALATION INTERCEPT: {str(e)}", exit_code=65, details=f"Unsigned changes detected in master code! Master Changed: {master_changed} | Build Changed: {build_changed}")
        # sys.exit(65) # Safely crashes the step before modifying the manifest or staging git updates

    for target_c, glue_key in circle_to_glue_map.items():
        current_hash = signatures_circle_registry.get(f"hash.{target_c}")
        old_hash = old_circle_block.get(f"hash.{target_c}", "")
        has_signature = bool(signatures_circle_registry.get(f"sign.{target_c}", ""))

        if current_hash != old_hash or not has_signature:
            # FIXED: Correctly extracts status weight integer from index 1 of the metadata tuple configuration
            bitmask_weight = existenzIntegrityGlue[glue_key][1] if glue_key in existenzIntegrityGlue else 0
            
            needed_keys = []
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM):  needed_keys.append("Platform")
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER): needed_keys.append("Developer")
            if bool(bitmask_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL):  needed_keys.append("Personal")

            if needed_keys:
                error_handler.print("=" * 90, level="local")
                error_handler.print(f" [!] UN-SIGNED payload track changes detected in Circle Ring: [{target_c.upper()}]", level="local")
                error_handler.print(f"     Structural Hash updated: {old_hash[:16]}... -> {current_hash[:16]}...", level="local")
                error_handler.print(f"     MANDATORY LOCAL ACTION: Requires signing with private keys: {needed_keys}", level="local")
                error_handler.print(f"     Downstream deployment builds will remain locked until keys are committed.", level="local")
                error_handler.print("=" * 90, level="local")

    # Assemble Consolidated Manifest Ledger Database File Structure
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
        error_handler.print("Not writing to manifest (DRY mode!).", level="notice")
        return

    # 4. Serialize layout straight to root path destination with sorted attributes
    try:
        with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
            json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
        error_handler.print("[+] SUCCESS: Manifest successfully consolidated.", level="notice")
    except Exception as e:
        error_handler.print(f"Failed to write to manifest: {e}", level="error", exit_code=32)

    # 5. Transition seamlessly straight to your bitmask-driven step calculation handler loop
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
