import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# =====================================================================
# 1. UNIVERSAL TREE WALKER (Using dot-notation paths)
# =====================================================================
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

# =====================================================================
# 2. MODULAR EXPORT PIPELINES (JSON & XML)
# =====================================================================
def export_to_json(filtered_tree, output_path):
    """Writes the filtered configuration tree directly into clean JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_tree, f, indent=4)
    print(f"[+] JSON Document generated at: {output_path}")

def dict_to_xml_element(tag_name, d):
    """Helper to dynamically convert a filtered dictionary branch into neat XML elements."""
    element = ET.Element(tag_name)
    if isinstance(d, dict):
        for key, val in d.items():
            # If the child value is a primitive string/int, write it as an XML attribute
            if not isinstance(val, (dict, list)):
                element.set(str(key), str(val))
            # If it's a nested dictionary, parse it recursively as a child node
            elif isinstance(val, dict):
                child = dict_to_xml_element(str(key), val)
                element.append(child)
    else:
        element.text = str(d)
    return element

def export_to_xml(filtered_tree, output_path, project_name="Existenz"):
    """Converts the filtered configuration tree into formatted XML layout strings."""
    root_element = ET.Element("existenz", project=project_name)
    
    # Process top level keys inside the filtered structural tree
    for key, content in filtered_tree.items():
        node = dict_to_xml_element(key, content)
        root_element.append(node)
        
    # Beautify the raw XML string output (pretty print with spacing tabs)
    raw_str = ET.tostring(root_element, encoding="utf-8")
    parsed_xml = minidom.parseString(raw_str)
    pretty_xml = parsed_xml.toprettyxml(indent="    ")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"[+] XML Document generated at: {output_path}")

# =====================================================================
# 3. PIPELINE ORCHESTRATOR
# =====================================================================
def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)

    master_file = "existenzCoreMaster.json"
    profiles_file = "existenzProfiles.json"

    # 1. Ingest Master Core Schema Data
    if not os.path.exists(master_file):
        print(f"[-] Critical Error: Missing master metadata data source file '{master_file}'")
        return
    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    # 2. Ingest Profile Configuration Paths 
    if not os.path.exists(profiles_file):
        print(f"[-] Critical Error: Missing export rules definitions layout '{profiles_file}'")
        return
    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles_config = json.load(f)

    # Extract target project name string dynamically out from master schema
    project_slug = master_data.get("project", "Existenz")

    # Change active structure layer depth here: compact | light | basic | detailed
    active_profile = "detailed"
    rules = profiles_config.get(active_profile, [])
    
    print(f"=== Running Multi-Pipeline Exporter [Profile: {active_profile.upper()}] ===")
    print(f" -> Source File: '{master_file}'")
    print(f" -> Rules File:  '{profiles_file}'\n")

    # 3. Core Universal Filter Run
    filtered_tree = {}
    for rule in rules:
        path_parts = rule.split(".")
        walk_tree(master_data, path_parts, filtered_tree)

    # 4. Trigger Target Architecture Modular Compilers simultaneously 
    json_out_path = os.path.join(out_dir, "existenz_core.json")
    xml_out_path = os.path.join(out_dir, "existenz_core.xml")

    # Execute JSON engine export
    export_to_json(filtered_tree, json_out_path)
    
    # Execute XML engine export
    export_to_xml(filtered_tree, xml_out_path, project_slug)

    print(f"\n[+] Processing finished. All structured targets written out.")

if __name__ == "__main__":
    main()
