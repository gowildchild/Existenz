# ==========================================================================
# EXISTENZ  master/struct/module/cliStateInit.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
from engineSigningMeta import existenzLocations

def execute(args, error_handler, repo_root: str):
    """
    Modular execution block for -stage init.
    Audits the master/ root directory files. If an asset is missing, it triggers
    a lookup in the master/struct/ vault to clone or adapt it over.
    """
    error_handler.print("Initiating structural integrity baseline pre-flight check...", level="notice")
    
    # Baseline tracking registers
    failed_initialization = False
    assets_to_sync = {}

    # 1. Audit Realm: Core Layout Configuration Primitives & Assembly Targets
    for token, relative_path in existenzLocations["core"].items():
        full_target_path = os.path.join(repo_root, relative_path)
        
        # Check if the asset is missing from its runtime location (mostly master/)
        if not os.path.exists(full_target_path):
            if token == "Schema":
                # The primary schema blueprint must exist inside master/struct/ or everything is crippled
                error_handler.print(f"Fatal Initialization fault: Master blueprint '{token}' missing at: {relative_path}", level="warning")
                failed_initialization = "config"
            else:
                filename = os.path.basename(relative_path)
                error_handler.print(f"Runtime target '{token}' ({filename}) missing from master/ workspace.", level="warning")
                
                # Catalog exactly what is missing and needs to be pulled/adapted from master/struct/
                assets_to_sync[token] = {
                    "runtime_path": relative_path,
                    "filename": filename
                }
        else:
            error_handler.print(f"Core Asset Verified:   {relative_path:<40} [FOUND]")

    # 2. Audit Realm: Operational Library Infrastructure Engine Components
    for token, relative_path in existenzLocations["engine"].items():
        clean_rel_path = relative_path.split(":")[-1] if ":" in relative_path else relative_path
        full_target_path = os.path.join(repo_root, clean_rel_path)
        
        if not os.path.exists(full_target_path):
            error_handler.print(f"Engine module script reference '{token}' missing at: {clean_rel_path}", level="warning")
            if not failed_initialization:
                failed_initialization = "init"
        else:
            error_handler.print(f"Engine Asset Verified: {clean_rel_path:<40} [FOUND]")

    # 3. Handle Critical Core Pipeline Execution Blockers
    if failed_initialization == "config":
        error_handler.print("Pre-flight execution blocked: Missing core layout master schema structure.", level="error", exit_code=16)
    elif failed_initialization == "init":
        error_handler.print("Pre-flight execution blocked: Missing system execution library modules.", level="error", exit_code=15)

    # 4. Trigger Adaptive Fallback Mirror and Compilation Loops
    if assets_to_sync:
        error_handler.print(" [*] Pre-flight Scan Complete: Missing assets detected. Routing to master/struct/ vault...", level="notice")
        try:
            from module import cliStateBuild
            # Pass the catalog of missing files to the builder module to handle copying or adapting
            cliStateBuild.execute_vault_sync(args, error_handler, repo_root, missing_assets=assets_to_sync)
        except ImportError:
            error_handler.print("Failed to load automated builder fallback module.", level="error", exit_code=1)

    error_handler.print("Initialization Complete: All repository structure dependencies verified successfully.", level="notice")
    sys.exit(0)
