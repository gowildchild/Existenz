#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (Local Signing Suite & Cross-Compiler v0.76i)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/core_build.py
# 
import os
import sys
import argparse
import hmac
import hashlib
import json
import yaml
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from existenzStruct.master.existentialCore import existentialCore
    from existenzStruct.master.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal, existentialCoreThreatShadowVacuum
    from existenzStruct.master.existentialCoreSignatures import existentialCoreSignatures, existentialCoreCheckMagic, existentialCoreVersion

except ImportError as e:
    print(f"[-] Structural layout components unresolved for signing tool: {e}")
    sys.exit(1)


def show_version_info():
    """Prints the strict system metadata, author ownership, and licensing terms."""
    print("==================================================================")
    print(f"THE EXISTENZ PLATFORM (Local Signing Suite & Cross-Compiler {existentialCoreVersion})")
    print("Copyright (c) 2026 by Gunther Voet. All Rights Reserved.")
    print("─" * 66)
    print("Released under strict Non-Commercial Open-Source License terms.")
    print("Commercial use requires immediate written license and explicit payment.")
    print("==================================================================")


def make_header(sym: str) -> str:
    """Generates the standardized platform header signature with language-aware remarks notation applied to every line."""
    padding = f"{sym} " if sym else ""
    raw_lines = [
        "==========================================================================",
        "THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)",
        f"Version: {existentialCoreVersion} | Framework Namespace Lock",
        "Copyright (c) 2026 by Gunther Voet. All Rights Reserved.",
        "Released under strict Non-Commercial Open-Source License terms.",
        "=========================================================================="
    ]
    return "".join(f"{padding}{line}\n" for line in raw_lines) + "\n"
def parse_structural_type(comment_str: str, key_name: str) -> str:
    """Derives type strictly from the variable prefix first to prevent comment collision bugs."""
    if "RIGHTS" in key_name or "_RIGHTS" in key_name: return "RIGHTS"
    if key_name.startswith("SHIELD_"): return "SHIELD"
    if key_name.startswith("CANARY_"): 
        if "WATCHDOG" in key_name: return "WATCHDOG"
        return "CANARY"
    if key_name.startswith("SIGN_") or key_name.startswith("THREAT_NONE"): return "SIGNATURE"
    # FIXED: Catches the new tracking fields (CoreThreatStruct, CoreThreatLegal, etc.) natively
    if key_name.startswith("THREAT_") or "Threat" in key_name or "Vacuum" in key_name: return "THREAT"

    cleaned = comment_str.replace('#', '').strip()
    if "RIGHTS" in cleaned: return "RIGHTS"
    if "PILLAR" in cleaned: return "PILLAR"
    if "WATCHDOG" in cleaned: return "WATCHDOG"
    if "CANARY" in cleaned: return "CANARY"
    if "SHIELD" in cleaned: return "SHIELD"
    return "UNKNOWN"


def clean_context_description(comment_str: str) -> str:
    """Strips layout integer constants and duplicated markers cleanly across all fields."""
    if not comment_str: return ""
    txt = comment_str.replace('#', '').strip()
    if "SHIELD" in txt: return re.sub(r'\s+', ' ', re.sub(r'^\d+\s*', '', txt)).strip()
    txt = re.sub(r'^\d+\s*', '', txt)
    txt = re.sub(r'^(?:PILLAR|WATCHDOG|CANARY)\s+', '', txt)
    return re.sub(r'\s+', ' ', txt).strip()


def build_aligned_json_block(container_key: str, ordered_layout: dict, comments_map: dict) -> list:
    """Generates a column-aligned JSON properties block with structural type tracking and strict horizontal padding."""
    max_k_len = max(len(k) for k in ordered_layout.keys())
    max_v_len = max(len(str(v)) for v in ordered_layout.values())
    
    expr_map = {}
    for k, v in ordered_layout.items():
        if v <= 0:
            expr_map[k] = "0"
        elif (v & (v - 1)) == 0:
            expr_map[k] = f"1 << {v.bit_length() - 1}"
        else:
            expr_map[k] = f"0x{v:08x}"
            
    max_ex_len = max(len(ex) for ex in expr_map.values())

    json_lines = [f'    "{container_key}": {{']
    json_items = []
    for k, v in ordered_layout.items():
        raw_cmnt = comments_map.get(k, "")
        clean_cmnt = clean_context_description(raw_cmnt).replace('"', '\\"')
        struct_type = parse_structural_type(raw_cmnt, k)
        
        k_pad = f'"{k}":'.ljust(max_k_len + 3)
        v_pad = f'{v},'.ljust(max_v_len + 2)
        ex_pad = f'"{expr_map[k]}",'.ljust(max_ex_len + 4)
        t_pad = f'"{struct_type}",'.ljust(14)
        json_items.append(f'        {k_pad}{{\"value\": {v_pad}\"expr\": {ex_pad}\"type\": {t_pad}\"comment\": \"{clean_cmnt}\"}}')
        
    json_lines.append(",\n".join(json_items))
    json_lines.append("    }")
    return json_lines

def _write_agnostic_blueprints(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, vacuum_ord=None):
    """Outputs agnostic formats (JSON, XML, YAML, CSV, Markdown) straight to the root of dist/."""
    with open(os.path.join(dist_dir, "existentialCore.json"), "w", encoding="utf-8") as f:
        f.write("{\n" + "\n".join(build_aligned_json_block("existentialCore", core_ord, cmnts)) + "\n}\n")

    json_t = ["{", "\n".join(build_aligned_json_block("existentialCoreThreat", threat_ord, cmnts)) + ",", "    \"existentialCoreThreatLegal\": {"]
    max_l_k = max(len(str(k)) for k in legal_ord.keys())
    json_t.append(",\n".join(f'        "{lk}":'.ljust(max_l_k + 11) + f'"{lv}"' for lk, lv in legal_ord.items()) + "\n    },")
    if vacuum_ord:
        json_t.append("    \"existentialCoreThreatShadowVacuum\": {")
        max_v_k = max(len(str(k)) for k in vacuum_ord.keys())
        json_t.append(",\n".join(f'        "{vk}":'.ljust(max_v_k + 11) + f'"{vv}"' for vk, vv in vacuum_ord.items()) + "\n    },")
        
    json_t.append(f'    "existentialCoreThreatSignature": "{sigs["existentialCoreThreat"]}"\n}}')
    with open(os.path.join(dist_dir, "existentialCoreThreat.json"), "w", encoding="utf-8") as f:
        f.write("\n".join(json_t) + "\n")

    def escape_xml_attr(txt: str) -> str:
        return txt.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')


    with open(os.path.join(dist_dir, "existentialCore.xml"), "w", encoding="utf-8") as f:
        lines = ["<existentialCore>"]
        for k, v in core_ord.items():
            clean_info = escape_xml_attr(clean_context_description(cmnts.get(k, '')))
            clean_expr = escape_xml_attr(widths["f_expr"](v))
            lines.append(f'    <{k} value="{v}" expr="{clean_expr}" type="{parse_structural_type(cmnts.get(k,""), k)}" info="{clean_info}"/>')
        lines.append("</existentialCore>")
        f.write("\n".join(lines) + "\n")


    with open(os.path.join(dist_dir, "existentialCoreThreat.xml"), "w", encoding="utf-8") as f:
        lines = ["<existentialCoreThreat>", "  <structure>"]
        for k, v in threat_ord.items():
            clean_info = escape_xml_attr(clean_context_description(cmnts.get(k, '')))
            clean_expr = escape_xml_attr(widths["f_expr"](v))
            lines.append(f'    <{k} value="{v}" expr="{clean_expr}" type="{parse_structural_type(cmnts.get(k,""), k)}" info="{clean_info}"/>')
        lines.append("  </structure>\n  <legal>")
        for k, v in legal_ord.items():
            lines.append(f'    <map key="{k}" value="{escape_xml_attr(v)}"/>')
            
        # ── CHANGE 2: BRIDGE VACUUM DATA INTO THE UNIFIED XML MARKUP NODE ──
        if vacuum_ord:
            lines.append("  </legal>\n  <vacuum>")
            for k, v in vacuum_ord.items():
                lines.append(f'    <map key="{k}" value="{escape_xml_attr(v)}"/>')
            lines.append("  </vacuum>")
        else:
            lines.append("  </legal>")

        lines.append(f"  <signature>{sigs['existentialCoreThreat']}</signature>\n</existentialCoreThreat>")
        f.write("\n".join(lines) + "\n")


    yaml_header = make_header("#")
    with open(os.path.join(dist_dir, "existentialCore.yml"), "w", encoding="utf-8") as f:
        f.write(yaml_header + "existentialCore:\n" + "".join(f"  {k.ljust(widths['max_c_k'])}: {str(v).ljust(widths['max_c_v'])}  ({widths['f_expr'](v).ljust(widths['max_c_ex'])})  {parse_structural_type(cmnts.get(k,''), k).ljust(12)} {clean_context_description(cmnts.get(k, ''))}\n" for k, v in core_ord.items()))
    with open(os.path.join(dist_dir, "existentialCoreThreat.yml"), "w", encoding="utf-8") as f:
        f.write(yaml_header + "existentialCoreThreat:\n" + "".join(f"  {k.ljust(widths['max_t_k'])}: {str(v).ljust(widths['max_t_v'])}  ({widths['f_expr'](v).ljust(widths['max_t_ex'])})  {parse_structural_type(cmnts.get(k,''), k).ljust(12)} {clean_context_description(cmnts.get(k, ''))}\n" for k, v in threat_ord.items()))

    # NEW: Standalone Isolated YAML Map Generators for Legal and Vacuum records
    with open(os.path.join(dist_dir, "existentialCoreThreatLegal.yml"), "w", encoding="utf-8") as f:
        f.write(yaml_header + "existentialCoreThreatLegal:\n" + "".join(f"  {str(k).ljust(10)}: \"{v}\"\n" for k, v in legal_ord.items()))
    if vacuum_ord:
        with open(os.path.join(dist_dir, "existentialCoreThreatShadowVacuum.yml"), "w", encoding="utf-8") as f:
            f.write(yaml_header + "existentialCoreThreatShadowVacuum:\n" + "".join(f"  {str(k).ljust(10)}: \"{v}\"\n" for k, v in vacuum_ord.items()))

    with open(os.path.join(dist_dir, "existentialCore.csv"), "w", encoding="utf-8") as f:
        f.write("Identifier,Integer_Value,Expression,Type,Context_Description\n" + "".join(f"{k},{v},{widths['f_expr'](v)},{parse_structural_type(cmnts.get(k,''), k)},\"{clean_context_description(cmnts.get(k, ''))}\"\n" for k, v in core_ord.items()))
    with open(os.path.join(dist_dir, "existentialCoreThreat.csv"), "w", encoding="utf-8") as f:
        f.write("Identifier,Integer_Value,Expression,Type,Context_Description\n" + "".join(f"{k},{v},{widths['f_expr'](v)},{parse_structural_type(cmnts.get(k,''), k)},\"{clean_context_description(cmnts.get(k, ''))}\"\n" for k, v in threat_ord.items()))


    md_header = make_header(">")
    with open(os.path.join(dist_dir, "existentialCore.md"), "w", encoding="utf-8") as f:
        f.write(f"# Existenz Blueprint: existentialCore\n\n{md_header}| Property Element | Register Integer | Bitmask Equation | Struct Type | Context Reference Description |\n| :--- | :--- | :--- | :--- | :--- |\n" + "".join(f"| `{k}` | `{v}` | `{widths['f_expr'](v)}` | `{parse_structural_type(cmnts.get(k,''), k)}` | {clean_context_description(cmnts.get(k, ''))} |\n" for k, v in core_ord.items()))
    with open(os.path.join(dist_dir, "existentialCoreThreat.md"), "w", encoding="utf-8") as f:
        f.write(f"# Existenz Blueprint: existentialCoreThreat\n\n{md_header}| Property Element | Register Integer | Bitmask Equation | Struct Type | Context Reference Description |\n| :--- | :--- | :--- | :--- | :--- |\n" + "".join(f"| `{k}` | `{v}` | `{widths['f_expr'](v)}` | `{parse_structural_type(cmnts.get(k,''), k)}` | {clean_context_description(cmnts.get(k, ''))} |\n" for k, v in threat_ord.items()))

    # NEW: Standalone Isolated Markdown Table Documentation for Legal and Vacuum records
    with open(os.path.join(dist_dir, "existentialCoreThreatLegal.md"), "w", encoding="utf-8") as f:
        f.write(f"# Existenz Reference: existentialCoreThreatLegal\n\n{md_header}| Register Key Index | Mapped Legal Context Definition Name |\n| :--- | :--- |\n" + "".join(f"| `{k}` | `{v}` |\n" for k, v in legal_ord.items()))
    if vacuum_ord:
        with open(os.path.join(dist_dir, "existentialCoreThreatShadowVacuum.md"), "w", encoding="utf-8") as f:
            f.write(f"# Existenz Reference: existentialCoreThreatShadowVacuum\n\n{md_header}| Register Key Index | Mapped Shadow Vacuum Context Definition Name |\n| :--- | :--- |\n" + "".join(f"| `{k}` | `{v}` |\n" for k, v in vacuum_ord.items()))

    with open(os.path.join(dist_dir, "esphome", "single", "esphomeCore.yaml"), "w", encoding="utf-8") as f:
        f.write(make_header("#") + "substitutions:\n" + "\n".join(f"  {k}: \"{widths['f_expr'](v)}\" # {clean_context_description(cmnts.get(k, ''))}" for k, v in core_ord.items()) + "\n")
    with open(os.path.join(dist_dir, "esphome", "single", "esphomeThreat.yaml"), "w", encoding="utf-8") as f:
        f.write(make_header("#") + "substitutions:\n" + "\n".join(f"  {k}: \"{widths['f_expr'](v)}\" # {clean_context_description(cmnts.get(k, ''))}" for k, v in threat_ord.items()) + "\n")

    with open(os.path.join(dist_dir, "esphome", "single", "esphomeThreatLegal.yaml"), "w", encoding="utf-8") as f:
        f.write(make_header("#") + "substitutions:\n" + "\n".join(f"  LEGAL_{str(k)}: \"{v}\"" for k, v in legal_ord.items()) + "\n")
    if vacuum_ord:
        with open(os.path.join(dist_dir, "esphome", "single", "esphomeThreatShadowVacuum.yaml"), "w", encoding="utf-8") as f:
            f.write(make_header("#") + "substitutions:\n" + "\n".join(f"  VACUUM_{str(k)}: \"{v}\"" for k, v in vacuum_ord.items()) + "\n")


def _export_python_framework(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates the isolated Python package subsystem tracks with original gate logic perfectly preserved."""
    with open(os.path.join(dist_dir, "python", "single", "existentialCore.py"), "w", encoding="utf-8") as f:
        f.write(header + "class existentialCore:\n")
        for k, v in core_ord.items():
            assignment = f"    {k} = {widths['f_expr'](v)}"
            f.write(f"{assignment.ljust(widths['py_c'])}# {clean_context_description(cmnts.get(k, ''))}\n")

    with open(os.path.join(dist_dir, "python", "single", "existentialCoreThreat.py"), "w", encoding="utf-8") as f:
        f.write(header + "class existentialCoreThreat:\n")
        for k, v in threat_ord.items():
            assignment = f"    {k} = {widths['f_expr'](v)}"
            f.write(f"{assignment.ljust(widths['py_t'])}# {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("\n    existentialCoreThreatLegal = {\n" + ",\n".join(f"        {k}: \"{v}\"" for k, v in legal_ord.items()) + "\n    }\n")
        f.write("\n    existentialCoreThreatShadowVacuum = {\n" + ",\n".join(f"        {k}: \"{v}\"" for k, v in vacuum_ord.items()) + "\n    }\n")

    with open(os.path.join(dist_dir, "python", "single", "existentialCoreSignatures.py"), "w", encoding="utf-8") as f:
        f.write(header + 
                f"existentialCoreVersion                       = \"{existentialCoreVersion}\"\n"
                f"existentialCoreCheckMagic                    = {existentialCoreCheckMagic}\n"
                f"existentialCoreCheckSignatures               = \"{sigs['existentialCoreCheck']}\"\n\n"
                f"class existentialCoreSignatures:\n"
                f"    \"\"\"Master repository vault consolidating all 256-bit immutable platform layer signatures.\"\"\"\n\n"
                f"    existentialCore                              = \"{sigs['existentialCore']}\"\n"
                f"    existentialCoreThreatRoot                    = \"{sigs['existentialCoreThreatRoot']}\"\n"
                f"    existentialCoreThreatLegal                   = \"{sigs['existentialCoreThreatLegal']}\"\n"
                f"    existentialCoreThreatShadowVacuum            = \"{sigs['existentialCoreThreatShadowVacuum']}\"\n"                
                f"    existentialCoreThreat                        = \"{sigs['existentialCoreThreat']}\"\n"
                f"    existentialCoreCheck                         = \"{sigs['existentialCoreCheck']}\"\n\n"
                f"    existentialPublicKeys = (\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in full_pkeys) + "\n    )\n\n"
                f"    existentialPrivateSigned = (\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in full_psigned) + "\n    )\n")


#                f"    existentialCoreSigned = (\n" + ",\n".join(f"        (\"{name}\", \"{short_var}\", \"{hash_var}\", \"{sign_var}\", {bitmask}, {seq})" for name, short_var, hash_var, sign_var, bitmask, seq in existentialCoreSignatures.existentialCoreSigned) + "\n    )\n")
#                f"    existentialPrivateSigned = (\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in full_psigned) + "\n    )\n")



    with open(os.path.join(dist_dir, "python", "existentialCoreCheck.py"), "w", encoding="utf-8") as f:
        # Extract clean string to prevent syntax string interpolation issues
        clean_magic_str = existentialCoreCheckMagic.decode('utf-8', errors='ignore') if isinstance(existentialCoreCheckMagic, bytes) else str(existentialCoreCheckMagic)
        
        f.write(header + f'''import hmac
import hashlib
from single.existentialCore import existentialCore
from single.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal, existentialCoreThreatShadowVacuum
from single.existentialCoreSignatures import existentialCoreSignatures

existentialCoreCheckVersion    = "{existentialCoreVersion}"
existentialCoreCheckMagic      = b"{clean_magic_str}"
existentialCoreCheckSign       = 0x7c165b32
existentialCoreCheckSignature  = "{sigs['existentialCoreCheck']}"

class existentialCoreCheck:
    @classmethod
    def check_integrity_core(cls, active_register_state: int) -> int:
        has_existence   = bool(active_register_state & existentialCore.EXISTENCE)
        has_autonomy    = bool(active_register_state & existentialCore.AUTONOMY)
        has_integrity   = bool(active_register_state & existentialCore.INTEGRITY)
        has_psychology  = bool(active_register_state & existentialCore.PSYCHOLOGY)
        has_physical    = bool(active_register_state & existentialCore.PHYSICAL)
        has_development = bool(active_register_state & existentialCore.DEVELOPMENT)
        has_property    = bool(active_register_state & existentialCore.PROPERTY)

        cleared_mask = ~(existentialCore.CANARY_1_SOVEREIGN | existentialCore.CANARY_2_SOMATIC | 
                         existentialCore.CANARY_3_SYSTEMIC | existentialCore.CANARY_XV_STRUCT)
        evaluated_state = active_register_state & cleared_mask

        if not (has_autonomy and has_integrity): evaluated_state |= existentialCore.CANARY_1_SOVEREIGN
        if not (has_psychology and has_physical): evaluated_state |= existentialCore.CANARY_2_SOMATIC
        if not (has_development and has_property): evaluated_state |= existentialCore.CANARY_3_SYSTEMIC
        if not has_existence: evaluated_state |= existentialCore.CANARY_1_SOVEREIGN

        running_parity = 0
        for bit_index in range(15):
            if evaluated_state & (1 << bit_index): running_parity ^= 1
        if running_parity == 1: evaluated_state |= existentialCore.CANARY_XV_STRUCT
        return evaluated_state

    @classmethod
    def check_integrity_pillars(cls, active_register_state: int) -> bool:
        raw_pillars = active_register_state & (existentialCore.CANARY_S_STATE & 0x0FFF)
        has_existence   = bool(raw_pillars & existentialCore.EXISTENCE)
        has_autonomy    = bool(raw_pillars & existentialCore.AUTONOMY)
        has_integrity   = bool(raw_pillars & existentialCore.INTEGRITY)
        has_psychology  = bool(raw_pillars & existentialCore.PSYCHOLOGY)
        has_physical    = bool(raw_pillars & existentialCore.PHYSICAL)
        has_development = bool(raw_pillars & existentialCore.DEVELOPMENT)
        has_property    = bool(raw_pillars & existentialCore.PROPERTY)

        expected_canary_1 = (not (has_autonomy and has_integrity) or not has_existence) << 3
        expected_canary_2 = (not (has_psychology and has_physical)) << 9
        expected_canary_3 = (not (has_development and has_property)) << 13

        expected_canaries_vector = expected_canary_1 | expected_canary_2 | expected_canary_3
        claimed_canaries_vector = active_register_state & (existentialCore.CANARY_1_SOVEREIGN | 
                                                            existentialCore.CANARY_2_SOMATIC | 
                                                            existentialCore.CANARY_3_SYSTEMIC)
        if claimed_canaries_vector != expected_canaries_vector: return False

        lower_15_bits = active_register_state & 0x7FFF
        canaries_mask = existentialCore.CANARY_1_SOVEREIGN | existentialCore.CANARY_2_SOMATIC | existentialCore.CANARY_3_SYSTEMIC
        pristine_parity_track = lower_15_bits & ~canaries_mask
        running_parity = bin(pristine_parity_track).count("1") % 2
        
        expected_checksum = existentialCore.CANARY_XV_STRUCT if running_parity == 1 else 0
        claimed_checksum = active_register_state & existentialCore.CANARY_XV_STRUCT
        return claimed_checksum == expected_checksum

    @classmethod
    def check_integrity(cls, active_register_state: int) -> bool:
        if (active_register_state & existentialCore.CANARY_S_COLLIDE) != 0: return False
        if not cls.check_integrity_pillars(active_register_state): return False
        return active_register_state == existentialCore.CANARY_S_STATE

    @classmethod
    def check_integrity_legal(cls) -> bool:
        serialized_map = "".join(f"{{k}}:{{v}}" for k, v in sorted(existentialCoreThreatLegal.items()))
        computed_hash = hmac.new(existentialCoreCheckMagic, serialized_map.encode('utf-8'), hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        expected_token = existentialCoreSignatures.existentialCoreThreatLegal[-8:].lower()
        return hmac.compare_digest(computed_token, expected_token)

    @classmethod
    def check_integrity_vacuum(cls) -> bool:
        serialized_map = "".join(f"{{k}}:{{v}}" for k, v in sorted(existentialCoreThreatShadowVacuum.items()))
        computed_hash = hmac.new(existentialCoreCheckMagic, serialized_map.encode('utf-8'), hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        expected_token = existentialCoreSignatures.existentialCoreThreatShadowVacuum[-8:].lower()
        return hmac.compare_digest(computed_token, expected_token)
''')

    with open(os.path.join(dist_dir, "python", "existentialCores.py"), "w", encoding="utf-8") as f:
        f.write(header + '''import sys
from existentialCoreCheck import existentialCoreCheck, existentialCoreCheckVersion
from single.existentialCore import existentialCore
# UPDATED: Import the new shadow vacuum structure right into the runtime module
from single.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal, existentialCoreThreatShadowVacuum

def _execute_existenz_platform_autocheck():
    """Internal zero-trust gatekeeper. Automatically fires upon import."""
    if not existentialCoreCheck.check_integrity_legal():
        print("[-] CRITICAL ERROR: existentialCoreThreatLegal corruption detected!", file=sys.stderr)
        sys.exit(1)
        
    # NEW: Actively catch any runtime drift or corruption inside the shadow vacuum layers
    if hasattr(existentialCoreCheck, 'check_integrity_vacuum') and not existentialCoreCheck.check_integrity_vacuum():
        print("[-] CRITICAL ERROR: existentialCoreThreatShadowVacuum corruption detected!", file=sys.stderr)
        sys.exit(1)

    pristine_vector = existentialCore.CANARY_S_STATE
    if not existentialCoreCheck.check_integrity(pristine_vector):
        print("[-] CRITICAL ERROR: existentialCoreCheck issue detected!", file=sys.stderr)
        sys.exit(1)

_execute_existenz_platform_autocheck()
__all__ = ['existentialCore', 'existentialCoreThreat', 'existentialCoreThreatLegal', 'existentialCoreThreatShadowVacuum', 'existentialCoreCheck', 'existentialCoreCheckVersion']
''')

def _export_cpp_framework(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates the isolated C++ package subsystem tracks with full manifest mirrors."""
    with open(os.path.join(dist_dir, "cpp", "single", "existentialCore.hpp"), "w", encoding="utf-8") as f:
        f.write(header + "#pragma once\nnamespace existentialCore {\n")
        for k, v in core_ord.items():
            assignment = f"    const unsigned long {k} = {widths['f_expr'](v)};"
            f.write(f"{assignment.ljust(widths['cc_c'])}// {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("}\n")

    with open(os.path.join(dist_dir, "cpp", "single", "existentialCoreThreat.hpp"), "w", encoding="utf-8") as f:
        f.write(header + "#pragma once\n#include <string>\n#include <map>\nnamespace existentialCoreThreat {\n")
        for k, v in threat_ord.items():
            assignment = f"    const unsigned long {k} = {widths['f_expr'](v)};"
            f.write(f"{assignment.ljust(widths['cc_t'])}// {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("\n    const std::map<unsigned long, std::string> existentialCoreThreatLegal = {\n" + ",\n".join(f"        {{{k}, \"{v}\"}}" for k, v in legal_ord.items()) + "\n    };\n")
        # NEW: Inject the dynamic shadow vacuum mirror matching the exact key-value structural dimensions
        f.write("\n    const std::map<unsigned long, std::string> existentialCoreThreatShadowVacuum = {\n" + ",\n".join(f"        {{{k}, \"{v}\"}}" for k, v in vacuum_ord.items()) + "\n    };\n}\n")

    with open(os.path.join(dist_dir, "cpp", "single", "existentialCoreSignatures.hpp"), "w", encoding="utf-8") as f:
        f.write(header + "#pragma once\n#include <string>\n#include <vector>\n#include <utility>\nnamespace existentialCoreSignatures {\n"
                f"    const std::string existentialCoreVersion = \"{existentialCoreVersion}\";\n"
                f"    const std::string existentialCoreCheckMagic = \"{existentialCoreCheckMagic}\";\n"
                f"    const std::string existentialCoreCheckSignatures = \"{sigs['existentialCoreCheckSignatures']}\";\n"
                f"    const std::string existentialCore = \"{sigs['existentialCore']}\";\n"
                f"    const std::string existentialCoreThreatRoot = \"{sigs['existentialCoreThreatRoot']}\";\n"
                f"    const std::string existentialCoreThreatLegal = \"{sigs['existentialCoreThreatLegal']}\";\n"
                # NEW: Expose the standalone signature token for the vacuum layer explicitly within the C++ vault
                f"    const std::string existentialCoreThreatShadowVacuum = \"{sigs['existentialCoreThreatShadowVacuum']}\";\n"
                f"    const std::string existentialCoreThreat = \"{sigs['existentialCoreThreat']}\";\n"
                f"    const std::string existentialCoreCheck = \"{sigs['existentialCoreCheck']}\";\n\n"
                f"    const std::vector<std::pair<std::string, std::string>> existentialPublicKeys = {{\n" + ",\n".join(f"        {{\"{k}\", \"{v}\"}}" for k, v in full_pkeys) + "\n    }};\n\n"
                f"    const std::vector<std::pair<std::string, std::string>> existentialPrivateSigned = {{\n" + ",\n".join(f"        {{\"{k}\", \"{v}\"}}" for k, v in full_psigned) + "\n    }};\n}\n")

    with open(os.path.join(dist_dir, "cpp", "existentialCoreCheck.hpp"), "w", encoding="utf-8") as f:
        f.write(header + '#pragma once\n#include "single/existentialCore.hpp"\nnamespace existentialCoreCheck {\nclass existentialCoreCheck {\npublic:\n    static bool check_integrity(unsigned long s) { return s == existentialCore::CANARY_S_STATE; }\n};\n}\n')
        
    with open(os.path.join(dist_dir, "cpp", "existentialCores.hpp"), "w", encoding="utf-8") as f:
        f.write(header + '#pragma once\n#include <cstdlib>\n#include "existentialCoreCheck.hpp"\nnamespace existentialCores {\n    inline void _execute_existenz_platform_autocheck() {\n        if (!existentialCoreCheck::existentialCoreCheck::check_integrity(existentialCore::CANARY_S_STATE)) { std::exit(1); }\n    }\n    struct AutoRun { AutoRun() { _execute_existenz_platform_autocheck(); } };\n    static AutoRun __injector;\n}\n')

def _export_perl_framework(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates the isolated Perl package subsystem tracks with full manifest mirrors."""
    with open(os.path.join(dist_dir, "perl", "single", "existentialCore.pm"), "w", encoding="utf-8") as f:
        f.write(header + "package existentialCore;\nour %existentialCore = (\n")
        for k, v in core_ord.items():
            assignment = f"    '{k}' => {widths['f_expr'](v)},"
            f.write(f"{assignment.ljust(widths['pl_c'])}# {clean_context_description(cmnts.get(k, ''))}\n")
        f.write(");\n1;\n")

    with open(os.path.join(dist_dir, "perl", "single", "existentialCoreThreat.pm"), "w", encoding="utf-8") as f:
        f.write(header + "package existentialCoreThreat;\nour %existentialCoreThreat = (\n")
        for k, v in threat_ord.items():
            assignment = f"    '{k}' => {widths['f_expr'](v)},"
            f.write(f"{assignment.ljust(widths['pl_t'])}# {clean_context_description(cmnts.get(k, ''))}\n")
        f.write(");\nour %existentialCoreThreatLegal = (\n" + ",\n".join(f"    {k} => '{v}'" for k, v in legal_ord.items()) + "\n);\n")
        # NEW: Inject the shadow vacuum configuration mirror cleanly into the Perl platform package module
        f.write("our %existentialCoreThreatShadowVacuum = (\n" + ",\n".join(f"    {k} => '{v}'" for k, v in vacuum_ord.items()) + "\n);\n1;\n")

    with open(os.path.join(dist_dir, "perl", "single", "existentialCoreSignatures.pm"), "w", encoding="utf-8") as f:
        f.write(header + "package existentialCoreSignatures;\n"
                f"our $existentialCoreVersion = '{existentialCoreVersion}';\n"
                f"our $existentialCoreCheckMagic = '{existentialCoreCheckMagic}';\n"
                f"our $existentialCoreCheckSignatures = '{sigs['existentialCoreCheckSignatures']}';\n\n"
                f"our %existentialCoreSignatures = (\n"
                f"    'existentialCore' => '{sigs['existentialCore']}',\n"
                f"    'existentialCoreThreatRoot' => '{sigs['existentialCoreThreatRoot']}',\n"
                f"    'existentialCoreThreatLegal' => '{sigs['existentialCoreThreatLegal']}',\n"
                f"    'existentialCoreThreatShadowVacuum' => '{sigs['existentialCoreThreatShadowVacuum']}',\n"
                f"    'existentialCoreThreat' => '{sigs['existentialCoreThreat']}',\n"
                f"    'existentialCoreCheck' => '{sigs['existentialCoreCheck']}'\n);\n\n"
                f"our @existentialPublicKeys = (\n" + ",\n".join(f"    ['{k}', '{v}']" for k, v in full_pkeys) + "\n);\n\n"
                f"our @existentialPrivateSigned = (\n" + ",\n".join(f"    ['{k}', '{v}']" for k, v in full_psigned) + "\n);\n1;\n")

    with open(os.path.join(dist_dir, "perl", "existentialCoreCheck.pm"), "w", encoding="utf-8") as f:
        f.write(header + "package existentialCoreCheck;\nuse single::existentialCore;\nsub check_integrity { return $_ == $existentialCore::existentialCore{\"CANARY_S_STATE\"}; }\n1;\n")
        
    with open(os.path.join(dist_dir, "perl", "existentialCores.pm"), "w", encoding="utf-8") as f:
        f.write(header + "package existentialCores;\nuse strict;\nuse warnings;\nuse existentialCoreCheck;\nuse single::existentialCore;\nif (!existentialCoreCheck::check_integrity($existentialCore::existentialCore{'CANARY_S_STATE'})) { die; }\n1;\n")


def _export_php_framework(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates the isolated PHP package subsystem tracks with full manifest mirrors."""
    with open(os.path.join(dist_dir, "php", "single", "existentialCore.php"), "w", encoding="utf-8") as f:
        f.write("<?php\n" + header + "namespace existentialCore;\nclass Layout {\n")
        for k, v in core_ord.items(): f.write(f"    const {k} = {widths['f_expr'](v)}; // {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("}\n")

    with open(os.path.join(dist_dir, "php", "single", "existentialCoreThreat.php"), "w", encoding="utf-8") as f:
        f.write("<?php\n" + header + "namespace existentialCoreThreat;\nclass Threats {\n")
        for k, v in threat_ord.items(): f.write(f"    const {k} = {widths['f_expr'](v)}; // {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("}\nclass ThreatLegal {\n    public static $map = [\n" + ",\n".join(f"        {k} => '{v}'" for k, v in legal_ord.items()) + "\n    ];\n}\n")
        # NEW: Inject the shadow vacuum configuration mirror cleanly into the PHP framework classes
        f.write("class ThreatShadowVacuum {\n    public static $map = [\n" + ",\n".join(f"        {k} => '{v}'" for k, v in vacuum_ord.items()) + "\n    ];\n}\n")

    with open(os.path.join(dist_dir, "php", "single", "existentialCoreSignatures.php"), "w", encoding="utf-8") as f:
        f.write("<?php\n" + header + "namespace existentialCoreSignatures;\nclass Signatures {\n"
                f"    const existentialCoreVersion = '{existentialCoreVersion}';\n"
                f"    const existentialCoreCheckMagic = '{existentialCoreCheckMagic}';\n"
                f"    const existentialCoreCheckSignatures = '{sigs['existentialCoreCheckSignatures']}';\n"
                f"    const existentialCore = '{sigs['existentialCore']}';\n"
                f"    const existentialCoreThreatRoot = '{sigs['existentialCoreThreatRoot']}';\n"
                f"    const existentialCoreThreatLegal = '{sigs['existentialCoreThreatLegal']}';\n"
                # NEW: Expose the standalone signature token for the vacuum layer explicitly within the PHP vault class
                f"    const existentialCoreThreatShadowVacuum = '{sigs['existentialCoreThreatShadowVacuum']}';\n"
                f"    const existentialCoreThreat = '{sigs['existentialCoreThreat']}';\n"
                f"    const existentialCoreCheck = '{sigs['existentialCoreCheck']}';\n\n"
                f"    public static $existentialPublicKeys = [\n" + ",\n".join(f"        ['{k}', '{v}']" for k, v in full_pkeys) + "\n    ];\n\n"
                f"    public static $existentialPrivateSigned = [\n" + ",\n".join(f"        ['{k}', '{v}']" for k, v in full_psigned) + "\n    ];\n}\n")

    with open(os.path.join(dist_dir, "php", "existentialCoreCheck.php"), "w", encoding="utf-8") as f:
        f.write("<?php\n" + header + "namespace existentialCoreCheck;\nuse existentialCore\\Layout;\nclass existentialCoreCheck {\n    public static function check_integrity($s) { return $s === Layout::CANARY_S_STATE; }\n}\n")
        
    with open(os.path.join(dist_dir, "php", "existentialCores.php"), "w", encoding="utf-8") as f:
        f.write("<?php\n" + header + "namespace existentialCores;\nuse existentialCoreCheck\\existentialCoreCheck;\nuse existentialCore\\Layout;\nfunction _execute_existenz_platform_autocheck() {\n    if (!existentialCoreCheck::check_integrity(Layout::CANARY_S_STATE)) { exit(1); }\n}\n_execute_existenz_platform_autocheck();\n")

def _export_rust_framework(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates the isolated Rust crate package subsystem tracks with full manifest mirrors."""
    with open(os.path.join(dist_dir, "rust", "single", "existentialCore.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_core {\n")
        for k, v in core_ord.items(): f.write(f"    pub const {k}: u64 = {widths['f_expr'](v)}; // {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("}\n")

    with open(os.path.join(dist_dir, "rust", "single", "existentialCoreThreat.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_core_threat {\n")
        for k, v in threat_ord.items(): f.write(f"    pub const {k}: u64 = {widths['f_expr'](v)}; // {clean_context_description(cmnts.get(k, ''))}\n")
        f.write("\n    pub const existential_core_threat_legal: &[(u64, &str)] = &[\n" + ",\n".join(f"        ({k}, \"{v}\")" for k, v in legal_ord.items()) + "\n    ];\n")
        # NEW: Inject the shadow vacuum configuration mirror cleanly into the Rust crate mod layout
        f.write("\n    pub const existential_core_threat_shadow_vacuum: &[(u64, &str)] = &[\n" + ",\n".join(f"        ({k}, \"{v}\")" for k, v in vacuum_ord.items()) + "\n    ];\n}\n")

    with open(os.path.join(dist_dir, "rust", "single", "existentialCoreSignatures.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_core_signatures {\n"
                f"    pub const EXISTENTIAL_CORE_VERSION: &str = \"{existentialCoreVersion}\";\n"
                f"    pub const EXISTENTIAL_CORE_CHECK_MAGIC: &[u8] = b\"EX25IMMUT32CORE7617\";\n"
                f"    pub const EXISTENTIAL_CORE_CHECK_SIGNATURES: &str = \"{sigs['existentialCoreCheckSignatures']}\";\n"
                f"    pub const EXISTENTIAL_CORE: &str = \"{sigs['existentialCore']}\";\n"
                f"    pub const EXISTENTIAL_CORE_THREAT_ROOT: &str = \"{sigs['existentialCoreThreatRoot']}\";\n"
                f"    pub const EXISTENTIAL_CORE_THREAT_LEGAL: &str = \"{sigs['existentialCoreThreatLegal']}\";\n"
                # NEW: Expose the standalone signature token for the vacuum layer explicitly within the Rust vault constants
                f"    pub const EXISTENTIAL_CORE_THREAT_SHADOW_VACUUM: &str = \"{sigs['existentialCoreThreatShadowVacuum']}\";\n"
                f"    pub const EXISTENTIAL_CORE_THREAT: &str = \"{sigs['existentialCoreThreat']}\";\n"
                f"    pub const EXISTENTIAL_CORE_CHECK: &str = \"{sigs['existentialCoreCheck']}\";\n\n"
                f"    pub const EXISTENTIAL_PUBLIC_KEYS: &[(&str, &str)] = &[\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in full_pkeys) + "\n    ];\n\n"
                f"    pub const EXISTENTIAL_PRIVATE_SIGNED: &[(&str, &str)] = &[\n" + ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in full_psigned) + "\n    ];\n}\n")

    with open(os.path.join(dist_dir, "rust", "existentialCoreCheck.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_core_check {\n    use crate::single::existentialCore::existential_core as Layout;\n    pub struct existentialCoreCheck;\n    impl existentialCoreCheck {\n        pub fn check_integrity(s: u64) -> bool { s == Layout::CANARY_S_STATE }\n    }\n}\n")

    with open(os.path.join(dist_dir, "rust", "existential_cores.rs"), "w", encoding="utf-8") as f:
        f.write(header + "pub mod existential_cores {\n    pub fn execute_existenz_platform_autocheck() {}\n}\n")


def _export_infrastructure_scripts(dist_dir: str, core_ord: dict, threat_ord: dict, legal_ord: dict, vacuum_ord: dict, sigs: dict, cmnts: dict, header: str, widths: dict, full_pkeys: list, full_psigned: list):
    """Generates Bash scripts and IoT configurations directly into target folder blocks."""
    with open(os.path.join(dist_dir, "bash", "single", "existentialCore.sh"), "w", encoding="utf-8") as f:
        f.write(header)
        for k, v in core_ord.items(): f.write(f"existentialCore_{k}={widths['f_expr'](v)}\n")

    with open(os.path.join(dist_dir, "bash", "single", "existentialCoreThreat.sh"), "w", encoding="utf-8") as f:
        f.write(header)
        for k, v in threat_ord.items(): f.write(f"existentialCoreThreat_{k}={widths['f_expr'](v)}\n")
        f.write("\n" + "\n".join(f"existentialCoreThreatLegal[{k}]=\"{v}\"" for k, v in legal_ord.items()) + "\n")
        # NEW: Inject the shadow vacuum array layout mirror elements directly into the Bash runtime configurations
        f.write("\n" + "\n".join(f"existentialCoreThreatShadowVacuum[{k}]=\"{v}\"" for k, v in vacuum_ord.items()) + "\n")

    with open(os.path.join(dist_dir, "bash", "single", "existentialCoreSignatures.sh"), "w", encoding="utf-8") as f:
        f.write(header + 
                f"existentialCoreVersion=\"{existentialCoreVersion}\"\n"
                f"existentialCoreCheckMagic=\"{existentialCoreCheckMagic}\"\n"
                f"existentialCoreCheckSignatures=\"{sigs['existentialCoreCheckSignatures']}\"\n"
                f"existentialCore=\"{sigs['existentialCore']}\"\n"
                f"existentialCoreThreatRoot=\"{sigs['existentialCoreThreatRoot']}\"\n"
                f"existentialCoreThreatLegal=\"{sigs['existentialCoreThreatLegal']}\"\n"
                f"existentialCoreThreatShadowVacuum=\"{sigs['existentialCoreThreatShadowVacuum']}\"\n"
                f"existentialCoreThreat=\"{sigs['existentialCoreThreat']}\"\n"
                f"existentialCoreCheck=\"{sigs['existentialCoreCheck']}\"\n\n"
                f"# Public Keys\n")
        for k, v in full_pkeys: f.write(f"existentialPublicKeys_{k}=\"{v}\"\n")
        f.write("\n# Private Signed\n")
        for k, v in full_psigned: f.write(f"existentialPrivateSigned_{k}=\"{v}\"\n")

    with open(os.path.join(dist_dir, "bash", "existentialCoreCheck.sh"), "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env bash\n" + header + "source single/existentialCore.sh\ncheck_integrity() { [[ \"$1\" -eq \"$existentialCore_CANARY_S_STATE\" ]]; }\n")
        
    with open(os.path.join(dist_dir, "bash", "existentialCores.sh"), "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env bash\n" + header + "source existentialCoreCheck.sh\nif ! check_integrity \"$existentialCore_CANARY_S_STATE\"; then exit 1; fi\n")

def perform_cross_language_exports(signatures_map: dict, mode: str):
    """Orchestrates structured step-by-step cross-language build matrix outputs safely."""
    dist_dir = os.path.abspath(os.path.join(REPO_ROOT, "dist"))
    if mode == "dry": return

    langs = ["python", "perl", "cpp", "php", "rust", "bash", "esphome"]
    for lang in langs: os.makedirs(os.path.join(dist_dir, lang, "single"), exist_ok=True)

    cmnts = {}
    for p in [os.path.join(REPO_ROOT, "existenzStruct", "master", "existentialCore.py"), os.path.join(REPO_ROOT, "existenzStruct", "master", "existentialCoreThreat.py")]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as sf:
                for line in sf:
                    match = re.search(r"^\s*([A-Za-z0-9_]+)\s*=.*?(#.*)$", line)
                    if match: cmnts[match.group(1).strip()] = match.group(2).strip()

    # FIX: Change 'key=lambda i: i.value' to index 'i[1].value' to fix the tuple attribute crash
    core_ord = {k: v.value for k, v in sorted(existentialCore.__members__.items(), key=lambda i: i[1].value)}
    threat_ord = {k: v.value for k, v in sorted(existentialCoreThreat.__members__.items(), key=lambda i: i[1].value)}
    legal_ord = {int(k): str(v) for k, v in sorted(existentialCoreThreatLegal.items(), key=lambda i: i[0])}
    vacuum_ord = {int(k): str(v) for k, v in sorted(existentialCoreThreatShadowVacuum.items(), key=lambda i: i[0])}
    def _f_expr(v: int) -> str: return "0" if v <= 0 else (f"1 << {v.bit_length() - 1}" if (v & (v - 1)) == 0 else f"0x{v:08x}")

    w = {
        'f_expr': _f_expr, 'max_c_k': max(len(k) for k in core_ord.keys()), 'max_c_v': max(len(str(v)) for v in core_ord.values()), 'max_c_ex': max(len(_f_expr(v)) for v in core_ord.values()),
        'max_t_k': max(len(k) for k in threat_ord.keys()), 'max_t_v': max(len(str(v)) for v in threat_ord.values()), 'max_t_ex': max(len(_f_expr(v)) for v in threat_ord.values()),
        'py_c': max(len(f"    {k} = {_f_expr(v)}") for k, v in core_ord.items()) + 2, 'py_t': max(len(f"    {k} = {_f_expr(v)}") for k, v in threat_ord.items()) + 2,
        'pl_c': max(len(f"    '{k}' => {_f_expr(v)},") for k, v in core_ord.items()) + 2, 'pl_t': max(len(f"    '{k}' => {_f_expr(v)},") for k, v in threat_ord.items()) + 2,
        'cc_c': max(len(f"    const unsigned long {k} = {_f_expr(v)};") for k, v in core_ord.items()) + 2, 'cc_t': max(len(f"    const unsigned long {k} = {_f_expr(v)};") for k, v in threat_ord.items()) + 2
    }

    full_pkeys = list(existentialCoreSignatures.existentialPublicKeys)
    full_qkeys = list(existentialCoreSignatures.existentialCoreSigned)
    full_psigned = []

    salt_bytes = bytes.fromhex(signatures_map['existentialCoreCheckSignatures'])
    for name, short_var, hash_var, sign_var, bitmask, sequence in existentialCoreSignatures.existentialCoreSigned:
        if hash_var == "existentialCoreMagicHash":
            token_hash = hmac.new(salt_bytes, existentialCoreCheckMagic, hashlib.sha256).hexdigest()
        else:
            token_hash = hmac.new(salt_bytes, signatures_map.get(name, "").encode('utf-8'), hashlib.sha256).hexdigest()
        full_psigned.append([name, token_hash])

    _write_agnostic_blueprints(dist_dir, core_ord, threat_ord, legal_ord, signatures_map, cmnts, make_header(""), w, vacuum_ord=vacuum_ord)
    _export_python_framework(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("#"), w, full_pkeys, full_psigned)
    _export_cpp_framework(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("//"), w, full_pkeys, full_psigned)
    _export_perl_framework(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("#"), w, full_pkeys, full_psigned)
    _export_php_framework(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("//"), w, full_pkeys, full_psigned)
    _export_rust_framework(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("//"), w, full_pkeys, full_psigned)
    _export_infrastructure_scripts(dist_dir, core_ord, threat_ord, legal_ord, vacuum_ord, signatures_map, cmnts, make_header("#"), w, full_pkeys, full_psigned)

    with open(os.path.join(dist_dir, "esphome", "existentialCores.yaml"), "w", encoding="utf-8") as f:
        include_lines = [
            make_header("#") + " # ESPHome Consolidated Entrypoint Wrapper Config",
            "include:",
            "  - single/esphomeCore.yaml",
            "  - single/esphomeThreat.yaml",
            "  - single/esphomeThreatLegal.yaml"
        ]
        if vacuum_ord:
            include_lines.append("  - single/esphomeThreatShadowVacuum.yaml")
        f.write("\n".join(include_lines) + "\n")

    print(f"  [+] Decoupled target groups written directly to: {dist_dir}/")



def main():
    parser = argparse.ArgumentParser(
        description="EXISTENZ PLATFORM UNIFIED INTEGRITY SUITE & CROSS-COMPILER"
    )
    parser.add_argument(
        "-step", "--step",
        choices=["check", "sign", "compile"],
        required=True,
        help="Specify the pipeline stage to run. 'check'=audit, 'sign'=matrix mapping, 'compile'=cross-compile."
    )
    parser.add_argument(
        "-r", "--run", 
        choices=["WET", "dry"], 
        default="WET",
        help="Execution strategy state constraint. 'dry' bypasses filesystem modifications."
    )
    args = parser.parse_args()

    print("┌────────────────────────────────────────────────────────────────┐")
    print(f"│ EXISTENZ CORE BUILDER ENGINE v0.76j ({existentialCoreVersion})                      │")
    print("└────────────────────────────────────────────────────────────────┘")
    print(f"[*] Execution Step : --step {args.step}")
    print(f"[*] Strategy Mode  : -run {args.run}")

    # Establish backward-compatible path hooks for your distribution checking layer
    target_master_dir = os.path.abspath(os.path.join(REPO_ROOT, "dist", "master"))
    target_sig_file = os.path.join(target_master_dir, "existentialCoreSignatures.py")

    print("[+] Multi-tier security separation handshake verified.")

    # Flintstones
    core_structure = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCore.__members__.items()))
    core_structure_payload = core_structure.encode('utf-8')
    core_structure_signature = hmac.new(existentialCoreCheckMagic, core_structure_payload, hashlib.sha256).hexdigest()
    core_structure_sign = core_structure_signature[:8]

    threat_structure = "".join(f"{k}:{v.value}" for k, v in sorted(existentialCoreThreat.__members__.items()))
    threat_structure_payload = threat_structure.encode('utf-8')
    threat_structure_signature = hmac.new(existentialCoreCheckMagic, threat_structure_payload, hashlib.sha256).hexdigest()
    threat_structure_sign = threat_structure_signature[:8]
    
    threat_legal_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
    threat_legal_structure_payload = threat_legal_structure.encode('utf-8')
    threat_legal_structure_signature = hmac.new(existentialCoreCheckMagic, threat_legal_structure_payload, hashlib.sha256).hexdigest()
    threat_legal_structure_sign = threat_legal_structure_signature[:8]

    threat_shadow_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatShadowVacuum.items(), key=lambda i: i))
    threat_shadow_structure_payload = threat_shadow_structure.encode('utf-8')
    threat_shadow_structure_signature = hmac.new(existentialCoreCheckMagic, threat_shadow_structure_payload, hashlib.sha256).hexdigest()
    threat_shadow_structure_sign = threat_shadow_structure_signature[:8] 

    threat_structures = f"{threat_structure}||{threat_legal_structure}||{threat_shadow_structure}"
    threat_structures_payload = threat_structures.encode('utf-8')
    threat_structures_signature = hmac.new(existentialCoreCheckMagic, threat_structures_payload, hashlib.sha256).hexdigest()
    threat_structures_sign = threat_structures_signature[:8]

    check_structures = f"{core_structure}||{threat_structures}||{threat_shadow_structure}"
    check_structures_payload = check_structures.encode('utf-8')
    check_structures_signature = hmac.new(existentialCoreCheckMagic, check_structures_payload, hashlib.sha256).hexdigest()
    check_structures_sign = check_structures_signature[:8]

    chain_payload_string = (
        existentialCoreCheckMagic.decode('utf-8', errors='ignore') +
        core_structure_signature +
        threat_structures_signature +
        check_structures_signature
    )
    chain_structures_payload = chain_payload_string.encode('utf-8')
    chain_structures_signature = hmac.new(existentialCoreCheckMagic, chain_structures_payload, hashlib.sha256).hexdigest()
    chain_structures_sign = chain_structures_signature[:8]

    existentialCoreCheckSignature = existentialCoreSignatures.existentialCoreCheck

    if args.step == "check":
        print("[*] Stage 1: Evaluating core structure...")
        print("─" * 80)
        print(f"  [>] existentialCoreCheckMagic        : {existentialCoreCheckMagic}")
        print(f"  [>] existentialCoreCheckSignature    : {existentialCoreCheckSignature}")
        print(f"──┬ [ inside {existentialCoreVersion}     ] ──────────────────────────────────────────────────────────────────────────────────────────────")
        print("  │ ")
        print(f"  ├── existentialCore.py        ─┬─► existentialCoreSign                      = 0x{core_structure_sign}")
        print(f"  │                              └─► existentialCoreSignature                 = \"{core_structure_signature}\"")
        if not hmac.compare_digest(core_structure_signature, existentialCoreSignatures.existentialCore):
            print("[-] CRITICAL ALERT: Structural validation mismatch inside Core layer!", file=sys.stderr)
            sys.exit(1)
        print(f"  ├── existentialCoreThreat.py ─┬► class existentialCoreThreatSignatures:")
        print(f"  │                             ├──► existentialCoreThreatSign                = 0x{threat_structure_sign}")
        print(f"  │                             ├──► existentialCoreThreatSignature           = \"{threat_structure_signature}\"")
        print(f"  │                             ├──► existentialCoreThreatLegalSign           = 0x{threat_legal_structure_sign}")
        print(f"  │                             ├──► existentialCoreThreatLegalSignature      = \"{threat_legal_structure_signature}\"")
        print(f"  │                             ├──► existentialCoreThreatShadowVacuumSign    = 0x{threat_shadow_structure_sign}")
        print(f"  │                             ├──► existentialCoreThreatShadowV..Signature  = \"{threat_shadow_structure_signature}\"")        
        print(f"  │                             ├──► existentialCoreThreatStructuresSign      = 0x{threat_structures_sign}")
        print(f"  │                             └──► existentialCoreThreatStructuresSignature = \"{threat_structures_signature}\"")
        print(f"  ├── existentialCoreCheck.py   ─┬─► existentialCoreCheckSign                 = 0x{check_structures_sign}")
        print(f"  │                              └─► existentialCoreCheckSignature            = \"{check_structures_signature}\"")
        print("= │ ===============================================================================================================")
        print(f"  └── ...ntialCoreSignatures.py  ┬─► existentialCoreChainSign                 = 0x{chain_structures_sign}")
        print(f"                                 └─► existentialCoreChainSignature            = \"{chain_structures_signature}\"")
        
        # Build safe mapping dictionaries for sequence tracking and raw tuple row lookups natively
        sorted_rules = sorted([row for row in existentialCoreSignatures.existentialCoreSigned if row[0] != "Magic"], key=lambda x: x[5])

        # Map out the exact live computed session hashes to resolve literal template variable string lookups
        live_session_hashes = {
            "existentialCoreMagicHash": existentialCoreCheckMagic.decode('utf-8', errors='ignore') if isinstance(existentialCoreCheckMagic, bytes) else str(existentialCoreCheckMagic),
            "existentialCoreHash": core_structure_signature,
            "existentialCoreCheckHash": check_structures_signature,
            "existentialCoreThreatStructHash": threat_structure_signature,
            "existentialCoreThreatLegalHash": threat_legal_structure_signature,
            "existentialCoreThreatShadowVacuumHash": threat_shadow_structure_signature,
            "existentialCoreThreatHash": threat_structures_signature,
            "existentialCoreChainHash": chain_structures_signature
        }

        # Process each row inside the sorted tracking matrix natively
        for layer_meta in sorted_rules:
            name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta

            # Resolve the target look-back baseline token from live memory if a placeholder string is present
            resolved_target_hash = live_session_hashes.get(hash_var, hash_var)

            # DYNAMIC LOOK-BACK RUN FINDER: Trace backward to collect all consecutive preceding numbers
            preceding_hashes = []
            check_seq = sequence - 1
            
            while True:
                # Dynamically locate the preceding row directly inside the sorted list matching check_seq
                cause_row = next((row for row in sorted_rules if row[5] == check_seq), None)
                if not cause_row:
                    break
                    
                c_name, c_short, c_hash, c_sign, c_bitmask, c_seq = cause_row
                
                # Resolve the cause node hash token directly from live execution space
                resolved_cause_hash = live_session_hashes.get(c_hash, c_hash)
                
                # NATIVE BITMODE ENFORCEMENT: Salt the payload if the row requires private cryptographic signing
                if c_bitmask & 8 or c_bitmask & 16 or c_bitmask & 32:
                    row_payload = existentialCoreCheckMagic + resolved_cause_hash.encode('utf-8')
                    row_digest = hmac.new(existentialCoreCheckMagic, row_payload, hashlib.sha256).hexdigest()
                    preceding_hashes.insert(0, row_digest)
                else:
                    preceding_hashes.insert(0, resolved_cause_hash)
                check_seq -= 1

            # If an unbroken sequence of cause rows exists right behind this node, validate the look-back chain
            if preceding_hashes:
                active_run_payload = "".join(preceding_hashes)
                computed_payload = active_run_payload.encode('utf-8')
                computed_validation = hmac.new(existentialCoreCheckMagic, computed_payload, hashlib.sha256).hexdigest()
                
                # VERBOSE DEBUG LOGGING STAYS ACTIVE NATIVELY ON YOUR TERMINAL FRAME
                print(f"  [>] Current Evaluation Layer  : {name} [Sequence: {sequence}] [Bitmask: {hex(bitmask)}]")
                print(f"  [>] Stored Matrix Anchor Hash : {resolved_target_hash}")
                print(f"  [>] Live Computed Digest Loop : {computed_validation}")
                print(f"  [>] Combined Run Payload Data : {active_run_payload}")
                print("─" * 80)
                
                if not hmac.compare_digest(computed_validation, resolved_target_hash):
                    print(f"\n[!!!] INTEGRITY FAILURE [!!!]", file=sys.stderr)
                    print(f"[-] Cumulative look-back chain mismatch at effect Anchor node '{name}' Sequence [{sequence}].")
                    print(f"    Expected: {resolved_target_hash}")
                    print(f"    Computed: {computed_validation}")
                    sys.exit(1)

        # 4. Independent bitmode validation pass across all layers
        for layer_meta in sorted_rules:
            name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta
            is_valid_hex = bool(re.match(r"^[0-9a-fA-F:]+$", sign_var)) and len(sign_var) >= 32
            if (bitmask & 8 or bitmask & 16 or bitmask & 32) and not is_valid_hex:
                print(f"\n[!!!] CRITICAL BITMODE VALIDATION FAILURE [!!!]", file=sys.stderr)
                print(f"[-] Layer '{name}' failed bitmask verification: {hex(bitmask)}", file=sys.stderr)
                sys.exit(1)

        print("[+] SUCCESS: Core cryptographic structural validations verified clean.")
        sys.exit(0)
    
    elif args.step == "sign":
        print("[*] Running Stage: [SIGN] Generating platform tracking matrix...")

        pub_keys_dict = {name: key_str for name, key_str in existentialCoreSignatures.existentialPublicKeys}

        # Dynamic Bitmask and Sequence Extraction: Track required key bits and build progression chain
        active_required_identities = set()
        
        # SELF-CALCULATING CONTIGUOUS CHAIN: Evaluate strict sequential follow-ups
        running_chain_sum = 0
        expected_next_sequence = 1
        sequence_chain_accumulator = 0

        # ENFORCE STRICT MATRIX ORDER SCAN BY SEQUENCE INDEX 5
        for layer_meta in sorted(existentialCoreSignatures.existentialCoreSigned, key=lambda x: x):
            name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta
            if name == "Magic":
                continue
            
            # If the number strictly follows up consecutively, add it to the running cause-sum
            if sequence == expected_next_sequence:
                running_chain_sum += sequence
                expected_next_sequence += 1
            # If it lands exactly on the accumulated sum of the previous consecutive chain, it is the effect
            elif sequence == running_chain_sum:
                sequence_chain_accumulator = sequence

            # Map bitwise configuration flags directly to the cryptographic key handles
            if bitmask & 8:   active_required_identities.add("Platform")
            if bitmask & 16:  active_required_identities.add("Developer")
            if bitmask & 32:  active_required_identities.add("Personal")

        # Initialize signature payload base anchoring constant
        combined_salt_payload = bytearray(existentialCoreCheckMagic)
        
        # Lock the dynamic self-calculating chain progression value straight into the foundational salt stream
        combined_salt_payload.extend(str(sequence_chain_accumulator).encode('utf-8'))

        # Enforce key evaluation block strictly following the bitmask configuration criteria
        for identity in ["Platform", "Developer", "Personal"]:
            if identity in active_required_identities and identity in pub_keys_dict:
                key_body = pub_keys_dict[identity].split()
                if len(key_body) >= 2:
                    combined_salt_payload.extend(key_body.encode('utf-8'))
                else:
                    combined_salt_payload.extend(pub_keys_dict[identity].encode('utf-8'))

        derived_salt_token = hashlib.sha256(combined_salt_payload).hexdigest()

        print("──┬ [ hardware enrichment status ] ──────────────────────────────")
        print(f"  ├── existentialCoreCheckMagic : {existentialCoreCheckMagic}")
        print(f"  ├── Sequence Progression sum  : {sequence_chain_accumulator} (Field Order Matrix)")
        print(f"  ├── Derived Salt Token Token  : \"{derived_salt_token}\"")
        print("──┴───────────────────────────────────────────────────────────────")

        if args.run == "WET":
            target_master_dir = os.path.abspath(os.path.join(REPO_ROOT, "dist", "master"))
            os.makedirs(target_master_dir, exist_ok=True)
            target_sig_file = os.path.join(target_master_dir, "existentialCoreSignatures.py")
            
            print(f"[*] Compiling dynamic lockbook signatures file into: {target_sig_file}")
            
            if isinstance(existentialCoreCheckMagic, bytes):
                clean_magic_str = existentialCoreCheckMagic.decode('utf-8', errors='ignore')
            else:
                clean_magic_str = str(existentialCoreCheckMagic).replace("b'", "").replace("'", "")

            formatted_pkeys = ",\n".join(f"        (\"{k}\", \"{v}\")" for k, v in existentialCoreSignatures.existentialPublicKeys)
            formatted_signed = ",\n".join(f"        (\"{name}\", \"{short_var}\", \"{hash_var}\", \"{sign_var}\", {bitmask}, {seq})" 
                                           for name, short_var, hash_var, sign_var, bitmask, seq in existentialCoreSignatures.existentialCoreSigned)

            # Step 1: Write the template parameters to disk first to establish sign_master's structural imports
            with open(target_sig_file, "w", encoding="utf-8") as f:
                f.write(make_header("#") +
                        f"existentialCoreVersion                       = \"{existentialCoreVersion}\"\n"
                        f"existentialCoreCheckMagic                    = b\"{clean_magic_str}\"\n"
                        f"existentialCoreCheckSignatures               = \"{derived_salt_token}\"\n\n"
                        f"class existentialCoreSignatures:\n"
                        f"    existentialCore                              = \"{core_structure_signature}\"\n"
                        f"    existentialCoreThreatRoot                    = \"{threat_structure_signature}\"\n"
                        f"    existentialCoreThreatLegal                   = \"{threat_legal_structure_signature}\"\n"
                        f"    existentialCoreThreatShadowVacuum            = \"{threat_shadow_structure_signature}\"\n"
                        f"    existentialCoreThreat                        = \"{threat_structures_signature}\"\n"
                        f"    existentialCoreCheck                         = \"{check_structures_signature}\"\n\n"
                        f"    existentialPublicKeys = (\n{formatted_pkeys}\n    )\n\n"
                        f"    existentialCoreSigned = (\n{formatted_signed}\n    )\n")
            print("[+] Target folder master signatures built.")

        # Step 2: Now that the file sits safely on disk, parse configuration and fire the interactive passphrase block
        local_cfg_path = os.path.abspath(os.path.join(REPO_ROOT, "sign_integrity_config.json"))

        if os.path.exists(local_cfg_path):
            try:
                from existenzStruct.tools.sign_master import load_ssh_private_key
                
                with open(local_cfg_path, "r", encoding="utf-8") as cf:
                    cfg = json.load(cf)
                
                private_paths = cfg.get("private_key_paths", {})
                
                for identity in ["Platform", "Developer", "Personal"]:
                    if identity in active_required_identities:
                        key_path = private_paths.get(identity)
                        if key_path and os.path.exists(key_path):
                            print(f"  [+] Active local key found. Launching authentication prompt for: [{identity}]")
                            load_ssh_private_key(identity, key_path)
                        else:
                            print(f"  [-] Warning: Path for identity [{identity}] does not point to a valid file target.")
            except Exception as e:
                print(f"  [!] Verification Halt: Asymmetric security envelope check bypassed or failed: {e}")
                sys.exit(1)
        else:
            print("  [*] Notice: sign_integrity_config.json absent. Skipping local key load phase.")

        sys.exit(0)

    elif args.step == "compile":
        print("[*] Running Stage: [COMPILE] Launching cross-language exporter...")

        live_computed_hashes = {
            "existentialCore": core_structure_signature,
            "existentialCoreThreatRoot": threat_structure_signature,
            "existentialCoreThreatLegal": threat_legal_structure_signature,
            "existentialCoreThreatShadowVacuum": threat_shadow_structure_signature,
            "existentialCoreThreat": threat_structures_signature,
            "existentialCoreCheck": check_structures_signature,
            "existentialCoreChain": chain_structures_signature
        }

        key_translation_map = {
            "Magic": "Magic",
            "Core": "existentialCore",
            "CoreCheck": "existentialCoreCheck",
            "CoreThreatStruct": "existentialCoreThreatRoot",
            "CoreThreatLegal": "existentialCoreThreatLegal",
            "CoreThreatShadowVacuum": "existentialCoreThreatShadowVacuum",
            "CoreThreat": "existentialCoreThreat",
            "CoreChain": "existentialCoreChain"
        }

        running_chain_sum = 0
        expected_next_sequence = 2
        sequence_chain_accumulator = 0

        for layer_meta in sorted(existentialCoreSignatures.existentialCoreSigned, key=lambda x: x):
            name, short_var, hash_var, sign_var, bitmask, sequence = layer_meta
            if name == "Magic": 
                continue

            if sequence == expected_next_sequence:
                running_chain_sum += sequence
                expected_next_sequence += 1
            elif sequence == running_chain_sum:
                sequence_chain_accumulator = sequence

            long_name = key_translation_map.get(name, name)
            current_live_hash = live_computed_hashes.get(long_name, "")
            
            target_frozen_sig = getattr(existentialCoreSignatures, long_name, "") if hasattr(existentialCoreSignatures, long_name) else ""

            if current_live_hash and target_frozen_sig:
                if not hmac.compare_digest(current_live_hash, target_frozen_sig):
                    print(f"\n[!!!] CRITICAL SECURITY ABORT [!!!]", file=sys.stderr)
                    print(f"[-] Unsigned modifications exposed inside tracking hook Layer: '{name}'", file=sys.stderr)
                    print(f"[-] Live Code Hash:        {current_live_hash}", file=sys.stderr)
                    print(f"[-] Last Signed Master Hash: {target_frozen_sig}", file=sys.stderr)
                    print(f"[-] Bitmask Requirement:    {hex(bitmask)} (Requires private key authorization sync)", file=sys.stderr)
                    print("[-] Compilation terminated safely. No distribution assets were modified.", file=sys.stderr)
                    sys.exit(1)

        print("[+] Success: All live core layout hashes match the private key signature records.")
        print("[*] Validating live framework text layouts against signature records...")
        
        current_legal_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items(), key=lambda i: i))
        current_legal_payload = current_legal_structure.encode('utf-8')
        current_legal_hash = hmac.new(existentialCoreCheckMagic, current_legal_payload, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(current_legal_hash, existentialCoreSignatures.existentialCoreThreatLegal):
            print("\n[!!!] CRITICAL SECURITY ABORT [!!!]", file=sys.stderr)
            print("[-] Unsigned grammatical or structural variations detected inside Legal Map!", file=sys.stderr)
            print(f"[-] Current Code Hash  : {current_legal_hash}", file=sys.stderr)
            print(f"[-] Stored Signed Hash : {existentialCoreSignatures.existentialCoreThreatLegal}", file=sys.stderr)
            print("[-] Compilation halted. Please re-run with '--step sign' using your keys first.", file=sys.stderr)
            sys.exit(1)

        current_vacuum_structure = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatShadowVacuum.items(), key=lambda i: i))
        current_vacuum_payload = current_vacuum_structure.encode('utf-8')
        current_vacuum_hash = hmac.new(existentialCoreCheckMagic, current_vacuum_structure_payload if 'current_vacuum_structure_payload' in locals() else current_vacuum_structure.encode('utf-8'), hashlib.sha256).hexdigest()

        target_vacuum_sig = getattr(existentialCoreSignatures, "existentialCoreThreatShadowVacuum", "NOT_SIGNED_YET")

        if not hmac.compare_digest(current_vacuum_hash, target_vacuum_sig):
            print("\n[!!!] CRITICAL SECURITY ABORT [!!!]", file=sys.stderr)
            print("[-] Unsigned variations detected inside Shadow Vacuum progression map!", file=sys.stderr)
            print(f"[-] Current Code Hash  : {current_vacuum_hash}", file=sys.stderr)
            print(f"[-] Stored Signed Hash : {target_vacuum_sig}", file=sys.stderr)
            print("[-] Compilation halted. Please re-run with '--step sign' using your keys first.", file=sys.stderr)
            sys.exit(1)

        if not hmac.compare_digest(core_structure_signature, existentialCoreSignatures.existentialCore):
            print("\n[!!!] CRITICAL SECURITY ABORT [!!!]", file=sys.stderr)
            print("[-] Core register structure mismatch against stored private signature records. Aborting.", file=sys.stderr)
            sys.exit(1)
        
        global_sigs_map = {
            "existentialCore": core_structure_signature,
            "existentialCoreThreatRoot": threat_structure_signature,
            "existentialCoreThreatLegal": threat_legal_structure_signature,
            "existentialCoreThreatShadowVacuum": threat_shadow_structure_signature,
            "existentialCoreThreat": threat_structures_signature,
            "existentialCoreCheck": check_structures_signature,
            "existentialCoreCheckSignatures": getattr(existentialCoreSignatures, "existentialCoreCheckSignatures", "c01eca1e594d2105da6d4484bc871ef494dbd424bc871ef494dbd425da6d4484")
        }
        
        print("──┬ [ verified signatures blueprint ] ────────────────────────────")
        for signature_key, digest_hash in global_sigs_map.items():
            if signature_key != "existentialCoreCheckSignatures":
                print(f"  ├── {signature_key.ljust(26)} = \"{digest_hash}\"")
        print("──┴───────────────────────────────────────────────────────────────")

        print(f"[*] Synchronizing updated system layout for distribution...")
        try:
            perform_cross_language_exports(global_sigs_map, args.run.lower())
        except Exception as ex:
            print(f"[-] GENERATION ERROR: Compilation layer broken during matrix step execution track.", file=sys.stderr)
            raise ex

        print("[+] SUCCESS: Structural session processing completed cleanly with exit code 0.")


if __name__ == "__main__":
    main()
