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

            # UNIFIED VERIFICATION GATEWAY: Intercept and process signature matrices
            if token in ["SignaturesPy", "SignaturesJson"]:
                try:
                    import engineSigningLibrary
                    live_json, live_replacements = engineSigningLibrary.compute_blueprint_signature_matrix(
                        repo_root, schema_data, magic_tag
                    )
                    is_json_format = filename.endswith(".json")
                    force_write_required = False

                    if not os.path.exists(target_path):
                        force_write_required = True
                    else:
                        if is_json_format:
                            try:
                                with open(target_path, "r", encoding="utf-8") as jf:
                                    existing_data = json.load(jf)
                                t_old = existing_data.get("existentialToken", {})
                                t_new = live_json.get("existentialToken", {})
                                if t_old.get("existenzMagic", t_old.get("MAGIC")) != t_new.get("existenzMagic", t_new.get("MAGIC")):
                                    force_write_required = True
                            except Exception:
                                force_write_required = True
                        else:
                            try:
                                with open(target_path, "r", encoding="utf-8") as pf:
                                    file_content = pf.read()
                                if "existentialToken =" not in file_content and "existenzIntegrity =" not in file_content:
                                    force_write_required = True
                            except Exception:
                                force_write_required = True

                    if force_write_required:
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
                                
                                token_map = live_json.get("existentialToken", {})
                                magic_data = token_map.get("existenzMagic", token_map.get("MAGIC", {}))
                                
                                f.write('    "existenzMagic": {\n')
                                for mk, mv in magic_data.items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                
                                f.write('    "master": {\n')
                                for mk, mv in token_map.get("master", {}).items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                f.write('    "chain": {\n')
                                for mk, mv in token_map.get("chain", {}).items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                f.write('    "manifest": {\n')
                                for mk, mv in token_map.get("manifest", {}).items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                f.write('    "structs": {\n')
                                for mk, mv in token_map.get("structs", {}).items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    },\n")
                                f.write('    "engine": {\n')
                                for mk, mv in token_map.get("engine", {}).items():
                                    f.write(f'        "{mk}":'.ljust(25) + f'"{mv}",\n')
                                f.write("    }\n")
                                f.write("}\n")
                        error_handler.print(f"    [SYNC LAYER] Recreated authoritative blueprint ledger file at: {target_path}", level="info")
                    else:
                        error_handler.print(f"    [PITCH CLEAN] Core artifact is fully up-to-date with active blueprint definitions: {filename}", level="info")
                except Exception as e:
                    error_handler.print(f"Failed executing auto-heal blueprint generation track for {filename}: {e}", level="error", exit_code=1)
            
            elif filename.endswith(".json") and token == "Cores":
                try:
                    import engineSigningLibrary
                    from engineSigningStruct import existenzCorePolicy
                    
                    # 1. Compile pristine Threat register entries line-by-line
                    threat_lines = {}
                    for k, d in sorted(schema_data.get("existentialCore", {}).items()):
                        if isinstance(d, dict) and "threat" in d and "val" in d:
                            v = d["val"]
                            expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                            threat_lines[str(d["threat"]).strip()] = {
                                "expr": str(expr).strip(),
                                "val": int(v)
                            }
                            
                    bitmask_lines = {}
                    policy_lines = {} 
                    for k, d in sorted(schema_data.get("existentialCore", {}).items()):
                        if isinstance(d, dict) and "msk" in d:
                            bitmask_lines[f"existentialCore.{str(k).strip()}"] = str(d["msk"]).strip()
                        if isinstance(d, dict) and "pol" in d:
                            policy_lines[f"existentialCore.{str(k).strip()}"] = str(d["pol"]).strip()
                            
                    # 2. Compile detailed Structural maps with clean properties
                    core_lines = {}
                    calculated_basic = []
                    calculated_immutable = []
                    for k, d in sorted(schema_data.get("existentialCore", {}).items()):
                        if not isinstance(d, dict) or "val" not in d or "pol" not in d:
                            continue
                        v = d["val"]
                        raw_pol = d["pol"]
                        pol = int(raw_pol, 16) if isinstance(raw_pol, str) and raw_pol.strip().startswith("0x") else int(raw_pol)
                        
                        if bool(pol & existenzCorePolicy.BIT_MASK):
                            calculated_expr = f"1 << {v.bit_length() - 1}"
                        else:
                            calculated_expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                            
                        if bool(pol & existenzCorePolicy.CORE_PILLAR): struct_type = "PILLAR"
                        elif bool(pol & existenzCorePolicy.CORE_RIGHTS): struct_type = "RIGHTS"
                        elif bool(pol & (existenzCorePolicy.CORE_CANARY | existenzCorePolicy.USER_CANARY)): struct_type = "CANARY"
                        elif bool(pol & existenzCorePolicy.CORE_INTEGRITY): struct_type = "SIGNATURE"
                        else: struct_type = "PILLAR"
                        
                        clean_k = str(k).strip()
                        if clean_k != "NONE" and bool(pol & existenzCorePolicy.CORE_IMMUTABLE):
                            calculated_immutable.append(clean_k)
                            if bool(pol & (existenzCorePolicy.CORE_PILLAR | existenzCorePolicy.CORE_RIGHTS)):
                                calculated_basic.append(clean_k)
                            elif bool(pol & existenzCorePolicy.CORE_CANARY) and clean_k in ["CANARY_1_SOVEREIGN", "CANARY_2_SOMATIC", "CANARY_3_ABLEISM"]:
                                calculated_basic.append(clean_k)
                                
                        core_lines[clean_k] = {
                            "comment": str(d.get("comment", "")).replace('"', '\\"').strip(),
                            "expr": str(calculated_expr).strip(),
                            "type": struct_type,
                            "val": int(v)
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
                        legal_entries[enum_token.strip()] = val.strip()
                        
                    vacuum_entries = {}
                    for raw_key, val in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                        enum_token = val_to_enum_map.get(int(raw_key), composite_fallbacks.get(int(raw_key), f"existentialCoreThreat.UNKNOWN_{raw_key}"))
                        vacuum_entries[enum_token.strip()] = val.strip()
                        
                    cores_global_dict = engineSigningLibrary.generate_integrity_block_payload(
                        repo_root, schema_data, "existentialCores", group_filter_id=None
                    )
                    core_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                        repo_root, schema_data, "existentialCore", group_filter_id=0x02
                    )
                    threat_integrity_dict = engineSigningLibrary.generate_integrity_block_payload(
                        repo_root, schema_data, "existentialCoreThreat", group_filter_id=0x03
                    )
                    
                    # Convert raw lists of signature tuples into clean serializable objects
                    def convert_sigs_to_list(sig_payload):
                        if not sig_payload or "Signatures" not in sig_payload: return []
                        res_list = []
                        for row in sig_payload["Signatures"]:
                            if isinstance(row, (list, tuple)) and len(row) >= 4:
                                # Keep it as a raw, flat array row to pass straight to the vertical line serializer
                                res_list.append([str(row[0]).strip(), int(row[1]), str(row[2]).strip(), str(row[3]).strip()])
                        return res_list

                    # Convert public keys safely by accommodating tuple arrays natively
                    global_public_keys = {}
                    for row in cores_global_dict.get("PublicKeys", ()):
                        if isinstance(row, (list, tuple)) and len(row) >= 3:
                            global_public_keys[str(row[0]).strip()] = {
                                "key": str(row[1]).strip(),
                                "bit": int(row[2])
                            }

                    # ==========================================================================
                    # FORCED CHRONOLOGICAL TOPOLOGY PAYLOAD MATRIXBUILDER
                    # ==========================================================================
                    json_matrix_payload = {}
                    
                    json_matrix_payload["existentialCoreMeta"] = {
                        "CoreRealm":     str(meta_block.get("CoreRealm", "Existenz")).strip(),
                        "CoreVersion":   str(version_str).strip(),
                        "CoreMagic":     str(meta_block.get("CoreMagic", "UNKNOWN")).strip(),
                        "CoreMagicRaw":  str(magic_raw).strip(),
                        "CoreAuthor":    str(meta_block.get("CoreAuthor", "Gunther Voet")).strip()
                    }
                    
                    json_matrix_payload["existentialCore"] = {
                        "structures":  core_lines,
                        "bitmasks":    bitmask_lines,
                        "policies":    policy_lines,
                        "basics":      sorted([str(b).strip() for b in calculated_basic]),
                        "immutables":  sorted([str(m).strip() for m in calculated_immutable]),
                        "signatures":  convert_sigs_to_list(core_integrity_dict)
                    }
                    
                    json_matrix_payload["existentialCoreThreat"] = {
                        "structures":  threat_lines,
                        "legal":       legal_entries,
                        "vacuum":      vacuum_entries,
                        "signatures":  convert_sigs_to_list(threat_integrity_dict)
                    }
                    
                    json_matrix_payload["existenzIntegrity"] = {
                        "existentialCores": cores_global_dict.get("existentialCores", {}),
                        "PublicKeys":       global_public_keys,
                        "Signatures":       convert_sigs_to_list(cores_global_dict)
                    }
                    def emit_strict_json_lines(obj, depth=0):
                        indent = "  " * depth
                        next_indent = "  " * (depth + 1)
                        deep_indent = "  " * (depth + 2)

                        if isinstance(obj, dict):
                            if not obj:
                                return "{}"
                            lines = ["{"]
                            # Fixed top-down chronology tree alignment rules
                            ordered_keys = []
                            if "existentialCoreMeta" in obj: ordered_keys.append("existentialCoreMeta")
                            if "existentialCore" in obj: ordered_keys.append("existentialCore")
                            if "existentialCoreThreat" in obj: ordered_keys.append("existentialCoreThreat")
                            if "existenzIntegrity" in obj: ordered_keys.append("existenzIntegrity")
                            
                            for k in sorted(obj.keys()):
                                if k not in ordered_keys:
                                    ordered_keys.append(k)
                                    
                            for i, k in enumerate(ordered_keys):
                                v = obj[k]
                                clean_k = str(k).strip()
                                val_str = emit_strict_json_lines(v, depth + 1)
                                comma = "," if i < len(ordered_keys) - 1 else ""
                                lines.append(f'{next_indent}"{clean_key}": {val_str}{comma}')
                            lines.append(indent + "}")
                            return "\n".join(lines)

                        elif isinstance(obj, list):
                            if not obj:
                                return "[]"
                            
                            # SPECIAL HANDLING FLUSHER FOR 4-COLUMN SECURITY SIGNATURE TUPLES
                            if all(isinstance(row, list) and len(row) == 4 for row in obj):
                                lines = ["{"]
                                for i, row in enumerate(obj):
                                    lbl_s, mask_s, hash_s, status_s = row
                                    lines.append(f'{next_indent}"{lbl_s}": {{')
                                    lines.append(f'{deep_indent}"bitmask": "{mask_s}",')
                                    lines.append(f'{deep_indent}"hash": "{hash_s}",')
                                    lines.append(f'{deep_indent}"status": "{status_s}"')
                                    comma = "}," if i < len(obj) - 1 else "}"
                                    lines.append(f'{next_indent}{comma}')
                                lines.append(indent + "}")
                                return "\n".join(lines)
                                
                            # Standard list items (basics / immutables) expanded exactly 1 per line
                            lines = ["["]
                            for i, item in enumerate(obj):
                                val_str = emit_strict_json_lines(item, depth + 1)
                                comma = "," if i < len(obj) - 1 else ""
                                lines.append(f'{next_indent}{val_str}{comma}')
                            lines.append(indent + "]")
                            return "\n".join(lines)

                        elif isinstance(obj, str):
                            clean_str = obj.strip().replace('"', '\\"')
                            return f'"{clean_str}"'

                        elif isinstance(obj, bool):
                            return "true" if obj else "false"

                        elif isinstance(obj, int) and not isinstance(obj, bool):
                            return str(obj)

                        elif obj is None:
                            return "null"

                        return f'"{str(obj).strip()}"'

                    # Write out the pristine text layout directly to disk
                    with open(target_path, "w", encoding="utf-8") as custom_out:
                        custom_out.write(emit_strict_json_lines(json_matrix_payload))

                    error_handler.print(f" [->] Synced Core Mirror: {token:<12} -> Blueprint ordered JSON written to root.", level="info")
                except Exception as e:
                    error_handler.print(f"Failed to clone JSON boundary layer {token}: {e}", level="error", exit_code=1)

            elif filename.endswith(".py"):
                if token == "Core":
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
                            immutable_meta = meta_block.get("immutable", {})
                            raw_pillars = immutable_meta.get("PILLARS", "")
                            if raw_pillars:
                                p_nodes = [p.strip() for p in raw_pillars.split("|") if p.strip() in core_source_data]
                                if p_nodes: f.write("\n    IMMUTABLE_PILLARS = (\n        " + " |\n        ".join(p_nodes) + "\n    )\n")
                            raw_rights = immutable_meta.get("RIGHTS", "")
                            if raw_rights:
                                r_nodes = [r.strip() for r in raw_rights.split("|") if r.strip() in core_source_data]
                                if r_nodes: f.write("\n    IMMUTABLE_RIGHTS = (\n        " + " |\n        ".join(r_nodes) + "\n    )\n")
                            f.write("\nexistentialCoreBitmask = {\n")
                            for k, d in core_source_data.items():
                                if isinstance(d, dict) and "msk" in d: f.write(f'    existentialCore.{k:<25}: "{d["msk"]}",\n')
                            f.write("}\n")
                            f.write("\nexistentialCorePolicy = {\n")
                            for k, d in core_source_data.items():
                                if isinstance(d, dict) and "pol" in d: f.write(f'    existentialCore.{k:<25}: "{d["pol"]}",\n')
                            f.write("}\n")
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
                            for k, d in schema_data["existentialCore"].items():
                                if isinstance(d, dict) and "threat" in d:
                                    v = d["val"]
                                    expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
                                    f.write(f"    {d['threat']:<30} = {expr}\n")
                            f.write("\nexistentialCoreThreatLegal = {\n")
                            for k, v in schema_data.get("existentialCoreThreatLegal", {}).items():
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if isinstance(d, dict) and "threat" in d and str(d["val"]) == str(k)), None)
                                if target_node: f.write(f"    existentialCoreThreat.{target_node}: \"{v}\",\n")
                            f.write("}\n")
                            f.write("\nexistentialCoreThreatShadowVacuum = {\n")
                            for k, v in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                                target_node = next((d["threat"] for d in schema_data["existentialCore"].values() if isinstance(d, dict) and "threat" in d and str(d["val"]) == str(k)), None)
                                if target_node: f.write(f"    existentialCoreThreat.{target_node}: \"{v}\",\n")
                            f.write("}\n")
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
