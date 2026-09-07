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

# Register the absolute parent vault directory to ensure all helper references resolve
PARENT_STRUCT_MASTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_STRUCT_MASTER not in sys.path:
    sys.path.insert(0, PARENT_STRUCT_MASTER)

import engineBuilderLibrary

def execute(args, error_handler, repo_root: str):
    """
    Modular execution block for -stage init.
    Scans runtime targets and dynamically self-heals the repository workspace
    by writing engine stubs, copying configurations, and compiling python classes.
    """
    error_handler.print("Initiating structural integrity baseline pre-flight check...", level="notice")
    error_handler.print(f"  [TARGET ROOT] {os.path.abspath(repo_root)}", level="info")
    
    failed_initialization = False
    core_assets_to_sync = {}
    engine_assets_to_sync = {}

    # 1. Audit Realm: Core Layout Configuration Primitives & Output Targets
    for token, relative_path in existenzLocations["core"].items():
        full_target_path = os.path.abspath(os.path.join(repo_root, relative_path))
        
        if not os.path.exists(full_target_path):
            if token == "Schema":
                error_handler.print(f"Fatal Initialization fault: Master blueprint '{token}' missing at: {full_target_path}", level="warning")
                failed_initialization = "config"
            else:
                filename = os.path.basename(relative_path)
                error_handler.print(f"Runtime target '{token}' missing -> Scheduled for write at: {full_target_path}", level="warning")
                core_assets_to_sync[token] = {
                    "runtime_path": relative_path,
                    "filename": filename
                }
        else:
            error_handler.print(f"Verified [FOUND]: {full_target_path}", level="info")

    if failed_initialization == "config":
        error_handler.print("Pre-flight execution blocked: Missing core layout master schema structure.", level="error", exit_code=16)

    # 2. Audit Realm: Operational Library Infrastructure Engine Components
    for token, relative_path in existenzLocations["engine"].items():
        clean_rel_path = relative_path.split(":")[-1] if ":" in relative_path else relative_path
        full_target_path = os.path.abspath(os.path.join(repo_root, clean_rel_path))
        
        if not os.path.exists(full_target_path):
            filename = os.path.basename(clean_rel_path)
            error_handler.print(f"Engine submodule component '{token}' missing -> Scheduled for stubbing at: {full_target_path}", level="warning")
            engine_assets_to_sync[token] = {
                "runtime_path": clean_rel_path,
                "filename": filename
            }
        else:
            error_handler.print(f"Verified [FOUND]: {full_target_path}", level="info")

    # 3. Execution Phase: Self-Heal and Provision Missing Workspace Blocks
    if core_assets_to_sync or engine_assets_to_sync:
        error_handler.print(" [*] Pre-flight Scan Complete: Bootstrapping runtime environment configurations...", level="notice")
        schema_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["Schema"]))
        
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
        except Exception as e:
            error_handler.print(f"Failed to parse master schema JSON database layers: {e}", level="error", exit_code=16)

        version_name = "module/cliStateInit.py"
        
        # Dynamic Extraction: Read version directly from the blueprint payload
        version_str = schema_data.get("existentialCoreVersion", schema_data.get("version", "v0.76.15"))

        # Export straight to GitHub Actions environment space natively
        github_env_file = os.environ.get('GITHUB_ENV')
        if github_env_file:
            try:
                with open(github_env_file, "a", encoding="utf-8") as gef:
                    gef.write(f"BLUEPRINT_VERSION={version_str}\n")
                error_handler.print(f"  [+] Dynamic Context Export: Loaded BLUEPRINT_VERSION={version_str} into environment map.", level="info")
            except Exception as env_err:
                error_handler.print(f"Non-fatal error mapping version variable to shell runner: {env_err}", level="debug")

        # A. Self-Heal Core Runtime Files (Compiling directly to final destination)
        for token, asset_data in core_assets_to_sync.items():
            target_path = os.path.abspath(os.path.join(repo_root, asset_data["runtime_path"]))
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            if filename.endswith(".json"):
                try:
                    if token == "Cores":
                        # Isolate ONLY the primary human core layout parameters to protect data boundaries
                        isolated_cores_block = {
                            "existentialCore": schema_data.get("existentialCore", {})
                        }
                        with open(target_path, "w", encoding="utf-8") as json_out:
                            json.dump(isolated_cores_block, json_out, indent=2)
                        error_handler.print(f"    [WRITE FILE] Created isolated cores database mirror at: {target_path}", level="info")
                    else:
                        shutil.copy2(schema_path, target_path)
                        error_handler.print(f"    [WRITE FILE] Created raw json blueprint mirror at: {target_path}", level="info")
                except Exception as e:
                    error_handler.print(f"Failed to clone JSON boundary layer {token}: {e}", level="error", exit_code=1)
            
            elif filename.endswith(".py"):
                if token == "Core":
                    try:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write("from enum import IntFlag\n\nclass existentialCore(IntFlag):\n")
                            for k, d in schema_data["existentialCore"].items():
                                v = d["val"]
                                expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                f.write(f"    {k:<30} = {expr}  # {d.get('comment', '')}\n")
                            
                            f.write("\nexistentialCoreBitmask = {\n")
                            for k, d in schema_data["existentialCore"].items():
                                if "msk" in d:
                                    f.write(f"    existentialCore.{k}: \"{d['msk']}\",\n")
                            f.write("}\n")
                        error_handler.print(f"    [COMPILE FILE] Compiled native IntFlag class and Bitmasks at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to compile existentialCore.py: {e}", level="error", exit_code=1)

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
                                    
                            f.write("\nexistentialCoreThreatLegal = {\n")
                            for k, v in schema_data.get("existentialCoreThreatLegal", {}).items():
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if "threat" in d and str(d["val"]) == k), None)
                                if target_node: f.write(f"    existentialCoreThreat.{target_node}: \"{v}\",\n")
                            f.write("}\n")

                            f.write("\nexistentialCoreThreatShadowVacuum = {\n")
                            for k, v in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if "threat" in d and str(d["val"]) == k), None)
                                if target_node: f.write(f"    existentialCoreThreat.{target_node}: \"{v}\",\n")
                            f.write("}\n")
                        error_handler.print(f"    [COMPILE FILE] Compiled native Threat legal & vacuum matrices at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to generate threat file: {e}", level="error", exit_code=1)

                elif token == "Check":
                    try:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write("import hmac\nimport hashlib\nfrom master.existentialCore import existentialCore\n\n")
                            f.write("class existentialCoreCheck:\n    @classmethod\n    def check_integrity(cls, active_register_state: int) -> bool:\n")
                            f.write("        return active_register_state == 0x055005f7  # CANARY_S_STATE\n")
                        error_handler.print(f"    [COMPILE FILE] Compiled integrity verification routines at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to compile existentialCoreCheck.py: {e}", level="error", exit_code=1)

                elif token == "Signatures":
                    try:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write(f"existentialCoreVersion = \"{version_str}\"\n")
                            f.write("existentialCoreCheckMagic = b\"EX25IMMUT32CORE7617\"\n\n")
                            f.write("class existentialCoreSignatures:\n    existentialCoreSigned = (\n")
                            f.write("        (\"Magic\", \"magic\", \"existentialCoreMagicHash\", \"\", 2, 0),\n")
                            f.write("        (\"Core\", \"core\", \"existentialCoreHash\", \"\", 12, 1),\n")
                            f.write("    )\n")
                        error_handler.print(f"    [COMPILE FILE] Compiled signature tracking registries at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to compile existentialCoreSignatures.py: {e}", level="error", exit_code=1)
                else:
                    struct_source = os.path.abspath(os.path.join(repo_root, "master", "struct", filename))
                    if os.path.exists(struct_source):
                        shutil.copy2(struct_source, target_path)
                        error_handler.print(f"    [SYNC FILE] Replicated fixed structural library component to: {target_path}", level="info")

        # B. Self-Heal Missing Engine Opcodes & Stubs
        for token, asset_data in engine_assets_to_sync.items():
            target_path = os.path.abspath(os.path.join(repo_root, asset_data["runtime_path"]))
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if filename.startswith("cliState") and filename.endswith(".py"):
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(engineBuilderLibrary.make_header(version_str, "#"))
                    f.write(f"# Auto-generated Operational Controller State Stub for {token}\n\n")
                    f.write("def execute(args, error_handler, repo_root):\n")
                    f.write(f"    error_handler.print('{token} phase initialized.', level='notice')\n")
                error_handler.print(f"    [STUB FILE] Provisioned operational execution script stub at: {target_path}", level="info")
                
            elif filename.endswith(".json"):
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump({"existentialCore": {}, "comment": f"Auto-initialized dictionary envelope layer for {token}"}, f, indent=2)
                error_handler.print(f"    [SEED FILE] Seeded empty structural JSON framework at: {target_path}", level="info")

    error_handler.print("Initialization Complete: All repository structure dependencies verified and self-healed.", level="notice")
    sys.exit(0)
