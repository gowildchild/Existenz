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
from existentialSignatures import existentialToken
import engineSigningLibrary

from visualMixEngineLogging import visualmixErrorHandler
import visualMixEngineCrypto

INT_NAME    = "engineSigningCLI.py"
INT_VERSION = "v0.76.15+"

# Dynamic workspace root tracking relative to master/struct
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STRUCT_DIR = os.path.dirname(os.path.abspath(__file__)) # master/struct/
MODULE_DIR = os.path.join(STRUCT_DIR, "module")         # master/struct/module/

for directory in [REPO_ROOT, STRUCT_DIR, MODULE_DIR]:
    if directory not in sys.path:
        sys.path.insert(0, directory)
        
DEFAULT_CONFIG_PATH = os.path.join(REPO_ROOT, "sign_integrity_config.json") 
MANIFEST_OUTPUT = os.path.join(REPO_ROOT, "manifest.json")
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
REPO_WINDOWS = sys.platform == "win32"

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Initialize the global diagnostic crash monitor interface
error_handler = visualmixErrorHandler(custom_post="_ERR")

def main():
    parser = argparse.ArgumentParser(description="EXISTENZ Veritas")
    # Added "init" into the parser stage choices profile array
    #    choices=['dist', 'tools', 'build', 'master', 'all'],
    parser.add_argument(
        '-circle', '--circle',
        default='all', 
        help='Target circle ring profile or comma-separated lists (tools,build,master)'
    )
    parser.add_argument(
        '-override',
        choices=['update', 'recreate', 'retry', 'newer'],
        default='update', # FIXED: Defaults straight to updating records smoothly
        help='State execution action parameter strategy'
    )
    parser.add_argument(
        '-run',
        choices=['wet', 'dry'],
        default='wet', # FIXED: Defaults straight to true live file system writes
        help='Execution routine target parameter block'
    )

    parser.add_argument(
        "-stage", "--stage", 
        choices=["test","init", "sign", "check", "verify", "manifest","integrity","veritas","build"], 
        required=True, 
        help="Manifest operation state selection."
    )    

    
    parser.add_argument("-bitmask","--bitmask", help="Select BitMask")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to your private key routes (offline signing)")
    parser.add_argument("-m", "--manifest", default=MANIFEST_OUTPUT, help="Path to your manifest file.")
    args = parser.parse_args()

    # Consolidated console blocks straight through uniform logging routing
    banner_payload = [
        f"  VisualMIX Veritas Triple Signer CLI {INT_VERSION}     by Gunther Voet ",
        f"  -stage {args.stage} -circle {args.circle} -o {args.override}" ]
    engineSigningLibrary.render_better_box(error_handler, banner_payload, title_str="Existenz")
    #error_handler.print("┌───────────────────────────────────  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ┐", level="local")
    #error_handler.print(f"│ VisualMIX Signing CLI {INT_VERSION}     by Gunther Voet │", level="local")
    #error_handler.print("└─  ── ─ ── ─  ─  ─ ─   ─ ─ ─  ──────────────────────────────────┘", level="local")
    error_handler.print(f"-c {args.config} -m {args.manifest}", level="local")
    engineSigningLibrary.pipeline_step_current(args.stage, error_handler)
    
    if args.stage == "test":
        from module import cliStateTest
        cliStateTest.execute(args, error_handler, REPO_ROOT)
    elif args.stage == "init":
        from module import cliStateInit
        cliStateInit.execute(args, error_handler, REPO_ROOT)
    elif args.stage == "manifest":
        from module import cliStateManifest
        cliStateManifest.execute(args, error_handler, REPO_ROOT)        
    elif args.stage == "verify":
        from module import cliStateVerify
        cliStateVerify.execute(args, error_handler, REPO_ROOT)     
    elif args.stage == "integrity":
        from module import cliStateIntegrity
        cliStateIntegrity.execute(args, error_handler, REPO_ROOT)           
    elif args.stage == "veritas":
        from module import cliStateVeritas
        cliStateVeritas.execute(args, error_handler, REPO_ROOT)           
    elif args.stage == "sign":
        from module import cliStateSign
        cliStateSign.execute(args, error_handler, REPO_ROOT)        
    elif args.stage == "build":
        from module import cliStateBuild
        cliStateBuild.execute(args, error_handler, REPO_ROOT)        

    #engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
    
if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        error_handler.notice(level="error", message=str(e), exit_code=visualmixErrorHandler.ERR_MISSING_FILE)
    except KeyError as e:
        error_handler.notice(level="error", message=f"Key Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_KEY)
    except Exception as e:
        error_handler.notice(level="error", message=f"Exception Error: {str(e)}", exit_code=visualmixErrorHandler.ERR_UNKNOWN)
