#!/usr/bin/env python3
# ==========================================================================d
# File: inspect_main_vault.py
# Purpose: Clear, raw telemetry mapping of the MAIN structure constants.
# ==========================================================================

import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MASTER_DIR = os.path.join(REPO_ROOT, "existenzStruct", "master")

def inspect_file(filename):
    file_path = os.path.join(MASTER_DIR, filename)
    print(f"\n📁 FILE STRUCTURE TELEMETRY: {file_path}")
    print("─" * 70)

    if not os.path.exists(file_path):
        print(f"  [!] Missing master source file at: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            # Capture only uppercase constants and variables to isolate the logic pairs
            match = re.search(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*([^#\n]+)", line)
            if match:
                var_name = match.group(1).strip()
                var_val = match.group(2).strip()
                print(f"  Line {str(line_num).ljust(4)} | Extracted -> {var_name.ljust(30)} = {var_val}")

if __name__ == "__main__":
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│ EXISTENZ CORE MASTER TELEMETRY MAP                             │")
    print("└────────────────────────────────────────────────────────────────┘")
    inspect_file("existentialCore.py")
    inspect_file("existentialCoreThreat.py")
