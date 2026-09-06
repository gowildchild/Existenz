import os
import sys
import json
import argparse
from enum import IntFlag
from typing import Dict, Any

from engineSigningMeta import existenzLocations, existenzMeta
from engineSigningStruct import existenzIntegrityGlue, existenzSignatures, existenzIntegrityKeysHandler
from existenzSignatures import existentialToken
import engineSigningLibrary

from visualMixEngineLogging import visualmixErrorHandler
import visualMixEngineCrypto

INT_VERSION = "v0.76.16"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json")
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Initialize the global diagnostic crash monitor interface
error_handler = visualmixErrorHandler(custom_post="_ERR")

def run_initialization_audit(args):
    """
    Validation routine checking for the presence of absolute filenames
    cataloged within core and engine location metadata frameworks.
    """
    print("  [*] Step Phase: Initiating structural integrity baseline pre-flight check...")
    
    # 1. Audit Realm: Core Layout Configuration Primitives
    for token, relative_path in existenzLocations["core"].items():
        full_target_path = os.path.join(REPO_ROOT, relative_path)
        if not os.path.exists(full_target_path):
            error_handler.notice(
                level="error",
                message=f"Initialization fault: Core structural file '{token}' missing at {relative_path}",
                exit_code=16  # Reused ERR_MISSING_CONFIG dynamically
            )
        print(f"      [+] Core Asset Verified:   {relative_path:<40} [FOUND]")

    # 2. Audit Realm: Operational Library Infrastructure Engine Components
    for token, relative_path in existenzLocations["engine"].items():
        # Clean the template prefix parameters (like 'sha256:') out of verification loops
        clean_rel_path = relative_path.split(":")[-1] if ":" in relative_path else relative_path
        full_target_path = os.path.join(REPO_ROOT, clean_rel_path)
        
        if not os.path.exists(full_target_path):
            error_handler.notice(
                level="error",
                message=f"Initialization fault: Essential engine script '{token}' missing at {clean_rel_path}",
                exit_code=15  # Leveraged ERR_MISSING_INIT dynamically
            )
        print(f"      [+] Engine Asset Verified: {clean_rel_path:<40} [FOUND]")

    print("\033[1;32m  [+] Initialization Complete: All repository structure dependencies verified successfully.\033[0m")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Existenz SHA256 Manifest")
    parser.add_argument("-stage", "--stage", choices=["sign", "check", "verify", "manifest"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-override", "--override", choices=["update", "recreate", "retry"], required=True, help="Manifest operation override.")
    parser.add_argument("-run","--run", choices=["wet","dry"], default="wet", required=True, help="DRY shows only what it does, WET writes files")
    parser.add_argument("-circle", "--circle", choices=["dist","tools","build","master","all"], default="all", help="Select circle")
    parser.add_argument("-bitmask","--bitmask", help="Select BitMask")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes (offline signing)")
    parser.add_argument("-o", "--manifest", default=MANIFEST_OUTPUT, help="Path to your manifest file.")
    args = parser.parse_args()

    print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐")
    print(f"│ VisualMIX Signing CLI {INT_VERSION}     by Gunther Voet │")
    print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘")
    print(f"  [*] Operational: -stage {args.stage} -circle {args.circle} -config {args.config} -o {args.manifest}")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        error_handler.notice(level="error", message=str(e), exit_code=visualmixErrorHandler.ERR_MISSING_FILE)
    except KeyError as e:
        error_handler.notice(level="error", message=f"Key Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_KEY)
    except Exception as e:
        error_handler.notice(level="error", message=f"Exception Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_UNKNOWN)
