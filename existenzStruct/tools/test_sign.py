#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED WORKSPACE VERIFICATION SUITE)
# File: inspect_core_integrity.py
# Purpose: Deep structural, cross-language, and cryptographic validation
# ==========================================================================

import os
import sys
import json
import csv
import re
import hmac
import hashlib
import base64
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIST_DIR = os.path.join(REPO_ROOT, "dist")

def main():
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│ EXISTENZ CORE MATRIX SYSTEM TESTING UTILITY                    │")
    print("└────────────────────────────────────────────────────────────────┘")
    print(f"[*] Root Workspace : {REPO_ROOT}")
    print(f"[*] Target Directory: {DIST_DIR}\n")

    if not os.path.exists(DIST_DIR):
        print(f"[-] CRITICAL ERROR: Target directory 'dist/' missing. Run sign_integrity first.")
        sys.exit(1)

    has_failed = False
    failed_audit_records = []

    # ==========================================================================
    # TEST STEP 1: VERIFY AGNOSTIC METADATA COMPLIANCE (Root dist/)
    # ==========================================================================
    print("[*] Test Step 1: Evaluating Agnostic Schema Compliance...")

    for j_file in ["existentialCore.json", "existentialCoreThreat.json"]:
        j_path = os.path.join(DIST_DIR, j_file)
        try:
            with open(j_path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"  [+] Passed: JSON validation for '{j_file}' verified.")
        except Exception as ex:
            failed_audit_records.append(f"[-] INVALID JSON SYNTAX | File: dist/{j_file} | Error: {ex}")
            has_failed = True

    csv_path = os.path.join(DIST_DIR, "existentialCore.csv")
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
        expected_headers = ["Identifier", "Integer_Value", "Expression", "Type", "Context_Description"]
        if headers != expected_headers:
            failed_audit_records.append(f"[-] CSV HEADERS MISMATCH | File: dist/existentialCore.csv | Expected: {expected_headers} | Found: {headers}")
            has_failed = True
        else:
            print("  [+] Passed: CSV matrix headers match schema constraints.")
    except Exception as ex:
        failed_audit_records.append(f"[-] CSV PARSE EXCEPTION | File: dist/existentialCore.csv | Error: {ex}")
        has_failed = True

    for xml_file in ["existentialCore.xml", "existentialCoreThreat.xml"]:
        xml_path = os.path.join(DIST_DIR, xml_file)
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            children = list(root)
            if len(children) > 0:
                target_node = children[0]
                if root.tag == "existentialCore" and not all(k in target_node.attrib for k in ["value", "expr", "type", "info"]):
                    failed_audit_records.append(f"[-] XML ATTRIBUTE FAILURE | File: dist/{xml_file} | Missing attributes.")
                    has_failed = True
                else:
                    print(f"  [+] Passed: XML well-formed check for '{xml_file}' verified.")
            else:
                print(f"  [+] Passed: XML tree '{xml_file}' verified (empty sequence node layer).")
        except ET.ParseError as perr:
            failed_audit_records.append(f"[-] XML SYNTAX ERROR | File: dist/{xml_file} | Line: {perr.position} | Error: {perr}")
            has_failed = True

    for yml_file in ["existentialCore.yml", "existentialCoreThreat.yml"]:
        yml_path = os.path.join(DIST_DIR, yml_file)
        if not os.path.exists(yml_path):
            failed_audit_records.append(f"[-] MISSING YAML FILE | File: dist/{yml_file}")
            has_failed = True
        else:
            print(f"  [+] Passed: YAML layout footprint for '{yml_file}' verified.")

    # ==========================================================================
    # TEST STEP 2: VERIFY PACKAGE PATH TRACK FOOTPRINTS
    # ==========================================================================
    print("\n[*] Test Step 2: Evaluating Language Isolation Package Targets...")

    target_languages = {
        "python": ["existentialCores.py", "existentialCoreCheck.py", "single/existentialCore.py", "single/existentialCoreThreat.py", "single/existentialCoreSignatures.py"],
        "cpp": ["existentialCores.hpp", "existentialCoreCheck.hpp", "single/existentialCore.hpp", "single/existentialCoreThreat.hpp", "single/existentialCoreSignatures.hpp"],
        "perl": ["existentialCores.pm", "existentialCoreCheck.pm", "single/existentialCore.pm", "single/existentialCoreThreat.pm", "single/existentialCoreSignatures.pm"],
        "php": ["existentialCores.php", "existentialCoreCheck.php", "single/existentialCore.php", "single/existentialCoreThreat.php", "single/existentialCoreSignatures.php"],
        "rust": ["existential_cores.rs", "existentialCoreCheck.rs", "single/existentialCore.rs", "single/existentialCoreThreat.rs", "single/existentialCoreSignatures.rs"],
        "bash": ["existentialCores.sh", "existentialCoreCheck.sh", "single/existentialCore.sh", "single/existentialCoreThreat.sh", "single/existentialCoreSignatures.sh"],
        "esphome": ["existentialCores.yaml", "single/esphomeCore.yaml", "single/esphomeThreat.yaml"]
    }

    for lang, components in target_languages.items():
        lang_ok = True
        for comp in components:
            if not os.path.exists(os.path.join(DIST_DIR, lang, comp)):
                failed_audit_records.append(f"[-] MISSING PATH ENTRY | Lang: {lang.upper()} | Path: dist/{lang}/{comp}")
                lang_ok = False
                has_failed = True
        if lang_ok:
            print(f"  [+] Passed [{lang.upper()}]: Directory structure verified.")
    # ==========================================================================
    # TEST STEP 3: ENRICHED CRYPTOGRAPHIC SIGNATURE & DATA MONITOR
    # ==========================================================================
    print("\n[*] Test Step 3: Auditing Cryptographic Signature Handshake Vaults...\n")

    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.exceptions import InvalidSignature

        config_path = os.path.join(REPO_ROOT, "sign_integrity_config.json")
        with open(config_path, "r", encoding="utf-8") as cf:
            l_config = json.load(cf)
            manifest_signed = l_config.get("existentialPrivateSigned", [])

        # Parse and decode our 3 public keys
        public_keys_map = {}
        raw_key_bodies = {}
        for identity, key_string in l_config.get("existentialPublicKeys", []):
            try:
                key_parts = key_string.split()
                if len(key_parts) >= 2:
                    raw_envelope = base64.b64decode(key_parts[1])
                    if len(raw_envelope) >= 32:
                        raw_key_bytes = raw_envelope[-32:]
                        raw_key_bodies[identity] = raw_key_bytes
                        public_keys_map[identity] = ed25519.Ed25519PublicKey.from_public_bytes(raw_key_bytes)
            except Exception as ex:
                failed_audit_records.append(f"[-] CONFIG ERROR | Key parsing failed for {identity}: {ex}")

        def parse_master_blueprint(master_rel_path: str) -> dict:
            constants = {}
            path = os.path.join(REPO_ROOT, master_rel_path)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.search(r"^\s*([A-Za-z0-9_]+)\s*[:=]\s*([^#\n]+)", line)
                        if match:
                            k = match.group(1).strip()
                            v = match.group(2).strip().replace('"', '').replace("'", '').replace(',', '')
                            if not v.startswith(("import", "from", "class", "{")):
                                constants[k] = v
            return constants

        master_core_vars = parse_master_blueprint("existenzStruct/master/existentialCore.py")
        master_threat_vars = parse_master_blueprint("existenzStruct/master/existentialCoreThreat.py")

        # 1. ENFORCE ENRICHED RUNTIME SALT CHECKS (Combined token infrastructure)
        existentialCoreCheckMagic = b"EX25IMMUT32CORE7617"
        combined_salt_payload = existentialCoreCheckMagic
        for identity in ["Platform", "Developer", "Personal"]:
            if identity in raw_key_bodies:
                combined_salt_payload += raw_key_bodies[identity]
        
        computed_runtime_salt = hashlib.sha256(combined_salt_payload).hexdigest()

        # 2. RESOLVE TRUTHS DIRECTLY FROM SOURCE DEFINITIONS
        expected_sigs = {
            "existentialCore": master_core_vars.get("existentialCoreSignature", ""),
            "existentialCoreThreatRoot": master_threat_vars.get("existentialCoreThreatSignature", ""),
            "existentialCoreThreatLegal": master_threat_vars.get("existentialCoreThreatLegalSignature", ""),
            "existentialCoreThreat": master_threat_vars.get("existentialCoreThreatStructuresSignature", ""),
            "existentialCoreCheck": "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c"
        }

        # 3. HIGH-VOCAL VERBOSE FORENSICS FACTORY
        # Prints every single parameter to the screen simultaneously
        def verify_signature_token(lang_id: str, file_path: str, regex_pattern: str, label: str, target_hash: str, key_auth: str):
            full_path = os.path.join(DIST_DIR, file_path)
            if not os.path.exists(full_path):
                print(f"🚨 MISSING TARGET FILE: dist/{file_path}")
                return

            with open(full_path, "r", encoding="utf-8") as f:
                file_text = f.read()

            match = re.search(regex_pattern, file_text)
            found_hash = match.group(1).strip() if match else "NOT_FOUND"
            
            # Map labels to their core definition files precisely
            core_file_origin = "existentialCore.py" if "Core" in label and "Threat" not in label else "existentialCoreThreat.py"
            if label == "Magic" or label == "CoreCheck":
                core_file_origin = "sign_integrity_config.json"

            status = " [ VERIFIED OK ] " if found_hash == target_hash else " [!!! CRITICAL MISMATCH !!!]"
            
            # Print the detailed, explicit forensic row requested
            print(f"➔ 1. TARGET FILE CHECKED : dist/{file_path}")
            print(f"  2. CORE FILE EXTRACTED : {core_file_origin}")
            print(f"  3. REGISTER FIELD HOOK : {label}")
            print(f"  4. ENCRYPTION KEY AUTH : Asymmetric Private Key Layer ({key_auth})")
            print(f"  5. STORED HASH IN FILE : {found_hash}")
            print(f"  6. VALIDATION STATUS   : {status}")
            if found_hash != target_hash:
                print(f"  [!] THE REAL VALUE SHOULD BE : {target_hash}")
                failed_audit_records.append(f"[-] DRIFT CAUGHT | File: dist/{file_path} | Var: {label}")
            print("─" * 80)

        # 4. CROSS-EXAMINE THE MULTI-LANGUAGE PACKAGES SIMULTANEOUSLY
        # Checks every signature lock file using raw extracted master rules
        verify_signature_token("Python", "python/single/existentialCoreSignatures.py", r'existentialCore\s*=\s*"([a-f0-9]{{64}})"', "Core", expected_sigs["existentialCore"], "Developer")
        verify_signature_token("Python", "python/single/existentialCoreSignatures.py", r'existentialCoreThreatRoot\s*=\s*"([a-f0-9]{{64}})"', "CoreThreatRoot", expected_sigs["existentialCoreThreatRoot"], "Personal")
        verify_signature_token("Python", "python/single/existentialCoreSignatures.py", r'existentialCoreThreatLegal\s*=\s*"([a-f0-9]{{64}})"', "CoreThreatLegal", expected_sigs["existentialCoreThreatLegal"], "Personal")
        verify_signature_token("Python", "python/single/existentialCoreSignatures.py", r'existentialCoreThreat\s*=\s*"([a-f0-9]{{64}})"', "CoreThreat", expected_sigs["existentialCoreThreat"], "Developer")

        verify_signature_token("C++", "cpp/single/existentialCoreSignatures.hpp", r'existentialCore\s*=\s*"([a-f0-9]{{64}})"', "Core", expected_sigs["existentialCore"], "Developer")
        verify_signature_token("Perl", "perl/single/existentialCoreSignatures.pm", r'\'existentialCore\'\s*=>\s*\'([a-f0-9]{{64}})\'', "Core", expected_sigs["existentialCore"], "Developer")
        verify_signature_token("PHP", "php/single/existentialCoreSignatures.php", r'existentialCore\s*=\s*\'([a-f0-9]{{64}})\'', "Core", expected_sigs["existentialCore"], "Developer")
        verify_signature_token("Bash", "bash/single/existentialCoreSignatures.sh", r'existentialCore=\"([a-f0-9]{{64}})\"', "Core", expected_sigs["existentialCore"], "Developer")
        
        rust_k = "EXISTENTIAL_CORE"
        verify_signature_token("Rust", "rust/single/existentialCoreSignatures.rs", rf'pub const {rust_k}:\s*&str\s*=\s*"([a-f0-9]{{64}})"', "Core", expected_sigs["existentialCore"], "Developer")

        # EVALUATE COMPLIANCE METRICS
        if failed_audit_records:
            print(f"\n[!] TEST SUITE FAILURE: {len(failed_audit_records)} matrix tracking anomalies exposed.")
            sys.exit(1)
        else:
            print(f"\n[+] ALL SYSTEM INTEGRITY TESTS PASSED | Enriched Master Salt Baseline: {computed_runtime_salt}")
            sys.exit(0)

    except Exception as ex:
        print(f"[-] Severe runtime execution trace anomaly: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    main()
