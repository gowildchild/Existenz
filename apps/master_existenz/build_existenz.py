import os
import json

def walk_tree(source_node, segments, target_tree):
    """
    Recursively pulls targeted layers out of source_node based on path segments.
    Recreates wildcards (*) and nested keys seamlessly inside target_tree.
    """
    if not segments:
        return

    current_key = segments[0]
    next_segments = segments[1:]

    # Handle wildcard nodes (*)
    if current_key == "*":
        if isinstance(source_node, dict):
            for key, val in source_node.items():
                if not next_segments:
                    target_tree[key] = val
                else:
                    if key not in target_tree:
                        target_tree[key] = {}
                    walk_tree(val, next_segments, target_tree[key])
        return

    # Handle exact lookup names
    if isinstance(source_node, dict) and current_key in source_node:
        val = source_node[current_key]
        if not next_segments:
            target_tree[current_key] = val
        else:
            if current_key not in target_tree:
                target_tree[current_key] = {}
            walk_tree(val, next_segments, target_tree[current_key])

def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)

    master_file = "existenzCoreMaster.json"
    profiles_file = "existenzProfiles.json"

    # 1. Ingest Master Specification File
    if not os.path.exists(master_file):
        print(f"[-] Critical Error: Missing '{master_file}' file.")
        return
        
    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)
    print(f"[+] Successfully loaded data layout master: {master_file}")

    # 2. Ingest Profile Configuration Paths
    if not os.path.exists(profiles_file):
        print(f"[-] Critical Error: Missing '{profiles_file}' configuration file.")
        return
        
    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles_config = json.load(f)
    print(f"[+] Successfully loaded filtering profiles: {profiles_file}")

    # Set selection depth profile: compact | light | basic | detailed
    active_profile = "detailed"
    rules = profiles_config.get(active_profile, [])
    
    print(f"[*] Processing Dynamic Export filtering for level: [{active_profile.upper()}]")
    
    # 3. Filter Matrix Tree Nodes
    output_result = {}
    for rule in rules:
        path_parts = rule.split(".")
        walk_tree(master_data, path_parts, output_result)

    # 4. Dump Final Clean Structured JSON file
    final_output_path = os.path.join(out_dir, "existenz_core.json")
    with open(final_output_path, "w", encoding="utf-8") as f:
        json.dump(output_result, f, indent=4)

    print(f"[+] Matrix Generation completed. Filtered records written to: {final_output_path}")

if __name__ == "__main__":
    main()
