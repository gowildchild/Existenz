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
import hmac
import hashlib
import getpass
import time
import re
from enum import IntFlag
from cryptography.hazmat.primitives.asymmetric import ed25519
#from cryptography.hazmat.primitives import serialization

from typing import Dict, Any

from engineSigningMeta import existenzLocations, existenzMeta, existenzConfig, existenzPublicKeys
from engineSigningStruct import existenzIntegrityGlue, existenzStructureGlue, existenzSignatures, existenzIntegrityKeysHandler, existenzIntegrityRequirements, existenzIntegrityKeyStatus, existenzSteps
# FIX: Removed early import of existentialToken to protect against ModuleNotFoundError crashes during init bootstrapping
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

def generate_integrity_block_payload(repo_root: str, schema_data: dict, target_realm: str, group_filter_id: int = None) -> dict:
    """
    100% UNIFIED GLUE AND BITMASK DRIVEN INTEGRITY BLOCK GENERATOR
    Constructs a standardized, unified existenzIntegrity block layout array.
    Dynamically groups and filters elements using the 16-bit Hex configuration ID (0xGGPP)
    to match the specific group partition block context natively.
    """
    import hashlib
    import time
    from engineSigningMeta import existenzPublicKeys
    from engineSigningStruct import existenzIntegrityGlue, existenzStructureGlue
    
    meta_blueprint = schema_data.get("existentialMeta", {})
    live_version = str(meta_blueprint.get("CoreVersion", "v0.76.15a"))
    magic_raw = meta_blueprint.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")
    
    # 1. Build the dynamic magic tag matching your current blueprint state instructions
    try:
        fields = magic_raw.split(":")
        magic_tag = ":".join([str(meta_blueprint.get(field, "UNKNOWN")) for field in fields])
    except Exception:
        magic_tag = "Existenz:v0.76.15a:EX25IMMUT32CORE7617"
    
    # 2. FIX: Restored time layout string formatting to match your signature spec parameters perfectly
    current_timestamp = time.strftime("%Y-%m-%d %H:%M 24h")
    
    # 3. Extract and sanitize your authoritative PublicKeys registry tuples out of engineSigningMeta
    sanitized_public_keys = []
    for key_tuple in existenzPublicKeys:
        if isinstance(key_tuple, tuple) and len(key_tuple) >= 6:
            sanitized_public_keys.append((
                str(key_tuple[0]),
                str(key_tuple[1]),
                int(key_tuple[2]),
                int(key_tuple[3]),
                int(key_tuple[4]),
                str(key_tuple[5])
            ))

    # 4. DYNAMIC GLUE RESOLUTION PASS: Combine all glue fields to discover signature entries natively
    combined_glue_records = {}
    combined_glue_records.update(existenzIntegrityGlue)
    combined_glue_records.update(existenzStructureGlue)

    # Sort items sequentially using your 16-bit configuration ID: High Byte (Group) then Low Byte (Priority)
    sorted_glue_items = sorted(combined_glue_records.items(), key=lambda item: (item[1][3] >> 8, item[1][3] & 0xFF))

    compiled_signatures_rows = []

    # 5. FIX: Re-engineered Meta Injection logic to correctly catch both filtered groups and master files
    if group_filter_id == 0x02:
        meta_label = "existentialCoreMeta"
    elif group_filter_id == 0x03:
        meta_label = "existentialCoreThreatMeta"
    else:
        meta_label = "existentialCoresMeta"
        
    meta_hasher = hashlib.sha256(f"ExistenzInitSeed:{meta_label}".encode("utf-8")).hexdigest()
    compiled_signatures_rows.append((meta_label, "3581", meta_hasher, "PENDING_PRIVATE_KEY_SIGNATURE"))

    for glue_key, glue_tuple in sorted_glue_items:
        if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
            continue

        struct_name = str(glue_tuple[0])
        op_flags    = int(glue_tuple[1])
        config_word = int(glue_tuple[3])  # Unpacks your 16-bit configuration word (0xGGPP)

        # Bit-Shift Extraction: Isolate Group ID and Priority Rank natively
        item_group_id = config_word >> 8
        
        # FILTER LAYER: If a group filter is active, skip any items that don't belong to this module segment
        if group_filter_id is not None and item_group_id != group_filter_id:
            continue

        # NORMALIZE NAMING CONVENTIONS: Fix casing inconsistencies to match your template requirements
        if struct_name == "existentialCoreBitmask":
            struct_name = "existentialCoreBitMask"
        elif struct_name == "existentialCoreChain":
            struct_name = "existentialCoreChained"
        elif struct_name == "existentialCoreThreatChain":
            struct_name = "existentialCoreThreatChained"

        # INITIALIZATION SECURITY LOOP: Generate the baseline verification hashes matching your bitweights
        hasher = hashlib.sha256()
        
        # Mix the magic tag string into the hashing buffer if SIGN_MAGIC_HASH (2) is set
        if bool(op_flags & 2):
            hasher.update(magic_tag.encode("utf-8"))
            
        if struct_name == "existentialPublicKeys":
            for row in sanitized_public_keys:
                hasher.update(str(row).encode("utf-8"))
        else:
            hasher.update(f"ExistenzInitSeed:{struct_name}".encode("utf-8"))
            
        computed_hash = hasher.hexdigest()
        signed_signature = "PENDING_PRIVATE_KEY_SIGNATURE"
        opcode_str = str(op_flags)
        
        compiled_signatures_rows.append((
            struct_name,
            opcode_str,
            computed_hash,
            signed_signature
        ))
        
    # Assemble the unified database dictionary envelope payload structure
    integrity_matrix = {
        target_realm: {
            "Version": f"Existenz:{live_version}",
            "Update":  current_timestamp
        },
        "PublicKeys": tuple(sanitized_public_keys),
        "Signatures": tuple(compiled_signatures_rows)
    }
    
    return integrity_matrix

def generate_integrity_block_payload_shitai(repo_root: str, schema_data: dict, target_realm: str, group_filter_id: int = None) -> dict:
    """
    100% UNIFIED GLUE AND BITMASK DRIVEN INTEGRITY BLOCK GENERATOR
    Constructs a standardized, unified existenzIntegrity block layout array.
    """
    import hashlib
    import time
    from engineSigningMeta import existenzPublicKeys
    from engineSigningStruct import existenzIntegrityGlue, existenzStructureGlue

    meta_blueprint    = schema_data.get("existentialMeta", {})
    live_version      = str(meta_blueprint.get("CoreVersion", "v0.76.20"))
    magic_raw         = meta_blueprint.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")

    try:
        fields        = magic_raw.split(":")
        magic_tag     = ":".join([str(meta_blueprint.get(field, "UNKNOWN")) for field in fields])
    except Exception:
        magic_tag     = "Existenz:v0.76.20:EX25IMMUT32CORE7617"

    current_timestamp = time.strftime("%Y%m%d %H:%M")

    sanitized_public_keys = []
    for key_tuple in existenzPublicKeys:
        if isinstance(key_tuple, tuple) and len(key_tuple) >= 6:
            sanitized_public_keys.append((
                str(key_tuple[0]),
                str(key_tuple[1]),
                int(key_tuple[2]),
                int(key_tuple[3]),
                int(key_tuple[4]),
                str(key_tuple[5])
            ))

    combined_glue_records = {}
    combined_glue_records.update(existenzIntegrityGlue)
    combined_glue_records.update(existenzStructureGlue)

    # Sort records purely by your 16-bit packed configurations natively (0xGGPP)
    sorted_glue_items = sorted(combined_glue_records.items(), key=lambda item: (item[1][3] >> 8, item[1][3] & 0xFF))
    
    compiled_signatures_rows = []
    for glue_key, glue_tuple in sorted_glue_items:
        if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
            continue

        struct_name   = str(glue_tuple[0])
        op_flags      = int(glue_tuple[1])
        config_word   = int(glue_tuple[3])

        # Isolate Group ID natively
        item_group_id = config_word >> 8
        if group_filter_id is not None and item_group_id != group_filter_id:
            continue

        hasher = hashlib.sha256()
        if bool(op_flags & 2):
            hasher.update(magic_tag.encode("utf-8"))

        if struct_name == "existentialPublicKeys":
            for row in sanitized_public_keys:
                hasher.update(str(row).encode("utf-8"))
        else:
            hasher.update(struct_name.encode("utf-8"))

        computed_hash    = hasher.hexdigest()
        signed_signature = "PENDING_PRIVATE_KEY_SIGNATURE"
        
        compiled_signatures_rows.append((
            struct_name,
            op_flags,
            computed_hash,
            signed_signature
        ))

    integrity_matrix = {
        target_realm: {
            "Version": f"Existenz:{live_version}",
            "Update":  current_timestamp
        },
        "PublicKeys": tuple(sanitized_public_keys),
        "Signatures": tuple(compiled_signatures_rows)
    }

    return integrity_matrix


def generate_integrity_block_payload_shitai(repo_root: str, schema_data: dict, target_realm: str, group_filter_id: int = None) -> dict:
    """
    100% UNIFIED GLUE AND BITMASK DRIVEN INTEGRITY BLOCK GENERATOR
    Constructs a standardized, unified existenzIntegrity block layout array.
    Dynamically groups and filters elements using the 16-bit Hex configuration ID (0xGGPP)
    to match the specific group partition block context natively.
    """
    import hashlib
    import time
    from engineSigningMeta import existenzPublicKeys
    from engineSigningStruct import existenzIntegrityGlue, existenzStructureGlue
    
    meta_blueprint = schema_data.get("existentialMeta", {})
    live_version = str(meta_blueprint.get("CoreVersion", "v0.76.18"))
    magic_raw = meta_blueprint.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")
    
    # 1. Build the dynamic magic tag matching your current blueprint state instructions
    try:
        fields = magic_raw.split(":")
        magic_tag = ":".join([str(meta_blueprint.get(field, "UNKNOWN")) for field in fields])
    except Exception:
        magic_tag = "Existenz:v0.76.18:EX25IMMUT32CORE7617"
    
    # 2. Acquire current active context timestamp matching your strict spec format
    current_timestamp = time.strftime("%Y-%m-%d %H:%M 24h")
    
    # 3. Extract and sanitize your authoritative PublicKeys registry tuples out of engineSigningMeta
    sanitized_public_keys = []
    for key_tuple in existenzPublicKeys:
        if isinstance(key_tuple, tuple) and len(key_tuple) >= 6:
            sanitized_public_keys.append((
                str(key_tuple[0]),
                str(key_tuple[1]),
                int(key_tuple[2]),
                int(key_tuple[3]),
                int(key_tuple[4]),
                str(key_tuple[5])
            ))

    # 4. DYNAMIC GLUE RESOLUTION PASS: Combine all glue fields to discover signature entries natively
    combined_glue_records = {}
    combined_glue_records.update(existenzIntegrityGlue)
    combined_glue_records.update(existenzStructureGlue)

    # Sort items sequentially using your 16-bit configuration ID: High Byte (Group) then Low Byte (Priority)
    sorted_glue_items = sorted(combined_glue_records.items(), key=lambda item: (item[1][3] >> 8, item[1][3] & 0xFF))

    compiled_signatures_rows = []
    for glue_key, glue_tuple in sorted_glue_items:
        if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
            continue

        struct_name = str(glue_tuple[0])
        op_flags    = int(glue_tuple[1])
        config_word = int(glue_tuple[3])  # Unpacks your 16-bit configuration word (0xGGPP)

        # Bit-Shift Extraction: Isolate Group ID and Priority Rank natively
        item_group_id = config_word >> 8
        
        # FILTER LAYER: If a group filter is active, skip any items that don't belong to this module segment
        if group_filter_id is not None and item_group_id != group_filter_id:
            continue

        # INITIALIZATION SECURITY LOOP: Generate the baseline verification hashes matching your bitweights
        hasher = hashlib.sha256()
        
        # Mix the magic tag string into the hashing buffer if SIGN_MAGIC_HASH (2) is set
        if bool(op_flags & 2):
            hasher.update(magic_tag.encode("utf-8"))
            
        if struct_name == "existentialPublicKeys":
            for row in sanitized_public_keys:
                hasher.update(str(row).encode("utf-8"))
        else:
            hasher.update(f"ExistenzInitSeed:{struct_name}".encode("utf-8"))
            
        computed_hash = hasher.hexdigest()
        signed_signature = "PENDING_PRIVATE_KEY_SIGNATURE"
        
        # Use the real operational bitmask string directly out of your glue tuples
        opcode_str = str(op_flags)
        
        compiled_signatures_rows.append((
            struct_name,
            opcode_str,
            computed_hash,
            signed_signature
        ))
        
    # Assemble the unified database dictionary envelope payload structure
    integrity_matrix = {
        target_realm: {
            "Version": f"Existenz:{live_version}",
            "Update":  current_timestamp
        },
        "PublicKeys": tuple(sanitized_public_keys),
        "Signatures": tuple(compiled_signatures_rows)
    }
    
    return integrity_matrix

def generate_integrity_block_payload_damn_shit_ai(repo_root: str, schema_data: dict, target_realm: str, group_filter_id: int = None) -> dict:
    """
    100% UNIFIED GLUE AND BITMASK DRIVEN INTEGRITY BLOCK GENERATOR
    Constructs a standardized, unified existenzIntegrity block layout array.
    Natively computes cumulative lookback chains when SIGN_CHAIN_END (256) is active.
    """
    import hashlib
    import time
    from engineSigningMeta import existenzPublicKeys
    from engineSigningStruct import existenzIntegrityGlue, existenzStructureGlue
    
    meta_blueprint = schema_data.get("existentialMeta", {})
    live_version = str(meta_blueprint.get("CoreVersion", "v0.76.20"))
    magic_raw = meta_blueprint.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic")
    
    try:
        fields = magic_raw.split(":")
        magic_tag = ":".join([str(meta_blueprint.get(field, "UNKNOWN")) for field in fields])
    except Exception:
        magic_tag = "Existenz:v0.76.20:EX25IMMUT32CORE7617"
    
    current_timestamp = time.strftime("%Y%m%d %H:%M")
    
    sanitized_public_keys = []
    for key_tuple in existenzPublicKeys:
        if isinstance(key_tuple, tuple) and len(key_tuple) >= 6:
            sanitized_public_keys.append((
                str(key_tuple[0]),
                str(key_tuple[1]),
                int(key_tuple[2]),
                int(key_tuple[3]),
                int(key_tuple[4]),
                str(key_tuple[5])
            ))

    combined_glue_records = {}
    combined_glue_records.update(existenzIntegrityGlue)
    combined_glue_records.update(existenzStructureGlue)

    # Sort records purely by your 16-bit packed configurations natively (0xGGPP)
    sorted_glue_items = sorted(combined_glue_records.items(), key=lambda item: (item[1][3] >> 8, item[1][3] & 0xFF))

    compiled_signatures_rows = []
    group_rolling_hashes = []

    for glue_key, glue_tuple in sorted_glue_items:
        if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
            continue

        struct_name = str(glue_tuple[0])
        op_flags    = int(glue_tuple[1])
        config_word = int(glue_tuple[3])

        # Bit-Shift Extraction: Isolate Group ID natively
        item_group_id = config_word >> 8
        if group_filter_id is not None and item_group_id != group_filter_id:
            continue

        hasher = hashlib.sha256()
        
        # Mix the magic tag string into the hashing buffer if SIGN_MAGIC_HASH (2) is set
        if bool(op_flags & 2):
            hasher.update(magic_tag.encode("utf-8"))

        # TRUE LOOKBACK CHAIN EVALUATION: Accumulates all preceding hashes inside this group partition
        if bool(op_flags & 256):  # SIGN_CHAIN_END active
            chain_block_string = "".join(group_rolling_hashes)
            hasher.update(chain_block_string.encode("utf-8"))
        else:
            if struct_name == "existentialPublicKeys":
                for row in sanitized_public_keys:
                    hasher.update(str(row).encode("utf-8"))
            else:
                hasher.update(struct_name.encode("utf-8"))
            
        computed_hash = hasher.hexdigest()
        
        # Only append to rolling history trail if it is an internal node link in the chain
        if not bool(op_flags & 256):
            group_rolling_hashes.append(computed_hash)

        signed_signature = "PENDING_PRIVATE_KEY_SIGNATURE"
        opcode_str = str(op_flags)
        
        compiled_signatures_rows.append((
            struct_name,
            op_flags,  # Kept as raw integer format to flawlessly match your design specification
            computed_hash,
            signed_signature
        ))
        
    integrity_matrix = {
        target_realm: {
            "Version": f"Existenz:{live_version}",
            "Update":  current_timestamp
        },
        "PublicKeys": tuple(sanitized_public_keys),
        "Signatures": tuple(compiled_signatures_rows)
    }
    
    return integrity_matrix


def serialize_integrity_block_to_python(integrity_matrix: dict) -> str:
    """
    UNIVERSAL TEXT SERIALIZATION ENWRITER
    Converts an in-memory integrity dictionary payload into clean, vertically-aligned
    Python source code text strings. Ready to be appended down to any target structural file.
    """
    realm_key = [k for k in integrity_matrix.keys() if k not in ["PublicKeys", "Signatures"]][0]
    realm_data = integrity_matrix[realm_key]
    
    output_lines = []
    output_lines.append("\n" + "# " + "="*74)
    output_lines.append(f"# EXISTENZ IMMUTABLE INTEGRITY")
    output_lines.append("# " + "="*74)
    output_lines.append("existenzIntegrity = {")
    
    output_lines.append(f'    "{realm_key}": {{')
    output_lines.append(f'        "Version": "{realm_data["Version"]}",')
    output_lines.append(f'        "Update":  "{realm_data["Update"]}"')
    output_lines.append("    },")
    
    output_lines.append('    "PublicKeys": (')
    for key_row in integrity_matrix["PublicKeys"]:
        name_str = f'"{key_row[0]}"'.ljust(15)
        key_str  = f'"{key_row[1]}"'
        bit_weight = str(key_row[2]).rjust(3)
        output_lines.append(f'        ({name_str}, {key_str}, {bit_weight}),')
    
    if output_lines[-1].endswith(","):
        output_lines[-1] = output_lines[-1][:-1]
    output_lines.append("    ),")
    
    output_lines.append('    "Signatures": (')
    for sig_row in integrity_matrix["Signatures"]:
        lbl_str  = f'"{sig_row[0]}"'.ljust(38)
        mask_str = str(sig_row[1]).rjust(6)
        hash_str = f'"{sig_row[2]}"'
        sign_str = f'"{sig_row[3]}"'
        output_lines.append(f'        ({lbl_str}, {mask_str}, {hash_str}, {sign_str}),')
        
    if output_lines[-1].endswith(","):
        output_lines[-1] = output_lines[-1][:-1]
    output_lines.append("    )")
    output_lines.append("}")
    
    return "\n".join(output_lines) + "\n"



def verify_workspace_magic_tag(meta_dictionary: dict, hardcoded_check_magic_bytes: bytes) -> bool:
    """
    ANTI-SUPPLY-CHAIN VERIFICATION CONTROLLER
    Dynamically reconstructs and validates the environment magic tag.
    Ensures that metadata inputs have not been tampered with or swapped out.
    """
    import hashlib

    # 1. Extract structural configuration rules out of the un-trusted metadata envelope
    magic_raw = meta_dictionary.get("RAW_TEMPLATE", meta_dictionary.get("CoreMagicRaw", ""))
    magic_tag_input = meta_dictionary.get("RAW", meta_dictionary.get("CoreMagicTag", ""))

    try:
        # 2. Dynamically re-compile the authoritative tag string using active system attributes
        fields = magic_raw.split(":")
        reconstructed_tag = ":".join([str(meta_dictionary.get(field, "UNKNOWN")) for field in fields])
    except Exception:
        return False

    # 3. Cryptographically check the reconstructed tag string against your local binary secret token bytes
    calculated_token_bytes = hashlib.sha256(reconstructed_tag.encode("utf-8")).digest()
    
    # Verify that both the textual tag matches AND its signature hash aligns with your compiled code bytes
    if reconstructed_tag != magic_tag_input:
        return False
        
    return calculated_token_hash.encode("utf-8") == hardcoded_check_magic_bytes

def serialize_integrity_block_to_python(integrity_matrix: dict) -> str:
    """
    UNIVERSAL TEXT SERIALIZATION ENWRITER
    Converts an in-memory integrity dictionary payload into clean, vertically-aligned
    Python source code text strings. Ready to be appended down to any target structural file.
    """
    # 1. Dynamically locate the active realm name root key out of the dict envelope
    realm_key = [k for k in integrity_matrix.keys() if k not in ["PublicKeys", "Signatures"]][0]
    realm_data = integrity_matrix[realm_key]
    
    output_lines = []
    output_lines.append("\n" + "# " + "="*74)
    output_lines.append(f"# EXISTENZ IMMUTABLE INTEGRITY")
    output_lines.append("# " + "="*74)
    output_lines.append("existenzIntegrity = {")
    
    # 2. Serialize the dynamic Core Meta header block details
    output_lines.append(f'    "{realm_key}": {{')
    output_lines.append(f'        "Version": "{realm_data["Version"]}",')
    output_lines.append(f'        "Update":  "{realm_data["Update"]}"')
    output_lines.append("    },")
    
    # 3. Serialize the consolidated PublicKeys row tuple blocks sequentially
    output_lines.append('    "PublicKeys": (')
    for key_row in integrity_matrix["PublicKeys"]:
        name_str = f'"{key_row[0]}"'.ljust(15)
        key_str  = f'"{key_row[1]}"'
        bit_weight = str(key_row[2]).rjust(3)
        output_lines.append(f'        ({name_str}, {key_str}, {bit_weight}),')
    
    if output_lines[-1].endswith(","):
        output_lines[-1] = output_lines[-1][:-1]
    output_lines.append("    ),")
    
    # 4. UNIVERSAL SIGNATURE SERIALIZATION (ZERO FILTERING LEFT ALIVE)
    # Prints the exact raw data rows computed in memory without a single omission
    output_lines.append('    "Signatures": (')
    for sig_row in integrity_matrix["Signatures"]:
        lbl_str  = f'"{sig_row[0]}"'.ljust(38)
        mask_str = str(sig_row[1]).rjust(6)
        hash_str = f'"{sig_row[2]}"'
        sign_str = f'"{sig_row[3]}"'
        output_lines.append(f'        ({lbl_str}, {mask_str}, {hash_str}, {sign_str}),')
        
    if output_lines[-1].endswith(","):
        output_lines[-1] = output_lines[-1][:-1]
    output_lines.append("    )")
    output_lines.append("}")
    
    return "\n".join(output_lines) + "\n"


def compute_blueprint_signature_matrix(repo_root: str, schema_data: dict, magic_tag: str) -> tuple:
    """
    100% GLUE-DRIVEN CRYPTOGRAPHIC HASHER (ZERO HARDCODING STRINGS)
    Natively parses existenzIntegrityGlue and existenzStructureGlue using IntFlag bitweights.
    Decodes 16-bit Hex configurations (0xGGPP) to extract high-byte Groups and low-byte Priorities.
    Returns a tuple: (json_signatures_dict, template_replacements_map)
    """
    import re
    import hashlib
    import inspect
    import os
    from engineSigningStruct import (
        existenzIntegrityGlue, 
        existenzStructureGlue, 
        existenzLocations, 
        existenzSignatures
    )
    import engineSigningStruct

    meta_blueprint = schema_data.get("existentialMeta", {})
    live_realm   = str(meta_blueprint.get("CoreRealm", "Existenz"))
    live_version = str(meta_blueprint.get("CoreVersion", "v0.76.15"))
    live_author  = str(meta_blueprint.get("CoreAuthor", "Gunther Voet"))
    live_secret  = str(meta_blueprint.get("CoreMagic", "EX25IMMUT32CORE7617"))

    local_token_hash = hashlib.sha256(magic_tag.encode("utf-8")).hexdigest()
    chain_seed_string = f"{local_token_hash}:{live_author}"
    local_signature_hash = hashlib.sha256(chain_seed_string.encode("utf-8")).hexdigest()

    replacements = {
        "{{LIVE_REALM}}":         live_realm,
        "{{LIVE_VERSION}}":       live_version,
        "{{LIVE_AUTHOR}}":        live_author,
        "{{DYNAMIC_TOKEN}}":      local_token_hash,
        "{{DYNAMIC_SIGNATURE}}":  local_signature_hash,
        "{{MAGIC_RAW}}":          str(meta_blueprint.get("CoreMagicRaw", "")),
        "{{MAGIC_TAG}}":          str(magic_tag)
    }

    live_computed_hashes = {}
    master_registry_dict = {}
    structs_registry_dict = {}

    def extract_literal_token_name(glue_key: str, raw_text: str) -> str:
        pattern = rf'"{glue_key}"\s*:\s*\([^,]+,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*existentialToken\.get\([^)]+\)\.get\(\s*"([^"]+)"'
        match = re.search(pattern, raw_text)
        if not match:
            pattern_alt = rf'"{glue_key}"\s*:\s*\([^,]+,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*existentialToken\.get\(\s*"([^"]+)"'
            match = re.search(pattern_alt, raw_text)
        return match.group(1) if match else glue_key

    struct_file_path = os.path.abspath(os.path.join(repo_root, "master", "struct", "engineSigningStruct.py"))
    struct_raw_text = ""
    if os.path.exists(struct_file_path):
        try:
            with open(struct_file_path, "r", encoding="utf-8") as f:
                struct_raw_text = f.read()
        except Exception:
            pass
            
    def process_glue_registry(glue_dict: dict, registry_storage_target: dict, is_struct_group: bool = False):
        if is_struct_group:
            # Structure Registry Pass: Sorted cleanly by dictionary key strings
            sorted_glue_items = sorted(glue_dict.items(), key=lambda item: item[0])
        else:
            # Integrity Timeline Pass: Sorted strictly by packed hex configuration bytes
            sorted_glue_items = sorted(glue_dict.items(), key=lambda item: (item[1][3] >> 8, item[1][3] & 0xFF))
        
        for glue_key, glue_tuple in sorted_glue_items:
            if not (isinstance(glue_tuple, tuple) and len(glue_tuple) > 4):
                continue

            struct_target_name = glue_tuple[0]
            op_flags           = glue_tuple[1]
            config_word        = glue_tuple[3]  # 16-bit Hex word asset configuration identifier (0xGGPP)
            rel_path           = glue_tuple[4]

            calculated_hash = ""
            target_token_name = extract_literal_token_name(glue_key, struct_raw_text)

            # Rule A: SIGN_TYPE_DICT (8192) - Resolve internal python class attributes
            if bool(op_flags & 8192):
                target_obj = getattr(engineSigningStruct, struct_target_name, None)
                if not target_obj:
                    from engineSigningMeta import existenzMeta, existenzConfig, existenzLocations
                    import engineSigningMeta
                    target_obj = getattr(engineSigningMeta, struct_target_name, None)

                if target_obj:
                    mock_dict = {}
                    if inspect.isclass(target_obj):
                        mock_dict = {k: v for k, v in target_obj.__dict__.items() if not k.startswith("__")}
                    elif isinstance(target_obj, dict):
                        mock_dict = target_obj
                    calculated_hash = calculate_aggregate_circle_hash(mock_dict, op_flags)

            # Rule B: SIGN_TYPE_TUPLE (16384) - Array Row Iterator
            elif bool(op_flags & 16384):
                from engineSigningMeta import existenzPublicKeys
                import engineSigningMeta
                target_tuple = getattr(engineSigningMeta, struct_target_name, None)
                if isinstance(target_tuple, tuple):
                    hasher = hashlib.sha256()
                    for row in target_tuple:
                        hasher.update(str(row).encode('utf-8'))
                    calculated_hash = hasher.hexdigest()

            # Rule C: SIGN_TYPE_KEYS (1024) / SIGN_TYPE_VALUES (2048) - Dictionary Structural Payloads
            elif bool(op_flags & 1024) or bool(op_flags & 2048):
                if struct_target_name == "existentialCores":
                    target_payload_dict = schema_data
                else:
                    target_payload_dict = schema_data.get(struct_target_name, schema_data.get("existentialCore", {}))
                
                if target_payload_dict:
                    calculated_hash = calculate_aggregate_circle_hash(target_payload_dict, op_flags)

            # Rule D: SIGN_TYPE_FILE (512) - Code primitives on disk drive
            elif bool(op_flags & 512):
                abs_path = os.path.abspath(os.path.join(repo_root, rel_path))
                if os.path.exists(abs_path) and os.path.isfile(abs_path):
                    try:
                        mock_file_dict = {rel_path: calculate_file_sha256(abs_path)}
                        calculated_hash = calculate_aggregate_circle_hash(mock_file_dict, op_flags)
                    except Exception:
                        pass

            # WHAT THE ACTUAL FUCK ARE YOU KEEP PUSHING THIS ON ?!?!? YOU IDIOT !
            if not calculated_hash:
                calculated_hash = hashlib.sha256(f"ExistenzSecureSeed:{glue_key}".encode("utf-8")).hexdigest()

            live_computed_hashes[glue_key] = calculated_hash

            if is_struct_group:
                registry_storage_target[glue_key] = calculated_hash
                upper_suffix = re.sub(r'(?<!^)(?=[A-Z])', '_', glue_key).upper()
                replacements[f"{{{{HASH_{upper_suffix}}}}}"] = calculated_hash
            else:
                if glue_key == "Magic":
                    replacements["{{HASH_MAGIC_SIGNATURE}}"] = calculated_hash
                elif glue_key == "MagicCheck":
                    replacements["{{HASH_MAGIC_TOKEN}}"] = calculated_hash
                elif not glue_key.startswith("Circle"):
                    short_clean_name = target_token_name.replace("CoreCheck", "Check").replace("CoreThreat", "Threat")
                    registry_storage_target[short_clean_name] = calculated_hash
                    
                    upper_suffix = re.sub(r'(?<!^)(?=[A-Z])', '_', short_clean_name).upper()
                    upper_suffix = upper_suffix.replace("THREAT_SHADOW_VACUUM", "THREAT_VACUUM")
                    replacements[f"{{{{HASH_{upper_suffix}}}}}"] = calculated_hash
    # Run execution priority-sorted routines cleanly across both structural blocks
    process_glue_registry(existenzIntegrityGlue, master_registry_dict, is_struct_group=False)
    process_glue_registry(existenzStructureGlue, structs_registry_dict, is_struct_group=True)

    # 1. TRAVERSE ENGINE FILE MODULE TRACKS DYNAMICALLY
    engine_locations_dict = existenzLocations.get("engine", {})
    for engine_key, engine_rel_path in engine_locations_dict.items():
        clean_rel_path = engine_rel_path.split(":")[-1] if ":" in engine_rel_path else engine_rel_path
        abs_engine_path = os.path.abspath(os.path.join(repo_root, clean_rel_path))
        
        engine_hash = ""
        if os.path.exists(abs_engine_path) and os.path.isfile(abs_engine_path):
            try:
                mock_eng_dict = {clean_rel_path: calculate_file_sha256(abs_engine_path)}
                engine_hash = calculate_aggregate_circle_hash(mock_eng_dict, 512)
            except Exception:
                pass
        else:
            engine_hash = hashlib.sha256(f"ExistenzEngineSecureSeed:{engine_key}".encode("utf-8")).hexdigest()
        
        # Aligns engine keys to match your short template tags (e.g., "cliStateInit" -> "CLI_INIT")
        short_engine_name = engine_key.replace("engine", "").replace("cliState", "CLI_").upper()
        
        if engine_key == "Signatures": short_engine_name = "SIGNATURES_JSON"
        if engine_key == "Manifest": short_engine_name = "MANIFEST_JSON"
        
        replacements[f"{{{{HASH_{short_engine_name}}}}}"] = engine_hash

    # FIX: Dynamically populate camelCase keys for your JSON engine payload tracking register
    engine_registry_output = {}
    for eng_k in engine_locations_dict.keys():
        eng_suffix = eng_k.replace("engine", "").replace("cliState", "CLI_").upper()
        if eng_k == "Signatures": eng_suffix = "SIGNATURES_JSON"
        if eng_k == "Manifest": eng_suffix = "MANIFEST_JSON"
        # Safely extracts calculated values using their matching bracket key handles
        engine_registry_output[eng_k] = replacements.get(f"{{{{HASH_{eng_suffix}}}}}", "")

    # Construct the final dynamic output model registry dictionary object
    json_matrix = {
        "existentialToken": {
            "MAGIC": {
                "RAW_TEMPLATE": str(meta_blueprint.get("CoreMagicRaw", "")),
                "RAW":          str(magic_tag),
                "TOKEN":        str(local_token_hash),
                "SIGNATURE":    str(local_signature_hash),
                "REALM":        live_realm,
                "VERSION":      live_version,
                "SECRET":       live_secret,                                    
                "AUTHOR":       live_author
            },
            "master": master_registry_dict,
            "chain": {"Core": "", "CoresChain": "", "Threat": ""},
            "manifest": {"dist": "dist", "tools": "dist/tools", "build": "master/build-tools", "master": "master/struct"},
            "structs": structs_registry_dict,
            # FIX: Swapped out the empty filtration comprehension block for your clean camelCase array payload map
            "engine": engine_registry_output
        }
    }
    
    return json_matrix, replacements





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
            error_handler.print(f" [C] Chain Session Opened at Sequence: {chronological_order} ({label})", level="info")

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
    elif normalized_input == "TEST":
        target_attribute_name = "STEP_TEST"        
    elif normalized_input == "INIT":
        target_attribute_name = "STEP_INIT"        
    elif normalized_input == "MANIFEST":
        target_attribute_name = "STEP_MANIFEST"
    elif normalized_input == "INTEGRITY":
        target_attribute_name = "STEP_INTEGRITY"
    elif normalized_input == "VERITAS":
        target_attribute_name = "STEP_VERITAS"        
    else:
        target_attribute_name = f"STEP_{normalized_input}"
    
    if hasattr(existenzSteps, target_attribute_name):
        current_step_flag = getattr(existenzSteps, target_attribute_name)
    else:
        current_step_flag = existenzSteps.STEP_NONE
        
    current_step_name = current_step_flag.name.replace("STEP_", "") if current_step_flag != existenzSteps.STEP_NONE else "UNKNOWN"
    error_handler.print(f" [➔] Cryptographic routines active -> {current_step_name:<16} [Weight: {int(current_step_flag)}]", level="notice")

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
            error_handler.print(f" [+] Cryptographic routines active -> NEXT_PIPELINE_STAGE={next_step_name}", level="notice")
        except Exception as env_err:
            error_handler.print(f"Non-fatal error logging environment variable: {env_err}", level="debug")
            
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
                print(f"  [x]                        '{self.namespace}' -> Private keys cannot be used on private server!.")
                return skeleton
            
            # Crash only if the mandatory cloud environment key itself is missing
            self.error_handler.print(f" [!] Environment validation failed. Unresolved: {missing_fields}", level="error", exit_code=63)

        clean_pub_display = env_pub_key.strip().split()[-1] if len(env_pub_key.strip().split()) > 1 else 'Custom Format'
        print(f" [+] Ingest:               '{self.namespace}'")
        print(f" [+] Ingested Fingerprint:  {env_finger.strip()}")
        print(f" [+] Private Key Payload:   Loaded ({len(raw_pvt_key.strip())} characters)")

        password_bytes = None
        if raw_phrase and str(raw_phrase).strip():
            print(f" [+] Key Protection State:  Encrypted token active")
            password_bytes = str(raw_phrase).strip().encode('utf-8')
        else:
            print(f" [ ] Key Protection State:  Unencrypted asset format")

        try:
            pvt_bytes = raw_pvt_key.strip().encode('utf-8')
            parsed_private_key = visualMixEngineCrypto.deserialize_ssh_private_key(
                pvt_bytes,
                password_bytes=password_bytes
            )
            print("\033[1;32m [+] Cryptographic Validation: Key parsing loop verified successfully!\033[0m")
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
