# ==========================================================================
# EXISTENZ  master/struct/engineSigningCLI.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
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

def main():
    parser = argparse.ArgumentParser(description="Existenz SHA256 Manifest")
    # Added "init" into the parser stage choices profile array
    parser.add_argument("-stage", "--stage", choices=["init", "sign", "check", "verify", "manifest"], required=True, help="Manifest operation state selection.")
    parser.add_argument("-override", "--override", choices=["update", "recreate", "retry"], required=True, help="Manifest operation override.")
    parser.add_argument("-run","--run", choices=["wet","dry"], default="wet", required=True, help="DRY shows only what it does, WET writes files")
    parser.add_argument("-circle", "--circle", choices=["dist","tools","build","master","all"], default="all", help="Select circle")
    parser.add_argument("-bitmask","--bitmask", help="Select BitMask")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes (offline signing)")
    parser.add_argument("-o", "--manifest", default=MANIFEST_OUTPUT, help="Path to your manifest file.")
    args = parser.parse_args()

    # Consolidated console blocks straight through uniform logging routing
    error_handler.print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐", level="local")
    error_handler.print(f"│ VisualMIX Signing CLI {INT_VERSION}     by Gunther Voet │", level="local")
    error_handler.print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘", level="local")
    error_handler.print(f"Operational: -stage {args.stage} -circle {args.circle} -config {args.config} -o {args.manifest}", level="info")
    
    if args.stage == "init":
        from module import cliStateInit
        cliStateInit.execute(args, error_handler, REPO_ROOT)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        error_handler.notice(level="error", message=str(e), exit_code=visualmixErrorHandler.ERR_MISSING_FILE)
    except KeyError as e:
        error_handler.notice(level="error", message=f"Key Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_KEY)
    except Exception as e:
        error_handler.notice(level="error", message=f"Exception Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_UNKNOWN)
