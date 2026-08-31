import os
import sys
import json
import argparse
import hashlib
import getpass
from enum import IntFlag
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

INT_VERSION = "v0.76.16"
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class visualmixGovernHandler(IntFlag):
    """signing handler for small and bigger things"""    
    SIGN_MAGIC_STRING    = 1
    SIGN_SHA256_HASH     = 2
    SIGN_WITH_VERIFIED   = 4
    SIGN_TIME            = 8
    SIGN_PVT_PLATFORM    = 16
    SIGN_PVT_DEVELOPER   = 32
    SIGN_PVT_PERSONAL    = 64
    SIGN_CHAIN           = 128

class visualmixGovernRing:
    RING_DIST            = 7
    RING_TOOLS           = 7
    RING_BUILD           = 55
    RING_MASTER          = 246

class visualmixErrorHandler:
    """Handles script termination and formats logs cleanly for both Local and GitHub environments."""
    ERR_GENERAL          = 1
    ERR_ARGPARSE         = 2
    ERR_MISSING_CORE     = 4
    ERR_MISSING_LOCAL    = 8
    ERR_MISSING_CONFIG   = 16
    ERR_MISSING_FILE     = 32
    ERR_MISSING_MANIFEST = 33
    ERR_MISSING_SIGN     = 62
    ERR_MISSING_KEY      = 63
    ERR_KEY              = 64
    ERR_KEY_DRIFTING     = 65
    ERR_KEY_VALUE        = 66
    ERR_KEY_FORMAT       = 67
    ERR_MISSING_EXECUTE  = 126
    ERR_MISSING_EXE      = 127
    ERR_UNKNOWN          = 254
    ERR_OUT_OF_RANGE     = 255
    
    ERR_MAP = {
        "error":   ("\033[1;31m[!] ERROR",   "::error", True),
        "warning": ("\033[1;33m[?] Warning", "::warning", True),
        "notice":  ("\033[1;36m[+] Notice",  "::notice", True),
        "debug":   ("\033[1;35m[-] Debug",   "::debug", True),
        "info":    ("\033[0;37m[ ] Info",    "  Info", True),
        "local":   ("\033[0;37m[ ] Local",   "", False)
    }
    
    def notice(self, level: str, message: str, exit_code: int = None, details: list = None):
        """Centralized logging method handling level logic and custom error codes."""
        notice_style, notice_github, notice_github_allowed = self.ERR_MAP.get(level, self.ERR_MAP["info"])
        if REPO_GITHUB:
            indent = " " * (len(level) + 2)
            if not notice_github_allowed:
                return

            no_details = level in ["info", "debug"] or not exit_code
            meta = "" if no_details else f" file=core_manifest.py::[Exit Code {exit_code}]"
            print(f"{notice_github}{meta}::{message}")
            if details:
                for line in details:
                    print(f"{indent}{line}")
        else:
            indent = " " * 10
            valid_err = {v: k for k, v in vars(self.__class__).items() if k.startswith("ERR_") and isinstance(v, int)}
            full_err = f"{notice_style}_{valid_err[exit_code]} ({exit_code})" if exit_code in valid_err else (f"{notice_style}_{exit_code}" if exit_code else f"{notice_style}")
            print(f"  {full_err}: {message}\033[0m")
            if details:
                for line in details:
                    print(f"{indent}{line}")

        if exit_code is not None:
            sys.exit(exit_code)

error_handler = visualmixErrorHandler()

try:
    from existenzStruct.master.existentialCoreSignatures import existentialCoreSignatures, existentialCoreVersion
except ImportError:
    error_handler.notice(
        level="error",
        message="Existenz foundational structure is missing!",
        exit_code=visualmixErrorHandler.ERR_MISSING_CORE
    )

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
        if "__pycache__" in root:
            continue

        for file in files:
            if file == "manifest.json" or file.endswith(".pyc"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, REPO_ROOT)
            # Ensure unified Unix-style forward slashes across platforms
            rel_path = rel_path.replace("\\", "/")
            file_matrix[rel_path] = compute_sha256(full_path)
    return file_matrix

def load_private_key(identity: str, path: str) -> ed25519.Ed25519PrivateKey:
    """Natively reads an asymmetric OpenSSH private key, capturing password requirements explicitly."""
    if REPO_GITHUB:
        error_handler.notice(
            level="error",
            message="GitHub CI is not supposed to sign with a private key!",
            exit_code=visualmixErrorHandler.ERR_MISSING_LOCAL
        )

    expanded_path = os.path.expanduser(path)
    if not os.path.exists(expanded_path):
        error_handler.notice(
            level="error",
            message=f"Key file missing at: {expanded_path}",
            exit_code=visualmixErrorHandler.ERR_MISSING_KEY
        )

    with open(expanded_path, "rb") as k_file:
        key_data = k_file.read()

    try:
        return serialization.load_ssh_private_key(key_data, password=None)
    except Exception as e:
        err_str = str(e).lower()
        if any(w in err_str for w in ["password", "unsupported", "encrypted", "passphrase"]):
            error_handler.notice(
                level="local",
                message=f"[SECURITY] Private key for manifest identity '{identity}' is password-protected."
            )
            pwd = getpass.getpass(f"   Enter interactive pass-phrase for [{identity}]: ").encode('utf-8')
            try:
                return serialization.load_ssh_private_key(key_data, password=pwd)
            except Exception as e:
                error_handler.notice(
                    level="error",
                    message=f"Invalid password entry or corrupt key format: {e}",
                    exit_code=visualmixErrorHandler.ERR_KEY_VALUE
                )
        else:
            error_handler.notice(
                level="error",
                message=f"Corrupt key format: {e}",
                exit_code=visualmixErrorHandler.ERR_KEY_FORMAT
            )

def main():
    parser = argparse.ArgumentParser(description="Existenz SHA256 Manifest")
    parser.add_argument("-stage", choices=["sign", "sign-master", "sign-dist", "verify-master", "verify-dist","sign-tools","verify-tools","verify-all"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes.")
    parser.add_argument("-o", "--output", default=MANIFEST_OUTPUT, help="Path to your manifest file.")
    args = parser.parse_args()

    print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐")
    print(f"│ EXISTENZ SHA256 MANIFEST {INT_VERSION}     by Gunther Voet │")
    print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘")
    print(f"  [*] Operational: -stage {args.stage} -o {MANIFEST_OUTPUT}")

    if os.path.exists(args.config) and not REPO_GITHUB:
        error_handler.notice(level="local", message=f"Configuration file found: {args.config}")
    elif os.path.exists(args.config) and REPO_GITHUB:
        error_handler.notice(
            level="local", 
            message="Configuration file found on GitHub!", 
            exit_code=visualmixErrorHandler.ERR_MISSING_LOCAL
        )

    public_keys_dict = {name: key_str for name, key_str in existentialCoreSignatures.existentialPublicKeys}

    if args.stage in ["sign", "sign-master", "sign-dist", "sign-tools"]:
        error_handler.notice(
            level="info",
            message=f"Stage: [{args.stage.upper()}] Scanning targeted directories..."
        )

        # OMNI-COMPATIBLE RECOVERY PASS: Consolidate historical flat arrays on load
        stored_manifest_map = {}
        existing_signatures = {}
        if os.path.exists(MANIFEST_OUTPUT):
            try:
                with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
                    old_data = json.load(mf)
                    existing_signatures = old_data.get("signatures", {})
                    # Pull down legacy 'files' fields OR new separated buckets
                    for bucket in ["files", "files.master", "files.build", "files.tools", "files.dist"]:
                        stored_manifest_map.update(old_data.get(bucket, {}))
            except Exception:
                pass

        files_master = {}
        files_build = {}
        files_tools = {}
        files_dist = {}
        live_files = {}

        if args.stage == "sign-master":
            error_handler.notice(level="info", message="Scoping Ring [MASTER] - Target: existenzStruct/master")
            files_master.update(gather_folder_files("existenzStruct/master"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            # Preserve existing distribution and utilities records untouched from historical maps
            for k, v in stored_manifest_map.items():
                if k.startswith("dist/"): files_dist[k] = v
                if k.startswith("tools/"): files_tools[k] = v
        elif args.stage == "sign-tools":
            error_handler.notice(level="info", message="Scoping Ring [TOOLS] - Target: tools/")
            files_tools.update(gather_folder_files("tools"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            # Preserve frozen master and distribution tracks safely untouched
            for k, v in stored_manifest_map.items():
                if k.startswith("existenzStruct/master/"): files_master[k] = v
                if k.startswith("dist/"): files_dist[k] = v
        elif args.stage == "sign-dist":
            error_handler.notice(level="info", message="Scoping Ring [DIST] - Target: dist/")
            files_dist.update(gather_folder_files("dist"))
            # Preserve existing system source footprints safely untouched
            for k, v in stored_manifest_map.items():
                if k.startswith("existenzStruct/master/"): files_master[k] = v
                if k.startswith("existenzStruct/tools/"): files_build[k] = v
                if k.startswith("tools/"): files_tools[k] = v
        else:  # Full global baseline overwrite ("sign")
            error_handler.notice(level="info", message="Scoping Full Workspace - Baseline Overwrite.")
            files_master.update(gather_folder_files("existenzStruct/master"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            files_tools.update(gather_folder_files("tools"))
            files_dist.update(gather_folder_files("dist"))

        manifest_data = {
            "version": existentialCoreVersion,
            "public_keys": public_keys_dict,
            "files.master": files_master,
            "files.build": files_build,
            "files.tools": files_tools,
            "files.dist": files_dist,
            "files": live_files,
            "signatures": existing_signatures
        }

        # Omni-Compatible Check: Tracks master presence across old flat structures OR new bucket maps
        has_master_records = any(
            k.startswith("existenzStruct/")
            for bucket in ("files", "files.master", "files.build", "files.tools", "files.dist")
            for k in manifest_data.get(bucket, {})
        )            
        
        if not has_master_records and args.stage == "sign-dist":
            error_handler.notice(
                level="notice",
                message="AUTOMATION OVERRIDE: Master metadata completely absent. Injecting source footprints."
            )
            manifest_data["files.master"].update(gather_folder_files("existenzStruct/master"))
            manifest_data["files.build"].update(gather_folder_files("existenzStruct/tools"))

        if os.path.exists(args.config):
            try:
                with open(args.config, "r", encoding="utf-8") as cf:
                    cfg = json.load(cf)

                key_routes = cfg.get("private_key_paths", {})
                
                # 1. Determine the active microcode ring weight mask dynamically
                current_ring_weight = visualmixGovernRing.RING_DIST
                if args.stage == "sign-master": current_ring_weight = visualmixGovernRing.RING_MASTER
                elif args.stage in ["sign-tools", "sign-build"]: current_ring_weight = visualmixGovernRing.RING_BUILD

                # 2. Extract the bit flags to see exactly which keys are mandated by the bitmask weight
                # 16 = Platform, 32 = Developer, 64 = Personal (Private)
                requires_platform  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PLATFORM)
                requires_developer = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_DEVELOPER)
                requires_personal  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PERSONAL)

                # Compress all active multi-ring file layers seamlessly into the signed canonical body
                flat_files = {k: v for b in ["files", "files.master", "files.build", "files.tools", "files.dist"] for k, v in manifest_data.get(b, {}).items()}
                payload_to_sign = {
                    "files": flat_files,
                    "public_keys": manifest_data["public_keys"]
                }
                
                serialized_manifest_body = json.dumps(payload_to_sign, sort_keys=True).encode('utf-8')

                # 3. Match keys actively mandated by the privilege ring mask flags
                # The names here explicitly mirror your config fields: "Platform", "Developer", "Personal"
                for identity, is_required in [("Platform", requires_platform), ("Developer", requires_developer), ("Personal", requires_personal)]:
                    if is_required:
                        key_path = key_routes.get(identity)
                        if key_path:
                            expanded_path = os.path.expanduser(key_path)
                            if os.path.exists(expanded_path) and not REPO_GITHUB:
                                priv_key = load_private_key(identity, expanded_path)
                                sig_bytes = priv_key.sign(serialized_manifest_body)
                                manifest_data["signatures"][identity] = sig_bytes.hex()
                                error_handler.notice(
                                    level="notice",
                                    message=f"Cryptographically signed manifest with key role: [{identity}]"
                                )
                            else:
                                error_handler.notice(
                                    level="warning",
                                    message=f"Skipping signature block: Private key route not found or inaccessible for [{identity}] at {expanded_path}"
                                )

            except Exception as e:
                error_handler.notice(
                    level="error",
                    message=f"During asymmetric signature generation: {e}",
                    exit_code=visualmixErrorHandler.ERR_KEY_EXCEPTION
                )
        else:
            error_handler.notice(level="error", message="Private signing is not allowed on a public server!")

        # 4. Filter missing signature alerts based strictly on active bitmask requirements
        mandated_signatures = []
        if requires_platform: mandated_signatures.append("Platform")
        if requires_developer: mandated_signatures.append("Developer")
        if requires_personal: mandated_signatures.append("Personal")

        missing_signatures = [k for k in mandated_signatures if k not in manifest_data["signatures"]]
        if missing_signatures:
            error_handler.notice(level="warning", message=f"Private signatures mandated by the ring mask are PENDING/MISSING for: {missing_signatures}")
        else:
            error_handler.notice(level="notice", message=f"All private signatures required by Ring Weight {current_ring_weight} are committed successfully!")

        with open(MANIFEST_OUTPUT, "w", encoding="utf-8") as mf:
            json.dump(manifest_data, mf, indent=2, sort_keys=True)
        error_handler.notice(level="notice", message="Manifest update is saved to disk.")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        error_handler.notice(
            level="error",
            message=str(e),
            exit_code=visualmixErrorHandler.ERR_MISSING_FILE
        )
    except KeyError as e:
        error_handler.notice(
            level="error",
            message=f"Key Error: {str(e)}",
            exit_code=visualmixErrorHandler.ERR_KEY
        )
    except Exception as e:
        error_handler.notice(
            level="error",
            message=f"Exception Error: {str(e)}",
            exit_code=visualmixErrorHandler.ERR_UNKNOWN
        )
        
