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
    target_attribute_name = f"STEP_{normalized_input}"
    
    current_step_flag = getattr(existenzSteps, target_attribute_name, existenzSteps.STEP_NONE)
    current_step_name = current_step_flag.name.replace("STEP_", "") if current_step_flag != existenzSteps.STEP_NONE else "UNKNOWN"
    
    # Render uniform block message tracking execution entry point
    error_handler.print(f"  [➔] Pipeline Stage Active: {current_step_name:<16} [Weight: {int(current_step_flag)}]", level="notice")
    
    github_env_file = os.environ.get('GITHUB_ENV')
    if github_env_file:
        try:
            with open(github_env_file, "a", encoding="utf-8") as gef:
                gef.write(f"CURRENT_PIPELINE_STAGE={current_step_name.lower()}\n")
        except Exception as env_err:
            error_handler.print(f"Non-fatal error logging current state token: {env_err}", level="debug")

def pipeline_step_next(current_stage_str: str, error_handler) -> str:
    """
    Evaluates the active execution step against the existenzSteps IntFlag bitweights,
    calculates the progressive next pipeline target, and registers it to GITHUB_ENV.
    """
    # 1. Normalize the string entry and dynamically resolve its corresponding IntFlag attribute
    normalized_input = str(current_stage_str).strip().upper()
    target_attribute_name = f"STEP_{normalized_input}"
    
    current_step_flag = getattr(existenzSteps, target_attribute_name, existenzSteps.STEP_NONE)
    
    # 2. Compute subsequent target from sequence block indices
    next_step_flag = existenzSteps.STEP_NONE
    try:
        current_index = PIPELINE_SEQUENCE.index(current_step_flag)
        if current_index + 1 < len(PIPELINE_SEQUENCE):
            next_step_flag = PIPELINE_SEQUENCE[current_index + 1]
    except ValueError:
        # Fall back gracefully if step name was unrecognized in sequence registry array
        pass

    # 3. Clean up the programmatic label token string fields
    if next_step_flag != existenzSteps.STEP_NONE:
        next_step_name = next_step_flag.name.replace("STEP_", "").lower()
    else:
        next_step_name = "success"

    # 4. Atomically commit the variable layer to GitHub Environment maps
    github_env_file = os.environ.get('GITHUB_ENV')
    if github_env_file:
        try:
            with open(github_env_file, "a", encoding="utf-8") as gef:
                gef.write(f"NEXT_PIPELINE_STAGE={next_step_name}\n")
            error_handler.print(f"  [+] Pipeline Link: Progressive routing unblocked -> NEXT_PIPELINE_STAGE={next_step_name}", level="notice")
        except Exception as env_err:
            error_handler.print(f"Non-fatal error logging workspace boundary variable path: {env_err}", level="debug")
            
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


def solve_ring_requirements(stage: str) -> tuple:
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
        """Loads environment configurations smoothly by handling strict uppercase mappings."""
        skeleton = {}

        keys_pub = ["PUBLIC", "FINGERPRINT"]
        keys_pvt = ["PRIVATE", "PHRASE"]

        for key in (keys_pvt + keys_pub):
            # FIXED: Force upper-case token matching across all config blocks to prevent mask drops
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
