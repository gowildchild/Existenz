# ==========================================================================
# EXISTENZ  master/struct/module/cliStateInit.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
import shutil
from engineSigningMeta import existenzLocations

# Force Python to look inside the parent master/struct vault directory
PARENT_STRUCT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_STRUCT_DIR not in sys.path:
    sys.path.insert(0, PARENT_STRUCT_DIR)

# Now the library will import flawlessly without throwing a 254 exception!
import engineBuilderLibrary

def execute(args, error_handler, repo_root: str):
    """
    Modular execution block for -stage init.
    Scans runtime targets and dynamically self-heals the repository workspace
    by creating engine stubs, copying configurations, and compiling python classes.
    """
    error_handler.print("Initiating structural integrity baseline pre-flight check...", level="notice")
    
    failed_initialization = False
    core_assets_to_sync = {}
    engine_assets_to_sync = {}

    # 1. Audit Realm: Core Layout Configuration Primitives & Output Targets
    for token, relative_path in existenzLocations["core"].items():
        full_target_path = os.path.join(repo_root, relative_path)
        
        if not os.path.exists(full_target_path):
            if token == "Schema":
                error_handler.print(f"Fatal Initialization fault: Master blueprint '{token}' missing at: {relative_path}", level="warning")
                failed_initialization = "config"
            else:
                filename = os.path.basename(relative_path)
                error_handler.print(f"Runtime target '{token}' ({filename}) missing from workspace. Scheduled for adaptation.", level="warning")
                core_assets_to_sync[token] = {
                    "runtime_path": relative_path,
                    "filename": filename
                }
        else:
            error_handler.print(f"Core Asset Verified:   {relative_path:<40} [FOUND]")

    if failed_initialization == "config":
        error_handler.print("Pre-flight execution blocked: Missing core layout master schema structure.", level="error", exit_code=16)

    # 2. Audit Realm: Operational Library Infrastructure Engine Components
    for token, relative_path in existenzLocations["engine"].items():
        clean_rel_path = relative_path.split(":")[-1] if ":" in relative_path else relative_path
        full_target_path = os.path.join(repo_root, clean_rel_path)
        
        if not os.path.exists(full_target_path):
            filename = os.path.basename(clean_rel_path)
            error_handler.print(f"Engine resource component '{token}' ({filename}) missing. Scheduled for stubbing.", level="warning")
            engine_assets_to_sync[token] = {
                "runtime_path": clean_rel_path,
                "filename": filename
            }
        else:
            error_handler.print(f"Engine Asset Verified: {clean_rel_path:<40} [FOUND]")

    # 3. Execution Phase: Self-Heal and Provision Missing Workspace Blocks
    if core_assets_to_sync or engine_assets_to_sync:
        error_handler.print(" [*] Pre-flight Scan Complete: Bootstrapping runtime environment configurations...", level="notice")
        schema_path = os.path.join(repo_root, existenzLocations["core"]["Schema"])
        
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
        except Exception as e:
            error_handler.print(f"Failed to parse master schema JSON database layers: {e}", level="error", exit_code=16)

        version_str = "v0.76.16"

        # A. Self-Heal Core Runtime Files
        for token, asset_data in core_assets_to_sync.items():
            target_path = os.path.join(repo_root, asset_data["runtime_path"])
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            if filename.endswith(".json"):
                try:
                    shutil.copy2(schema_path, target_path)
                    error_handler.print(f"    [->] Synced Core Mirror: {token:<12} -> Blueprint copied to root.", level="info")
                except Exception as e:
                    error_handler.print(f"Failed to clone JSON boundary layer {token}: {e}", level="error", exit_code=1)
            
            elif filename.endswith(".py"):
                if token == "Core":
                    engineBuilderLibrary._export_python_framework(
                        dist_dir=os.path.dirname(target_path),
                        core_registry=schema_data["existentialCore"],
                        version_str=version_str,
                        w={
                            'f_expr': lambda v: "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}"),
                            'py_c': max(len(f"    {k} = " + ("0" if d["val"] <= 0 else (f"1 << {d['val'].bit_length() - 1}" if (d["val"] & (d["val"] - 1)) == 0 else f"0x{d['val']:08x}"))) for k, d in schema_data["existentialCore"].items()) + 2
                        },
                        header=engineBuilderLibrary.make_header(version_str, "#")
                    )
                    single_out = os.path.join(os.path.dirname(target_path), "python", "single", "existentialCore.py")
                    if os.path.exists(single_out):
                        shutil.move(single_out, target_path)
                        shutil.rmtree(os.path.join(os.path.dirname(target_path), "python"))
                    error_handler.print(f"    [->] Compiled Enums Matrix: Core         -> Generated existentialCore.py", level="info")

                elif token == "Threat":
                    try:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write("from enum import IntFlag\n\nclass existentialCoreThreat(IntFlag):\n")
                            for k, d in schema_data["existentialCore"].items():
                                if "threat" in d:
                                    v = d["val"]
                                    expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                    f.write(f"    {d['threat']:<30} = {expr}\n")
                        error_handler.print(f"    [->] Compiled Enums Matrix: Threat       -> Generated existentialCoreThreat.py", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to generate threat file: {e}", level="error", exit_code=1)
                else:
                    struct_source = os.path.join(repo_root, "master", "struct", filename)
                    if os.path.exists(struct_source):
                        shutil.copy2(struct_source, target_path)
                        error_handler.print(f"    [->] Synced Script Asset: {token:<12} -> Restored from vault.", level="info")

        # B. Self-Heal Missing Engine Opcodes & Stubs
        for token, asset_data in engine_assets_to_sync.items():
            target_path = os.path.join(repo_root, asset_data["runtime_path"])
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if filename.startswith("cliState") and filename.endswith(".py"):
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(engineBuilderLibrary.make_header(version_str, "#"))
                    f.write(f"# Auto-generated Operational Controller State Stub for {token}\n\n")
                    f.write("def execute(args, error_handler, repo_root):\n")
                    f.write(f"    error_handler.print('{token} phase initialized.', level='notice')\n")
                error_handler.print(f"    [->] Provisioned State Hook:  {token:<16} -> Stub generated.", level="info")
                
            elif filename.endswith(".json"):
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump({"existentialCore": {}, "comment": f"Auto-initialized dictionary envelope layer for {token}"}, f, indent=2)
                error_handler.print(f"    [->] Seeded Data Blueprint:   {token:<16} -> JSON template written.", level="info")

    error_handler.print("Initialization Complete: All repository structure dependencies verified and self-healed.", level="notice")
    sys.exit(0)
