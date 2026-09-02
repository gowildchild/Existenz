#!/usr/bin/env python3
# ==========================================================================
# File: core_telemetry.py
# Purpose: Deep, un-bypassable telemetry readout of the true MAIN structure.
# ==========================================================================

import os
import json
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MASTER_DIR = os.path.join(REPO_ROOT, "master", "struct")
CONFIG_FILE = os.path.join(REPO_ROOT, "sign_integrity_config.json")

def dump_master_file_payload(filename: str):
    file_path = os.path.join(MASTER_DIR, filename)
    print(f"\n[MAIN STRUCTURE FILE DATA] -> {file_path}")
    print("─" * 80)
    
    if not os.path.exists(file_path):
        print(f"  [-] CRITICAL: Source file missing at {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            stripped = line.strip()
            # Intercept every valid signature asset statement, legal map, and assignment parameter
            if stripped and ("=" in stripped or "=>" in stripped or ":" in stripped) and not stripped.startswith(("#", "import", "from")):
                print(f"  Line {str(line_num).ljust(4)} | {stripped}")

def dump_config_profile():
    print(f"\n[MASTER SCHEMA CONFIG DATA] -> {CONFIG_FILE}")
    print("─" * 80)
    
    if not os.path.exists(CONFIG_FILE):
        print(f"  [-] CRITICAL: Configuration file missing at {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            config_data = json.load(f)
            
            # 1. Output true hardcoded structural signatures baseline map
            print("  ▶ Master Signatures Allocation Block:")
            sigs = config_data.get("signatures") or config_data.get("computed_signatures") or config_data
            for k, v in sigs.items():
                if isinstance(v, str) and len(v) == 64:
                    print(f"    {k.ljust(30)} = \"{v}\"")
            
            # 2. Output forensic Legal Map elements
            print("\n  ▶ Master Threat Legal Mapping Matrix:")
            legal_map = config_data.get("existentialCoreThreatLegal") or {}
            for k, v in legal_map.items():
                print(f"    Key Index {str(k).ljust(6)} => '{v}'")

            # 3. Output tracking Public Key infrastructure
            print("\n  ▶ Master Public Certificates Manifest:")
            for item in config_data.get("existentialPublicKeys", []):
                print(f"    Identity: {item[0].ljust(12)} | Key: {item[1]}")

            # 4. Output operational Private Signed definitions
            print("\n  ▶ Master Private Signed Manifest Matrix:")
            for item in config_data.get("existentialPrivateSigned", []):
                print(f"    Label: {item[0].ljust(16)} | Target Variable Hook: {item[1]}")

        except Exception as ex:
            print(f"  [-] PARSE ERROR: Unable to parse json config payload: {ex}")

if __name__ == "__main__":
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│ EXISTENZ CRITICAL MAIN STRUCTURE COMPLETE telemetry MONITOR  │")
    print("└────────────────────────────────────────────────────────────────┘")
    dump_master_file_payload("existentialCore.py")
    dump_master_file_payload("existentialCoreThreat.py")
    dump_config_profile()
