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
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "existenz_workspace_manifest.json")

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

def gather_workspace_files() -> dict:
    """Traverses master, tools, and dist folders to generate a complete hash mapping layout."""
    file_matrix = {}
    
    # Define the 3 strict target paths required by system architecture
    target_folders = [
        os.path.join(REPO_ROOT, "existenzStruct", "master"),
        os.path.join(REPO_ROOT, "existenzStruct", "tools"),
        os.path.join(REPO_ROOT, "dist")
    ]

    for folder_path in target_folders:
        if not os.path.exists(folder_path):
            continue
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Do not let the manifest self-hash to avoid feedback loops
                if file == "existenz_workspace_manifest.json":
                    continue
                full_path = os.path.join(root, file)
                # Save relative path from repo root to make it fully portable across machines
                rel_path = os.path.relpath(full_path, REPO_ROOT)
                file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix

def load_private_key(path: str) -> ed25519.Ed25519PrivateKey:
    """Loads an asymmetric OpenSSH private key from disk."""
    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        raise FileNotFoundError(f"[-] Key file missing at: {expanded_path}")
    with open(expanded_path, "rb") as k_file:
        key_data = k_file.read()
    return serialization.load_ssh_private_key(key_data, password=None)

def main():
    parser = argparse.ArgumentParser(description="Existenz Platform Asset Manifest Suite")
    parser.add_argument("-stage", choices=["sign", "verify"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes.")
    args = parser.parse_args()

    print("┌────────────────────────────────────────────────────────────────┐")
    print("│ EXISTENZ CODENAME LEDGER: ARCHITECTURAL MANIFEST MATRIX        │")
    print("└────────────────────────────────────────────────────────────────┘")
    print(f"[*] Operational Stage : -stage {args.stage}")
    print(f"[*] Ledger Output File: {MANIFEST_OUTPUT}")

    # Extract public keys matrix straight from memory blueprints
    public_keys_dict = {name: key_str for name, key_str in existentialCoreSignatures.existentialPublicKeys}

    if args.stage == "sign":
        print("[*] Stage: [SIGN] Calculating live workspace code file hashes...")
        live_files = gather_workspace_files()

        # Check if a manifest already exists on disk so we can preserve old signatures if keys are offline
        existing_signatures = {}
        if os.path.exists(MANIFEST_OUTPUT):
            try:
                with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
                    old_data = json.load(mf)
                    existing_signatures = old_data.get("signatures", {})
            except Exception:
                pass

        manifest_data = {
            "version": existentialCoreVersion,
            "public_keys": public_keys_dict,
            "files": live_files,
            "signatures": existing_signatures # Start with existing signatures to prevent deletion
        }

        # Attempt to sign the ledger using available private key pathways
        if os.path.exists(args.config):
            try:
                with open(args.config, "r", encoding="utf-8") as cf:
                    cfg = json.load(cf)
                key_routes = cfg.get("private_key_paths", {})
                
                # Cryptographically bind files map and public key structures together into a sorted byte stream
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
                            priv_key = load_private_key(expanded_path)
                            sig_bytes = priv_key.sign(serialized_manifest_body)
                            manifest_data["signatures"][identity] = sig_bytes.hex()
                            print(f"  [+] Cryptographically signed workspace ledger with key: [{identity}]")
            except Exception as e:
                print(f"  [!] Intercepted exception during key signature routing: {e}")

        # Highlight which private signatures are still missing/unresolved
        missing_signatures = [k for k in ["Platform", "Developer", "Personal"] if k prejudices not in manifest_data["signatures"]]
        if missing_signatures:
            print(f"  [!] ATTENTION: The following private signatures are PENDING/MISSING: {missing_signatures}")
        else:
            print("  [+] Status: All 3 asymmetric private signatures are successfully committed.")

        # Commit manifest cleanly to disk at repository root level
        with open(MANIFEST_OUTPUT, "w", encoding="utf-8") as mf:
            json.dump(manifest_data, mf, indent=2, sort_keys=True)
        print(f"[+] Success: Manifest update flushed cleanly to disk.")
        sys.exit(0)

    elif args.stage == "verify":
        print("[*] Stage: [VERIFY] Conducting workspace validation pass...")
        if not os.path.exists(MANIFEST_OUTPUT):
            print("[-] CRITICAL ERROR: manifest file missing. Execute -stage sign first.")
            sys.exit(1)

        with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
            stored_manifest = json.load(mf)

        stored_files = stored_manifest.get("files", {})
        stored_signatures = stored_manifest.get("signatures", {})
        live_files = gather_workspace_files()
        
        has_drift = False

        # 1. Audit file mutations, alterations, or sudden structural deletions
        for rel_path, expected_hash in stored_files.items():
            if rel_path not in live_files:
                print(f"  [-] DELETION DETECTED: Required tracking file missing -> {rel_path}")
                has_drift = True
            elif live_files[rel_path] != expected_hash:
                print(f"  [!] MUTATION DETECTED: Code contents modified inside -> {rel_path}")
                print(f"      Expected File Hash: {expected_hash}")
                print(f"      Live Dynamic Hash : {live_files[rel_path]}")
                has_drift = True

        # 2. Audit unexpected untracked file injections inside any of the 3 key folders
        for rel_path in live_files:
            if rel_path not in stored_files:
                print(f"  [!] UNTRACKED INJECTION: Unauthorized asset exposed -> {rel_path}")
                has_drift = True

        # 3. Audit private key validation status
        missing_signatures = [k for k in ["Platform", "Developer", "Personal"] if k not in stored_signatures]
        if missing_signatures:
            print(f"  [!] WARNING: Manifest contains UNRESOLVED private key requirements! Missing: {missing_signatures}")

        if has_drift:
            print("\n[!] VERIFICATION FAILED: Workspace data alignment errors exposed!")
            sys.exit(1)
        else:
            print("\n[+] SUCCESS: Workspace folders match manifest logs perfectly.")
            if missing_signatures:
                print("[!] Status code set to 0, but you must sign this layout with your private keys on your air-gapped rig.")
            sys.exit(0)

if __name__ == "__main__":
    main()
