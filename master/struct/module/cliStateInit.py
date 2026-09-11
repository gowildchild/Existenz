# ==========================================================================
# EXISTENZ master/struct/module/cliStateInit.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
import shutil
from engineSigningMeta import existenzLocations, existenzMeta

# 1. OPTIMIZE SCROLL SCOPE FIRST: Force Python to unlock parent folder visibility
PARENT_STRUCT_MASTER = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_STRUCT_MASTER not in sys.path:
    sys.path.insert(0, PARENT_STRUCT_MASTER)

# 2. SAFE NATIVE IMPORTS: Now resolves flawlessly from the active parent search path
import engineBuilderLibrary
from engineSigningStruct import existenzIntegrityGlue, existenzCorePolicy

def execute(args, error_handler, repo_root: str):
    """
    Modular execution block for -stage init.
    Scans runtime targets and dynamically self-heals the repository workspace
    by writing engine stubs, copying configurations, and compiling python classes.
    """
    error_handler.print("Initiating structural integrity baseline pre-flight check...", level="notice")
    error_handler.print(f" [TARGET ROOT] {os.path.abspath(repo_root)}", level="info")

    # Analyze the structural glue data definitions array dynamically
    virtual_tokens = []
    for glue_key, glue_tuple in existenzIntegrityGlue.items():
        if isinstance(glue_tuple, tuple) and len(glue_tuple) > 1:
            glue_bitmask = glue_tuple[1]
            if bool(glue_bitmask & 512):
                virtual_tokens.append(glue_key)

    failed_initialization = False
    core_assets_to_sync = {}
    engine_assets_to_sync = {}

    # 1. Audit Realm: Core Layout Configuration Primitives & Output Targets
    for token, relative_path in existenzLocations["core"].items():
        if token in virtual_tokens:
            error_handler.print(f" [+] Virtual Key Bypassed: {token:<24} -> Regulated by signature chain.", level="debug")
            continue
            
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

        version_str = schema_data.get("existentialMeta", {}).get("CoreVersion", "v0.76.09")
        meta_block = schema_data.get("existentialMeta", {})
        magic_raw = meta_block.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")

        try:
            fields = magic_raw.split(":")
            magic_tag = ":".join([str(meta_block.get(field, "UNKNOWN")) for field in fields])
        except Exception:
            magic_tag = "Existenz:v0.76.20:EX25IMMUT32CORE7617"

        # A. Self-Heal Core Runtime Files (Compiling directly to final destination)
        for token, asset_data in core_assets_to_sync.items():
            target_path = os.path.abspath(os.path.join(repo_root, asset_data["runtime_path"]))
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if token in ["SignaturesPy", "SignaturesJson"] or filename == "existentialCores.json":
                try:
                    import engineSigningLibrary
                    live_json, live_replacements = engineSigningLibrary.compute_blueprint_signature_matrix(
                        repo_root, schema_data, magic_tag
                    )
                    is_json_format = filename.endswith(".json")
                    
                    if is_json_format:
                        with open(target_path, "w", encoding="utf-8") as sf_out:
                            json.dump(live_json, sf_out, indent=2)
                    else:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write("# " + "="*74 + "\n")
                            f.write(f"# EXISTENZ GENERATED SYSTEM SIGNATURES LEDGER\n")
                            f.write("# Released under strict Non-Commercial Open-Source License terms.\n")
                            f.write("# " + "="*74 + "\n\n")
                            f.write("from engineSigningMeta import existenzLocations, existenzMeta\n\n")
                            f.write("existentialToken = {\n")
                            
                            for block_name in ["MAGIC", "master", "chain", "manifest", "structs", "engine"]:
                                f.write(f'    "{block_name}": {{\n')
                                inner_dict = live_json["existentialToken"][block_name]
                                for mk, mv in inner_dict.items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                if f.tell() > 2:
                                    f.seek(f.tell() - 2, 0)
                                    f.write("\n")
                                f.write("    },\n")
                            f.seek(f.tell() - 2, 0)
                            f.write("\n}\n")
                            
                    error_handler.print(f"    [SYNC LAYER] Recreated and synchronized authoritative blueprint ledger file at: {target_path}", level="info")
                except Exception as e:
                    error_handler.print(f"Failed executing auto-heal blueprint generation track for {filename}: {e}", level="error", exit_code=1)

            elif filename.endswith(".json") and token == "Cores":
                try:
                    import engineSigningLibrary
                    
                    core_lines = []
                    calculated_basic = []
                    calculated_immutable = []
                    core_source_data = schema_data.get("existentialCore", {})
                    
                    for k, d in core_source_data.items():
                        if not isinstance(d, dict) or "val" not in d or "pol" not in d:
                            continue
                        v = d["val"]
                        raw_pol = d["pol"]
                        pol = int(raw_pol, 16) if str(raw_pol).startswith("0x") else int(raw_pol)
                        
                        if v <= 0: expr = "0"
                        elif (v & (v - 1)) == 0: expr = f"1 << {v.bit_length() - 1}"
                        else: expr = f"0x{v:08x}"
                        
                        struct_type = "PILLAR"
                        if bool(pol & 2): struct_type = "RIGHTS"
                        elif bool(pol & 16): struct_type = "CANARY"
                        elif bool(pol & 8): struct_type = "SIGNATURE"
                        
                        if k != "NONE" and bool(pol & 262144):
                            calculated_immutable.append(f'    "{k}"')
                            if bool(pol & 1) or bool(pol & 2):
                                calculated_basic.append(f'    "{k}"')
                                
                        val_string = f"{v},".ljust(12)
                        line_entry = f'    "{k}":'.ljust(33) + f'{{ "val": {val_string}"expr": "{expr}",'.ljust(55) + f'"type": "{struct_type}", "comment": "{d.get("comment", "")}" }}'
                        core_lines.append(line_entry)
                        
                    cores_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                        repo_root, schema_data, "existentialCores", group_filter_id=None
                    )
                    
                    json_str_payload = "{\n"
                    json_str_payload += '  "existentialCore": {\n' + ",\n".join(core_lines) + "\n  },\n"
                    json_str_payload += f'  "existenzIntegrity": {json.dumps(cores_integrity_dict, indent=2)}\n}}'
                    
                    with open(target_path, "w", encoding="utf-8") as custom_out:
                        custom_out.write(json_str_payload)
                except Exception as e:
                    error_handler.print(f"Failed to clone JSON boundary layer {token}: {e}", level="error", exit_code=1)

            elif filename.endswith(".py") and token == "Core":
                try:
                    import engineSigningLibrary
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(engineBuilderLibrary.make_header(version_str, "#"))
                        f.write("from enum import IntFlag\n\nclass existentialCore(IntFlag):\n")
                        
                        core_source_data = schema_data.get("existentialCore", {})
                        for k, d in core_source_data.items():
                            if not isinstance(d, dict) or "val" not in d:
                                continue
                            v = d["val"]
                            expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                            f.write(f"    {k:<30} = {expr}  # {d.get('comment', '')}\n")
                            
                        core_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                            repo_root, schema_data, "existentialCore", group_filter_id=0x02
                        )
                        f.write(engineSigningLibrary.serialize_integrity_block_to_python(core_integrity_dict))
                except Exception as e:
                    error_handler.print(f"Failed to compile existentialCore.py: {e}", level="error", exit_code=1)

        # B. Self-Heal Missing Engine Opcodes & Stubs
        for token, asset_data in engine_assets_to_sync.items():
            target_path = os.path.abspath(os.path.join(repo_root, asset_data["runtime_path"]))
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            if filename.startswith("cliState") and filename.endswith(".py"):
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(engineBuilderLibrary.make_header(version_str, "#"))
                    f.write("def execute(args, error_handler, repo_root):\n    pass\n")

    error_handler.print("Initialization Complete: All repository structure dependencies verified and self-healed.", level="notice")
    sys.exit(0)
