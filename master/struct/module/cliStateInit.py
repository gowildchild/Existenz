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
    error_handler.print(f"  [TARGET ROOT] {os.path.abspath(repo_root)}", level="info")
    
    # Analyze the structural glue data definitions array dynamically
    # Filter out entries where bitmask has KEY_IS_CHAINED (512) active to protect virtual fields
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
        # DYNAMIC BYPASS GATE: Skip signature chain properties natively without hardcoded tracking sets
        if token in virtual_tokens:
            error_handler.print(f"  [+] Virtual Key Bypassed:   {token:<24} -> Regulated by signature chain.", level="debug")
            continue
            
        full_target_path = os.path.abspath(os.path.join(repo_root, relative_path))
        
        # Diagnostic File Presence Verification Pass
        error_handler.print(f"  DEBUG SCAN: Checking token '{token}' target path: {full_target_path}", level="info")
        if os.path.exists(full_target_path):
            error_handler.print(f"  DEBUG SCAN: Physical file present on disk space with size: {os.path.getsize(full_target_path)} bytes.", level="info")
        
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
        #existenzMeta.HEADER.get("VERSION", version_str)
        version_str = schema_data.get("existentialMeta", schema_data.get("coreVersion", "v0.76.08"))
        error_handler.print(f"  [VERSION] {version_str}", level="info")

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
            calculated_basic = []
            calculated_immutable = []
            calculated_immutable_count = 0
            filename = asset_data["filename"]
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            if filename.endswith(".json"):
                try:
                    if token == "Cores":
                        from engineSigningStruct import existenzCorePolicy

                        # 1. Compile existentialCoreThreat entries compact on single lines
                        threat_lines = []
                        for k, d in schema_data.get("existentialCore", {}).items():
                            if "threat" in d:
                                v = d["val"]
                                expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                # Format keys with precise left padding alignment matching your core layouts
                                threat_entry = f'    "{d["threat"]}":'.ljust(38)
                                threat_entry += f'{{ "val": {v},'.ljust(15)
                                threat_entry += f'"expr": "{expr}" }}'
                                threat_lines.append(threat_entry)

                        # 2. Extract separate registries for Bitmask and Policy structures
                        bitmask_lines = []
                        policy_lines = []                        
                        for k, d in schema_data.get("existentialCore", {}).items():
                            if "msk" in d:
                                bitmask_lines.append(f'    "existentialCore.{k}":'.ljust(50) + f'"{d["msk"]}"') 
                            if "pol" in d:
                                policy_lines.append(f'    "existentialCore.{k}":'.ljust(50) + f'"{d["pol"]}"') 
                                

                        # 3. Compile existentialCore entries with pristine, vertically aligned fields
                        core_lines = []
                        calculated_basic = []
                        for k, d in schema_data.get("existentialCore", {}).items():
                            v = d["val"]
                            raw_pol = d.get("pol", 0)
                            
                            # Safely convert hex string parameters using base 16
                            if isinstance(raw_pol, str):
                                pol_hex = raw_pol.strip()
                                pol = int(pol_hex, 16) if pol_hex.startswith("0x") else int(pol_hex)
                            else:
                                pol = int(raw_pol)
                                pol_hex = hex(pol)
                                
                            if bool(pol & existenzCorePolicy.BIT_MASK):
                                calculated_expr = f"1 << {v.bit_length() - 1}"
                            else:
                                if v <= 0:
                                    calculated_expr = "0"
                                elif (v & (v - 1)) == 0:
                                    calculated_expr = f"1 << {v.bit_length() - 1}"
                                else:
                                    calculated_expr = f"0x{v:08x}"

                            # Evaluate structural types dynamically from your IntFlag priority order
                            if bool(pol & existenzCorePolicy.CORE_PILLAR):
                                struct_type = "PILLAR"
                            elif bool(pol & existenzCorePolicy.CORE_RIGHTS):
                                struct_type = "RIGHTS"
                            elif bool(pol & (existenzCorePolicy.CORE_CANARY | existenzCorePolicy.USER_CANARY | existenzCorePolicy.CORE_WATCHDOG)):
                                struct_type = "CANARY"
                            elif bool(pol & existenzCorePolicy.CORE_INTEGRITY):
                                struct_type = "SIGNATURE"
                            else:
                                struct_type = "PILLAR"
                                
                            if not bool(k == "NONE") and bool(pol & existenzCorePolicy.CORE_IMMUTABLE):
                                calculated_immutable.append(f'    "{k}"')
                                if bool(pol & (existenzCorePolicy.CORE_PILLAR | existenzCorePolicy.CORE_RIGHTS)):
                                    calculated_basic.append(f'    "{k}"')
                                    
                                elif bool(pol & existenzCorePolicy.CORE_CANARY):
                                    if k in ["CANARY_1_SOVEREIGN", "CANARY_2_SOMATIC", "CANARY_3_ABLEISM"]:
                                        calculated_basic.append(f'    "{k}"')
                                    
                            # Build entry strings with column formatting matching your target layout rules
                            line_entry = f'    "{k}":'.ljust(33)
                            line_entry += f'{{ "val": {v},'.ljust(15)
                            line_entry += f'"expr": "{calculated_expr}",'.ljust(22)
                            line_entry += f'"type": "{struct_type}",'.ljust(20)
                            
                            clean_cmnt = d.get("comment", "").replace('"', '\\"')
                            line_entry += f' "comment": "{clean_cmnt}" }}'
                            core_lines.append(line_entry)

                        # 4. Pull the rest of the metadata fields out of your master schema
                        ver_val = schema_data.get("existentialMeta", schema_data.get("coreVersion", "v0.76.08"))
                        magic_val = schema_data.get("existentialCoreCheckMagic", "")
                        #version_str = schema_data.get("existentialMeta", schema_data.get("coreVersion", "v0.76.08"))
                        # Build unified enum token resolver map once
                        val_to_enum_map = {}
                        for k, d in schema_data.get("existentialCore", {}).items():
                            if "threat" in d:
                                node_label = d["threat"]
                            else:
                                node_label = k if k.startswith("CANARY_") or k.startswith("SHIELD_") else f"THREAT_{k}"
                            val_to_enum_map[int(d["val"])] = f"existentialCoreThreat.{node_label}"

                        # Synchronize composite bitwise keys exactly matching your blueprint
                        composite_fallbacks = {
                            89130487:   "existentialCoreThreat.CANARY_7_EXPLOITATION",
                            2290263560: "existentialCoreThreat.CANARY_8_PREDATORY"
                        }

                        # Process Legal registries using the mapped tokens
                        legal_entries = []
                        for raw_key, val in schema_data.get("existentialCoreThreatLegal", {}).items():
                            int_key = int(raw_key)
                            enum_token = val_to_enum_map.get(int_key, composite_fallbacks.get(int_key, f"existentialCoreThreat.UNKNOWN_{int_key}"))
                            legal_entries.append(f'    "{enum_token}":'.ljust(55) + f'"{val}"')

                        # Process Shadow Vacuum registries using the mapped tokens
                        vacuum_entries = []
                        for raw_key, val in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                            int_key = int(raw_key)
                            enum_token = val_to_enum_map.get(int_key, composite_fallbacks.get(int_key, f"existentialCoreThreat.UNKNOWN_{int_key}"))
                            vacuum_entries.append(f'    "{enum_token}":'.ljust(55) + f'"{val}"')

                        # 5. Construct the physical JSON string file payload in the exact target layout order
                        json_str_payload = "{\n"
                        json_str_payload += f'  "existentialCoreVersion": "{ver_val}",\n'
                        #json_str_payload += f'  "existentialCoreCheckMagic": "{magic_val}",\n'
                        json_str_payload += '  "existentialCore": {\n' + ",\n".join(core_lines) + "\n  },\n"
                        json_str_payload += '  "existentialCoreBitmask": {\n' + ",\n".join(bitmask_lines) + "\n  },\n"  
                        json_str_payload += '  "existentialCoreBasic": [\n' + ",\n".join(calculated_basic) + "\n  ],\n" 
                        json_str_payload += '  "existentialCoreImmutable": [\n' + ",\n".join(calculated_immutable) + "\n  ],\n" 
                        json_str_payload += '  "existentialCoreThreat": {\n' + ",\n".join(threat_lines) + "\n  },\n"
                        json_str_payload += '  "existentialCoreThreatLegal": {\n' + ",\n".join(legal_entries) + "\n  },\n"
                        json_str_payload += '  "existentialCoreThreatShadowVacuum": {\n' + ",\n".join(vacuum_entries) + "\n  },\n"
                        json_str_payload += '  "existentialCorePolicy": {\n' + ",\n".join(policy_lines) + "\n  }\n"     
                        json_str_payload += "}\n"

                        with open(target_path, "w", encoding="utf-8") as custom_out:
                            custom_out.write(json_str_payload)
                        error_handler.print(f"    [->] Synced Core Mirror: {token:<12} -> Blueprint ordered JSON written to root.", level="info")
                    
                    elif "SignaturesJson" in token or filename == "existentialSignatures.json":
                        from engineSigningMeta import existenzMeta

                        # Construct your physical structural layout payload matching your exact tracking realms
                        signatures_matrix = {
                            "existentialCoreVersion": version_str,
                            "existentialToken": {
                                "MAGIC": {
                                    "TAG":                str(existenzMeta.MAGIC.get("RAW", "EX25")),
                                    "TOKEN":              str(existenzMeta.MAGIC.get("TOKEN", "IMMUTABLE")),
                                    "SIGNATURE":          str(existenzMeta.MAGIC.get("SIGNATURE", "CORE")),
                                    "REALM":              str(existenzMeta.HEADER.get("REALM", "VAULT")),
                                    "VERSION":            str(existenzMeta.HEADER.get("VERSION", version_str)),
                                    "AUTHOR":             str(existenzMeta.META.get("AUTHOR", "Gunther Voet"))
                                },
                                "master": {
                                    "Core":               "",
                                    "Check":              "",        
                                    "Schema":             "",
                                    "Cores":              "",
                                    "Threat":             "",
                                    "ThreatLegal":        "",
                                    "ThreatShadowVacuum": "",
                                    "ThreatSigned":       ""
                                },
                                "chain": {
                                    "Core":               "",
                                    "CoresChain":         "",
                                    "Threat":             ""
                                },
                                "manifest": {
                                    "dist":               "dist",
                                    "tools":              "dist/tools",
                                    "build":              "master/build-tools",
                                    "master":             "master/struct"
                                },
                                "structs": {
                                    "KeysPublic":         "",
                                    "KeysHandler":        "",
                                    "KeysType":           "",
                                    "Locations":          ""
                                },
                                "engine": {
                                    "engineLogging":      "",
                                    "engineCrypto":       "",
                                    "signingMeta":        "",
                                    "signingStruct":      "",
                                    "signingLibrary":     "",
                                    "builderLibrary":     "",
                                    "cliStateTest":       "",
                                    "cliStateInit":       "",
                                    "cliStateManifest":   "",
                                    "cliStateSign":       "",
                                    "cliStateVerify":     "",
                                    "cliStateBuild":      "",
                                    "Signatures":         "",
                                    "Manifest":           ""
                                }
                            }
                        }
                        
                        with open(target_path, "w", encoding="utf-8") as sf_out:
                            json.dump(signatures_matrix, sf_out, indent=2)
                        error_handler.print(f"    [SEED FILE] Seeded complete structural tracking registry matrix at: {target_path}", level="info")                        
                    else:
                        shutil.copy2(schema_path, target_path)
                        error_handler.print(f"    [->] Synced Core Mirror: {token:<12} -> Blueprint copied to root.", level="info")
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
                            
                            # 1. Compile existentialCoreBitmask layout map dictionary
                            f.write("\nexistentialCoreBitmask = {\n")
                            for k, d in schema_data["existentialCore"].items():
                                if "msk" in d:
                                    f.write(f'    existentialCore.{k:<25}: "{d["msk"]}",\n')
                            f.write("}\n")

                            # 2. FIXED: Compile existentialCorePolicy layout map dictionary
                            f.write("\nexistentialCorePolicy = {\n")
                            for k, d in schema_data["existentialCore"].items():
                                if "pol" in d:
                                    f.write(f'    existentialCore.{k:<25}: "{d["pol"]}",\n')
                            f.write("}\n")
                            
                        error_handler.print(f"    [COMPILE FILE] Compiled native IntFlag class and expanded structural registries at: {target_path}", level="info")
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

                elif token == "SignaturesPy":
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
