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
    Strictly queries tuple arrays by explicit numerical indices to prevent unpacking errors.
    """
    error_handler.print("Initiating universal structural signature engine [MODE: INTEGRITY]...", level="notice")
    
    session_hashes = {}
    magic_salt_bytes = existenzMeta.MAGIC["RAW"].encode('utf-8')

    # 1. PHASE ONE: Dynamic Component Hashing via Clean Index Extraction
    for key, glue_tuple in existenzIntegrityGlue.items():
        # Safely extract records from the 6-element tuple via explicit index placement
        name          = str(glue_tuple[0])
        status_mask   = int(glue_tuple[1])
        op_flags      = int(glue_tuple[2])
        hex_id        = str(glue_tuple[3])
        relative_path = str(glue_tuple[4])
        old_sig       = str(glue_tuple[5])

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
            computed_hash = engineSigningLibrary.calculate_op_driven_hash({"payload": str(old_sig)}, op_flags)

        # Agnostic Fallback: Resolve via standard path verification if flags are empty
        if not computed_hash:
            computed_hash = engineSigningLibrary.calculate_file_sha256(absolute_path) if os.path.exists(absolute_path) else "0000000000000000000000000000000000000000"

        session_hashes[f"{key}_hash"] = computed_hash
        session_hashes[f"{key}_sign"] = hex_id

    # 2. PHASE TWO: Agnostic Blockchain Link Sequencer via Direct Indices
    active_tree_rules = existenzSignatures.existentialCore
    
    # Sorts strictly using index 2 (the order priority integer field)
    sorted_rules = sorted(active_tree_rules, key=lambda x: x[2])
    
    chain_active = False
    accumulated_chain_hashes = []

    for rule_row in sorted_rules:
        label = str(rule_row[0])
        inner_glue_record = rule_row[1]
        chronological_order = int(rule_row[2])
        
        # Extract op_flags strictly from index 2 of the inner 6-element config tuple
        op_flags = int(inner_glue_record[2])
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

    # 3. PHASE THREE: Prepare session tokens dynamically to drive your custom tree visualizer
    tree_session_hashes = {
        "existentialCoreMagicHash": session_hashes.get("MagicCheck_hash", "UNKNOWN"),
        "existentialCoreCheckHash": session_hashes.get("CoreCheck_hash", "UNSIGNED"),
    }
    
    # FIXED: Reconstruct a clean 6-element matrix format to feed your actual tree renderer function perfectly
    pushed_matrix_rows = []
    for rule_row in sorted_rules:
        label = str(rule_row[0])
        inner_glue = rule_row[1]
        
        # Pull live hashes computed in this run
        live_hash = session_hashes.get(f"{label}_hash", "")
        
        # Synthesize a full 6-element row matching your tree renderer expectations exactly
        rebuilt_row = [
            label,               # Name [0]
            inner_glue[1],       # Short var / Weight status [1]
            live_hash,           # Hash variable value [2]
            inner_glue[5],       # Signature value field token string [3]
            inner_glue[1],       # Bitmask integer payload [4]
            rule_row[2]          # Sequence sequence tracking identifier [5]
        ]
        pushed_matrix_rows.append(rebuilt_row)
        
        tree_session_hashes[f"existential{label}Hash"] = live_hash
        tree_session_hashes[f"{label.lower()}_sign"] = session_hashes.get(f"{label}_sign", "00000000")

    # Pass the correctly formed 6-element matrix rows down to prevent tree viewer unpack failure crashes
    engineSigningLibrary.render_cryptographic_structural_tree(error_handler, tree_session_hashes, pushed_matrix_rows)

    # 4. PHASE FOUR: Flush Universal Tracking Maps to Disk Filesystem Targets
    py_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesPy"]))
    json_signatures_path = os.path.abspath(os.path.join(repo_root, existenzLocations["core"]["SignaturesJson"]))

    master_dict_lines = []
    for rule_row in sorted_rules:
        label = str(rule_row[0])
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
