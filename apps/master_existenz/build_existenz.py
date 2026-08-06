import os
import json

def get_dynamic_path(data, path_segments, output_tree, current_out_level=None):
    """
    Recursively walks through source data matching your exact dot-notation tokens,
    including wildcards (*), and reproduces the filtered output structure dynamically.
    """
    if not path_segments:
        return
        
    current_seg = path_segments[0]
    remaining_segs = path_segments[1:]
    
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

def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Dynamically merge any file ending in .json (except profiles and manifest data)
    master_spec = {}
    for f_name in os.listdir("."):
        if f_name.endswith(".json") and f_name not in ["export_profiles.json", "package.json"]:
            try:
                with open(f_name, "r", encoding="utf-8") as f:
                    master_spec.update(json.load(f))
            except Exception as e:
                print(f"[-] Failed parsing dynamic input {f_name}: {e}")

    # 2. Load the dynamic filtering profiles
    try:
        with open("ExistenzProfiles.json", "r", encoding="utf-8") as f:
            profile_rules = json.load(f)
    except Exception as e:
        print("[-] Error loading export_profiles.json profile rules config file.")
        return

    # Choose your active selection profile dynamically: "compact", "light", "basic", "detailed"
    target_profile = "detailed" 
    
    print(f"[*] Dynamically compiling profile filter: '{target_profile}'")
    result = compile_dynamic_export(master_spec, profile_rules, target_profile)
    
    # 3. Save clean dynamically outputted file
    out_path = os.path.join(out_dir, "existenz_core.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
        
    print(f"[+] Dynamic output successfully generated at: {out_path}")

if __name__ == "__main__":
    main()
