# ==========================================================================
# EXISTENZ  master/struct/module/cliStateIntegrity.py
# Universal Opcode-Driven Cryptographic Structural Integrity Assembly Engine
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import hashlib
import hmac
import engineSigningLibrary
from engineSigningMeta import existenzLocations, existenzMeta
from engineSigningStruct import existenzIntegrityKeysHandler, existenzIntegrityGlue, existenzSignatures

def execute(args, error_handler, repo_root: str):
    """
    Executes a project-agnostic structural integrity scanning pass.
    Safely unpacks variable length metadata tuples using protective slicing fallbacks.
    """
    error_handler.print("Initiating universal structural signature engine [MODE: INTEGRITY]...", level="notice")
    
    session_hashes = {}
    magic_salt_bytes = existenzMeta.MAGIC["RAW"].encode('utf-8')

    # 1. PHASE ONE: Dynamic Component Hashing via Protective Tuple Inspection
    for key, raw_tuple in existenzIntegrityGlue.items():
        # FIXED: Protective variable length chunk builder ensures 6 slots are always present
        padded_tuple = list(raw_tuple) + ["", 0, 0, 0, "", ""]
        name          = str(padded_tuple[0])
        status_mask   = int(padded_tuple[1]) if isinstance(padded_tuple[1], int) else 0
        op_flags      = int(padded_tuple[2]) if isinstance(padded_tuple[2], int) else 0
        hex_id        = str(padded_tuple[3])
        relative_path = str(padded_tuple[4])
        old_sig       = str(padded_tuple[5])

        absolute_path = os.path.abspath(os.path.join(repo_root, relative_path))
        computed_hash = ""

        # Check Opcode: SIGN_TYPE_FILE
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_FILE) and os.path.exists(absolute_path):
            if absolute_path.endswith(".json"):
                with open(absolute_path, "r", encoding="utf-8") as j_in:
                    json_payload = json.load(j_in)
                computed_hash = engineSigningLibrary.calculate_op_driven_hash(json_payload, op_flags)
            else:
                computed_hash = engineSigningLibrary.calculate_file_sha256(absolute_path)

        # Check Opcode: SIGN_TYPE_STRING
        elif bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_STRING):
            computed_hash = engineSigningLibrary.calculate_op_driven_hash({"payload": old_sig}, op_flags)

        # Agnostic Fallback: Resolve via standard path verification if flags are completely empty
        if not computed_hash:
            computed_hash = engineSigningLibrary.calculate_file_sha256(absolute_path) if os.path.exists(absolute_path) else "0000000000000000000000000000000000000000"

        session_hashes[f"{key}_hash"] = computed_hash
        session_hashes[f"{key}_sign"] = hex_id

    # 2. PHASE TWO: Agnostic Blockchain Link Sequencer
    active_tree_rules = existenzSignatures.existentialCore
    sorted_rules = sorted(active_tree_rules, key=lambda x: x[2]) # Sorted explicitly by index 2 (order field)
    
    chain_active = False
    accumulated_chain_hashes = []

    for label, raw_inner_tuple, chronological_order in sorted_rules:
        # FIXED: Protective variable length chunk builder applied here as well
        padded_inner = list(raw_inner_tuple) + ["", 0, 0, 0, "", ""]
        op_flags      = int(padded_inner[2]) if isinstance(padded_inner[2], int) else 0
        
        current_node_hash = session_hashes.get(f"{label}_hash", "")

        # Open Chain Frame (SIGN_CHAIN_START)
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_CHAIN_START):
            chain_active = True
            accumulated_chain_hashes = []

        if chain_active and current_node_hash:
            if bool(op_flags & existenzIntegrityKeysHandler.SIGN_MAGIC_HASH):
                salted_bytes = magic_salt_bytes + current_node_hash.encode('utf-8')
                link_hash = hmac.new(magic_salt_bytes, salted_bytes, hashlib.sha256).hexdigest()
            else:
                link_hash = current_node_hash
            accumulated_chain_hashes.append(link_hash)

        # Seal Chain Frame (SIGN_CHAIN_END)
        if bool(op_flags & existenzIntegrityKeysHandler.SIGN_CHAIN_END) and chain_active:
            consolidated_trail_string = "".join(accumulated_chain_hashes)
            final_chain_signature = hmac.new(magic_salt_bytes, consolidated_trail_string.encode('utf-8'), hashlib.sha256).hexdigest()
            
            session_hashes[f"{label}_hash"] = final_chain_signature
            chain_active = False

    # 3. PHASE THREE: Dynamic Tree Rendering Pass
    tree_session_hashes = {
        "existentialCoreMagicHash": session_hashes.get("MagicCheck_hash", "UNKNOWN"),
        "existentialCoreCheckHash": session_hashes.get("CoreCheck_hash", "UNSIGNED"),
    }
    for label, _, _ in sorted_rules:
        tree_session_hashes[f"existential{label}Hash"] = session_hashes.get(f"{label}_hash", "")
        tree_session_hashes[f"{label.lower()}_sign"] = session_hashes.get(f"{label}_sign", "00000000")

    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, tree_session_hashes, sorted_rules)

    # 4. PHASE FOUR: Flush Universal Tracking Maps to Disk Filesystem Targets
    py_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesPy"]))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    master_dict_lines = []
    for label, _, _ in sorted_rules:
        master_dict_lines.append(f'        "{label}":'.ljust(30) + f'"{session_hashes.get(f"{label}_hash")}"')

    py_payload = f"""# ==========================================================================
# UNIVERSAL INTEGRITY REGISTER TRACKING LEDGER BLUEPRINT ASSET
# Generated dynamically by engine validation execution modules.
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
    "master": {{\n{",\n".join(master_dict_lines)}\n    }},
    "chain": {{}},
    "manifest": {{
        "dist":               "dist",
        "tools":              "dist/tools",
        "build":              "master/build-tools",
        "master":             "master/struct"
    }}
}}
"""
    if str(args.run).strip().lower() != "dry":
        try:
            with open(py_signatures_path, "w", encoding="utf-8") as py_out:
                py_out.write(py_payload)
            with open(json_signatures_path, "w", encoding="utf-8") as json_out:
                json.dump({"existentialToken": session_hashes}, json_out, indent=2, sort_keys=True)
            error_handler.print("[+] SUCCESS: Project-agnostic tracking maps consolidated perfectly.", level="notice")
        except Exception as io_err:
            error_handler.print(f"Failed writing structural registers to file: {io_err}", level="error", exit_code=32)

    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
