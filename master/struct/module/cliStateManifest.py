# ==========================================================================
# EXISTENZ  master/struct/module/cliStateManifest.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzMeta, existenzPublicKeys

def execute(args, error_handler, repo_root: str):
    """
    Executes progressive forensic workspace directory scanning and manifest file cataloging.
    Preserves untouched signature tracks while consolidating live cryptographic circle layers.
    """
    error_handler.print("Initiating repository forensic file validation tracking scan...", level="notice")
    
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
        files_master.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["master"]))
        files_build.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["build"]))
        files_tools.update(old_tools_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "tools":
        error_handler.print("Re-signing Ring [TOOLS]. Preserving Master, Build, and Dist tracks.", level="info")
        files_tools.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["tools"]))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_dist.update(old_dist_bucket)
        
    elif active_circle == "dist":
        error_handler.print("Re-signing Ring [DIST]. Preserving Master, Build, and Tools tracks.", level="info")
        files_dist.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["dist"]))
        files_master.update(old_master_bucket)
        files_build.update(old_build_bucket)
        files_tools.update(old_tools_bucket)
        
    else: # Full global baseline overwrite ("circleall" or default fallback configuration)
        error_handler.print("Scoping Full Workspace - Baseline Overwrite.", level="info")
        files_dist.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["dist"]))
        files_tools.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["tools"]))
        files_build.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["build"]))
        files_master.update(engineSigningLibrary.gather_folder_files(repo_root, manifest_paths["master"]))

    # 2. Build Unified Public Keys Map Record Dictionary 1:1 out of your tuple profiles
    public_keys_registry = {}
    for key_meta in existenzPublicKeys:
        name, pub_str, _, _, _, _ = key_meta
        public_keys_registry[name] = pub_str

    # 3. Assemble Consolidated Manifest Ledger Database File Structure
    manifest_data = {
        "existentialCoreVersion": existenzMeta.HEADER["VERSION"].decode(),
        "commit": git_commit_sha,
        "public_keys": public_keys_registry,
        "files.dist": files_dist,
        "files.tools": files_tools,
        "files.build": files_build,
        "files.master": files_master,
        "signatures": old_data.get("signatures", {})
    }

    # Bypasses direct file saves if strategy is set to dry simulation
    if str(args.run).strip().lower() == "dry":
        error_handler.print("Bypassing manifest ledger writes due to dry strategy constraint.", level="notice")
        return

    # 4. Serialize layout straight to root path destination with sorted attributes
    try:
        with open(manifest_target_path, "w", encoding="utf-8") as out_mf:
            json.dump(manifest_data, out_mf, indent=2, sort_keys=True)
        error_handler.print("[+] SUCCESS: Manifest ledger successfully consolidated.", level="notice")
    except Exception as e:
        error_handler.print(f"Failed to write output manifest ledger target: {e}", level="error", exit_code=32)

    # 5. Transition seamlessly straight to your bitmask-driven step calculation handler loop
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
