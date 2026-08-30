#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (DYNAMIC MASTER BLUEPRINT CRYPTOGRAPHIC SIGNER)
# File: sign_master.py
# Purpose: Implements asymmetric private key multi-signing from dynamic tuples.
# v 0.76i
# ==========================================================================
import os
import sys
import json
import re
import argparse
import hashlib
import getpass
import hmac
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
#import existentialCoreSignatures
#from existentialCoreSignatures import existentialCoreSignatures, existentialCoreVersion, existentialCoreCheckMagic

get_distro = "master"
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
TARGET_DIST_DIR = os.path.join(REPO_ROOT, "dist", "master")
CORES_DIST_DIR = os.path.join(REPO_ROOT, "existenzStruct", "master")


CURRENT_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_TOOL_DIR not in sys.path:
    sys.path.insert(0, CURRENT_TOOL_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
int_ver = "v0.76.15"

try:
    # Safely load the local signatures file without namespace prefix drift failures
    import existenzStruct.master.existentialCoreSignatures
    from existentialCoreSignatures import existentialCoreSignatures, existentialCoreVersion, existentialCoreCheckMagic, existentialCores

except ImportError:
    print("    [sign_master.py] ")
    print("[-] CRITICAL ERROR: Foundational compiled lockbook structure missing inside master.")
    print("    Please execute 'core_build.py -step sign' first to generate base parameters.")
    sys.exit(1)

def show_version_info():
    """Prints the strict system metadata, author ownership, and licensing terms."""
    print("==================================================================")
    print(f"EXISTENZ PLATFORM {existentialCoreVersion} (Private Key Signer)")
    print("Copyright (c) 2026 by Gunther Voet. All Rights Reserved.")
    print("─" * 66)
    print("Released under strict Non-Commercial Open-Source License terms.")
    print("Commercial use requires immediate written license and explicit payment.")
    print("==================================================================")

def make_header(sym: str) -> str:
    """Generates the standardized platform header signature with language-aware remarks notation applied to every line."""
    padding = f"{sym} " if sym else ""
    raw_lines = [
        "==========================================================================",
        f"EXISTENZ CORE MASTER Private Key Signer {existentialCoreVersion}",
        "Copyright (c) 2026 by Gunther Voet. All Rights Reserved.",
        "Released under strict Non-Commercial Open-Source License terms.",
        "=========================================================================="
    ]
    return "".join(f"{padding}{line}\n" for line in raw_lines) + "\n"

def load_ssh_private_key(identity, path):
    """Natively reads an asymmetric OpenSSH private key, capturing password requirements explicitly."""
    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        raise FileNotFoundError(f"[-] Private key missing for '{identity}' at path: {expanded_path}")
    
    with open(expanded_path, "rb") as k_file:
        key_data = k_file.read()
        
    try:
        # Attempt to load the private key unencrypted first
        return serialization.load_ssh_private_key(key_data, password=None)
    except Exception as e:
        err_str = str(e).lower()
        if "password" in err_str or "unsupported" in err_str or "encrypted" in err_str or "passphrase" in err_str:
            print(f"🔒 [SECURITY ENVELOPE] Private key access token for '{identity}' is password-protected.")
            pwd = getpass.getpass(f"   Enter interactive pass-phrase for [{identity}]: ").encode('utf-8')
            try:
                return serialization.load_ssh_private_key(key_data, password=pwd)
            except Exception as ex:
                raise ValueError(f"Invalid password entry sequence or corrupted key format: {ex}")
        else:
            raise e

def main():
    parser = argparse.ArgumentParser(description="The Existenz Platform: Master Asymmetric Private Signer")
    parser.add_argument("-stage", "--stage", choices=["verify", "sign"], required=True, help="Operational state selection.")
    parser.add_argument("-dist", "--dist", choices=["existenzStruct", "dist"], default="existenzStruct", required=True, help="Sign which distro.")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to local private key location config file.")
    parser.add_argument("-run", choices=["wet", "dry"], default="wet", help="Execution mutation layer gate. Default is 'wet'.")
    parser.add_argument("-v", "--version", action="store_true", help="Display platform version metadata.")
    args = parser.parse_args()

    if args.version:
        show_version_info()
        sys.exit(0)

    print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐")
    print("│ EXISTENZ OFFLINE PRIVATE KEY SIGNER            by Gunther Voet │")
    print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ─── ───── ────────────────────────┘")
    print(f"[*] Execution Stage: -stage {args.stage}      -dist {args.dist}")
    print(f"[*] Configuration   : {args.config}")

    target_master_dir = os.path.abspath(os.path.join(REPO_ROOT, args.dist, "master"))
    target_sig_file = os.path.join(target_master_dir, "existentialCoreSignatures.py")

    if not os.path.exists(args.config):
        print(f"[-] CRITICAL ERROR: Local private key path mapping configuration missing at: {args.config}")
        sys.exit(1)

    with open(args.config, "r", encoding="utf-8") as cf:
        private_config = json.load(cf)

    private_paths = private_config.get("private_key_paths", {})

    loaded_keys = {}
    computed_asymmetric_signatures = []

    # Map out the exact live hash variables generated by core_build.py
    hash_payloads_map = {
        "Magic": existentialCoreSignatures.existentialCoreCheck,
        "Core": existentialCoreSignatures.existentialCore,
        "Cores": existentialCoreSignatures.existentialCores,
        "CoreThreat": existentialCoreSignatures.existentialCoreThreat,
        "CoreThreatStruct": existentialCoreSignatures.existentialCoreThreatRoot,
        "CoreThreatLegal": existentialCoreSignatures.existentialCoreThreatLegal,
        "CoreThreatShadowVacuum": getattr(existentialCoreSignatures, "existentialCoreThreatShadowVacuum", "NOT_SIGNED_YET"),
        "CoreCheck": existentialCoreSignatures.existentialCoreCheck,
        "CoreItem": existentialCoreSignatures.existentialCoreCheck
    }

    # Order everything cleanly by sequence hierarchy (Sequence 0 -> 1 -> 2 -> 3 -> 9)
    sorted_signing_rules = sorted(
        existentialCoreSignatures.existentialCoreSigned, 
        key=lambda element: element[5]
    )

    if args.stage == "verify":
        # FIXED: Prevents string decode attribute crash bugs
        clean_magic_str = existentialCoreCheckMagic.decode('utf-8', errors='ignore') if isinstance(existentialCoreCheckMagic, bytes) else str(existentialCoreCheckMagic)
        print(f"[*] Active Magic Token : {clean_magic_str}")
        print("──┬ [ COMPREHENSIVE ONE-LINE AUDIT OVERVIEW ] ────────────────────────────────────")
        
    running_chain_sum = 0
    expected_next_sequence = 1
    sequence_chain_accumulator = 0

    for struct_rule in sorted_signing_rules:
        name, short_var, hash_var, sign_var, bitmask, sequence = struct_rule
        
        # ADDED: Evaluates consecutive integers dynamically to capture the sliding chain logic
        if name != "Magic":
            if sequence == expected_next_sequence:
                running_chain_sum += sequence
                expected_next_sequence += 1
            elif sequence == running_chain_sum:
                sequence_chain_accumulator = sequence

        # Pull key assignments from bitmask settings natively
        # Evaluate bits independently to capture all cumulative multi-signature requirements
        required_keys = []
        if bitmask & 8:   required_keys.append("Platform")
        if bitmask & 16:  required_keys.append("Developer")
        if bitmask & 32:  required_keys.append("Personal")
        
        if not required_keys:
            required_keys.append("Developer")

        expected_hash = hash_payloads_map.get(name, "UNKNOWN")

        if args.stage == "sign":
            current_row_signatures = []
            for target_key in required_keys:
                if target_key not in loaded_keys:
                    key_path = private_paths.get(target_key)
                    if not key_path:
                        print(f"  [-] Skip: No local physical path registered for key: '{target_key}'.")
                        continue
                    try:
                        loaded_keys[target_key] = load_ssh_private_key(target_key, key_path)
                    except Exception as ex:
                        print(f"  [-] Terminal Error opening key for [{target_key}]: {ex}")
                        sys.exit(1)
                
                try:
                    private_signature_bytes = loaded_keys[target_key].sign(expected_hash.encode('utf-8'))
                    signature_hex_output = private_signature_bytes.hex()
                    current_row_signatures.append(signature_hex_output)

                    print(f"  [+] Signed Layer: {name:<18} | Key: [{target_key}]")
                except Exception as e:
                    print(f"  [-] Cryptographic signing error on layer '{name}' via [{target_key}]: {e}")
                    sys.exit(1)

            if current_row_signatures:
                final_sig_hex = ":".join(current_row_signatures) if len(current_row_signatures) > 1 else current_row_signatures[-1]
                short_code_hex_output = current_row_signatures[-1][:8]
                computed_asymmetric_signatures.append(
                    f"        (\"{name}\", \"{short_code_hex_output}\", \"{hash_var}\", \"{final_sig_hex}\", {bitmask}, {sequence})"
                )
            elif not any(private_paths.get(k) for k in required_keys):
                computed_asymmetric_signatures.append(
                    f"        (\"{name}\", \"{short_var}\", \"{hash_var}\", \"{sign_var}\", {bitmask}, {sequence})"
                )

        elif args.stage == "verify":
            is_signed = len(sign_var) > 40 and not sign_var.startswith("existential")
            if is_signed:
                live_short = sign_var[:8]
                status_lbl = "VERIFIED" if live_short == short_var[:8] else "DRIFTING"
                display_sig = sign_var
            else:
                live_short = "--------"
                status_lbl = "DRIFTING"
                display_sig = sign_var  # Explicitly print the pending template string variable name

            print(f"  ├──[{sequence}] {name:<18} 0x{live_short} : {expected_hash}")
            print(f"  ├──[{sequence}] [ {status_lbl} ] 0x{display_sig}")


    if args.stage == "verify":
        print("──┴───────────────────────────────────────────────────────────────────────────────")
        print(f"[+] Audit sequence chain check sum computed: {sequence_chain_accumulator}")
        print("[+] Audit validation tracking execution pass completed.")
        sys.exit(0)

    elif args.stage == "sign":
        if args.run == "dry":
            print("\n[Simulation Pass: DRY] Asymmetric signatures generated cleanly in memory. Filesystem unchanged.")
            sys.exit(0)

        #output_signatures_file = os.path.join(TARGET_DIST_DIR, "existentialCoreSignatures.py")
        output_signatures_file = os.path.join(CORES_DIST_DIR, "existentialCoreSignatures.py")
        print(f"\n[*] Committing complete asymmetric signature array to: {output_signatures_file}")

        clean_magic_str = existentialCoreCheckMagic.decode('utf-8', errors='ignore') if isinstance(existentialCoreCheckMagic, bytes) else str(existentialCoreCheckMagic)
        target_vacuum_sig = getattr(existentialCoreSignatures, "existentialCoreThreatShadowVacuum", "NOT_SIGNED_YET")

        with open(output_signatures_file, "w", encoding="utf-8") as f:
            f.write(make_header("#") +
                    f"existentialCoreVersion                       = \"{existentialCoreVersion}\"\n"
                    f"existentialCoreCheckMagic                    = b\"{clean_magic_str}\"\n"
                    f"existentialCoreCheckSignature                = \"{existentialCoreSignatures.existentialCoreCheck}\"\n\n"
                    f"class existentialCoreSignatures:\n"
                    f"    existentialCore                              = \"{existentialCoreSignatures.existentialCore}\"\n"
                    f"    existentialCores                             = \"{existentialCoreSignatures.existentialCores}\"\n"                         
                    f"    existentialCoreThreatRoot                    = \"{existentialCoreSignatures.existentialCoreThreatRoot}\"\n"
                    f"    existentialCoreThreatLegal                   = \"{existentialCoreSignatures.existentialCoreThreatLegal}\"\n"
                    f"    existentialCoreThreatShadowVacuum            = \"{target_vacuum_sig}\"\n"
                    f"    existentialCoreThreat                        = \"{existentialCoreSignatures.existentialCoreThreat}\"\n"               
                    f"    existentialCoreCheck                         = \"{existentialCoreSignatures.existentialCoreCheck}\"\n\n"
                    f"    existentialPublicKeys = (\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in existentialCoreSignatures.existentialPublicKeys) + "\n    )\n\n"
                    f"    existentialCoreSigned = (\n" + ",\n".join(computed_asymmetric_signatures) + "\n    )\n")

        print("\n[+] SUCCESS: ASYMMETRIC MULTI-SIGNATURE PASSTHROUGH SYSTEM LOCKED DOWN CLEANLY.")

if __name__ == "__main__":
    main()

#        # --- EXECUTION TRACK B: THE SINGLE ONE-LINE DESCRIPTIVE AUDIT VERIFY ROUTINE ---
#        elif args.stage == "verify":
#            is_signed = len(sign_var) > 40 and not sign_var.startswith("existential")
#            
#            if is_signed:
#                live_short = sign_var[:8]
#                live_long = sign_var
#                status_msg = "[ VERIFIED CLEAN ]" if live_short == short_var[:8] else "[ DRIFTING ]"
#            else:
#                live_short = "--------"
#                live_long = "WAITING FOR PRIVATE SIGN"
#                status_msg = "[ UNRESOLVED ]"
#
#            print(f"  ├──[{sequence}] {name:<16} 0x{live_short} : {expected_hash}")
#            print(f"  ├──[{sequence}] {status_msg:<12} 0x{live_long}")
#            print(f"  ├── Track       : {name:<18} | Sequence: {sequence}")
#            print(f"  │   ├── Short   : 0x{live_short}")
#            print(f"  │   ├── Hash    : {expected_hash}")
#            print(f"  │   ├── Long Sig: {live_long}")
#            print(f"  │   └── Status  : {status_msg}")
#            print(f"  │")    
