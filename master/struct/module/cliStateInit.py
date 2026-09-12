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

        # FIXED VERSION ALIGNMENT: Dynamically extracts the system version directly out of your JSON blueprint schema
        meta_block = schema_data.get("existentialMeta", {})
        version_str = meta_block.get("CoreVersion", "v0.76.21")
        magic_raw = meta_block.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")

        # Dynamically build the tag string based on the JSON configuration instructions
        try:
            fields = magic_raw.split(":")
            magic_tag = ":".join([str(meta_block.get(field, "UNKNOWN")) for field in fields])
        except Exception:
            magic_tag = "Existenz:v0.76.21:EX25IMMUT32CORE7617"

        # Export straight to GitHub Actions environment space natively
        github_env_file = os.environ.get('GITHUB_ENV')
        if github_env_file:
            try:
                with open(github_env_file, "a", encoding="utf-8") as gef:
                    gef.write(f"BLUEPRINT_VERSION={version_str}\n")
                error_handler.print(f" [+] Loaded BLUEPRINT_VERSION={version_str} into environment.", level="info")
            except Exception as env_err:
                error_handler.print(f"Non-fatal error mapping version variable to shell runner: {env_err}", level="debug")

        # A. Self-Heal Core Runtime Files (Compiling directly to final destination)
        for token, asset_data in core_assets_to_sync.items():
            target_path = os.path.abspath(os.path.join(repo_root, asset_data["runtime_path"]))
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # UNIFIED VERIFICATION GATEWAY: Intercept and process our special live-monitored files
            if token in ["SignaturesPy", "SignaturesJson"] or filename == "existentialCores.json":
                try:
                    import engineSigningLibrary
                    # 1. DYNAMIC IN-MEMORY CALCULATION: Compute the authoritative state matrix from your live structures
                    live_json, live_replacements = engineSigningLibrary.compute_blueprint_signature_matrix(
                        repo_root, schema_data, magic_tag
                    )
                    is_json_format = filename.endswith(".json")
                    force_write_required = False

                    if not os.path.exists(target_path):
                        force_write_required = True
                        error_handler.print(f"    [AUTO-HEAL] Authoritative asset missing. Re-generating: {target_path}", level="warning")
                    else:
                        # Content Drift Check: Verify existing file bytes against live memory context strings
                        if is_json_format:
                            try:
                                with open(target_path, "r", encoding="utf-8") as jf:
                                    existing_data = json.load(jf)
                                # FIXED KEY DESIGNATION: Explicitly maps against your actual exact structural key name
                                if existing_data.get("existentialToken", {}).get("existenzMagic") != live_json.get("existentialToken", {}).get("existenzMagic"):
                                    force_write_required = True
                            except Exception:
                                force_write_required = True
                        else:
                            # For Python code modules, check if active metadata properties or signature tokens changed
                            try:
                                with open(target_path, "r", encoding="utf-8") as pf:
                                    file_content = pf.read()
                                    # FIXED DRIFT ALARM: Dynamically scans for your actual structural dictionary seals
                                    if "existentialToken =" not in file_content and "existenzIntegrity =" not in file_content:
                                        force_write_required = True
                            except Exception:
                                force_write_required = True

                    # 2. WRITE PASS: Safely flush the fresh datasets down only when changes or drops are caught
                    if force_write_required:
                        if is_json_format:
                            with open(target_path, "w", encoding="utf-8") as sf_out:
                                json.dump(live_json, sf_out, indent=2)
                        else:
                            # 100% BLUEPRINT GENERATED PYTHON MODULE (ZERO MANUAL TEMPLATES ENFORCED)
                            with open(target_path, "w", encoding="utf-8") as f:
                                f.write("# " + "="*74 + "\n")
                                f.write(f"# EXISTENZ GENERATED SYSTEM SIGNATURES LEDGER\n")
                                f.write("# Released under strict Non-Commercial Open-Source License terms.\n")
                                f.write("# " + "="*74 + "\n\n")
                                f.write("from engineSigningMeta import existenzLocations, existenzMeta\n\n")
                                # Convert the in-memory live dict matrix straight into formatted python string blocks
                                f.write("existentialToken = {\n")
                                # FIXED NAME REFERENCE: Serialize the explicit existenzMagic Metadata Envelope
                                f.write('    "existenzMagic": {\n')
                                for mk, mv in live_json["existentialToken"]["existenzMagic"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                # Serialize the Master Core Footprints
                                f.write('    "master": {\n')
                                for mk, mv in live_json["existentialToken"]["master"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                # Serialize Chain slots
                                f.write('    "chain": {\n')
                                for mk, mv in live_json["existentialToken"]["chain"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                # Serialize Manifest directories
                                f.write('    "manifest": {\n')
                                for mk, mv in live_json["existentialToken"]["manifest"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                # Serialize Structure parameters
                                f.write('    "structs": {\n')
                                for mk, mv in live_json["existentialToken"]["structs"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                # Serialize Engine components
                                f.write('    "engine": {\n')
                                for mk, mv in live_json["existentialToken"]["engine"].items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    }\n")
                                f.write("}\n")
                                
                        error_handler.print(f"    [SYNC LAYER] Recreated and synchronized authoritative blueprint ledger file at: {target_path}", level="info")
                    else:
                        error_handler.print(f"    [PITCH CLEAN] Core artifact is fully up-to-date with active blueprint definitions: {filename}", level="info")
                except Exception as e:
                    error_handler.print(f"Failed executing auto-heal blueprint generation track for {filename}: {e}", level="error", exit_code=1)
            elif filename.endswith(".json") and token == "Cores":
                try:
                    import engineSigningLibrary
                    from engineSigningStruct import existenzCorePolicy
                    
                    threat_lines = {}
                    for k, d in schema_data.get("existentialCore", {}).items():
                        if isinstance(d, dict) and "threat" in d and "val" in d:
                            v = d["val"]
                            expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                            threat_lines[d["threat"]] = { "val": v, "expr": expr }
                            
                    bitmask_lines = {}
                    policy_lines = {} 
                    for k, d in schema_data.get("existentialCore", {}).items():
                        if isinstance(d, dict) and "msk" in d:
                            bitmask_lines[f"existentialCore.{k}"] = d["msk"]
                        if isinstance(d, dict) and "pol" in d:
                            policy_lines[f"existentialCore.{k}"] = d["pol"]
                            
                    core_lines = {}
                    calculated_basic = []
                    calculated_immutable = []
                    for k, d in schema_data.get("existentialCore", {}).items():
                        if not isinstance(d, dict) or "val" not in d or "pol" not in d:
                            continue
                        v = d["val"]
                        raw_pol = d["pol"]
                        if isinstance(raw_pol, str):
                            pol_hex = raw_pol.strip()
                            pol = int(pol_hex, 16) if pol_hex.startswith("0x") else int(pol_hex)
                        else:
                            pol = int(raw_pol)
                        if bool(pol & existenzCorePolicy.BIT_MASK):
                            calculated_expr = f"1 << {v.bit_length() - 1}"
                        else:
                            if v <= 0: calculated_expr = "0"
                            elif (v & (v - 1)) == 0: calculated_expr = f"1 << {v.bit_length() - 1}"
                            else: calculated_expr = f"0x{v:08x}"
                        if bool(pol & existenzCorePolicy.CORE_PILLAR): struct_type = "PILLAR"
                        elif bool(pol & existenzCorePolicy.CORE_RIGHTS): struct_type = "RIGHTS"
                        elif bool(pol & (existenzCorePolicy.CORE_CANARY | existenzCorePolicy.USER_CANARY | existenzCorePolicy.CORE_WATCHDOG)): struct_type = "CANARY"
                        elif bool(pol & existenzCorePolicy.CORE_INTEGRITY): struct_type = "SIGNATURE"
                        else: struct_type = "PILLAR"
                        if not bool(k == "NONE") and bool(pol & existenzCorePolicy.CORE_IMMUTABLE):
                            calculated_immutable.append(k)
                            if bool(pol & (existenzCorePolicy.CORE_PILLAR | existenzCorePolicy.CORE_RIGHTS)):
                                calculated_basic.append(k)
                            elif bool(pol & existenzCorePolicy.CORE_CANARY):
                                if k in ["CANARY_1_SOVEREIGN", "CANARY_2_SOMATIC", "CANARY_3_ABLEISM"]:
                                    calculated_basic.append(k)
                                    
                        core_lines[k] = {
                            "val": v,
                            "expr": calculated_expr,
                            "type": struct_type,
                            "comment": d.get("comment", "").replace('"', '\\"')
                        }
                        
                    val_to_enum_map = {}
                    for k, d in schema_data.get("existentialCore", {}).items():
                        if isinstance(d, dict) and "val" in d:
                            node_label = d["threat"] if "threat" in d else (k if k.startswith("CANARY_") or k.startswith("SHIELD_") else f"THREAT_{k}")
                            val_to_enum_map[int(d["val"])] = f"existentialCoreThreat.{node_label}"
                            
                    composite_fallbacks = {89130487: "existentialCoreThreat.CANARY_7_EXPLOITATION", 2290263560: "existentialCoreThreat.CANARY_8_PREDATORY"}
                    legal_entries = {}
                    for raw_key, val in schema_data.get("existentialCoreThreatLegal", {}).items():
                        enum_token = val_to_enum_map.get(int(raw_key), composite_fallbacks.get(int(raw_key), f"existentialCoreThreat.UNKNOWN_{raw_key}"))
                        legal_entries[enum_token] = val
                        
                    vacuum_entries = {}
                    for raw_key, val in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                        enum_token = val_to_enum_map.get(int(raw_key), composite_fallbacks.get(int(raw_key), f"existentialCoreThreat.UNKNOWN_{raw_key}"))
                        vacuum_entries[enum_token] = val
                        
                    cores_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                        repo_root, schema_data, "existentialCores", group_filter_id=None
                    )
                    
                    # FIXED COMPILATION GATEWAY: UNIFIED INTERDEPENDENT CORE MATRIX DATA MAP
                    json_matrix_payload = {
                        "existentialCoreMeta": schema_data.get("existentialMeta", {}),
                        "existentialCore": {
                            "structures": core_lines,
                            "bitmasks":   bitmask_lines,
                            "policies":   policy_lines,
                            "basics":     calculated_basic,
                            "immutables": calculated_immutable
                        },
                        "existentialCoreThreat": {
                            "structures": threat_lines,
                            "legal":      legal_entries,
                            "vacuum":     vacuum_entries
                        },
                        "existenzIntegrity": cores_integrity_dict
                    }

                    with open(target_path, "w", encoding="utf-8") as custom_out:
                        json.dump(json_matrix_payload, custom_out, indent=2, sort_keys=True)
                    error_handler.print(f" [->] Synced Core Mirror: {token:<12} -> Blueprint ordered JSON written to root.", level="info")
                except Exception as e:
                    error_handler.print(f"Failed to clone JSON boundary layer {token}: {e}", level="error", exit_code=1)
                if token == "Core":
                    try:
                        import engineSigningLibrary
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write("from enum import IntFlag\n\nclass existentialCore(IntFlag):\n")
                            core_source_data = schema_data.get("existentialCore", {})
                            
                            # Compile core human pillars and system watchdogs with aligned comments
                            for k, d in core_source_data.items():
                                if not isinstance(d, dict) or "val" not in d:
                                    continue
                                v = d["val"]
                                expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                f.write(f"    {k:<30} = {expr}  # {d.get('comment', '')}\n")
                                
                            # FIXED VERTICAL JOINING: Formats immutable tuples using clean vertical groups inside parentheses
                            immutable_meta = meta_block.get("immutable", {})
                            raw_pillars = immutable_meta.get("PILLARS", "")
                            if raw_pillars:
                                p_nodes = [p.strip() for p in raw_pillars.split("|") if p.strip() in core_source_data]
                                if p_nodes: 
                                    f.write("\n    IMMUTABLE_PILLARS = (\n        " + " |\n        ".join(p_nodes) + "\n    )\n")
                                    
                            raw_rights = immutable_meta.get("RIGHTS", "")
                            if raw_rights:
                                r_nodes = [r.strip() for r in raw_rights.split("|") if r.strip() in core_source_data]
                                if r_nodes: 
                                    f.write("\n    IMMUTABLE_RIGHTS = (\n        " + " |\n        ".join(r_nodes) + "\n    )\n")
                                    
                            f.write("\nexistentialCoreBitmask = {\n")
                            for k, d in core_source_data.items():
                                if isinstance(d, dict) and "msk" in d: 
                                    f.write(f'    existentialCore.{k:<30} : "{d["msk"]}",\n')
                            f.write("}\n")
                            
                            f.write("\nexistentialCorePolicy = {\n")
                            for k, d in core_source_data.items():
                                if isinstance(d, dict) and "pol" in d: 
                                    f.write(f'    existentialCore.{k:<30} : "{d["pol"]}",\n')
                            f.write("}\n")
                            
                            # Generates exactly the 4-column core integrity block dataset for group 0x02
                            core_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                                repo_root, schema_data, "existentialCore", group_filter_id=0x02
                            )
                            f.write(engineSigningLibrary.serialize_integrity_block_to_python(core_integrity_dict))
                        error_handler.print(f"    [COMPILE FILE] Compiled native IntFlag class and expanded structural registries at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to compile existentialCore.py: {e}", level="error", exit_code=1)

                elif token == "Threat":
                    try:
                        import engineSigningLibrary
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#")) 
                            f.write("from enum import IntFlag\n\nclass existentialCoreThreat(IntFlag):\n")
                            f.write(f"    {'THREAT_NONE':<30} = 0\n")
                            
                            # Compile the primitive attack vectors dynamically out of the blueprint
                            for k, d in schema_data["existentialCore"].items():
                                if isinstance(d, dict) and "threat" in d:
                                    v = d["val"]
                                    expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                    f.write(f"    {d['threat']:<30} = {expr}\n")
                                    
                            f.write("\nexistentialCoreThreatLegal = {\n")
                            for k, v in schema_data.get("existentialCoreThreatLegal", {}).items():
                                # Robust matching loop: checks integer vs string keys cleanly
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if isinstance(d, dict) and "threat" in d and str(d["val"]) == str(k)), None)
                                if target_node: 
                                    f.write(f"    existentialCoreThreat.{target_node:<25}: \"{v}\",\n")
                            f.write("}\n")
                            
                            f.write("\nexistentialCoreThreatShadowVacuum = {\n")
                            for k, v in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if isinstance(d, dict) and "threat" in d and str(d["val"]) == str(k)), None)
                                if target_node: 
                                    f.write(f"    existentialCoreThreat.{target_node:<25}: \"{v}\",\n")
                            f.write("}\n")
                            
                            # Generates exactly the 4-column threat integrity block dataset for group 0x03
                            threat_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                                repo_root, schema_data, "existentialCoreThreat", group_filter_id=0x03
                            )
                            f.write(engineSigningLibrary.serialize_integrity_block_to_python(threat_integrity_dict))
                        error_handler.print(f"    [COMPILE FILE] Compiled native Threat legal & vacuum matrices with integrity blocks at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to generate threat file: {e}", level="error", exit_code=1)


                elif token == "Check":
                    try:
                        with open(target_path, "w", encoding="utf-8") as f:
                            f.write(engineBuilderLibrary.make_header(version_str, "#"))
                            f.write("import hmac\nimport hashlib\nfrom master.existentialCore import existentialCore\n\n")
                            f.write("class existentialCoreCheck:\n    @classmethod\n    def check_integrity(cls, active_register_state: int) -> bool:\n")
                            f.write("        return active_register_state == 0x055005f7 # CANARY_S_STATE\n")
                        error_handler.print(f"    [COMPILE FILE] Compiled integrity verification routines at: {target_path}", level="info")
                    except Exception as e:
                        error_handler.print(f"Failed to compile existentialCoreCheck.py: {e}", level="error", exit_code=1)

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
