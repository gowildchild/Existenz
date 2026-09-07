def compile_root_structures(output_dir: str, blueprint_data: dict, header: str, error_handler):
    """Generates the primary consolidated framework scripts inside the root folder."""
    core_signed_elements = blueprint_data.get("existentialCoreSigned", [])
    
    lines = [header, "class ExistenzCoreThreatStatus:\n"]
    for row in core_signed_elements:
        if len(row) >= 5:
            label, hex_id, hash_var, _, bitmask_val, *_ = row
            comment = f"# Bitmask: {hex(bitmask_val)} | Hash mapping: {hash_var}"
            lines.append(f"    {label:<32} = {bitmask_val}".ljust(64) + comment)

    # Writes directly to the target root: dist/python/existentialCoreThreat.py
    with open(os.path.join(output_dir, "existentialCoreThreat.py"), "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(lines) + "\n")

def compile_loose_structures(sub_dir: str, blueprint_data: dict, header: str, error_handler):
    """Generates standalone components in loose form inside a sub-folder."""
    core_signed_elements = blueprint_data.get("existentialCoreSigned", [])
    
    for row in core_signed_elements:
        if len(row) >= 5:
            label, hex_id, hash_var, _, bitmask_val, *_ = row
            lines = [
                header,
                f"# Loose form definition for structure component element: {label}",
                f"BIT_VALUE = {bitmask_val}",
                f"HEX_IDENTIFIER = \"{hex_id}\"",
                f"HASH_VARIABLE = \"{hash_var}\""
            ]
            # Writes directly to loose folder form: dist/python/structures/<LabelName>.py
            with open(os.path.join(sub_dir, f"{label}.py"), "w", encoding="utf-8") as out_f:
                out_f.write("\n".join(lines) + "\n")

def inject_fetch_logic(output_dir: str, header: str, error_handler):
    """Generates two clean alternative approaches to fetch existentialCores.json."""
    fetch_logic = header + """import json
import os

# APPROACH 1: Standard File Ingestion Stream Read
def fetch_cores_from_local_disk(file_path="../existentialCores.json"):
    if not os.path.exists(file_path): return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# APPROACH 2: Fast Live Environment Buffer Lookup
def fetch_cores_from_memory():
    return json.loads(os.environ.get("EXISTENZ_CORES_EMBEDDED_BUFFER", "{}"))
"""
    with open(os.path.join(output_dir, "existentialFetchLogic.py"), "w", encoding="utf-8") as out_f:
        out_f.write(fetch_logic)
