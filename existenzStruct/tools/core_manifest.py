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

    # ==========================================================================
    # CORE SIGNING BLOCKS (INCREMENTAL RE-SIGN WITH PARTIAL PRESERVATION)
    # ==========================================================================
    if args.stage in ["sign", "sign-master", "sign-dist", "sign-tools"]:
        error_handler.notice(
            level="info",
            message=f"Stage: [{args.stage.upper()}] Scanning targeted directories..."
        )

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

        files_master = {}
        files_build = {}
        files_tools = {}
        files_dist = {}
        live_files = {}
        
        if args.stage == "sign-master":
            files_master.update(gather_folder_files("existenzStruct/master"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            for k, v in stored_files.items():
                if k.startswith("dist/"): files_dist[k] = v
        elif args.stage == "sign-tools":
            files_tools.update(gather_folder_files("tools"))
            for k, v in stored_files.items():
                if not k.startswith("tools/"):
                    if k.startswith("existenzStruct/tools"): files_build[k] = v
        elif args.stage == "sign-dist":
            files_dist.update(gather_folder_files("dist"))
            for k, v in stored_files.items():
                if k.startswith("existenzStruct/"): files_master[k] = v
        else:  # Full global baseline overwrite ("sign")
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
                flat_files = {k: v for b in ["files", "files.master", "files.build", "files.tools", "files.dist"] for k, v in manifest_data.get(b, {}).items()}
                payload_to_sign = {
                    "files": flat_files,
                    "public_keys": manifest_data["public_keys"]
                }
                
                serialized_manifest_body = json.dumps(
                    payload_to_sign, 
                    sort_keys=True, 
                    ensure_ascii=True, 
                    separators=(',', ':')
                ).encode('utf-8')

                current_ring_weight = visualmixGovernRing.RING_DIST
                if args.stage == "sign-master": current_ring_weight = visualmixGovernRing.RING_MASTER
                elif args.stage in ["sign-tools", "sign-build"]: current_ring_weight = visualmixGovernRing.RING_BUILD

                requires_platform  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PLATFORM)
                requires_developer = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_DEVELOPER)
                requires_personal  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PERSONAL)

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
                                    level="local",
                                    message=f"Cryptographically signed manifest with key role: [{identity}]"
                                )

            except Exception as e:
                error_handler.notice(
                    level="error",
                    message=f"During asymmetric signature generation: {e}",
                    exit_code=visualmixErrorHandler.ERR_KEY_EXCEPTION
                )
        else:
            error_handler.notice(level="error", message="Private signing is not allowed on a public server!")

        missing_signatures = [k for k in ["Platform", "Developer", "Personal"] if k not in manifest_data["signatures"]]
        if missing_signatures:
            error_handler.notice(level="warning", message=f"Private signatures are PENDING/MISSING for: {missing_signatures}")
        else:
            error_handler.notice(level="notice", message="Private signatures are committed with success!")

        with open(MANIFEST_OUTPUT, "w", encoding="utf-8") as mf:
            json.dump(manifest_data, mf, indent=2, sort_keys=True)
        error_handler.notice(level="notice", message="Manifest update is saved to disk.")
        sys.exit(0)
    # ==========================================================================
    # CORE VERIFICATION BLOCKS (ISOLATED SPACE TESTING)
    # ==========================================================================
    elif args.stage in ["verify-master", "verify-dist", "verify-tools", "verify-all", "verify"]:
        if not os.path.exists(MANIFEST_OUTPUT):
            error_handler.notice(
                level="error",
                message=f"Manifest file is missing, execute -stage sign first.",
                exit_code=visualmixErrorHandler.ERR_MISSING_MANIFEST
            )

        with open(MANIFEST_OUTPUT, "r", encoding="utf-8") as mf:
            stored_manifest = json.load(mf)

        stored_signatures = stored_manifest.get("signatures", {})
        
        stored_files = {}
        for bucket in ["files", "files.master", "files.build", "files.tools", "files.dist"]:
            stored_files.update(stored_manifest.get(bucket, {}))

        live_files = {}      
        files_dist, files_master, files_build, files_tools = {}, {}, {}, {}

        if args.stage in ["verify-all", "verify"]:
            error_handler.notice(level="notice", message="Stage [VERIFY-ALL] Reading source folders...")
            files_master.update(gather_folder_files("existenzStruct/master"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            files_tools.update(gather_folder_files("tools"))            
            files_dist.update(gather_folder_files("dist"))
            for d in [files_master, files_build, files_tools, files_dist]: live_files.update(d)
            
        elif args.stage == "verify-master":
            error_handler.notice(level="notice", message="Stage [VERIFY-MASTER] Reading source folders...")
            files_master.update(gather_folder_files("existenzStruct/master"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            files_tools.update(gather_folder_files("tools"))
            files_dist.update(gather_folder_files("dist"))
            for d in [files_master, files_build]: live_files.update(d)
            
        elif args.stage == "verify-tools":
            error_handler.notice(level="notice", message="Stage [VERIFY-TOOLS] Reading source folders...")
            files_tools.update(gather_folder_files("tools"))
            files_build.update(gather_folder_files("existenzStruct/tools"))
            for d in [files_tools, files_build]: live_files.update(d)
            
        else:  # verify-dist
            error_handler.notice(level="notice", message="Stage [VERIFY-DIST] Reading distribution folders...")
            files_dist.update(gather_folder_files("dist"))
            live_files.update(files_dist)

        has_drift = False

        for rel_path, expected_hash in stored_files.items():
            if args.stage == "verify-master" and not rel_path.startswith("existenzStruct/"):
                continue
            if args.stage == "verify-dist" and not rel_path.startswith("dist/"):
                continue
            if args.stage == "verify-tools" and not rel_path.startswith("tools/") and not rel_path.startswith("existenzStruct/tools/"):
                continue

            error_handler.notice(level="info", message=f"Auditing: {rel_path}")

            if rel_path not in live_files:
                error_handler.notice(level="warning", message=f"MISSING File: {rel_path}")
                has_drift = True
            elif live_files[rel_path] != expected_hash:
                error_handler.notice(
                    level="warning",
                    message=f"TAMPER DETECTION in file: {rel_path}",
                    details=[f"Current SHA-256:   {live_files[rel_path]}", f"Expected SHA-256:  {expected_hash}"]
                )
                has_drift = True

        for rel_path in live_files:
            if rel_path not in stored_files:
                # Target Verification Boundaries accurately
                if args.stage == "verify-master" and not rel_path.startswith("existenzStruct/master/") and not rel_path.startswith("existenzStruct/tools/"):
                    continue
                if args.stage == "verify-tools" and not rel_path.startswith("tools/") and not rel_path.startswith("existenzStruct/tools/"):
                    continue
                if args.stage == "verify-dist" and not rel_path.startswith("dist/"):
                    continue
                    
                error_handler.notice(level="warning", message=f"UNTRACKED INJECT: Unauthorized asset exposed: {rel_path}!")
                has_drift = True

        has_signature_failure = False
        current_ring_weight = visualmixGovernRing.RING_DIST
        if args.stage == "verify-master": current_ring_weight = visualmixGovernRing.RING_MASTER
        elif args.stage in ["verify-tools", "verify-build"]: current_ring_weight = visualmixGovernRing.RING_BUILD
        
        requires_platform  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PLATFORM)
        requires_developer = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_DEVELOPER)
        requires_personal  = bool(current_ring_weight & visualmixGovernHandler.SIGN_PVT_PERSONAL)

        missing_signatures = []
        if requires_platform and "Platform" not in stored_signatures: missing_signatures.append("Platform")
        if requires_developer and "Developer" not in stored_signatures: missing_signatures.append("Developer")
        if requires_personal and "Personal" not in stored_signatures: missing_signatures.append("Personal")

        if missing_signatures:
            error_handler.notice(level="error", message=f"manifest contains UNRESOLVED private key signatures for active ring requirements: {missing_signatures}")
            has_signature_failure = True

        if has_drift:
            error_handler.notice(
                level="warning",
                message=f"manifest contains DRIFTING data: {args.stage.upper()}",
                exit_code=visualmixErrorHandler.ERR_KEY_DRIFTING
            )
        elif has_signature_failure:
            sys.exit(visualmixErrorHandler.ERR_MISSING_SIGN)
        else:
            if requires_platform or requires_developer or requires_personal:
                error_handler.notice(level="info", message="Executing asymmetric cryptographic signature verification...")
                
                # FIXED: Pull directly from your clean, consolidated stored_files map 
                # This guarantees the dictionary sequence matches your file loop state perfectly
                payload_to_verify = {
                    "files": stored_files,
                    "public_keys": public_keys_dict
                }
                
                serialized_body = json.dumps(
                    payload_to_verify, 
                    sort_keys=True, 
                    ensure_ascii=True, 
                    separators=(',', ':')
                ).encode('utf-8')
                payload_sha = hashlib.sha256(serialized_body).hexdigest()
                error_handler.notice(
                    level="info", 
                    message=f"CRITICAL MATRIX STATE: Payload contains {len(payload_to_verify['files'])} registered file rows. Global Body SHA256: {payload_sha}"
                )
                
                for identity, is_required in [("Platform", requires_platform), ("Developer", requires_developer), ("Personal", requires_personal)]:
                    if is_required:
                        sig_hex = stored_signatures.get(identity)
                        pub_key_ssh = stored_manifest.get("public_keys", {}).get(identity)
                        
                        try:
                            pub_bytes = pub_key_ssh.encode('utf-8')
                            public_key = serialization.load_ssh_public_key(pub_bytes)
                            public_key.verify(bytes.fromhex(sig_hex), serialized_body)
                            error_handler.notice(level="local", message=f"Cryptographic Signature Footprint verified: [{identity}] -> VALID")
                        except Exception as crypto_fault:
                            error_handler.notice(
                                level="error",
                                message=f"CRYPTOGRAPHIC CORRUPTION: Signature match failure for key [{identity}]: {crypto_fault}",
                                exit_code=visualmixErrorHandler.ERR_KEY
                            )

            error_handler.notice(
                level="info",
                message=f"All files inside {args.stage.upper()} are secure and mathematically verified!"
            )
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        error_handler.notice(level="error", message=str(e), exit_code=visualmixErrorHandler.ERR_MISSING_FILE)
    except KeyError as e:
        error_handler.notice(level="error", message=f"Key Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_KEY)
    except Exception as e:
        error_handler.notice(level="error", message=f"Exception Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_UNKNOWN)
