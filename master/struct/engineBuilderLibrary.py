# ==========================================================================
# EXISTENZ  master/struct/engineBuilderLibrary.py  v0.7
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import json
import shutil

import os
import json
import importlib.util
import inspect
from enum import IntFlag

class existentialBuildStep(IntFlag):
    BUILD_NONE              = 0
    BUILD_DATA_STUCTURES    = 1
    BUILD_DATA_MERGED       = 2
    BUILD_DATA_SEPARATED    = 4
    BUILD_DATA_VARIABLES    = 8
    BUILD_CODE_FETCH        = 16
    BUILD_CODE_VERIFY       = 32
    BUILD_CODE_TEST         = 64
    BUILD_CODE_SYMBOL_LIST  = 128
    BUILD_TEST_CODE         = 256
    BUILD_CHANGE_VARIABLES  = 512
    BUILD_ERROR             = 1024
    BUILD_BUSY              = 2048
    BUILD_WORKING           = 4096
    BUILD_SUCCESS           = 8192

class existentialBuildLanguage(IntFlag):
    BUILD_NONE              = 0
    BUILD_JSON              = 1
    BUILD_XML               = 2
    BUILD_CSV               = 4
    BUILD_MD                = 8
    BUILD_TXT               = 16
    BUILD_YAML              = 32
    BUILD_HTML_JS           = 64
    BUILD_PDF               = 128
    BUILD_BASH              = 256
    BUILD_PYTHON            = 512
    BUILD_PERL              = 1024
    BUILD_CPP               = 2048
    BUILD_ESPHOME           = 4096
    BUILD_PHP               = 8192
    BUILD_RUST              = 16384
    BUILD_POWERSHELL        = 32768
    BUILD_TYPESCRIPT        = 65536

def execute_universal_builder_matrix(repo_root: str, error_handler, bitmask_arg: int, blueprint_path: str):
    """
    Ingests the master blueprint JSON data matrix and processes active languages 
    sequentially by dynamically invoking isolated code-generation plugins.
    """
    dist_dir = os.path.abspath(os.path.join(repo_root, "dist"))
    
    if not os.path.exists(blueprint_path):
        error_handler.print(f"Build aborted: Blueprint source file tracking asset missing: {blueprint_path}", level="error", exit_code=35)

    # 1. Ingest your data map straight out of your master blueprint JSON file
    with open(blueprint_path, "r", encoding="utf-8") as bf:
        blueprint_data = json.load(bf)

    # Extract dynamic environment variables and version meta data to pass down to modules
    version_str = blueprint_data.get("existentialMeta", {}).get("CoreVersion", "v0.76.16")

    # 2. Define the complete decoupling route map matching your language bitmasks
    language_routing_blueprint = [
        (existentialBuildLanguage.BUILD_JSON,       "json",       "#"),
        (existentialBuildLanguage.BUILD_XML,        "xml",        "<!--"),
        (existentialBuildLanguage.BUILD_CSV,        "csv",        "#"),
        (existentialBuildLanguage.BUILD_MD,         "md",         "<!--"),
        (existentialBuildLanguage.BUILD_TXT,        "txt",        "#"),
        (existentialBuildLanguage.BUILD_YAML,       "yaml",       "#"),
        (existentialBuildLanguage.BUILD_HTML_JS,    "html_js",    "//"),
        (existentialBuildLanguage.BUILD_BASH,       "bash",       "#"),
        (existentialBuildLanguage.BUILD_PYTHON,     "python",     "#"),
        (existentialBuildLanguage.BUILD_PERL,       "perl",       "#"),
        (existentialBuildLanguage.BUILD_CPP,        "cpp",        "//"),
        (existentialBuildLanguage.BUILD_ESPHOME,    "esphome",    "#"),
        (existentialBuildLanguage.BUILD_PHP,        "php",        "//"),
        (existentialBuildLanguage.BUILD_RUST,       "rust",       "//"),
        (existentialBuildLanguage.BUILD_TYPESCRIPT, "typescript", "//")
    ]

    # 3. RUN PROGRAMMATIC TRANSFORMS OVER ENABLED BITMASK ENTRIES
    for lang_bit, plugin_name, comment_char in language_routing_blueprint:
        # Check if this language bit is flagged active inside your -bitmask argument parameter
        if not (bitmask_arg & lang_bit):
            continue

        error_handler.print(f" [*] Spanning Build Target Phase for Language Track: [{plugin_name.upper()}]", level="info")
        
        # Look up plugin module file inside your builder modules folder path location
        plugin_file_path = os.path.abspath(os.path.join(repo_root, f"master/build-tools/module/builder/{plugin_name}.py"))
        
        if not os.path.exists(plugin_file_path):
            error_handler.print(f"  [ ] Skipping compiler track [{plugin_name.upper()}]: Plugin script missing on disk.", level="warning")
            continue

        try:
            # Dynamically look up and load the plugin module directly into memory context
            spec = importlib.util.spec_from_file_location(f"builder_{plugin_name}", plugin_file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            # Setup structured output root paths: /dist/<languagename>/
            lang_root_dir = os.path.join(dist_dir, plugin_name)
            lang_sub_dir  = os.path.join(lang_root_dir, "structures")
            
            os.makedirs(lang_root_dir, exist_ok=True)
            os.makedirs(lang_sub_dir, exist_ok=True)

            # Construct your standardized type-safe layout header file block string
            generated_header = f"{comment_char} " + "=" * 74 + f"\n{comment_char} EXISTENZ Auto-Generated Release Asset [{version_str}]\n{comment_char} " + "=" * 74 + "\n\n"

            # Trigger Phase 1: Output compilation core files cleanly into root folder
            # (existentialCores, existentialCore, existentialSignatures, existentialCoreThreat)
            if hasattr(mod, "compile_root_structures"):
                mod.compile_root_structures(lang_root_dir, blueprint_data, generated_header, error_handler)
                
            # Trigger Phase 2: Output individual structures in loose form inside the sub-folder
            if hasattr(mod, "compile_loose_structures"):
                mod.compile_loose_structures(lang_sub_dir, blueprint_data, generated_header, error_handler)
                
            # Trigger Phase 3: Output two alternative code approaches to fetch existentialCores.json
            if hasattr(mod, "inject_fetch_logic"):
                mod.inject_fetch_logic(lang_root_dir, generated_header, error_handler)

            error_handler.print(f"  [+] Finished compiling target folder paths: dist/{plugin_name}/", level="notice")

        except Exception as plugin_fault:
            error_handler.print(f"Critical execution error inside language plugin compiler [{plugin_name}]: {plugin_fault}", level="error")
            continue

def execute_universal_builder_matrix_v1(repo_root: str, error_handler, active_langs_mask: int, blueprint_path: str):
    """
    Ingests the master blueprint JSON data matrix and processes active languages 
    sequentially by dynamically invoking isolated code-generation plugins.
    """
    dist_dir = os.path.abspath(os.path.join(repo_root, "dist"))
    
    if not os.path.exists(blueprint_path):
        error_handler.print(f"Build aborted: Blueprint source file tracking asset missing: {blueprint_path}", level="error", exit_code=35)

    # 1. Ingest your data map straight out of your master blueprint JSON file
    with open(blueprint_path, "r", encoding="utf-8") as bf:
        blueprint_data = json.load(bf)

    # Extract dynamic environment variables and version meta data to pass down to modules
    version_str = blueprint_data.get("existentialMeta", {}).get("CoreVersion", "v0.76.16")

    # 2. Define the complete decoupling route map matching your language bitmasks
    language_routing_blueprint = [
        (1,     "json",       "json",      "#"),
        (2,     "xml",        "xml",       "<!--"),
        (4,     "csv",        "csv",       "#"),
        (8,     "md",         "markdown",  "<!--"),
        (16,    "txt",        "txt",       "#"),
        (32,    "yaml",       "yaml",      "#"),
        (64,    "html_js",    "html_js",   "//"),
        (256,   "bash",       "bash",      "#"),
        (512,   "python",     "python",    "#"),
        (1024,  "perl",       "perl",      "#"),
        (2048,  "cpp",        "cpp",       "//"),
        (4096,  "esphome",    "esphome",   "#"),
        (8192,  "php",        "php",       "//"),
        (16384, "rust",       "rust",      "//"),
        (65536, "typescript", "typescript","//")
    ]

    # 3. RUN PROGRAMMATIC TRANSFORMS OVER ENABLED BITMASK ENTRIES
    for lang_bit, plugin_name, folder_name, comment_char in language_routing_blueprint:
        if not (active_langs_mask & lang_bit):
            continue

        error_handler.print(f" [*] Spinning Build Target Phase for Language Track: [{plugin_name.upper()}]", level="info")
        
        # Look up plugin module file inside your builder modules folder path location
        plugin_file_path = os.path.abspath(os.path.join(repo_root, f"master/build-tools/module/builder/{plugin_name}.py"))
        
        if not os.path.exists(plugin_file_path):
            error_handler.print(f"  [ ] Skipping compiler track [{plugin_name.upper()}]: Plugin script missing on disk.", level="warning")
            continue

        try:
            # Dynamically look up and load the plugin module directly into memory context
            spec = importlib.util.spec_from_file_location(f"builder_{plugin_name}", plugin_file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            # Setup dedicated target loose folder destination under /dist/
            target_output_dir = os.path.join(dist_dir, folder_name)
            os.makedirs(target_output_dir, exist_ok=True)

            # Construct your standardized type-safe layout header file block string
            generated_header = f"{comment_char} " + "=" * 74 + f"\n{comment_char} EXISTENZ Auto-Generated Release Asset [{version_str}]\n{comment_char} " + "=" * 74 + "\n\n"

            # Trigger Phase 1: Output compilation data structures cleanly into loose form folders
            if hasattr(mod, "compile_structures"):
                mod.compile_structures(target_output_dir, blueprint_data, generated_header, error_handler)
                
            # Trigger Phase 2: Output code snippets to cleanly fetch existentialCores.json
            if hasattr(mod, "inject_fetch_logic"):
                mod.inject_fetch_logic(target_output_dir, generated_header, error_handler)

            error_handler.print(f"  [+] Finished compiling target folder: dist/{folder_name}/", level="notice")

        except Exception as plugin_fault:
            error_handler.print(f"Critical execution error inside language plugin compiler [{plugin_name}]: {plugin_fault}", level="error")
            continue


def resolve_target_structures() -> dict:
    """Reflects over your active system structures dynamically to extract clean token pairs."""
    from engineSigningStruct import existenzSteps, existenzIntegrityKeyStatus, existenzIntegrityKeysHandler
    import existentialCoreCheck
    import existentialCoreThreat
    
    extracted_registry = {}
    structures_to_scan = [
        ("existenzSteps", existenzSteps),
        ("existenzIntegrityKeyStatus", existenzIntegrityKeyStatus),
        ("existenzIntegrityKeysHandler", existenzIntegrityKeysHandler)
    ]
    
    # Safely scan dynamic code variables inside your file modules
    for name, obj in inspect.getmembers(existentialCoreThreat, inspect.isclass):
        if issubclass(obj, IntFlag) or isinstance(obj, dict):
            structures_to_scan.append((name, obj))

    for struct_name, struct_obj in structures_to_scan:
        if isinstance(struct_obj, dict):
            extracted_registry[struct_name] = sorted(struct_obj.items(), key=lambda x: str(x[0]))
        elif issubclass(struct_obj, IntFlag):
            extracted_registry[struct_name] = sorted(
                [(n, int(v)) for n, value in struct_obj.__members__.items()],
                key=lambda x: x[1]
            )
    return extracted_registry

def flush_build_artifact(repo_root: str, language_folder: str, file_name: str, content: str, error_handler):
    """Surgically deposits a type-safe generated compilation file directly into your dist matrix."""
    target_destination_dir = os.path.abspath(os.path.join(repo_root, "dist", language_folder.lower()))
    os.makedirs(target_destination_dir, exist_ok=True)
    
    absolute_filepath = os.path.join(target_destination_dir, file_name)
    try:
        with open(absolute_filepath, "w", encoding="utf-8") as out_f:
            out_cpp.write(content) if hasattr(out_f, 'write') else out_f.write(content)
    except Exception as io_err:
        error_handler.print(f"Failed to deposit artifact payload block [{file_name}]: {io_err}", level="error")

def make_header(existentialCoreVersion: str, sym: str) -> str:
    """Generates the standardized platform header signature with clean comment notations."""
    padding = f"{sym} " if sym else ""
    raw_lines = [
        "==========================================================================",
        "EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)",
        f"Version: {existentialCoreVersion} | Github Deployment",
        "Copyright (c) 2026 by Gunther Voet. All Rights Reserved.",
        "Released under strict Non-Commercial Open-Source License terms.",
        "=========================================================================="
    ]
    return "".join(f"{padding}{line}\n" for line in raw_lines) + "\n"

def build_aligned_json_block(container_key: str, schema_registry: dict) -> list:
    """Generates a column-aligned JSON properties block directly from the blueprint elements."""
    max_k_len = max(len(k) for k in schema_registry.keys())
    max_v_len = max(len(str(d["val"])) for d in schema_registry.values())
    
    expr_map = {}
    for k, d in schema_registry.items():
        v = d["val"]
        if v <= 0: expr_map[k] = "0"
        elif (v & (v - 1)) == 0: expr_map[k] = f"1 << {v.bit_length() - 1}"
        else: expr_map[k] = f"0x{v:08x}"
            
    max_ex_len = max(len(ex) for ex in expr_map.values())

    json_lines = [f'    "{container_key}": {{']
    json_items = []
    for k, d in schema_registry.items():
        v = d["val"]
        clean_cmnt = d.get("comment", "").replace('"', '\\"')
        
        # ELIMINATED parse_structural_type: Pull type or default directly from the schema property!
        struct_type = d.get("type", "UNKNOWN")
        
        k_pad = f'"{k}":'.ljust(max_k_len + 3)
        v_pad = f'{v},'.ljust(max_v_len + 2)
        ex_pad = f'"{expr_map[k]}",'.ljust(max_ex_len + 4)
        t_pad = f'"{struct_type}",'.ljust(14)
        json_items.append(f'        {k_pad}{{\"value\": {v_pad}\"expr\": {ex_pad}\"type\": {t_pad}\"comment\": \"{clean_cmnt}\"}}')
        
    json_lines.append(",\n".join(json_items))
    json_lines.append("    }")
    return json_lines

def execute_cross_language_build(error_handler, repo_root: str, schema_data: dict, version_str: str, run_mode: str):
    """
    Orchestrates cross-language build matrix outputs natively from the blueprint JSON object.
    Bypasses all old text-scraping and legacy prefix regex routines.
    """
    dist_dir = os.path.abspath(os.path.join(repo_root, "dist"))
    error_handler.print(f"X-Language target synchronization directory: {dist_dir}/", level="info")
    
    if run_mode.lower() == "dry":
        error_handler.print("Bypassing cross-language filesystem writes due to dry strategy constraint.", level="notice")
        return

    # Provision workspace target directories
    langs = ["python", "perl", "cpp", "php", "rust", "bash", "esphome"]
    for lang in langs: 
        os.makedirs(os.path.join(dist_dir, lang, "single"), exist_ok=True)

    core_registry = schema_data["existentialCore"]
    legal_map = schema_data.get("existentialCoreThreatLegal", {})
    vacuum_map = schema_data.get("existentialCoreThreatShadowVacuum", {})
    
    def _f_expr(v: int) -> str: 
        return "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")

    # Compile dynamic padding formatting constraints
    w = {
        'f_expr': _f_expr,
        'max_c_k': max(len(k) for k in core_registry.keys()),
        'max_c_v': max(len(str(d["val"])) for d in core_registry.values()),
        'max_c_ex': max(len(_f_expr(d["val"])) for d in core_registry.values()),
        'py_c': max(len(f"    {k} = {_f_expr(d['val'])}") for k, d in core_registry.items()) + 2,
    }

    # 1. Output raw JSON blueprint tracking structures
    _export_agnostic_blueprints(dist_dir, core_registry, w)

    # 2. Generate Python Framework scripts
    _export_python_framework(dist_dir, core_registry, version_str, w, make_header(version_str, "#"))

    # 3. Generate C++ headers
    _export_cpp_framework(dist_dir, core_registry, w, make_header(version_str, "//"))

    # 4. Generate Rust crates module framework
    _export_rust_framework(dist_dir, core_registry, w, make_header(version_str, "//"))

    # 5. Generate Bash and ESPHome files
    _export_bash_and_esphome(dist_dir, core_registry, w, make_header(version_str, "#"))

    error_handler.print(f"Decoupled target groups written directly to: {dist_dir}/", level="notice")


def _export_agnostic_blueprints(dist_dir: str, core_registry: dict, w: dict):
    """Outputs matching blueprint JSON blocks straight to dist/ root."""
    with open(os.path.join(dist_dir, "existentialCore.json"), "w", encoding="utf-8") as f:
        f.write("{\n" + ",\n".join(build_aligned_json_block("existentialCore", core_registry)[1:-1]) + "\n}\n")


def _export_python_framework(dist_dir: str, core_registry: dict, version_str: str, w: dict, header: str):
    """Stamps out isolated runtime Python elements using clean metadata mapping."""
    with open(os.path.join(dist_dir, "python", "single", "existentialCore.py"), "w", encoding="utf-8") as f:
        f.write(header + "class existentialCore:\n")
        for k, d in core_registry.items():
            assignment = f"    {k} = {w['f_expr'](d['val'])}"
            f.write(f"{assignment.ljust(w['py_c'])}# {d.get('comment', '')}\n")


def _export_cpp_framework(dist_dir: str, core_registry: dict, w: dict, header: str):
    """Stamps out native safe C++ headers directly from schema records."""
    with open(os.path.join(dist_dir, "cpp", "single", "existentialCore.hpp"), "w", encoding="utf-8") as f:
        f.write(header + "#pragma once\nnamespace existentialCore {\n")
        for k, d in core_registry.items():
            f.write(f"    const unsigned long {k} = {w['f_expr'](d['val'])}; // {d.get('comment', '')}\n")
        f.write("}\n")


def _export_rust_framework(dist_dir: str, core_registry: dict, w: dict, header: str):
    """Stamps out safe un-mutable Rust crate mods directly from schema records."""
    with open(os.path.join(dist_dir, "rust", "single", "existentialCore.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_core {\n")
        for k, d in core_registry.items():
            f.write(f"    pub const {k}: u64 = {w['f_expr'](d['val'])}; // {d.get('comment', '')}\n")
        f.write("}\n")


def _export_bash_and_esphome(dist_dir: str, core_registry: dict, w: dict, header: str):
    """Outputs shells for shell orchestration and ESPHome smart subs."""
    with open(os.path.join(dist_dir, "bash", "single", "existentialCore.sh"), "w", encoding="utf-8") as f:
        f.write(header)
        for k, d in core_registry.items(): 
            f.write(f"existentialCore_{k}={w['f_expr'](d['val'])}\n")
            
    with open(os.path.join(dist_dir, "esphome", "single", "esphomeCore.yaml"), "w", encoding="utf-8") as f:
        f.write(header + "substitutions:\n" + "\n".join(f"  {k}: \"{w['f_expr'](d['val'])}\" # {d.get('comment', '')}" for k, d in core_registry.items()) + "\n")
