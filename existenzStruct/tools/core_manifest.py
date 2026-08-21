#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (DYNAMIC WORKSPACE LEDGER & MULTI-SIGNATURE GENERATOR)
# File: core_manifest.py v0.76i
# Purpose: Tracks, hashes, and validates code updates across master, tools, and dist.
# ==========================================================================
import os
import sys
import json
import argparse
import hashlib
import getpass
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# Natively bridge your existing workspace root paths and master config files
INT_VERSION = "v0.76h"
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from existenzStruct.master.existentialCoreSignatures import existentialCoreSignatures, existentialCoreVersion
except ImportError:
    print("[-] CRITICAL ERROR: Foundational compiled lockbook structure missing.")
    sys.exit(1)

def compute_sha256(file_path: str) -> str:
    """Computes a strict binary SHA-256 hash of a target file asset."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def gather_folder_files(folder_relative_path: str) -> dict:
    """Traverses a single target folder recursively to catalog all available file hashes."""
    file_matrix = {}
    full_folder_path = os.path.join(REPO_ROOT, folder_relative_path)
    
    if not os.path.exists(full_folder_path):
        return file_matrix

    for root, _, files in os.walk(full_folder_path):
        # NEW CRITICAL FILTER: Natively skip tracking inside any python caching folders
        if "__pycache__" in root:
            continue
            
        for file in files:
            # Skip the manifest ledger itself and any temporary compiled byte fragments
            if file == "manifest.json" or file.endswith(".pyc"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, REPO_ROOT)
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix

def load_private_key(identity: str, path: str) -> ed25519.Ed25519PrivateKey:
    """Natively reads an asymmetric OpenSSH private key, capturing password requirements explicitly."""
    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        raise FileNotFoundError(f"[-] Key file missing at: {expanded_path}")
        
    with open(expanded_path, "rb") as k_file:
        key_data = k_file.read()
        
    try:
        # Attempt to load the private key unencrypted first
        return serialization.load_ssh_private_key(key_data, password=None)
    except Exception as e:
        # FIXED: Catch all encryption parsing traps to reliably trigger password prompts
        err_str = str(e).lower()
        if "password" in err_str or "unsupported" in err_str or "encrypted" in err_str or "passphrase" in err_str:
            print(f"🔒 [SECURITY ENVELOPE] Private key for manifest identity '{identity}' is password-protected.")
            pwd = getpass.getpass(f"   Enter interactive pass-phrase for [{identity}]: ").encode('utf-8')
            try:
                return serialization.load_ssh_private_key(key_data, password=pwd)
            except Exception as ex:
                raise ValueError(f"Invalid password entry sequence or corrupted key format: {ex}")
        else:
            raise e
            
def main():
    parser = argparse.ArgumentParser(description="Existenz SHA256 Manifest")
    # ENFORCED PARAMETERS: Explicit split tracks for both signing and verifying
    parser.add_argument("-stage", choices=["sign", "sign-master", "sign-dist", "verify-master", "verify-dist","sign-tools","verify-tools"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes.")
    args = parser.parse_args()

    print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐")
    print("│ EXISTENZ SHA256 MANIFEST                       by Gunther Voet │")
    print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘")
    print(f"[*] Operational Stage : -stage {args.stage}")
    if not args.stage in ["verify-dist","verify-master","verify","check","verify-tools"]:
      print(f"[*] Configuration File: {args.config}")
    print(f"[*] Ledger Output File: {MANIFEST_OUTPUT}")

    public_keys_dict = {name: key_str for name, key_str in existentialCoreSignatures.existentialPublicKeys}

    # ==========================================================================
    # CORE SIGNING BLOCKS (INCREMENTAL RE-SIGN WITH PARTIAL PRESERVATION)
    # ==========================================================================
    if args.stage in ["sign", "sign-master", "sign-dist","sign-tools"]:
        print(f"[*] Stage: [{args.stage.upper()}] Scanning targeted directories...")
        
        # Pull down the existing file baseline records to guarantee signature persistence
        stored_files = {}
        existing_signatures = {}
        if os.path.exists(MANIFEST_OUTPUT):
            try:
                with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
                    old_data = json.load(mf)
                    stored_files = old_data.get("files", {})
                    existing_signatures = old_data.get("signatures", {})
            except Exception:
                pass

        # Dynamically evaluate the target execution space parameters
        live_files = {}
        if args.stage == "sign-master":
            live_files.update(gather_folder_files("existenzStruct/master"))
            live_files.update(gather_folder_files("existenzStruct/tools"))
            # Preserve existing compiled dist records untouched
            for k, v in stored_files.items():
                if k.startswith("dist/"): live_files[k] = v
        elif args.stage == "sign-tools":
            live_files.update(gather_folder_files("existenzStruct/tools"))
            # Preserve existing source file records untouched
            for k, v in stored_files.items():
                if k.startswith("existenzStruct/tools"): live_files[k] = v
        elif args.stage == "sign-dist":
            live_files.update(gather_folder_files("dist"))
            # Preserve existing source file records untouched
            for k, v in stored_files.items():
                if k.startswith("existenzStruct/"): live_files[k] = v
        else: # Full global baseline overwrite ("sign")
            live_files.update(gather_folder_files("existenzStruct/master"))
            live_files.update(gather_folder_files("existenzStruct/tools"))
            live_files.update(gather_folder_files("dist"))

        manifest_data = {
            "version": existentialCoreVersion,
            "public_keys": public_keys_dict,
            "files": live_files,
            "signatures": existing_signatures
        }

        # Check if the master files are present at all. If empty, force complete signing rules block.
        has_master_records = any(k.startswith("existenzStruct/") for k in manifest_data["files"])
        if not has_master_records and args.stage == "sign-dist":
            print("  [!] AUTOMATION OVERRIDE: Master metadata completely absent. Injecting source footprints.")
            manifest_data["files"].update(gather_folder_files("existenzStruct/master"))
            manifest_data["files"].update(gather_folder_files("existenzStruct/tools"))

        # Asymmetric Cryptographic Signing Handshake Suite using custom config flag parameters path
        if os.path.exists(args.config):
            try:
                with open(args.config, "r", encoding="utf-8") as cf:
                    cfg = json.load(cf)
                # FIXED ROUTING DICTIONARY LOOKUP: Correctly traces 'private_key_paths' matching your design format
                key_routes = cfg.get("private_key_paths", {})
                
                payload_to_sign = {
                    "files": manifest_data["files"],
                    "public_keys": manifest_data["public_keys"]
                }
                serialized_manifest_body = json.dumps(payload_to_sign, sort_keys=True).encode('utf-8')

                for identity in ["Platform", "Developer", "Personal"]:
                    key_path = key_routes.get(identity)
                    if key_path:
                        expanded_path = os.path.expanduser(key_path)
                        if os.path.exists(expanded_path):
                            # FIXED: Invokes passphrase check passing down both identity context and file paths
                            priv_key = load_private_key(identity, expanded_path)
                            sig_bytes = priv_key.sign(serialized_manifest_body)
                            manifest_data["signatures"][identity] = sig_bytes.hex()
                            print(f"  [+] Cryptographically signed workspace ledger with key: [{identity}]")
            except Exception as e:
                print(f"  [!] Terminal error during asymmetric signature generation: {e}")
                sys.exit(1)
        else:
            print(f"  [!] Warning: This tool is used on a public server, no private signing allowed!")
        #    print(f"  [!] Warning: Local configuration file map absent at {args.config}. Manifest built unsigned.")
        # Flag missing signatures visibly
        missing_signatures = [k for k in ["Platform", "Developer", "Personal"] if k not in manifest_data["signatures"]]
        if missing_signatures:
            print(f"  [!] ATTENTION: The following private signatures are PENDING/MISSING: {missing_signatures}")
        else:
            print("  [+] Status: All 3 asymmetric private signatures are successfully committed.")

        with open(MANIFEST_OUTPUT, "w", encoding="utf-8") as mf:
            json.dump(manifest_data, mf, indent=2, sort_keys=True)
        print(f"[+] Success: Manifest update flushed cleanly to disk.")
        sys.exit(0)

    # ==========================================================================
    # CORE VERIFICATION BLOCKS (ISOLATED SPACE TESTING)
    # ==========================================================================
    elif args.stage in ["verify-master", "verify-dist","verify-tools"]:
        if not os.path.exists(MANIFEST_OUTPUT):
            print("[-] CRITICAL ERROR: manifest file missing. Execute -stage sign first.")
            sys.exit(1)

        with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
            stored_manifest = json.load(mf)

        stored_files = stored_manifest.get("files", {})
        stored_signatures = stored_manifest.get("signatures", {})
        
        if args.stage == "verify-master":
            print("[*] Stage: [VERIFY-MASTER] Sweeping source layout folders...")
            live_files = {}
            live_files.update(gather_folder_files("existenzStruct/master"))
            live_files.update(gather_folder_files("existenzStruct/tools"))
        elif args.stage == "verify-tools":
            print("[*] Stage: [VERIFY-TOOLS] Sweeping source tools folders...")
            live_files = {}
            live_files.update(gather_folder_files("existenzStruct/tools"))            
        else:
            print("[*] Stage: [VERIFY-DIST] Sweeping compiled language vaults...")
            live_files = gather_folder_files("dist")

        has_drift = False

        # 1. Audit mutations or layout updates within the targeted tracks scope
        for rel_path, expected_hash in stored_files.items():
            if args.stage == "verify-master" and not rel_path.startswith("existenzStruct/"):
                continue
            if args.stage == "verify-dist" and not rel_path.startswith("dist/"):
                continue

            if rel_path not in live_files:
                print(f"  [-] DELETION DETECTED: Required tracking file missing -> {rel_path}")
                has_drift = True
            elif live_files[rel_path] != expected_hash:
                print(f"  [!] TAMPER DETECTED:   Code contents modified inside -> {rel_path}")
                print(f"      Current SHA-256:   {live_files[rel_path]}")
                print(f"      Expected SHA-256:  {expected_hash}")
                has_drift = True

        # 2. Catch unexpected external folder injections
        for rel_path in live_files:
            if rel_path not in stored_files:
                print(f"  [!] UNTRACKED INJECTION: Unauthorized asset exposed -> {rel_path}")
                has_drift = True

        # 3. Handle private signature reporting loops safely
        missing_signatures = [k for k in ["Platform", "Developer", "Personal"] if k not in stored_signatures]
        if missing_signatures:
            print(f"  [!!!] WARNING [!!!!] Manifest contains UNRESOLVED private key signatures! Missing: {missing_signatures}")
            sys.exit(1)
        if has_drift:
            print(f"\n[!] VERIFICATION FAILED: {args.stage.upper()} alignment errors exposed!")
            sys.exit(1)
        else:
            print(f"\n[+] SUCCESS: Checked tracks inside {args.stage.upper()} are perfectly secure.")
            sys.exit(0)

if __name__ == "__main__":
    main()
