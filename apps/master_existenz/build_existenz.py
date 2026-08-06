#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import html
import xml.etree.ElementTree as ET
from xml.dom import minidom

def walk_tree(source_node, segments, target_tree):
    """
    Recursively pulls targeted paths out of source node maps.
    Handles wildcards (*) and exact property matches seamlessly.
    """
    if not segments:
        return
    current_key = segments[0]
    next_segments = segments[1:]

    if current_key == "*":
        if isinstance(source_node, dict):
            for k, v in source_node.items():
                if not next_segments:
                    target_tree[k] = v
                else:
                    if k not in target_tree:
                        target_tree[k] = {}
                    walk_tree(v, next_segments, target_tree[k])
        return

    if isinstance(source_node, dict) and current_key in source_node:
        val = source_node[current_key]
        if not next_segments:
            target_tree[current_key] = val
        else:
            if current_key not in target_tree:
                target_tree[current_key] = {}
            walk_tree(val, next_segments, target_tree[current_key])

def dict_to_xml_element(tag_name, d):
    """
    Converts filtered dictionaries into valid nested XML elements.
    Strictly sanitises tags and content values to follow XML W3C specs.
    """
    safe_tag = str(tag_name).strip()
    
    # XML tags cannot contain wildcards or illegal symbols; clean with underscores
    safe_tag = re.sub(r'[^a-zA-Z0-9_-]', '_', safe_tag)
    
    # XML tags cannot start with raw numerical digits
    if safe_tag.isdigit() or (safe_tag.startswith('_') and len(safe_tag) > 1 and safe_tag[1:].isdigit()):
        safe_tag = f"key_{safe_tag}"
        
    element = ET.Element(safe_tag)
    
    if isinstance(d, dict):
        for k, v in d.items():
            if not isinstance(v, (dict, list)):
                # Clean dot attributes out of XML tracking keys
                safe_attr_key = re.sub(r'[^a-zA-Z0-9_-]', '_', str(k))
                if safe_attr_key.isdigit() or (safe_attr_key.startswith('_') and len(safe_attr_key) > 1 and safe_attr_key[1:].isdigit()):
                    safe_attr_key = f"attr_{safe_attr_key}"
                
                element.set(safe_attr_key, html.escape(str(v)))
            elif isinstance(v, dict):
                element.append(dict_to_xml_element(str(k), v))
            elif isinstance(v, list):
                list_wrapper = ET.Element(re.sub(r'[^a-zA-Z0-9_-]', '_', f"array_{k}"))
                for idx, item in enumerate(v):
                    child = ET.Element(f"item_{idx}")
                    child.text = html.escape(str(item))
                    list_wrapper.append(child)
                element.append(list_wrapper)
    else:
        element.text = html.escape(str(d))
        
    return element

def main():
    out_dir = "generated_outputs"
    os.makedirs(out_dir, exist_ok=True)

    master_file = "existenzCoreMaster.json"
    profiles_file = "existenzProfiles.json"

    # 1. Ingest Validated Specification Core Data
    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    # Export a beautifully alphabetised layout copy to separate file
    with open("existenzCoreDone.json", "w", encoding="utf-8") as f_done:
        json.dump(master_data, f_done, indent=4, sort_keys=True)

    # 2. Ingest Profile Selection Rules
    if not os.path.exists(profiles_file):
        print(f"[-] Missing Profile file: {profiles_file}")
        return

    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles_config = json.load(f)

    active_profile = "detailed"
    rules = profiles_config.get(active_profile, [])
    project_slug = master_data.get("project", "Existenz")

    # 3. Process Dynamic Multi-Dimensional Sweeps
    filtered_tree = {}
    for rule in rules:
        walk_tree(master_data, rule.split("."), filtered_tree)

    # 4. Generate Sorted Compliant Output Assets
    json_path = os.path.join(out_dir, "existenz_core.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(filtered_tree, f, indent=4, sort_keys=True)

    xml_path = os.path.join(out_dir, "existenz_core.xml")
    root_el = ET.Element("existenz", project=project_slug)
    for k, content in filtered_tree.items():
        root_el.append(dict_to_xml_element(k, content))
    
    pretty_xml = minidom.parseString(ET.tostring(root_el, encoding="utf-8")).toprettyxml(indent="    ")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print("[+] All structural core matrix compilation routines finished perfectly!")

if __name__ == "__main__":
    main()
