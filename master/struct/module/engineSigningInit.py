# ==========================================================================
# EXISTENZ  master/struct/module/engineSigningInit.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
from engineSigningMeta import existenzLocations

def execute(args, error_handler, repo_root: str):
    """
    Modular execution block for -stage init.
    Audits the presence of all configured infrastructure elements.
    """
    error_handler.print("Initiating structural integrity baseline pre-flight check...", level="notice")
    failed_initialization = False

    # 1. Audit Realm: Core Layout Configuration Primitives
    for token, relative_path in existenzLocations["core"].items():
        full_target_path = os.path.join(repo_root, relative_path)
        if not os.path.exists(full_target_path):
            error_handler.print(f"Core structural asset reference '{token}' missing at: {relative_path}", level="warning")
            failed_initialization = "config"
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

    # 3. Final Multi-Fault Boundary Evaluation Check
    if failed_initialization == "config":
        error_handler.print("Pre-flight execution blocked: Missing core layout dependency structures.", level="error", exit_code=16)
    elif failed_initialization == "init":
        error_handler.print("Pre-flight execution blocked: Missing system execution library modules.", level="error", exit_code=15)

    error_handler.print("Initialization Complete: All repository structure dependencies verified successfully.", level="notice")
    sys.exit(0)
