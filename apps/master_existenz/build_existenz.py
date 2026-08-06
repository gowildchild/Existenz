import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Dunno if this one works 

def walk_tree(source_node, segments, target_tree):
    """Recursively pulls targeted paths out of source node layout maps."""
    if not segments: return
    current_key = segments[0]
    next_segments = segments[1:]

    if current_key == "*":
        if isinstance(source_node, dict):
            for k, v in source_node.items():
                if not next_segments: target_tree[k] = v
                else:
                    if k not in target_tree: target_tree[k] = {}
                    walk_tree(v, next_segments, target_tree[k])
        return

    if isinstance(source_node, dict) and current_key in source_node:
        val = source_node[current_key]
        if not next_segments: target_tree[current_key] = val
        else:
            if current_key not in target_tree: target_tree[current_key] = {}
            walk_tree(val, next_segments, target_tree[current_key])

def dict_to_xml_element(tag_name, d):
    """Converts filtered dictionaries into valid nested XML elements."""
    element = ET.Element(tag_name)
    if isinstance(d, dict):
        for k, v in d.items():
            if not isinstance(v, (dict, list)): element.set(str(k), str(v))
            elif isinstance(v, dict): element.append(dict_to_xml_element(str(k), v))
    else:
        element.text = str(d)
    return element

def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)

    master_file = "existenzCoreMaster.json"
    profiles_file = "existenzProfiles.json"

    # 1. Ingest Master Core Schema
    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    # 💾 TASK A: Export perfectly alphabetised layout copy to existenzCoreDone.json
    with open("existenzCoreDone.json", "w", encoding="utf-8") as f_done:
        json.dump(master_data, f_done, indent=4, sort_keys=True)
    print("[+] Formatted reference file generated: existenzCoreDone.json")

    # 2. Ingest Profile Configuration Paths
    if not os.path.exists(profiles_file):
        print("[-] Skipping multi-language compilation: existenzProfiles.json not present.")
        return

    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles_config = json.load(f)

    active_profile = "detailed"
    rules = profiles_config.get(active_profile, [])
    project_slug = master_data.get("project", "Existenz")

    # 3. Dynamic Filter Walking Sweeping
    filtered_tree = {}
    for rule in rules:
        walk_tree(master_data, rule.split("."), filtered_tree)

    # 💾 TASK B: Output Filtered JSON Asset
    json_path = os.path.join(out_dir, "existenz_core.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(filtered_tree, f, indent=4, sort_keys=True)

    # 💾 TASK C: Output Filtered XML Asset
    xml_path = os.path.join(out_dir, "existenz_core.xml")
    root_el = ET.Element("existenz", project=project_slug)
    for k, content in filtered_tree.items():
        root_el.append(dict_to_xml_element(k, content))
    
    pretty_xml = minidom.parseString(ET.tostring(root_el, encoding="utf-8")).toprettyxml(indent="    ")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print("[+] All structural compilation exports finished successfully!")

if __name__ == "__main__":
    main()
