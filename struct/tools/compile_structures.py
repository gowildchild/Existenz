#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (UNIVERSAL MULTI-LANGUAGE STRUCTURE COMPILER)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: struct/tools/compile_structures.py
#
import json
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Locate the repository root directory dynamically to guarantee clean imports
# Since this script sits in struct/tools/, the root is two directory levels up
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Ingest master classes and suite runner safely from the updated struct.master path
try:
    from struct.master.existentialCoreTest import run_architecture_suite
    from struct.master.existentialCores import existentialCore, existentialCoreThreat, PLATFORM_VERSION
except ImportError as e:
    print(f"[-] Execution Error: Could not resolve pathing headers. Details: {e}")
    print("[-] Ensure you run this utility script from the repository root directory.")
    sys.exit(1)

def export_json(data_matrix, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    output_file = os.path.join(folder_path, "existentialCore.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data_matrix, f, indent=4)
    print(f"[+] Successfully compiled universal JSON structure to: {output_file}")

def export_xml(data_matrix, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    output_file = os.path.join(folder_path, "existentialCore.xml")
    
    root = ET.Element("existenz_platform", version=data_matrix["metadata"]["version"])
    
    # Process metadata block
    meta_node = ET.SubElement(root, "metadata")
    for k, v in data_matrix["metadata"].items():
        ET.SubElement(meta_node, k).text = str(v)
        
    # Process human core pillars
    core_node = ET.SubElement(root, "existential_core")
    for k, v in data_matrix["existential_core"]["pillars"].items():
        ET.SubElement(core_node, "pillar", name=k, mask=str(v))
    for k, v in data_matrix["existential_core"]["canaries"].items():
        ET.SubElement(core_node, "canary", name=k, mask=str(v))
    for k, v in data_matrix["existential_core"]["signatures"].items():
        ET.SubElement(core_node, "signature", name=k, hex=str(v))

    # Process threat landscape matrix
    threat_node = ET.SubElement(root, "existential_core_threat")
    for k, v in data_matrix["existential_core_threat"]["vectors"].items():
        ET.SubElement(threat_node, "vector", name=k, mask=str(v))
    
    legal_node = ET.SubElement(threat_node, "legal_map")
    for k, v in data_matrix["existential_core_threat"]["legal_map"].items():
        ET.SubElement(legal_node, "mapping", mask=str(k), label=v)
    for k, v in data_matrix["existential_core_threat"]["signatures"].items():
        ET.SubElement(threat_node, "signature", name=k, hex=str(v))

    # Pretty-print XML structure
    raw_xml = ET.tostring(root, encoding="utf-8")
    parsed_xml = minidom.parseString(raw_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="    ")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"[+] Successfully compiled universal XML structure to: {output_file}")

def prepare_language_directories(languages_base_path):
    """Creates individual target language namespaces inside struct/languages/"""
    target_langs = ["perl", "cpp", "php", "rust"]
    paths = {}
    for lang in target_langs:
        lang_dir = os.path.join(languages_base_path, lang)
        os.makedirs(lang_dir, exist_ok=True)
        paths[lang] = lang_dir
    print(f"[+] Initialized cross-language source directories inside: {languages_base_path}")
    return paths

def main():
    # Step 1: Force system test suite execution first
    print("[*] Launching verification checks before data extraction...")
    # Executing the test runner directly from the master test harness file
    if not run_architecture_suite():
        print("[-] Compilation halted: Master signature checks or NAND gates failed verification.")
        sys.exit(1)
        
    print("\n[*] Initializing structured data model compilation...")
    
    # Step 2: Build language-agnostic data model directly from the master python files
    data_matrix = {
        "metadata": {
            "version": PLATFORM_VERSION,
            "anchor_key_salt": "EX25IMMUT32CORE7617"
        },
        "existential_core": {
            "pillars": {k: v.value for k, v in sorted(existentialCore.__members__.items()) if not k.startswith("CANARY_") and not k.startswith("SIGN_")},
            "canaries": {k: v.value for k, v in sorted(existentialCore.__members__.items()) if k.startswith("CANARY_")},
            "signatures": {k: hex(v.value) for k, v in sorted(existentialCore.__members__.items()) if k.startswith("SIGN_")}
        },
        "existential_core_threat": {
            "vectors": {k: v.value for k, v in sorted(existentialCoreThreat.__members__.items()) if k.startswith("THREAT_") and not k == "THREAT_RIGHTS_LEGAL"},
            "legal_map": {int(k): v for k, v in sorted(existentialCoreThreat.THREAT_RIGHTS_LEGAL.items())},
            "signatures": {k: hex(v.value) for k, v in sorted(existentialCoreThreat.__members__.items()) if k.startswith("SIGN_")}
        }
    }

    # Step 3: Enforce absolute path targeting for serialization output directories
    # Binds directly to the unified structural tree blueprint structure
    json_path = os.path.join(REPO_ROOT, "struct", "json")
    xml_path = os.path.join(REPO_ROOT, "struct", "xml")
    langs_path = os.path.join(REPO_ROOT, "struct", "languages")

    # Step 4: Run execution loops to output serialized structural parameters
    export_json(data_matrix, json_path)
    export_xml(data_matrix, xml_path)
    prepare_language_directories(langs_path)
    
    print("[+] Core platform data structures successfully frozen for multi-language scaling.")

if __name__ == "__main__":
    main()
