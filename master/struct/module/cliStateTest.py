# ==========================================================================
# EXISTENZ  master/struct/module/cliStateTest.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys

def execute(args, error_handler, repo_root: str):
    """
    Diagnostic testing sandbox.
    Maps out environment paths, system variables, and traces file visibility.
    """
    error_handler.print("┌──────────────────────────────────────────────────────────────────┐", level="local")
    error_handler.print("│ EXISTENZ CORE DEBUG PASS - PLATFORM DIAGNOSTIC AUDIT REGISTER    │", level="local")
    error_handler.print("└──────────────────────────────────────────────────────────────────┘", level="local")

    # 1. Audit active physical script path tracks
    current_file_location = os.path.abspath(__file__)
    current_dir_location = os.path.dirname(current_file_location)
    calculated_parent = os.path.abspath(os.path.join(current_dir_location, ".."))

    error_handler.print(f"  [*] Live Script Path:     {current_file_location}", level="info")
    error_handler.print(f"  [*] Live Module Folder:   {current_dir_location}", level="info")
    error_handler.print(f"  [*] Calculated Parent:    {calculated_parent}", level="info")
    error_handler.print(f"  [*] Repository Root:      {repo_root}", level="info")
    error_handler.print("", level="local")

    # 2. Audit exactly what Python sees in sys.path
    error_handler.print("──┬ [ Active Python Search Paths (sys.path) ] ──────────────────────", level="local")
    for idx, path in enumerate(sys.path):
        error_handler.print(f"  ├── [{idx:02d}] {path}", level="info")
    error_handler.print("──┴───────────────────────────────────────────────────────────────", level="local")
    error_handler.print("", level="local")

    # 3. Test hard file-system visibility of your compiler library
    target_library_file = os.path.join(calculated_parent, "engineBuilderLibrary.py")
    library_exists = os.path.exists(target_library_file)
    
    error_handler.print("──┬ [ Hard Filesystem Visibility Check ] ───────────────────────────", level="local")
    error_handler.print(f"  ├── Target File:   {target_library_file}", level="info")
    if library_exists:
        error_handler.print("  ├── Status:        [VISIBLE ON DISK]", level="notice")
    else:
        error_handler.print("\033[1;31m  ├── Status:        [MISSING / HIDDEN ON DISK]\033[0m", level="local")
    error_handler.print("──┴───────────────────────────────────────────────────────────────", level="local")
    error_handler.print("", level="local")

    # 4. Attempt runtime import challenge
    error_handler.print("  [*] Testing runtime import resolution step...", level="notice")
    try:
        if calculated_parent not in sys.path:
            sys.path.insert(0, calculated_parent)
            error_handler.print(f"  [+] Injected parent directory path to top of search list.", level="info")
        
        import engineBuilderLibrary
        error_handler.print("\033[1;32m  [+] SUCCESS: engineBuilderLibrary loaded into memory flawlessly!\033[0m", level="local")
    except Exception as e:
        error_handler.print(f"\033[1;31m  [-] FAILURE: Python engine could not import the module: {e}\033[0m", level="local")

    error_handler.print("\nDiagnostic pass completed cleanly.", level="notice")
    sys.exit(0)
