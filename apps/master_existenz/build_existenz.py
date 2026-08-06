import os
import json

# =====================================================================
# 1. DYNAMIC DOT-NOTATION TREE PARSER (Fixed Segment Indexing)
# =====================================================================
def get_dynamic_path(data, segments, output_tree):
    """
    Recursively walks through source data matching dot-notation tokens,
    including wildcards (*), and reproduces the filtered output tree.
    """
    if not segments:
        return
        
    current_seg = segments[0]
    remaining_segs = segments[1:]
    
    # Handle Wildcards (*) dynamically
    if current_seg == "*":
        if isinstance(data, dict):
            for key, val in data.items():
                if not remaining_segs:
                    output_tree[key] = val
                else:
                    if key not in output_tree:
                        output_tree[key] = {}
                    get_dynamic_path(val, remaining_segs, output_tree[key])
        return

    # Handle Explicit Keys dynamically
    if isinstance(data, dict) and current_seg in data:
        target_val = data[current_seg]
        if not remaining_segs:
            output_tree[current_seg] = target_val
        else:
            if current_seg not in output_tree:
                output_tree[current_seg] = {}
            get_dynamic_path(target_val, remaining_segs, output_tree[current_seg])

def compile_dynamic_export(spec_data, profile_rules, active_level):
    """Reads selection rules array from profiles and filters data dynamically."""
    rules = profile_rules.get(active_level, [])
    filtered_output = {}
    
    for rule in rules:
        segments = rule.split(".")
        get_dynamic_path(spec_data, segments, filtered_output)
        
    return filtered_output

# =====================================================================
# 2. FILE INGESTION & PIPELINE RUNNER
# =====================================================================
def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    # Define your source specification file and profile rules explicitly
    MASTER_FILE = "existenzCoreMaster.json"
    PROFILE_FILE = "existenzProfiles.json"
    
    master_spec = {}
    
    print("=== [1/3] Starting Explicit Specification Ingestion ===")
    
    # 1. Load the Master Spec Document
    if os.path.exists(MASTER_FILE):
        try:
            with open(MASTER_FILE, "r", encoding="utf-8") as f:
                master_spec = json.load(f)
            print(f" -> Successfully imported master file: '{MASTER_FILE}'")
        except Exception as e:
            print(f" [!] Error parsing JSON format in file '{MASTER_FILE}': {e}")
            return
    else:
        print(f" [!] Critical Error: Expected master file '{MASTER_FILE}' was not found in path.")
        return

    # 2. Load the Profiling Filter Templates
    if not os.path.exists(PROFILE_FILE):
        print(f" [!] Critical Error: Profile definition file '{PROFILE_FILE}' is missing.")
        return
        
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            profile_rules = json.load(f)
        print(f" -> Successfully imported filters from: '{PROFILE_FILE}'")
    except Exception as e:
        print(f" [!] Error parsing JSON format in file '{PROFILE_FILE}': {e}")
        return

    # Target output profile configuration level: compact | light | basic | detailed
    target_profile = "detailed" 
    
    print(f"\n=== [2/3] Executing Dynamic Profile Filtering ===")
    print(f" -> Active Profile Strategy: [{target_profile.upper()}]")
    result = compile_dynamic_export(master_spec, profile_rules, target_profile)
    
    # 3. Save the Filtered Node Tree
    out_path = os.path.join(out_dir, "existenz_core.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
        
    print(f"\n=== [3/3] Export Processing Complete ===")
    print(f" -> Filtered data successfully dumped to target file: {out_path}")

if __name__ == "__main__":
    main()
