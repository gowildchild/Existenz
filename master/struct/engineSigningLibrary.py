# ==========================================================================
# EXISTENZ  master/struct/engineSigningLibrary.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import visualMixEngineCrypto
import os
import sys
import json
import subprocess
import argparse
import hashlib
import getpass
import time
from enum import IntFlag
from cryptography.hazmat.primitives.asymmetric import ed25519
#from cryptography.hazmat.primitives import serialization

from typing import Dict, Any

from engineSigningMeta import existenzLocations, existenzMeta, existenzConfig, existenzPublicKeys
# Added missing existenzIntegrityKeyStatus registration dependency entry
from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeysHandler, existenzIntegrityKeyStatus, existenzSteps
from existentialSignatures import existentialToken

from visualMixEngineLogging import visualmixErrorHandler

INT_VERSION = "v0.76.15+"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Initialize global diagnostic loop interceptor
error_handler = visualmixErrorHandler(custom_post="_ERR")

# The precise bitwise progression order for your repository pipeline matching your layout
PIPELINE_SEQUENCE = [
    existenzSteps.STEP_TEST,
    existenzSteps.STEP_INIT,
    existenzSteps.STEP_COMMIT,
    existenzSteps.STEP_MANIFEST,
    existenzSteps.STEP_SIGN_PUBLIC,
    existenzSteps.STEP_SIGN_ENVIRONMENT,
    existenzSteps.STEP_VERIFY,
    existenzSteps.STEP_SIGN_PRIVATE,
    existenzSteps.STEP_SIGN_SUCCESS,
    existenzSteps.STEP_BUILD_DIST,
    existenzSteps.STEP_BUILD_TOOLS,
    existenzSteps.STEP_BUILD_BUILD,
    existenzSteps.STEP_BUILD_MASTER,
    existenzSteps.STEP_BUILD_SUCCESS,
    existenzSteps.STEP_SUCCESS
]


import hmac
import hashlib
from engineSigningMeta import existenzMeta

import re

def render_better_box(error_handler, raw_lines_list: list, title_str: str = "SYSTEM STATUS"):
    """
    Renders a pristine, fully dynamic visual box enclosure layout around text elements.
    Calculates lengths accurately by stripping ANSI escape color sequences to keep borders straight.
    """
    # 1. Strip ANSI escape color tracks purely to calculate accurate terminal layout spaces
    def get_visible_length(text_line: str) -> int:
        return len(re.sub(r'\033\[[0-9;]*m', '', str(text_line)))

    # 2. Determine target width scaling limits based on content payload attributes
    max_visible_len = max((get_visible_length(line) for line in raw_lines_list), default=len(title_str))
    box_width = max(60, max_visible_len + 4)

    # 3. Compile structural perimeter headers
    header_left = f"──┤ [ {title_str} ] ├"
    header_dash_fill = max(4, box_width - get_visible_length(header_left))
    
    # 4. Stream out the unified visual grid lines through error_handler.print
    error_handler.print(f"┌{header_left}{'─' * header_dash_fill}┐", level="local")
    
    for line in raw_lines_list:
        clean_line = str(line).rstrip()
        visible_len = get_visible_length(clean_line)
        padding_spaces = " " * (box_width - visible_len)
        error_handler.print(f"│ {clean_line}{padding_spaces} │", level="local")
        
    error_handler.print("└" + "─" * (box_width + 2) + "┘", level="local")

def render_cryptographic_structural_tree_boxed(error_handler, session_hashes: dict, matrix_signed_rows: list):
    """
    Renders a pristine, fully dynamic visual box layout mapping your cryptographic
    verification layers and session hashes, guaranteed to never wrap or break.
    """
    from engineSigningStruct import existenzIntegrityKeyStatus

    # 1. Build rapid rule lookup directories eliminating global name collisions
    matrix_rules_lookup = {row[0]: row for row in matrix_signed_rows if row[0] != "Magic"}

    def get_layer_tags(layer_name, is_last_in_group=False):
        chain_arrow = " | "
        connector = "└──" if is_last_in_group else "├──"
        v_line    = "│  "
        
        if layer_name not in matrix_rules_lookup:
            return "0x00", "0", "+[HASH]+", connector, v_line, chain_arrow
            
        name, short_var, hash_var, sign_var, bitmask, seq = matrix_rules_lookup[layer_name]
        
        requires_signing = bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER or
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
                                
        is_signed = len(sign_var) >= 64 and not sign_var.startswith(name)
        
        if bool(bitmask > 1 and (bitmask & existenzIntegrityKeyStatus.KEY_IS_PUBLIC)):
            chain_arrow = " ► "
            connector = "╚══" if is_last_in_group else "╠══"
            v_line    = "║  "

        tags = []
        if is_signed:
            if bitmask > 1 and (bitmask & existenzIntegrityKeyStatus.KEY_IS_PUBLIC): tags.append("+[CHN]")
            if bitmask & existenzIntegrityKeyStatus.KEY_IS_VERIFIED:   tags.append("+[MAGIC]")
            if bitmask & existenzIntegrityKeyStatus.KEY_IS_PRIVATE:    tags.append("+[SHA256]")
            if bitmask & 262144:                                       tags.append("+[IMMUTABLE]")
        else:
            if requires_signing:
                pfm_tag = "+PFM" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM) else ""
                dev_tag = "+DEV" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER) else ""
                psn_tag = "+PSN" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL) else ""
                tags.append(f"+PK:{pfm_tag}{dev_tag}{psn_tag}")
            else:
                pfm_tag = "-PFM" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM) else ""
                dev_tag = "-DEV" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER) else ""
                psn_tag = "-PSN" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL) else ""
                tags.append(f"-PK:{pfm_tag}{dev_tag}{psn_tag}")

        if not is_signed and requires_signing:
            return f"{hex(bitmask)}", str(seq), f"\033[1;31m[ ! NOT SIGNED ! ] {' '.join(tags)}\033[0m", "├──", "│ ", " └► " if is_last_in_group else "├──"
            
        return f"{hex(bitmask)}", str(seq), " ".join(tags), connector, v_line, chain_arrow

    magic_token = session_hashes.get("existentialCoreMagicHash", "UNKNOWN")
    check_token = session_hashes.get("existentialCoreCheckHash", "UNSIGNED")
    core_ver    = "v0.76.16"

    # Ingest layout parameter configurations dynamically
    bm_c, sq_c, tg_c, _, _, _ = get_layer_tags("Core")
    bm_cb, sq_cb, tg_cb, _, _, _ = get_layer_tags("Cores")        
    bm_cc, sq_cc, tg_cc, _, _, _ = get_layer_tags("CoreCheck")
    bm_ch, sq_ch, tg_ch, _, _, _ = get_layer_tags("CoreChain")        
    bm_ct, sq_ct, tg_ct, conn_ct, vl_ct, ch_ct = get_layer_tags("CoreThreatStruct", is_last_in_group=False)
    bm_ctl, sq_ctl, tg_ctl, conn_ctl, vl_ctl, ch_ctl = get_layer_tags("CoreThreatLegal", is_last_in_group=False)
    bm_ctv, sq_ctv, tg_ctv, conn_ctv, vl_ctv, ch_ctv = get_layer_tags("CoreThreatShadowVacuum", is_last_in_group=False)
    bm_cts, sq_cts, tg_cts, conn_cts, vl_cts, ch_cts = get_layer_tags("CoreThreat", is_last_in_group=True)

    # 2. Gather all lines dynamically to determine the absolute widest string element
    raw_lines = [
        f" [MAGIC] existentialCoreCheckMagic        : {magic_token}",
        f" [CHECK] existentialCoreCheckSignature    : {check_token}",
        "",
        f" ──┬ [ Existenz {core_ver}   ] ──────────────────────────",
        "   │ ",
        f"   ├── [SQ {sq_c.zfill(2)} | {bm_c.ljust(6)}] existentialCore.py          ─┬─► Sign: 0x{session_hashes.get('core_sign', '00000000')} | {tg_c}",
        f"   │                                              └─► Signature: \"{session_hashes.get('existentialCoreHash', '')}\"",
        f"   ├── [SQ {sq_cb.zfill(2)} | {bm_cb.ljust(6)}] existentialCores.json       ─┬─► Sign: 0x{session_hashes.get('cores_sign', '00000000')} | {tg_cb}",
        f"   │                                              └─► Signature: \"{session_hashes.get('existentialCoresHash', '')}\"",
        f"   ├── [SQ {sq_cc.zfill(2)} | {bm_cc.ljust(6)}] existentialCoreCheck.py     ─┬─► Sign: 0x{session_hashes.get('check_sign', '00000000')} | {tg_cc}",
        f"   │                                              └─► Signature: \"{session_hashes.get('existentialCoreCheckHash', '')}\"",
        "   │  ",
        "   ├──► class existentialCoreThreatSignatures ────────────  ── ─ ── ─────  ─  ─ ─   ─ ─ ─  ─►",
        f"   │    {conn_ct} [SQ {sq_ct.zfill(2)}{ch_ct}{bm_ct.ljust(6)}] existentialCoreThreat    ─┬──► Sign: 0x{session_hashes.get('threat_struct_sign', '00000000')} {ch_ct} {tg_ct}",
        f"   │    {vl_ct}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatStructHash', '')}\"",
        f"   │    {conn_ctl} [SQ {sq_ctl.zfill(2)}{ch_ctl}{bm_ctl.ljust(6)}] CoreThreatLegal          ─┬──► Sign: 0x{session_hashes.get('threat_legal_sign', '00000000')} {ch_ctl} {tg_ctl}",
        f"   │    {vl_ct}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatLegalHash', '')}\"",
        f"   │    {conn_ctv} [SQ {sq_ctv.zfill(2)}{ch_ctv}{bm_ctv.ljust(6)}] CoreThreatShadowVacuum    ─┬─► Sign: 0x{session_hashes.get('threat_vacuum_sign', '00000000')} {ch_ctv} {tg_ctv}",
        f"   │    {vl_ctv}                                          └─► Signature: \"{session_hashes.get('existentialCoreThreatShadowVacuumHash', '')}\"",
        f"   │    {conn_cts} [SQ {sq_cts.zfill(2)}{ch_cts}{bm_cts.ljust(6)}] existentialCoreThreat.py  ─┬─► Sign: 0x{session_hashes.get('threat_sign', '00000000')} {ch_cts} {tg_cts}",
        f"   │                                                 └─► Signature: \"{session_hashes.get('existentialCoreThreatHash', '')}\"",
        " ─ │ ───────────────────────────────────────────────────",
        f"   └── [SQ {sq_ch.zfill(2)} : {bm_ch.ljust(6)}] existen...CoreSignatures.py   ──┬─► Sign: 0x{session_hashes.get('chain_sign', '00000000')} | {tg_ch}",
        f"                                                    └─► Signature: \"{session_hashes.get('existentialCoreChainHash', '')}\""
    ]

    # Helper function to remove ANSI escape color codes when calculating terminal character lengths
    def clean_len(s):
        import re
        return len(re.sub(r'\033\[[0-9;]*m', '', s))

    # Calculate precise horizontal box padding boundaries
    max_content_width = max(clean_len(line) for line in raw_lines)
    box_width = max_content_width + 4

    # 3. PAINT THE PERFECT SEAMLESS ENCLOSURE BOX
    error_handler.print("┌" + "─" * box_width + "┐", level="local")
    
    for line in raw_lines:
        visible_length = clean_len(line)
        trailing_spaces = " " * (box_width - visible_length - 2)
        error_handler.print(f"│ {line}{trailing_spaces} │", level="local")
        
    error_handler.print("└" + "─" * box_width + "┘", level="local")


def calculate_file_sha256(file_path: str) -> str:
    """
    Computes a pristine SHA-256 hash across a target file by streaming 
    its raw binary data payload in safe, high-performance 64 KB memory chunks.
    """
    if not os.path.exists(file_path):
        return "0000000000000000000000000000000000000000"

    sha256_hasher = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as binary_stream:
            # Read in 64 KB chunks to handle large structures without memory exhaustion
            for block_chunk in iter(lambda: binary_stream.read(65536), b""):
                sha256_hasher.update(block_chunk)
        return sha256_hasher.hexdigest()
    except Exception:
        # Fallback tracking stub if an asset is locked or blocked by OS access constraints
        return "0000000000000000000000000000000000000000"



def compute_integrity_chain(error_handler, rule_group_list: list, live_hashes: dict) -> dict:
    """
    Natively parses structural sequences, aggregates look-back history blocks, 
    and writes the final compiled signature tokens straight into the ending chain node.
    """
    # Sort rules strictly by their order sequence field parameter to keep the trail predictable
    sorted_elements = sorted(rule_group_list, key=lambda x: x[2])
    
    chain_active = False
    accumulated_trail_hashes = []
    chain_metadata_log = []
    
    # Extract your root magic string bytes to salt your loops
    magic_salt_bytes = existenzMeta.MAGIC["RAW"].encode('utf-8')

    for label, glue_tuple, chronological_order in sorted_elements:
        struct_name, status_mask, op_flags, hex_identifier, file_path, old_sig = glue_tuple
        
        # Look up the current hash computed during this session
        hash_var_name = f"existential{label}Hash"
        current_node_hash = live_hashes.get(hash_var_name, "")

        # 1. TRIGGER: Open Chain Window Sequence
        if bool(op_flags & 1): # SIGN_CHAIN_START
            chain_active = True
            accumulated_trail_hashes = []
            chain_metadata_log = []
            error_handler.print(f"      [⛓️] Chain Session Opened at Sequence: {chronological_order} ({label})", level="info")

        if chain_active and current_node_hash:
            # Check if this link requires magic salting blocks
            if bool(op_flags & 2): # SIGN_MAGIC_HASH
                salted_payload = magic_salt_bytes + current_node_hash.encode('utf-8')
                link_hash = hmac.new(magic_salt_bytes, salted_payload, hashlib.sha256).hexdigest()
                chain_metadata_log.append(f"Seq {chronological_order} ({label}) + MAGIC")
            else:
                link_hash = current_node_hash
                chain_metadata_log.append(f"Seq {chronological_order} ({label}) + HASH")
                
            accumulated_trail_hashes.append(link_hash)

        # 2. ANCHOR TRIGGER: Seal and Commit the Compiled Signature
        if bool(op_flags & 256) and chain_active: # SIGN_CHAIN_END
            # Assemble the consolidated block signature boundaries
            block_payload_string = "".join(accumulated_trail_hashes)
            final_chain_hash = hmac.new(magic_salt_bytes, block_payload_string.encode('utf-8'), hashlib.sha256).hexdigest()
            
            # Map the resulting hash straight to the ending node's session tracking variable
            live_hashes[f"existential{label}ChainHash"] = final_chain_hash
            
            error_handler.print(f"      [🔒] Chain Sealed at Sequence {chronological_order}! Connected Elements: {chain_metadata_log}", level="notice")
            error_handler.print(f"           Final Compiled Signature: {final_chain_hash[:32]}...", level="info")
            
            # Close the tracking window until the next START bit triggers
            chain_active = False

    return live_hashes


def calculate_op_driven_hash(target_dict: dict, op_flags: int) -> str:
    """
    Executes an opcode-driven cryptographic hash pass based on your 
    existenzIntegrityKeysHandler execution instructions.
    """
    from engineSigningStruct import existenzIntegrityKeysHandler
    
    if not target_dict:
        return hashlib.sha256(b"").hexdigest()

    # Sort keys alphabetically to keep serialization perfectly predictable
    sorted_keys = sorted(target_dict.keys())
    hasher = hashlib.sha256()

    # Determine execution behavior based on bitmask flags
    include_keys = bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_KEYS)
    include_values = bool(op_flags & existenzIntegrityKeysHandler.SIGN_TYPE_VALUES)

    # Fallback to signing both if neither bit is explicitly set but dictionary tracking is active
    if not include_keys and not include_values:
        include_keys = True
        include_values = True

    for k in sorted_keys:
        v = target_dict[k]
        
        # 1. Execute SIGN_TYPE_KEYS path if enabled
        if include_keys:
            hasher.update(str(k).encode('utf-8'))
            
        # 2. Execute SIGN_TYPE_VALUES path if enabled
        if include_values:
            # Flatten inner dictionary structures to safe string data-dense tracks if nested
            if isinstance(v, dict):
                v_str = json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
            else:
                v_str = str(v)
            hasher.update(v_str.encode('utf-8'))

    return hasher.hexdigest()



def calculate_aggregate_circle_hash_v1(circle_files_dict: dict) -> str:
    """
    Computes a canonical SHA-256 hash across all sorted filename-hash pairs 
    in a tracking circle to capture an absolute state snapshot.
    """
    if not circle_files_dict:
        return hashlib.sha256(b"").hexdigest()
        
    # Serialize with strict, sorted, zero-whitespace rules matching your configuration
    canonical_body = json.dumps(
        circle_files_dict, 
        sort_keys=True, 
        ensure_ascii=True, 
        separators=(',', ':')
    ).encode('utf-8')
    
    return hashlib.sha256(canonical_body).hexdigest()

def calculate_aggregate_circle_hash(circle_files_dict: dict, op_flags: int = 0) -> str:
    """
    Computes an absolute state snapshot hash across all filename-hash pairs 
    in a tracking circle using the active integrity opcode parameters.
    """
    # If explicit dictionary tracking opcodes are passed, route directly through the opcode evaluator
    if op_flags > 0:
        return calculate_op_driven_hash(circle_files_dict, op_flags)
        
    # Standard fallback tracking if called raw
    if not circle_files_dict:
        return hashlib.sha256(b"").hexdigest()
        
    canonical_body = json.dumps(
        circle_files_dict, 
        sort_keys=True, 
        ensure_ascii=True, 
        separators=(',', ':')
    ).encode('utf-8')
    
    return hashlib.sha256(canonical_body).hexdigest()


def resolve_live_git_commit(repo_root: str) -> str:
    """Dynamically extracts the raw local 64-character SHA-256 Git commit head tracking signature hash."""
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], 
            cwd=repo_root, 
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return commit_hash
    except Exception:
        # Graceful fallback signature stub if executing in an uninitialized environment space
        return "0000000000000000000000000000000000000000"


def gather_folder_files_v2(folder_relative_path: str, repo_root: str = None) -> dict:
    """Traverses a single target folder recursively to catalog all available file hashes."""
    file_matrix = {}
    
    # Dynamically resolve root: use the passed parameter or fall back to your global tracking flag constant
    active_root = repo_root if repo_root is not None else (REPO_ROOT if 'REPO_ROOT' in globals() else ".")
    full_folder_path = os.path.join(active_root, folder_relative_path)

    if not os.path.exists(full_folder_path):
        return file_matrix

    for root, _, files in os.walk(full_folder_path):
        if "__pycache__" in root or ".git" in root:
            continue

        for file in files:
            if file == "manifest.json" or file.endswith(".pyc") or file.startswith("."):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, active_root)
            rel_path = rel_path.replace("\\", "/")
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix

def gather_folder_files_v1(folder_relative_path: str, repo_root: str = None) -> dict:
    """Traverses a single target folder recursively to catalog all available file hashes."""
    file_matrix = {}
    
    # Dynamically resolve root: use the passed parameter or fall back to your global tracking flag constant
    active_root = repo_root if repo_root is not None else (REPO_ROOT if 'REPO_ROOT' in globals() else ".")
    full_folder_path = os.path.join(active_root, folder_relative_path)

    if not os.path.exists(full_folder_path):
        return file_matrix

    for root, _, files in os.walk(full_folder_path):
        if "__pycache__" in root or ".git" in root:
            continue

        for file in files:
            if file == "manifest.json" or file.endswith(".pyc") or file.startswith("."):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, active_root)
            rel_path = rel_path.replace("\\", "/")
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix

def catalog_circle_track(repo_root: str, relative_path: str, manifest_filename: str) -> dict:
    """
    Recursively scans an active ring folder directory and compiles its internal file 
    structures into a clean tracking map of relative repository path keys to binary SHA-256 hashes.
    """
    track_matrix = {}
    absolute_folder_path = os.path.abspath(os.path.join(repo_root, relative_path))
    
    if not os.path.exists(absolute_folder_path):
        return track_matrix

    for root, _, files in os.walk(absolute_folder_path):
        if "__pycache__" in root or ".git" in root:
            continue
            
        for file in files:
            # Explicitly exclude state tracking lockfiles, configurations, or the manifest ledger itself
            if file in [manifest_filename, "sign_integrity_config.json", ".existentialLock"] or file.endswith(".pyc") or file.startswith("."):
                continue

            full_file_path = os.path.abspath(os.path.join(root, file))
            # Build forward-slash path keys matching standard web repository tracking rules
            relative_repo_key = os.path.relpath(full_file_path, repo_root).replace("\\", "/")
            
            # Use your library's binary hasher routine natively
            hasher_signature = engineSigningLibrary.calculate_file_sha256(full_file_path)
            if hasher_signature:
                track_matrix[relative_repo_key] = hasher_signature

    return track_matrix

def pipeline_step_current(current_stage_str: str, error_handler):
    """
    Resolves the incoming stage string against existenzSteps bitweights,
    logs the current active state token, and exports it to the environment.
    """
    normalized_input = str(current_stage_str).strip().upper()
    
    # FIXED: Map unified staging terms directly to your exact IntFlag tokens
    if normalized_input == "SIGN":
        target_attribute_name = "STEP_SIGN_PUBLIC"
    elif normalized_input == "VERIFY":
        target_attribute_name = "STEP_VERIFY"
    elif normalized_input == "MANIFEST":
        target_attribute_name = "STEP_MANIFEST"
    else:
        target_attribute_name = f"STEP_{normalized_input}"
    
    if hasattr(existenzSteps, target_attribute_name):
        current_step_flag = getattr(existenzSteps, target_attribute_name)
    else:
        current_step_flag = existenzSteps.STEP_NONE
        
    current_step_name = current_step_flag.name.replace("STEP_", "") if current_step_flag != existenzSteps.STEP_NONE else "UNKNOWN"
    error_handler.print(f"  [➔] Pipeline Stage Active: {current_step_name:<16} [Weight: {int(current_step_flag)}]", level="notice")

def pipeline_step_next(current_stage_str: str, error_handler) -> str:
    """
    Evaluates the active execution step string and advances the tracking state.
    Maps simple stage arguments to the next logical step name for GITHUB_ENV.
    """
    stage_lower = str(current_stage_str).strip().lower()
    
    # Directly translate clean unified command states into their next chronological target names
    if stage_lower == "manifest":
        next_step_name = "sign"
    elif stage_lower == "sign":
        next_step_name = "verify"
    else:
        next_step_name = "success"

    github_env_file = os.environ.get('GITHUB_ENV')
    if github_env_file:
        try:
            with open(github_env_file, "a", encoding="utf-8") as gef:
                gef.write(f"NEXT_PIPELINE_STAGE={next_step_name}\n")
            error_handler.print(f"  [+] Pipeline Link: Progressive routing unblocked -> NEXT_PIPELINE_STAGE={next_step_name}", level="notice")
        except Exception as env_err:
            error_handler.print(f"Non-fatal error logging workspace environment variable: {env_err}", level="debug")
            
    return next_step_name


def compute_sha256(file_path: str) -> str:
    """Redirects file streaming straight through your uniform crypto engine helper."""
    return visualMixEngineCrypto.calculate_file_sha256(file_path)

def gather_folder_files(folder_relative_path: str, repo_root: str = None) -> dict:
    """Traverses a single target folder recursively to catalog all available file hashes."""
    file_matrix = {}
    
    # Dynamically resolve root: use the passed parameter or fall back to your global tracking flag constant
    active_root = repo_root if repo_root is not None else (REPO_ROOT if 'REPO_ROOT' in globals() else ".")
    full_folder_path = os.path.join(active_root, folder_relative_path)

    if not os.path.exists(full_folder_path):
        return file_matrix

    for root, _, files in os.walk(full_folder_path):
        if "__pycache__" in root or ".git" in root:
            continue

        for file in files:
            if file == "manifest.json" or file.endswith(".pyc") or file.startswith("."):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, active_root)
            rel_path = rel_path.replace("\\", "/")
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix


def load_private_key(identity: str, path: str) -> ed25519.Ed25519PrivateKey:
    """Invokes the consolidated global cryptography library handler."""
    return visualMixEngineCrypto.load_private_key(identity, path, error_handler, REPO_GITHUB)

def solve_ring_requirements(stage: str, circle: str = "dist") -> tuple:
    """
    BITWISE ROUTINE ROUTER: Intersects stage tokens AND active circle targets 
    against IntFlag bitweights to enforce air-tight signing constraints.
    """
    from engineSigningStruct import existenzIntegrityKeyStatus
    
    stage_lower = str(stage).lower()
    circle_lower = str(circle).lower()
    
    # 1. Elevate bit weights natively based on the absolute highest privilege targeted
    if "master" in stage_lower or circle_lower == "master":
        # Master tracks act as the final gatekeeper, requiring ALL private key states
        ring_weight = (existenzIntegrityKeyStatus.KEY_PVT_PLATFORM | 
                       existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER | 
                       existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
    elif "tools" in stage_lower or "build" in stage_lower or circle_lower in ["tools", "build"]:
        # Tools and build options scale up by enforcing Developer and Platform checks
        ring_weight = (existenzIntegrityKeyStatus.KEY_PVT_PLATFORM | 
                       existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
    else:
        # Default baseline environment fallback layer state configuration for distribution
        ring_weight = existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT

    return (
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
    )


def solve_ring_requirements_v1(stage: str) -> tuple:
    """
    BITWISE ROUTINE ROUTER: Uses IntFlag bitmask matching to verify which keys are needed.
    Returns: (requires_environment, requires_platform, requires_developer, requires_personal)
    """
    # Normalize input string constraints smoothly
    stage_lower = str(stage).lower()
    
    if "master" in stage_lower:
        # Master ring requires every structural key active to sign the core base paths
        ring_weight = (existenzIntegrityKeyStatus.KEY_PVT_PLATFORM | 
                       existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER | 
                       existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
    elif "tools" in stage_lower or "build" in stage_lower:
        # Tools and build options scale up by enforcing Developer and Platform checks
        ring_weight = (existenzIntegrityKeyStatus.KEY_PVT_PLATFORM | 
                       existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER)
    else:
        # Default fallback ring for deployment distribution channels (dist)
        ring_weight = existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT

    return (
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER),
        bool(ring_weight & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
    )

class visualMixEngineEnvironment:
    def __init__(self, error_handler, repo_github_flag: bool, post: str = "SIGN_EXISTENZ_AUDIT_", conf: dict = None, namespace="visualMix"):
        self.error_handler = error_handler
        self.repo_github_flag = repo_github_flag
        self.post   = post
        self.conf   = conf or {}
        self.namespace = namespace

    def load_secret_key(self) -> dict:
        """Loads environment configurations smoothly, bypassing missing offline keys on remote public runners."""
        skeleton = {}

        keys_pub = ["PUBLIC", "FINGERPRINT"]
        keys_pvt = ["PRIVATE", "PHRASE"]

        for key in (keys_pvt + keys_pub):
            conf_key = f"{self.post}{key.upper()}"
            env_key  = f"{self.post}{key.upper()}"

            env_fallback_value = os.environ.get(env_key)
            skeleton[env_key] = self.conf.get(conf_key, env_fallback_value)

        time_key = f"{self.post}TIME"
        skeleton[time_key] = self.conf.get(time_key, os.environ.get(time_key, int(time.time())))
        
        raw_pvt_key = skeleton.get(f"{self.post}PRIVATE")
        env_pub_key = skeleton.get(f"{self.post}PUBLIC")
        env_finger  = skeleton.get(f"{self.post}FINGERPRINT")
        raw_phrase  = skeleton.get(f"{self.post}PHRASE")

        missing_fields = []
        if not raw_pvt_key: missing_fields.append(f"{self.post}PRIVATE")
        if not env_pub_key:  missing_fields.append(f"{self.post}PUBLIC")
        if not env_finger:   missing_fields.append(f"{self.post}FINGERPRINT")
        
        if missing_fields:
            # FIXED: If running on a public server, missing offline keys are totally normal. Skip instead of crashing.
            if self.repo_github_flag and self.post != "SIGN_EXISTENZ_AUDIT_":
                print(f"  [ ] Ingest Namespace:      '{self.namespace}' -> Skipping offline signing track (running on public server).")
                return skeleton
            
            # Crash only if the mandatory cloud environment key itself is missing
            self.error_handler.print(f"Loop-driven environment validation failed. Unresolved tracks: {missing_fields}", level="error", exit_code=63)

        clean_pub_display = env_pub_key.strip().split()[-1] if len(env_pub_key.strip().split()) > 1 else 'Custom Format'
        print(f"  [+] Ingest Namespace:      '{self.namespace}' Loop-Driven Tracker Block")
        print(f"  [+] Ingested Public Key:   '{clean_pub_display}'")
        print(f"  [+] Ingested Fingerprint:  {env_finger.strip()}")
        print(f"  [+] Private Key Payload:   Loaded ({len(raw_pvt_key.strip())} characters)")

        password_bytes = None
        if raw_phrase and str(raw_phrase).strip():
            print(f"  [+] Key Protection State:  Encrypted passphrase token active")
            password_bytes = str(raw_phrase).strip().encode('utf-8')
        else:
            print(f"  [ ] Key Protection State:  Assuming plaintext unencrypted asset format")

        try:
            pvt_bytes = raw_pvt_key.strip().encode('utf-8')
            parsed_private_key = visualMixEngineCrypto.deserialize_ssh_private_key(
                pvt_bytes,
                password_bytes=password_bytes
            )
            print("\033[1;32m  [+] Cryptographic Validation: Key parsing loop verified successfully!\033[0m")
            skeleton["_OBJECT"] = parsed_private_key
            
        except Exception as crypto_fault:
            self.error_handler.print(f"Failed to instantiate environment key: {crypto_fault}", level="error", exit_code=67)

        return skeleton

def render_cryptographic_structural_tree(error_handler, session_hashes: dict, matrix_signed_rows: list):
    """
    Renders your exact data-dense repository tree map natively using your 
    centralized, decoupled logging engine interface shortcuts.
    """
    from engineSigningStruct import existenzIntegrityKeyStatus

    # 1. Build rapid rule lookup directories eliminating global name collisions
    matrix_rules_lookup = {row[0]: row for row in matrix_signed_rows if row[0] != "Magic"}

    def get_layer_tags(layer_name, is_last_in_group=False):
        chain_arrow = " | "
        connector = "└──" if is_last_in_group else "├──"
        v_line    = "│  "
        
        if layer_name not in matrix_rules_lookup:
            return "0x00", "0", "+[HASH]+", connector, v_line, chain_arrow
            
        name, short_var, hash_var, sign_var, bitmask, seq = matrix_rules_lookup[layer_name]
        
        # FIXED: Bound strictly to your true IntFlag structural attributes to avoid mask dropping
        requires_signing = bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_ENVIRONMENT or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER or
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
                                
        is_signed = len(sign_var) >= 64 and not sign_var.startswith(name)
        
        # Check if the asset is chained natively via the status flags
        if bool(bitmask > 1 and (bitmask & existenzIntegrityKeyStatus.KEY_IS_PUBLIC)):
            chain_arrow = " ► "
            connector = "╚══" if is_last_in_group else "╠══"
            v_line    = "║  "

        tags = []
        if is_signed:
            if bitmask > 1 and (bitmask & existenzIntegrityKeyStatus.KEY_IS_PUBLIC): tags.append("+[CHN]")
            if bitmask & existenzIntegrityKeyStatus.KEY_IS_VERIFIED:   tags.append("+[MAGIC]")
            if bitmask & existenzIntegrityKeyStatus.KEY_IS_PRIVATE:    tags.append("+[SHA256]")
            if bitmask & 262144:                                       tags.append("+[IMMUTABLE]") # Core Immutable boundary check
        else:
            if requires_signing:
                pfm_tag = "+PFM" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM) else ""
                dev_tag = "+DEV" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER) else ""
                psn_tag = "+PSN" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL) else ""
                tags.append(f"+PK:{pfm_tag}{dev_tag}{psn_tag}")
            else:
                pfm_tag = "-PFM" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM) else ""
                dev_tag = "-DEV" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER) else ""
                psn_tag = "-PSN" if bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL) else ""
                tags.append(f"-PK:{pfm_tag}{dev_tag}{psn_tag}")

        if not is_signed and requires_signing:
            return f"{hex(bitmask)}", str(seq), f"\033[1;31m[ ! NOT SIGNED ! ] {' '.join(tags)}\033[0m", "├──", "│ ", " └► " if is_last_in_group else "├──"
            
        return f"{hex(bitmask)}", str(seq), " ".join(tags), connector, v_line, chain_arrow

    # 2. Extract specific session tokens safely avoiding lookup dropouts
    magic_token = session_hashes.get("existentialCoreMagicHash", "UNKNOWN")
    check_token = session_hashes.get("existentialCoreCheckHash", "UNSIGNED")
    core_ver    = "v0.76.16"

    # 3. Stream out your vibrant structural mapping grid lines through error_handler.print
    error_handler.print(f"  [MAGIC] existentialCoreCheckMagic        : {magic_token}", level="local")
    error_handler.print(f"  [CHECK] existentialCoreCheckSignature    : {check_token}", level="local")
    error_handler.print("", level="local")
    
    # Combined line construction matching horizontal tree padding specs
    error_handler.print(f"──┬ [ Existenz {core_ver}   ] " + "─" * 103, level="local")

    bm_c, sq_c, tg_c, _, _, _ = get_layer_tags("Core")
    bm_cb, sq_cb, tg_cb, _, _, _ = get_layer_tags("Cores")        
    bm_cc, sq_cc, tg_cc, _, _, _ = get_layer_tags("CoreCheck")
    bm_ch, sq_ch, tg_ch, _, _, _ = get_layer_tags("CoreChain")        
    bm_ct, sq_ct, tg_ct, conn_ct, vl_ct, ch_ct = get_layer_tags("CoreThreatStruct", is_last_in_group=False)
    bm_ctl, sq_ctl, tg_ctl, conn_ctl, vl_ctl, ch_ctl = get_layer_tags("CoreThreatLegal", is_last_in_group=False)
    bm_ctv, sq_ctv, tg_ctv, conn_ctv, vl_ctv, ch_ctv = get_layer_tags("CoreThreatShadowVacuum", is_last_in_group=False)
    bm_cts, sq_cts, tg_cts, conn_cts, vl_cts, ch_cts = get_layer_tags("CoreThreat", is_last_in_group=True)

    error_handler.print("  │ ", level="local")
    error_handler.print(f"  ├── [SQ {sq_c.zfill(2)} | {bm_c.ljust(6)}] existentialCore.py          ─┬─► Sign: 0x{session_hashes.get('core_sign', '00000000')} | {tg_c}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoreHash', '')}\"", level="local")
    
    error_handler.print(f"  ├── [SQ {sq_cb.zfill(2)} | {bm_cb.ljust(6)}] existentialCores.json       ─┬─► Sign: 0x{session_hashes.get('cores_sign', '00000000')} | {tg_cb}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoresHash', '')}\"", level="local")        
    
    error_handler.print(f"  ├── [SQ {sq_cc.zfill(2)} | {bm_cc.ljust(6)}] existentialCoreCheck.py     ─┬─► Sign: 0x{session_hashes.get('check_sign', '00000000')} | {tg_cc}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoreCheckHash', '')}\"", level="local")
    
    error_handler.print("  │  ", level="local")            
    error_handler.print("  ├──► class existentialCoreThreatSignatures ────────────  ── ─ ── ─────  ─  ─ ─   ─ ─ ─  ─►", level="local")
    
    error_handler.print(f"  │    {conn_ct} [SQ {sq_ct.zfill(2)}{ch_ct}{bm_ct.ljust(6)}] existentialCoreThreat    ─┬──► Sign: 0x{session_hashes.get('threat_struct_sign', '00000000')} {ch_ct} {tg_ct}", level="local")
    error_handler.print(f"  │    {vl_ct}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatStructHash', '')}\"", level="local")
    
    error_handler.print(f"  │    {conn_ctl} [SQ {sq_ctl.zfill(2)}{ch_ctl}{bm_ctl.ljust(6)}] CoreThreatLegal          ─┬──► Sign: 0x{session_hashes.get('threat_legal_sign', '00000000')} {ch_ctl} {tg_ctl}", level="local")
    error_handler.print(f"  │    {vl_ctl}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatLegalHash', '')}\"", level="local")
    
    error_handler.print(f"  │    {conn_ctv} [SQ {sq_ctv.zfill(2)}{ch_ctv}{bm_ctv.ljust(6)}] CoreThreatShadowVacuum    ─┬─► Sign: 0x{session_hashes.get('threat_vacuum_sign', '00000000')} {ch_ctv} {tg_ctv}", level="local")
    error_handler.print(f"  │    {vl_ctv}                                          └─► Signature: \"{session_hashes.get('existentialCoreThreatShadowVacuumHash', '')}\"", level="local")        
    
    error_handler.print(f"  │    {conn_cts} [SQ {sq_cts.zfill(2)}{ch_cts}{bm_cts.ljust(6)}] existentialCoreThreat.py  ─┬─► Sign: 0x{session_hashes.get('threat_sign', '00000000')} {ch_cts} {tg_cts}", level="local")
    error_handler.print(f"  │                                                 └─► Signature: \"{session_hashes.get('existentialCoreThreatHash', '')}\"", level="local")
    
    error_handler.print("─ │ ─" + "─" * 122, level="local")
    error_handler.print(f"  └── [SQ {sq_ch.zfill(2)} : {bm_ch.ljust(6)}] existen...CoreSignatures.py   ──┬─► Sign: 0x{session_hashes.get('chain_sign', '00000000')} | {tg_ch}", level="local")
    error_handler.print(f"                                                    └─► Signature: \"{session_hashes.get('existentialCoreChainHash', '')}\"", level="local")
    error_handler.print("─" * 127, level="local")

def render_cryptographic_structural_tree_old(error_handler, session_hashes: dict, matrix_signed_rows: list):
    """
    Renders your exact data-dense repository tree map natively using your 
    centralized, decoupled logging engine interface shortcuts.
    """
    # 1. Build rapid rule lookup directories eliminating global name collisions
    matrix_rules_lookup = {row[0]: row for row in matrix_signed_rows if row[0] != "Magic"}

    def get_layer_tags(layer_name, is_last_in_group=False):
        chain_arrow = " | "
        connector = "└──" if is_last_in_group else "├──"
        v_line    = "│  "
        
        if layer_name not in matrix_rules_lookup:
            return "0x00", "0", "+[HASH]+", connector, v_line, chain_arrow
            
        name, short_var, hash_var, sign_var, bitmask, seq = matrix_rules_lookup[layer_name]
        requires_signing = bool(bitmask & 16 or bitmask & 32 or bitmask & 64) # Synced to your new KeyStatus flags
        is_signed = len(sign_var) >= 64 and not sign_var.startswith(name)
        
        if bool(bitmask > 1 and (bitmask & 1)):
            chain_arrow = " ► "
            connector = "╚══" if is_last_in_group else "╠══"
            v_line    = "║  "

        tags = []
        if is_signed:
            if bitmask > 1 and (bitmask & 1): tags.append("+[CHN]")
            if bitmask & 2:   tags.append("+[MAGIC]")
            if bitmask & 8:   tags.append("+[SHA256]")
            if bitmask & 262144: tags.append("+[IMMUTABLE]")
        else:
            if requires_signing:
                tags.append("+PK:" + ("+PFM" if bitmask & 32 else "") + ("+DEV" if bitmask & 64 else "") + ("+PSN" if bitmask & 128 else ""))
            else:
                tags.append("-PK:" + ("-PFM" if bitmask & 32 else "") + ("-DEV" if bitmask & 64 else "") + ("-PSN" if bitmask & 128 else ""))

        if not is_signed and requires_signing:
            return f"{hex(bitmask)}", str(seq), f"\033[1;31m[ ! NOT SIGNED ! ] {' '.join(tags)}\033[0m", "├──", "│ ", " └► " if is_last_in_group else "├──"
            
        return f"{hex(bitmask)}", str(seq), " ".join(tags), connector, v_line, chain_arrow

    # 2. Extract specific session tokens safely avoiding lookup dropouts
    magic_token = session_hashes.get("existentialCoreMagicHash", "UNKNOWN")
    check_token = session_hashes.get("existentialCoreCheckHash", "UNSIGNED")
    core_ver    = "v0.76.16"

    # 3. Stream out your vibrant structural mapping grid lines through error_handler.print
    error_handler.print(f"  [MAGIC] existentialCoreCheckMagic        : {magic_token}", level="local")
    error_handler.print(f"  [CHECK] existentialCoreCheckSignature    : {check_token}", level="local")
    error_handler.print("", level="local")
    
    # Combined line construction matching horizontal tree padding specs
    error_handler.print(f"──┬ [ Existenz {core_ver}   ] " + "─" * 103, level="local")

    bm_c, sq_c, tg_c, _, _, _ = get_layer_tags("Core")
    bm_cb, sq_cb, tg_cb, _, _, _ = get_layer_tags("Cores")        
    bm_cc, sq_cc, tg_cc, _, _, _ = get_layer_tags("CoreCheck")
    bm_ch, sq_ch, tg_ch, _, _, _ = get_layer_tags("CoreChain")        
    bm_ct, sq_ct, tg_ct, conn_ct, vl_ct, ch_ct = get_layer_tags("CoreThreatStruct", is_last_in_group=False)
    bm_ctl, sq_ctl, tg_ctl, conn_ctl, vl_ctl, ch_ctl = get_layer_tags("CoreThreatLegal", is_last_in_group=False)
    bm_ctv, sq_ctv, tg_ctv, conn_ctv, vl_ctv, ch_ctv = get_layer_tags("CoreThreatShadowVacuum", is_last_in_group=False)
    bm_cts, sq_cts, tg_cts, conn_cts, vl_cts, ch_cts = get_layer_tags("CoreThreat", is_last_in_group=True)

    error_handler.print("  │ ", level="local")
    error_handler.print(f"  ├── [SQ {sq_c.zfill(2)} | {bm_c.ljust(6)}] existentialCore.py          ─┬─► Sign: 0x{session_hashes.get('core_sign', '00000000')} | {tg_c}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoreHash', '')}\"", level="local")
    
    error_handler.print(f"  ├── [SQ {sq_cb.zfill(2)} | {bm_cb.ljust(6)}] existentialCores.json       ─┬─► Sign: 0x{session_hashes.get('cores_sign', '00000000')} | {tg_cb}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoresHash', '')}\"", level="local")        
    
    error_handler.print(f"  ├── [SQ {sq_cc.zfill(2)} | {bm_cc.ljust(6)}] existentialCoreCheck.py     ─┬─► Sign: 0x{session_hashes.get('check_sign', '00000000')} | {tg_cc}", level="local")
    error_handler.print(f"  │                                              └─► Signature: \"{session_hashes.get('existentialCoreCheckHash', '')}\"", level="local")
    
    error_handler.print("  │  ", level="local")            
    error_handler.print("  ├──► class existentialCoreThreatSignatures ────────────  ── ─ ── ─────  ─  ─ ─   ─ ─ ─  ─►", level="local")
    
    error_handler.print(f"  │    {conn_ct} [SQ {sq_ct.zfill(2)}{ch_ct}{bm_ct.ljust(6)}] existentialCoreThreat    ─┬──► Sign: 0x{session_hashes.get('threat_struct_sign', '00000000')} {ch_ct} {tg_ct}", level="local")
    error_handler.print(f"  │    {vl_ct}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatStructHash', '')}\"", level="local")
    
    error_handler.print(f"  │    {conn_ctl} [SQ {sq_ctl.zfill(2)}{ch_ctl}{bm_ctl.ljust(6)}] CoreThreatLegal          ─┬──► Sign: 0x{session_hashes.get('threat_legal_sign', '00000000')} {ch_ctl} {tg_ctl}", level="local")
    error_handler.print(f"  │    {vl_ctl}                                         └──► Signature: \"{session_hashes.get('existentialCoreThreatLegalHash', '')}\"", level="local")
    
    error_handler.print(f"  │    {conn_ctv} [SQ {sq_ctv.zfill(2)}{ch_ctv}{bm_ctv.ljust(6)}] CoreThreatShadowVacuum    ─┬─► Sign: 0x{session_hashes.get('threat_vacuum_sign', '00000000')} {ch_ctv} {tg_ctv}", level="local")
    error_handler.print(f"  │    {vl_ctv}                                          └─► Signature: \"{session_hashes.get('existentialCoreThreatShadowVacuumHash', '')}\"", level="local")        
    
    error_handler.print(f"  │    {conn_cts} [SQ {sq_cts.zfill(2)}{ch_cts}{bm_cts.ljust(6)}] existentialCoreThreat.py  ─┬─► Sign: 0x{session_hashes.get('threat_sign', '00000000')} {ch_cts} {tg_cts}", level="local")
    error_handler.print(f"  │                                                 └─► Signature: \"{session_hashes.get('existentialCoreThreatHash', '')}\"", level="local")
    
    error_handler.print("─ │ ─" + "─" * 122, level="local")
    error_handler.print(f"  └── [SQ {sq_ch.zfill(2)} : {bm_ch.ljust(6)}] existen...CoreSignatures.py   ──┬─► Sign: 0x{session_hashes.get('chain_sign', '00000000')} | {tg_ch}", level="local")
    error_handler.print(f"                                                    └─► Signature: \"{session_hashes.get('existentialCoreChainHash', '')}\"", level="local")
    error_handler.print("─" * 127, level="local")

def execute_lookback_chain_validation(error_handler, live_session_hashes: dict, sorted_rules: list, magic_bytes: bytes):
    """
    Executes a rigorous backward trace through active sequence keys to assert 
    unbroken chain continuity and intercept unauthorized payload drift.
    """
    # Extract structural array index tracking flags natively
    all_active_sequences = {row[5] for row in sorted_rules}

    # 1. Phase One: Step through sorted execution rules and evaluate look-back vectors
    for layer_meta in sorted_rules:
        name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta
        resolved_target_hash = live_session_hashes.get(hash_var, hash_var)
        preceding_hashes, chain_metadata_log = [], []
        
        # Target the trailing boundary node of a sequence sequence loop block
        if (sequence - 1 in all_active_sequences) and (sequence + 1 not in all_active_sequences):
            check_seq = sequence - 1
            
            while True:
                # Trace backward to find preceding transactional node causes
                cause_row = next((row for row in sorted_rules if row[5] == check_seq), None)
                if not cause_row: 
                    break
                    
                c_name, c_short, c_hash, c_sign, c_bitmask, c_seq = cause_row
                resolved_cause_hash = live_session_hashes.get(c_hash, c_hash)
                
                # Check for cryptographic protection layers matching KeyStatus bit permissions
                requires_signature_modes = bool(c_bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM or 
                                                c_bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER or 
                                                c_bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
                
                if requires_signature_modes:
                    row_payload = magic_bytes + resolved_cause_hash.encode('utf-8')
                    preceding_hashes.insert(0, hmac.new(magic_bytes, row_payload, hashlib.sha256).hexdigest())
                    chain_metadata_log.insert(0, f"      [*] Seq {c_seq}+MAGIC | Connected Cryptographic Node: '{c_name}'")
                else:
                    preceding_hashes.insert(0, resolved_cause_hash)
                    chain_metadata_log.insert(0, f"      [*] Seq {c_seq}+HASH  | Connected Structural Asset:  '{c_name}'")
                
                check_seq -= 1
                
            if preceding_hashes:
                # Output operational validation steps cleanly to screen
                for log_line in chain_metadata_log: 
                    error_handler.print(log_line, level="local")
                    
                # Assemble consolidated block signature mapping boundaries
                accumulated_byte_string = "".join(preceding_hashes)
                computed_verify_hash = hmac.new(magic_bytes, accumulated_byte_string.encode('utf-8'), hashlib.sha256).hexdigest()
                
                # FIXED: Verified computed live values straight against target frozen signature mappings
                if not hmac.compare_digest(resolved_target_hash, computed_verify_hash):
                    error_handler.print("=" * 90, level="local")
                    error_handler.print(f" [!!!] CRYPTOGRAPHIC INTEGRITY MISSING [!!!]", level="local")
                    error_handler.print(f"       Layer Name:   '{name}' [Sequence: {sequence}]", level="local")
                    error_handler.print(f"       Expected:     {resolved_target_hash}", level="local")
                    error_handler.print(f"       Computed:     {computed_verify_hash}", level="local")
                    error_handler.print("=" * 90, level="local")
                    error_handler.print(f"Look-back mismatch at node '{name}' Seq [{sequence}]. Execution terminated.", level="error", exit_code=1)

    # 2. Phase Two: Assert that all required cryptographic format constraints remain unbroken
    for layer_meta in sorted_rules:
        name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta
        requires_signing = bool(bitmask & existenzIntegrityKeyStatus.KEY_PVT_PLATFORM or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_DEVELOPER or 
                                bitmask & existenzIntegrityKeyStatus.KEY_PVT_PERSONAL)
                                
        if requires_signing:
            valid_hex_format = bool(re.match(r"^[0-9a-fA-F:]+$", sign_var)) and len(sign_var) >= 32
            if not valid_hex_format:
                error_handler.print(f"Bitfield cryptographic cryptographic validation failure: Layer '{name}' failed bitmask check {hex(bitmask)}", level="error", exit_code=67)

    error_handler.print("Core cryptographic structural validations verified clean.", level="notice")


if __name__ == "__main__":
    # Test stub trigger when run directly in your workflow file
    if REPO_GITHUB:
        error_handler.notice(
            level="info", 
            message=f"engineSigningLibrary.py: [{REPO_GITHUB}]"
        )
                
    else:
        print("[!] Local execution skipped. This test routine targets GitHub Actions environment contexts.")
