#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED WORKSPACE VERIFICATION SUITE)
# File: test_integrity.py
# Purpose: Deep structural, cross-language, and cryptographic validation
# ==========================================================================

import os
import sys
import json
import csv
import re
import hmac
import hashlib
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

    # 1. Parse JSON Formats Natively
    for j_file in ["existentialCore.json", "existentialCoreThreat.json"]:
        j_path = os.path.join(DIST_DIR, j_file)
        try:
            with open(j_path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"  [+] Passed: JSON validation for '{j_file}' verified.")
        except Exception as ex:
            failed_audit_records.append(f"[-] INVALID JSON SYNTAX | File: dist/{j_file} | Error: {ex}")
            has_failed = True

    # 2. Parse CSV Database Layout
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

    # 3. Parse XML Schemes Safely with Escape Evaluation Tracking
    for xml_file in ["existentialCore.xml", "existentialCoreThreat.xml"]:
        xml_path = os.path.join(DIST_DIR, xml_file)
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            print(f"  [+] Passed: XML well-formed check for '{xml_file}' verified.")
        except ET.ParseError as perr:
            failed_audit_records.append(f"[-] XML SYNTAX ERROR | File: dist/{xml_file} | Line: {perr.position} | Error: {perr}")
            has_failed = True

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

    print("\n[*] Test Step 3: Auditing Cryptographic Signature Handshake Vaults...")

    try:
        config_path = os.path.join(REPO_ROOT, "sign_integrity_config.json")
        with open(config_path, "r", encoding="utf-8") as cf:
            l_config = json.load(cf)
            manifest_signed = l_config.get("existentialPrivateSigned", [])
            public_keys_manifest = l_config.get("existentialPublicKeys", [])

        # Extract active tokens dynamically from your local config profile
        signatures_payload = l_config.get("signatures") or l_config.get("computed_signatures") or l_config
        salt_token = signatures_payload.get("hardwareEnrichedSaltToken") or ""
        salt_bytes = bytes.fromhex(salt_token) if salt_token else b""
        existentialCoreCheckMagic = b"EX25IMMUT32CORE7617"

        # ==========================================================================
        # ZERO HARDCODED STRINGS: RECOMPUTE LIVE EXPECTED TRUTH AT RUNTIME
        # ==========================================================================
        expected_sigs = {}
        core_master_path = os.path.join(REPO_ROOT, "existenzStruct", "master", "existentialCore.py")
        threat_master_path = os.path.join(REPO_ROOT, "existenzStruct", "master", "existentialCoreThreat.py")

        def compute_source_file_hash(file_path: str) -> str:
            """Reads master blueprints directly and computes fresh cryptographic digests."""
            if not os.path.exists(file_path): return ""
            with open(file_path, "rb") as f:
                content = f.read()
            # Normalize line endings to prevent cross-platform whitespace test pollution
            normalized = content.replace(b"\r\n", b"\n").strip()
            return hashlib.sha256(normalized).hexdigest()

        # Generate live reference targets on the fly directly from your master files
        expected_sigs["existentialCore"] = compute_source_file_hash(core_master_path)
        expected_sigs["existentialCoreThreat"] = compute_source_file_hash(threat_master_path)
        
        # Pull core platform verification anchors dynamically from your local system payload context
        expected_sigs["existentialCoreThreatRoot"] = signatures_payload.get("existentialCoreThreatRoot", "")
        expected_sigs["existentialCoreThreatLegal"] = signatures_payload.get("existentialCoreThreatLegal", "")
        expected_sigs["existentialCoreThreatShadowVacuum"] = signatures_payload.get("existentialCoreThreatShadowVacuum", "")
        expected_sigs["existentialCoreCheck"] = signatures_payload.get("existentialCoreCheck", "")
# check c2
        # Reconstruct true signature handshake tokens inside memory using the live salt bytes
        recalculated_signed_matrix = {}
        if salt_bytes:
            for label, target_var in manifest_signed:
                if target_var == "existentialCoreCheckMagic":
                    recalculated_signed_matrix[label] = hmac.new(salt_bytes, existentialCoreCheckMagic, hashlib.sha256).hexdigest()
                else:
                    raw_sig_str = expected_sigs.get(target_var, "")
                    if raw_sig_str:
                        recalculated_signed_matrix[label] = hmac.new(salt_bytes, raw_sig_str.encode('utf-8'), hashlib.sha256).hexdigest()

        # AGGREGATED ERROR DASHBOARD ARRAY MODULE
        failed_audit_records = []

        def verify_signature_token(lang_id: str, file_path: str, regex_pattern: str, friendly_var: str, target_hash: str):
            if not target_hash: return # Skip checking if master reference hashes are empty
            full_path = os.path.join(DIST_DIR, file_path)
            if not os.path.exists(full_path):
                failed_audit_records.append(f"[-] MISSING FILE | Lang: {lang_id} | Path: dist/{file_path}")
                return
            with open(full_path, "r", encoding="utf-8") as f:
                file_text = f.read()
            match = re.search(regex_pattern, file_text)
            found_hash = match.group(1).strip() if match else "NOT_FOUND"
            if found_hash != target_hash:
                failed_audit_records.append(
                    f"[-] SIGNATURE DRIFT | Lang: {lang_id.upper()} | Path: dist/{file_path} | "
                    f"Var: {friendly_var} | Expected: {target_hash} | Found: {found_hash}"
                )

        def parse_master_source_constants(master_relative_path: str) -> dict:
            master_path = os.path.join(REPO_ROOT, master_relative_path)
            constants = {}
            if os.path.exists(master_path):
                with open(master_path, "r", encoding="utf-8") as mf:
                    for line in mf:
                        match = re.search(r"^\s*([A-Za-z0-9_]+)\s*=\s*([^#\n]+)", line)
                        if match:
                            var_name = match.group(1).strip()
                            var_val = match.group(2).strip().replace('"', '').replace("'", '')
                            if not var_val.startswith(("import", "from", "class")):
                                constants[var_name] = var_val
            return constants

        #master_core_vars = parse_master_constants("existenzStruct/master/existentialCore.py")
        #master_threat_vars = parse_master_constants("existenzStruct/master/existentialCoreThreat.py")
        master_core_vars = parse_master_source_constants("existenzStruct/master/existentialCore.py")
        master_threat_vars = parse_master_source_constants("existenzStruct/master/existentialCoreThreat.py")

        def enforce_language_blueprint_values(lang: str, file_rel_path: str, regex_pattern: str, master_map: dict):
            full_path = os.path.join(DIST_DIR, file_rel_path)
            if not os.path.exists(full_path):
                failed_audit_records.append(f"[-] MISSING FILE | Lang: {lang} | Path: dist/{file_rel_path}")
                return
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            for var_name, expected_val in master_map.items():
                if not var_name.isupper(): continue
                clean_expected = expected_val.strip().replace(' ', '')
                match = re.search(regex_pattern.format(var_name), content)
                found_val = match.group(1).strip().replace(' ', '') if match else "NOT_FOUND"
                if found_val != clean_expected:
                    failed_audit_records.append(
                        f"[-] VALUE MUTATION | Lang: {lang.upper()} | Path: dist/{file_rel_path} | "
                        f"Var: {var_name} | Expected: {clean_expected} | Found: {found_val}"
                    )

        # Deep Perl Legal Dictionary Map Auditor cross-checks all element indices dynamically
        def audit_threat_legal_mappings():
            perl_threat_path = os.path.join(DIST_DIR, "perl", "single", "existentialCoreThreat.pm")
            if os.path.exists(perl_threat_path):
                with open(perl_threat_path, "r", encoding="utf-8") as f: pm_text = f.read()
                matches = re.findall(r"(\d+)\s*=>\s*'([^']+)'", pm_text)
                found_keys = [int(m) for m in matches]
                
                # Dynamic verification: Read the actual master keys array straight out of your config map
                threat_legal_config = l_config.get("existentialCoreThreatLegal") or {}
                if isinstance(threat_legal_config, dict):
                    for true_k in sorted(list(threat_legal_config.keys()), key=lambda x: int(x)):
                        if int(true_k) not in found_keys:
                            failed_audit_records.append(f"[-] LEGAL MAP LEAK | Lang: PERL | Path: dist/perl/single/existentialCoreThreat.pm | Missing Expected Key Index: {true_k}")

        # Execute dynamic payload validations on root files
        audit_threat_legal_mappings()
        # SYSTEMATIC VERIFICATION SLOTS: Parallel sweeps across all distribution assets
        # 1. Python Target Tracks
        enforce_language_blueprint_values("Python", "python/single/existentialCore.py", r"{0}\s*=\s*([^#\n]+)", master_core_vars)
        enforce_language_blueprint_values("Python", "python/single/existentialCoreThreat.py", r"{0}\s*=\s*([^#\n]+)", master_threat_vars)
        
        # 2. Perl Target Tracks
        enforce_language_blueprint_values("Perl", "perl/single/existentialCore.pm", r"'{0}'\s*=>\s*([^,\n#]+)", master_core_vars)
        enforce_language_blueprint_values("Perl", "perl/single/existentialCoreThreat.pm", r"'{0}'\s*=>\s*([^,\n#]+)", master_threat_vars)

        # 3. PHP Target Tracks
        enforce_language_blueprint_values("PHP", "php/single/existentialCore.php", r"const\s+{0}\s*=\s*([^;\n#]+)", master_core_vars)
        enforce_language_blueprint_values("PHP", "php/single/existentialCoreThreat.php", r"const\s+{0}\s*=\s*([^;\n#]+)", master_threat_vars)

        # 4. C++ Target Tracks
        enforce_language_blueprint_values("C++", "cpp/single/existentialCore.hpp", r"const\s+unsigned\s+long\s+{0}\s*=\s*([^;\n//]+)", master_core_vars)
        enforce_language_blueprint_values("C++", "cpp/single/existentialCoreThreat.hpp", r"const\s+unsigned\s+long\s+{0}\s*=\s*([^;\n//]+)", master_threat_vars)

        # 5. Rust Target Tracks
        enforce_language_blueprint_values("Rust", "rust/single/existentialCore.rs", r"pub\s+const\s+{0}:\s*u64\s*=\s*([^;\n//]+)", master_core_vars)
        enforce_language_blueprint_values("Rust", "rust/single/existentialCoreThreat.rs", r"pub\s+const\s+{0}:\s*u64\s*=\s*([^;\n//]+)", master_threat_vars)

        # 6. Bash Target Tracks
        enforce_language_blueprint_values("Bash", "bash/single/existentialCore.sh", r"existentialCore_{0}=([^#\n]+)", master_core_vars)
        enforce_language_blueprint_values("Bash", "bash/single/existentialCoreThreat.sh", r"existentialCoreThreat_{0}=([^#\n]+)", master_threat_vars)

        # CRYPTOGRAPHIC VAULT CHECKS: Validate signature locks in every language module
        for k, hsh in expected_sigs.items():
            if not hsh: continue
            verify_signature_token("Python", "python/single/existentialCoreSignatures.py", rf'{k}\s*=\s*"([a-f0-9]{{64}})"', k, hsh)
            verify_signature_token("C++", "cpp/single/existentialCoreSignatures.hpp", rf'const std::string {k}\s*=\s*"([a-f0-9]{{64}})"', k, hsh)
            verify_signature_token("Perl", "perl/single/existentialCoreSignatures.pm", rf'\'{k}\'\s*=>\s*\'([a-f0-9]{{64}})\'', k, hsh)
            verify_signature_token("PHP", "php/single/existentialCoreSignatures.php", rf'const {k}\s*=\s*\'([a-f0-9]{{64}})\'', k, hsh)
            verify_signature_token("Bash", "bash/single/existentialCoreSignatures.sh", rf'{k}=\"([a-f0-9]{{64}})\"', k, hsh)
            
            rust_key = "EXISTENTIAL_" + re.sub(r'(?<!^)(?=[A-Z])', '_', k).upper().replace("EXISTENTIAL_", "")
            verify_signature_token("Rust", "rust/single/existentialCoreSignatures.rs", rf'pub const {rust_key}:\s*&str\s*=\s*"([a-f0-9]{{64}})"', rust_key, hsh)

        for label, expected_hmac in recalculated_signed_matrix.items():
            verify_signature_token("Python", "python/single/existentialCoreSignatures.py", rf'\"{label}\"\s*,\s*\"([a-f0-9]{{64}})\"', label, expected_hmac)
            verify_signature_token("C++", "cpp/single/existentialCoreSignatures.hpp", rf'{{\"{label}\"\s*,\s*"([a-f0-9]{{64}})"}}', label, expected_hmac)
            verify_signature_token("Perl", "perl/single/existentialCoreSignatures.pm", rf'\[\'{label}\'\s*,\s*\'([a-f0-9]{{64}})\'\]', label, expected_hmac)
            verify_signature_token("PHP", "php/single/existentialCoreSignatures.php", rf'\[\'{label}\'\s*,\s*\'([a-f0-9]{{64}})\'\]', label, expected_hmac)
            verify_signature_token("Bash", "bash/single/existentialCoreSignatures.sh", rf'existentialPrivateSigned_{label}=\"([a-f0-9]{{64}})\"', label, expected_hmac)
            verify_signature_token("Rust", "rust/single/existentialCoreSignatures.rs", rf'\(\"{label}\"\s*,\s*"([a-f0-9]{{64}})"\)', label, expected_hmac)

        # UNIFIED GRANULAR AUDIT CONSOLE REPORT
        if failed_audit_records:
            print(f"\n  [!] CRITICAL INTEGRITY MONITOR DEVIATION DETECTED ({len(failed_audit_records)} leaks identified):")
            for record in failed_audit_records:
                print(f"      {record}")
            print("")
            has_failed = True
        else:
            print("  [+] Passed [GLOBAL]: All cross-language files and dynamic signatures verified OK")

    except Exception as ex:
        print(f"  [-] FAIL [CRYPTO]: Exception raised during deep dynamic verification checks: {ex}")
        has_failed = True



    print("\n──────────────────────────────────────────────────────────────────")
    if has_failed:
        print("[!] TEST SUITE FAILURE: Workspace matrix alignment bugs exposed. Fix layout generation blocks.")
        sys.exit(1)
    else:
        print("[+] ALL SYSTEM INTEGRITY TESTS PASSED: Cross-language distribution is secure and fully aligned.")
        sys.exit(0)

if __name__ == "__main__":
    main()
