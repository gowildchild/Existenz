# ==========================================================================
# EXISTENZ  master/struct/module/cliStateIntegrity.py
# Opcode-Driven Cryptographic Structural Integrity Assembly Engine
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import hashlib
import hmac
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzMeta, existenzIntegrityGlue, existenzSignatures
from engineSigningStruct import existenzIntegrityKeysHandler, existenzIntegrityKeyStatus

def execute(args, error_handler, repo_root: str):
    """
    Executes deep opcode-driven integrity scanning across individual structural components.
    Computes links, salts blocks via MAGIC, seals chains, and updates signatures files.
    """
    error_handler.print("Initiating forensic structural signature engine [MODE: INTEGRITY]...", level="notice")
    
    # 1. Initialize temporary tracking storage dictionaries for this session
    session_hashes = {}
    magic_salt_bytes = existenzMeta.MAGIC["RAW"].encode('utf-8')

    # Load local configuration key paths if available
    config_target_path = os.path.abspath(os.path.join(repo_root, args.config))
    config_paths = {}
    if os.path.exists(config_target_path):
        try:
            with open(config_target_path, "r", encoding="utf-8") as cf:
                config_paths = json.load(cf).get("private_key_paths", {})
        except Exception:
            pass

    # 2. STEP ONE: Phase One - Run Opcode-Driven Individual Component Hashing
    for key, glue_tuple in existenzIntegrityGlue.items():
        name, status_mask, op_flags, hex_id, relative_path, old_sig = glue_tuple
        absolute_path = os.path.abspath(os.path.join(repo_root, relative_path))
        
        computed_hash = ""

        # Check Opcode Type 1: SIGN_TYPE_FILE
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_FILE) and os.path.exists(absolute_path):
            if absolute_path.endswith(".json"):
                with open(absolute_path, "r", encoding="utf-8") as j_in:
                    json_payload = json.load(j_in)
                computed_hash = engineSigningLibrary.calculate_op_driven_hash(json_payload, op_flags)
            else:
                computed_hash = engineSigningLibrary.calculate_file_sha256(absolute_path)

        # Check Opcode Type 2: SIGN_TYPE_STRING
        elif bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_STRING):
            # Target literal string parameters or configuration tokens
            payload_dict = {"payload": str(old_sig)}
            computed_hash = engineSigningLibrary.calculate_op_driven_hash(payload_dict, op_flags)

        if computed_hash:
            session_hashes[f"{key}_hash"] = computed_hash
            session_hashes[f"{key}_sign"] = hex_id
        else:
            session_hashes[f"{key}_hash"] = "0000000000000000000000000000000000000000"
            session_hashes[f"{key}_sign"] = "00000000"

    # 3. STEP TWO: Phase Two - Process Cryptographic Sequential Blockchain Loops
    # Sort rules strictly by their order sequence priority fields to ensure predictable trails
    sorted_rules = sorted(existenzSignatures.existentialCore, key=lambda x: x[2])
    
    chain_active = False
    accumulated_chain_hashes = []

    for label, glue_tuple, chronological_order in sorted_rules:
        name, status_mask, op_flags, hex_id, relative_path, old_sig = glue_tuple
        current_node_hash = session_hashes.get(f"{label}_hash", "")

        # A. Detect Chain Initialization (SIGN_CHAIN_START)
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_CHAIN_START):
            chain_active = True
            accumulated_chain_hashes = []

        if chain_active and current_node_hash:
            # Check if this node demands high-security magic salting
            if bool(op_flags & existenzIntegrityKeysHandler.SIGN_MAGIC_HASH):
                salted_bytes = magic_salt_bytes + current_node_hash.encode('utf-8')
                link_hash = hmac.new(magic_salt_bytes, salted_bytes, hashlib.sha256).hexdigest()
            else:
                link_hash = current_node_hash
            accumulated_chain_hashes.append(link_hash)

        # B. Detect Chain Boundary Cap (SIGN_CHAIN_END)
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_CHAIN_END) and chain_active:
            consolidated_trail_string = "".join(accumulated_chain_hashes)
            final_chain_signature = hmac.new(magic_salt_bytes, consolidated_trail_string.encode('utf-8'), hashlib.sha256).hexdigest()
            
            # Anchor the compiled tracking token right into your ending layer
            session_hashes[f"{label}_hash"] = final_chain_signature
            chain_active = False

    # 4. STEP THREE: Phase Three - Render your exact data-dense hierarchy graph onto the screen
    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, session_hashes, sorted_rules)

    # 5. STEP FOUR: Phase Four - Write Compiled Data Layers out to files
    py_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesPy"]))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    # Generate the pristine python tracking script structure matching your layout
    py_payload = f"""# ==========================================================================
# EXISTENZ master/struct/existentialSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {{
    "MAGIC": {{
        "TAG":                "{existenzMeta.MAGIC["RAW"]}",
        "TOKEN":              "{existenzMeta.MAGIC["TOKEN"]}",
        "SIGNATURE":          "{existenzMeta.MAGIC["SIGNATURE"]}",
        "REALM":              "{existenzMeta.HEADER["REALM"].decode()}",
        "VERSION":            "{existenzMeta.HEADER["VERSION"].decode()}",
        "AUTHOR":             "{existenzMeta.META["AUTHOR"]}"
    }},
    "master": {{
        "Core":               "{session_hashes.get('Core_hash')}",
        "Check":              "{session_hashes.get('CoreCheck_hash')}",        
        "Schema":             "{session_hashes.get('Schema_hash')}",
        "Cores":              "{session_hashes.get('Cores_hash')}",
        "Threat":             "{session_hashes.get('CoreThreat_hash')}",
        "ThreatLegal":        "{session_hashes.get('CoreThreatLegal_hash')}",
        "ThreatShadowVacuum": "{session_hashes.get('CoreThreatShadowVacuum_hash')}",
        "ThreatSigned":       "{session_hashes.get('CoreThreatSigned_hash')}"
    }},
    "chain": {{
        "Core":               "",
        "CoresChain":         "",
        "Threat":             ""
    }},
    "manifest": {{
        "dist":               "dist",
        "tools":              "dist/tools",
        "build":              "master/build-tools",
        "master":             "master/struct"
    }},
    "structs": {{
        "KeysPublic":         "",
        "KeysHandler":        "",
        "KeysType":           "",
        "Locations":          ""
    }},
    "engine": {{
        "Manifest":           ""
    }}
}}
"""
    try:
        with open(py_signatures_path, "w", encoding="utf-8") as py_out:
            py_out.write(py_payload)
            
        with open(json_signatures_path, "w", encoding="utf-8") as json_out:
            json.dump({"existentialToken": session_hashes}, json_out, indent=2, sort_keys=True)
            
        error_handler.print("[+] SUCCESS: Structural hashes committed and mirrored safely.", level="notice")
    except Exception as io_err:
        error_handler.print(f"Failed writing structural registers to file: {io_err}", level="error", exit_code=32)

    # Calculate dynamic progression steps natively
    engineSigningLibrary.pipeline_step_next(args.args.stage, error_handler)
