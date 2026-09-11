# ==========================================================================
# EXISTENZ  master/struct/module/cliStateInit.py
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
        #error_handler.print(f"  DEBUG SCAN: Checking token '{token}' target path: {full_target_path}", level="info")
        #if os.path.exists(full_target_path):
        #    error_handler.print(f"  DEBUG SCAN: Physical file present on disk space with size: {os.path.getsize(full_target_path)} bytes.", level="info")
        
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
        #meta_path = os.path.abspath(os.path.join(repo_root, existenzLocations["engine"]["signingMeta"]))
        meta_data = ""
        
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
        except Exception as e:
            error_handler.print(f"Failed to parse master schema JSON database layers: {e}", level="error", exit_code=16)

        #try:
        #    with open(meta_path, "r", encoding="utf-8") as f:
        #        meta_data = json.load(f)
        #except Exception as e:
        #    error_handler.print(f"Failed to parse meta JSON database layers: {e}", level="error", exit_code=16)

        
        version_name = "module/cliStateInit.py"
        
        # Dynamic Extraction: Read version directly from the blueprint payload
        #existenzMeta.HEADER.get("VERSION", version_str)
        version_full = schema_data.get("existentialMeta", schema_data.get("coreVersion", "v0.76.08"))
        version_str = schema_data.get("existentialMeta", {}).get("CoreVersion", schema_data.get("coreVersion", "v0.76.09"))
        meta_block = schema_data.get("existentialMeta", {})
        magic_raw = meta_block.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")
        
        # Dynamically build the tag string based on the JSON configuration instructions
        try:
            fields = magic_raw.split(":")
            magic_tag = ":".join([str(meta_block.get(field, "UNKNOWN")) for field in fields])
        except Exception:
            magic_tag = "Existenz:v0.76.18:EX25IMMUT32CORE7617"

        # Export straight to GitHub Actions environment space natively
        github_env_file = os.environ.get('GITHUB_ENV')
        if github_env_file:
            try:
                with open(github_env_file, "a", encoding="utf-8") as gef:
                    gef.write(f"BLUEPRINT_VERSION={version_str}\n")
                error_handler.print(f"  [+] Loaded BLUEPRINT_VERSION={version_str} into environment.", level="info")
            except Exception as env_err:
                error_handler.print(f"Non-fatal error mapping version variable to shell runner: {env_err}", level="debug")

        
        #error_handler.print(f"  [VERSION1] {version_str} {version_name}", level="debug")
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

                        threat_lines = []
                        for k, d in schema_data.get("existentialCore", {}).items():
                            if "threat" in d:
                                v = d["val"]
                                expr = "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")
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
                                
                        core_lines = []
                        calculated_basic = []
                        calculated_immutable = [] # FIX: Initialized here to prevent variable lookup NameError crash
                        for k, d in schema_data.get("existentialCore", {}).items():
                            v = d["val"]
                            raw_pol = d.get("pol", 0)
                            
                            # Safely convert hex string parameters base 16
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
                                    
                            line_entry = f'    "{k}":'.ljust(33)
                            line_entry += f'{{ "val": {v},'.ljust(15)
                            line_entry += f'"expr": "{calculated_expr}",'.ljust(22)
                            line_entry += f'"type": "{struct_type}",'.ljust(20)
                            
                            clean_cmnt = d.get("comment", "").replace('"', '\\"')
                            line_entry += f' "comment": "{clean_cmnt}" }}'
                            core_lines.append(line_entry)

                        ver_val = schema_data.get("existentialMeta", schema_data.get("coreVersion", "v0.76.10"))
                        ver_val_meta = schema_data.get("existentialMeta", {})
                        ver_val_json = json.dumps(ver_val_meta, indent=2)
                        ver_val_json_indent = ver_val_json.replace("\n", "\n  ")
                        magic_val = ver_val_meta.get("coreVersion", "v0.76.08")
                        val_to_enum_map = {}
                        for k, d in schema_data.get("existentialCore", {}).items():
                            if "threat" in d:
                                node_label = d["threat"]
                            else:
                                node_label = k if k.startswith("CANARY_") or k.startswith("SHIELD_") else f"THREAT_{k}"
                            val_to_enum_map[int(d["val"])] = f"existentialCoreThreat.{node_label}"

                        composite_fallbacks = {
                            89130487:   "existentialCoreThreat.CANARY_7_EXPLOITATION",
                            2290263560: "existentialCoreThreat.CANARY_8_PREDATORY"
                        }

                        legal_entries = []
                        for raw_key, val in schema_data.get("existentialCoreThreatLegal", {}).items():
                            int_key = int(raw_key)
                            enum_token = val_to_enum_map.get(int_key, composite_fallbacks.get(int_key, f"existentialCoreThreat.UNKNOWN_{int_key}"))
                            legal_entries.append(f'    "{enum_token}":'.ljust(55) + f'"{val}"')

                        vacuum_entries = []
                        for raw_key, val in schema_data.get("existentialCoreThreatShadowVacuum", {}).items():
                            int_key = int(raw_key)
                            enum_token = val_to_enum_map.get(int_key, composite_fallbacks.get(int_key, f"existentialCoreThreat.UNKNOWN_{int_key}"))
                            vacuum_entries.append(f'    "{enum_token}":'.ljust(55) + f'"{val}"')

                        json_str_payload = "{\n"
                        json_str_payload += f'  "existentialCoreMeta": {ver_val_json_indent},\n'
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
                        #error_handler.print(f"  [VERSION2] {ver_val}", level="debug")
                    
                        with open(target_path, "w", encoding="utf-8") as custom_out:
                            custom_out.write(json_str_payload)
                        error_handler.print(f"    [->] Synced Core Mirror: {token:<12} -> Blueprint ordered JSON written to root.", level="info")
                        #error_handler.print(f"  [VERSION2] {ver_val}", level="debug")
                    
                    elif "SignaturesJson" in token or filename == "existentialSignatures.json":
                        import hashlib
                        meta_blueprint = schema_data.get("existentialMeta", {})

                        # 1. DYNAMIC SECURITY LAYER: Generate cryptographic signatures straight from the blueprint data
                        live_realm   = str(meta_blueprint.get("CoreRealm", "Existenz"))
                        live_version = str(meta_blueprint.get("CoreVersion", "v0.76.18"))
                        live_secret  = str(meta_blueprint.get("CoreMagic", "EX25IMMUT32CORE7617"))
                        live_author  = str(meta_blueprint.get("CoreAuthor", "Gunther Voet"))
                        
                        # Generate dynamic TOKEN hash from your live assembled magic_tag string data asset
                        dynamic_token_hash = hashlib.sha256(magic_tag.encode("utf-8")).hexdigest()
                        
                        # Chain token hash with author attribute to dynamically compute SIGNATURE
                        chain_seed_string = f"{dynamic_token_hash}:{live_author}"
                        dynamic_signature_hash = hashlib.sha256(chain_seed_string.encode("utf-8")).hexdigest()

                        # Helper logic to dynamically calculate hashes of physical workspace code targets
                        def get_file_hash(target_token):
                            rel_p = existenzLocations["core"].get(target_token)
                            if not rel_p:
                                return ""
                            abs_p = os.path.abspath(os.path.join(repo_root, rel_p))
                            if os.path.exists(abs_p):
                                try:
                                    with open(abs_p, "rb") as fh:
                                        return hashlib.sha256(fh.read()).hexdigest()
                                except Exception:
                                    return ""
                            return ""

                        # Construct your physical structural layout payload matching your exact tracking realms
                        signatures_matrix = {
                            "existentialToken": {
                                "MAGIC": {
                                    "RAW_TEMPLATE":       str(meta_blueprint.get("CoreMagicRaw", "")),
                                    "RAW":                str(magic_tag),
                                    "TOKEN":              str(dynamic_token_hash),
                                    "SIGNATURE":          str(dynamic_signature_hash),
                                    "REALM":              live_realm,
                                    "VERSION":            live_version,
                                    "SECRET":             live_secret,                                    
                                    "AUTHOR":             live_author
                                },
                                "master": {
                                    "Core":               get_file_hash("Core"),
                                    "Check":              get_file_hash("Check"),        
                                    "Schema":             get_file_hash("Schema"),
                                    "Cores":              get_file_hash("Cores"),
                                    "Threat":             get_file_hash("Threat"),
                                    "ThreatLegal":        get_file_hash("Threat"), 
                                    "ThreatShadowVacuum": get_file_hash("Threat"),
                                    "ThreatSigned":       get_file_hash("SignaturesPy")
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

                            immutable_meta = meta_block.get("immutable", {})
                            raw_pillars = immutable_meta.get("PILLARS", "")
                            if raw_pillars:
                                p_nodes = [p.strip() for p in raw_pillars.split("|") if p.strip() in schema_data["existentialCore"]]
                                if p_nodes:
                                    f.write("\n    IMMUTABLE_PILLARS = (\n        " + " |\n        ".join(p_nodes) + "\n    )\n")
                            
                            raw_rights = immutable_meta.get("RIGHTS", "")
                            if raw_rights:
                                r_nodes = [r.strip() for r in raw_rights.split("|") if r.strip() in schema_data["existentialCore"]]
                                if r_nodes:
                                    f.write("\n    IMMUTABLE_RIGHTS = (\n        " + " |\n        ".join(r_nodes) + "\n    )\n")
                            
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
                            f.write("# " + "="*74 + "\n")
                            f.write("# EXISTENZ CORE SIGNATURE CONTEXT\n")
                            f.write("# " + "="*74 + "\n")
                            f.write(f'CoreMagicRaw = "{magic_raw}"\n')
                            f.write(f'CoreMagicTag = "{magic_tag}"\n\n')                            
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
                        import hashlib
                        struct_template_path = os.path.abspath(os.path.join(repo_root, "master", "struct", filename))
                        
                        if os.path.exists(struct_template_path):
                            # Read the pristine template structure directly into the memory buffer context
                            with open(struct_template_path, "r", encoding="utf-8") as tf:
                                template_content = tf.read()
                                
                            # Extract metadata properties from the active master blueprint payload dict
                            meta_blueprint = schema_data.get("existentialMeta", {})
                            live_realm   = str(meta_blueprint.get("CoreRealm", "Existenz"))
                            live_version = str(meta_blueprint.get("CoreVersion", "v0.76.15"))
                            live_author  = str(meta_blueprint.get("CoreAuthor", "Gunther Voet"))

                            # Compute live cryptographic tokens natively using the global magic_tag string
                            local_token_hash = hashlib.sha256(magic_tag.encode("utf-8")).hexdigest()
                            chain_seed_string = f"{local_token_hash}:{live_author}"
                            local_signature_hash = hashlib.sha256(chain_seed_string.encode("utf-8")).hexdigest()

                            # 1. INITIALIZE DYNAMIC REPLACEMENTS WITH GLOBAL BLUEPRINT METADATA
                            replacements = {
                                "{{LIVE_REALM}}":         live_realm,
                                "{{LIVE_VERSION}}":       live_version,
                                "{{LIVE_AUTHOR}}":        live_author,
                                "{{DYNAMIC_TOKEN}}":      local_token_hash,
                                "{{DYNAMIC_SIGNATURE}}":  local_signature_hash,
                                "{{MAGIC_RAW}}":          str(magic_raw),
                                "{{MAGIC_TAG}}":          str(magic_tag)
                            }

                            # 2. GLUE-DRIVEN TRAVERSAL: Automate asset discovery using engineSigningStruct parameters
                            from engineSigningStruct import existenzIntegrityGlue, existenzIntegrityKeysHandler

                            for glue_key, glue_tuple in existenzIntegrityGlue.items():
                                if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
                                    continue
                                
                                # Extract properties natively: [0]=variable, [1]=bitmask, [2]=opcode, [3]=id, [4]=relative_path
                                rel_path = glue_tuple[4]
                                op_flags = glue_tuple[2]
                                
                                # Build template bracket token keys matching your template file standard
                                hook_key = f"{{{{HASH_{glue_key.upper()}}}}}"
                                
                                # Resolve the physical file path on the running host system container
                                abs_path = os.path.abspath(os.path.join(repo_root, rel_path))
                                
                                # Rule A: Standalone or Magic-Salted targets mapped directly to distinct files on disk
                                if os.path.exists(abs_path) and os.path.isfile(abs_path):
                                    try:
                                        with open(abs_path, "rb") as fh:
                                            calculated_hash = hashlib.sha256(fh.read()).hexdigest()
                                    except Exception:
                                        calculated_hash = ""
                                        
                                # Rule B: Folders/Directories mapped inside manifest rings are kept clean or route to build
                                elif os.path.exists(abs_path) and os.path.isdir(abs_path):
                                    calculated_hash = ""
                                    
                                # Rule C: Sub-registries or chained structures remain unpopulated until processing loops sign them
                                else:
                                    calculated_hash = ""
                                    
                                replacements[hook_key] = calculated_hash

                            # 3. Apply the dynamic mapping substitutions completely across the template content
                            for hook, live_value in replacements.items():
                                template_content = template_content.replace(hook, live_value)

                            # Flush the finalized, fully signed python code file directly to disk space
                            with open(target_path, "w", encoding="utf-8") as f:
                                f.write(template_content)

                            error_handler.print(f"    [COMPILE FILE] Seeded signature module out of source template path: {target_path}", level="info")
                        else:
                            error_handler.print(f"Fatal Initialization fault: Master signatures template missing at: {struct_template_path}", level="warning")
                    except Exception as e:
                        error_handler.print(f"Failed template compilation for existentialSignatures.py: {e}", level="error", exit_code=1)
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
