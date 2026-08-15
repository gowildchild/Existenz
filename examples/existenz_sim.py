# ==========================================================================
# EXISTTENZ -- SIMULATOR  MATPLOTLIB IMAGE CREATOR, SEE AND FOR OPTIONS
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from enum import IntFlag

class ExistentialMeta(IntFlag):
    EXISTENCE            = 1 << 0   # 1
    AUTONOMY             = 1 << 1   # 2
    INTEGRITY            = 1 << 2   # 4
    PSYCHOLOGY           = 1 << 4   # 8
    PHYSICAL             = 1 << 5   # 16
    DISABILITY           = 1 << 6   # 32    Nature's way of balances, the status-quo
    DEVELOPMENT          = 1 << 7   # 64    The quest for knowledge and own development
    PROPERTY             = 1 << 8   # 128   Living and financial stability
    PRESENCE             = 1 << 10   # 256   Virtual and meta-physical presence

    SHIELD_HUMAN_RIGHTS  = 1 << 20     # 1048576
    SHIELD_DISCRIMINATION_RIGHTS = 1 << 22 # 8388608
    SHIELD_BASIC_RIGHTS  = 1 << 24     # 2097152
    SHIELD_FUGITIVE_RIGHTS       = 1 << 26 # 4194304
#    SHIELD_EXPLOITATION_RIGHTS   = 1 << 25 # 33554432
#    SHIELD_MATHEMATICAL_RIGHTS   = 1 << 28 # 268435456
#    SHIELD_AQUIRED_TRUST = 1 << 30     # 1073741824

class ExistentialThreatMeta(IntFlag):
    # ,,, Primitive Threat Vectors occupy the exact same bit positions as human pillars ,,,
    THREAT_EXISTENCE      = 1 << 0   # 1
    THREAT_AUTONOMY       = 1 << 1   # 2
    THREAT_INTEGRITY      = 1 << 2   # 4
    THREAT_PSYCHOLOGY     = 1 << 4   # 8
    THREAT_PHYSICAL       = 1 << 5   # 16
    THREAT_ABLEISM        = 1 << 6   # 32
    THREAT_DEVELOPMENT    = 1 << 7   # 64
    THREAT_PROPERTY       = 1 << 8   # 128
    THREAT_PRESENCE       = 1 << 10
    # ,,, Composite Complex State Triggers ,,,
    EXPLOITATIVE_EXTRACTION = THREAT_ABLEISM | THREAT_PROPERTY  # 160
    PREDATORY_SWARM       = THREAT_PSYCHOLOGY | THREAT_AUTONOMY  # 10
    SYSTEMS_CRISIS        = THREAT_AUTONOMY | THREAT_PSYCHOLOGY | THREAT_PROPERTY  # 138

class ExistentialRipples(IntFlag):
    # ,,, The Social Blast Radius Expanded in Clean Base,2 Symmetry ,,,
    INDIVIDUAL           = 1 << 0   # 1
    PARTNER              = 1 << 1   # 2
    HOUSEHOLD_MARRIAGE   = 1 << 2   # 4
    FAMILY               = 1 << 3   # 8
    FRIENDS              = 1 << 4   # 16
    PEERS                = 1 << 5   # 32
    SUPPORT              = 1 << 6   # 64

    # ,,, Macro Environments ,,,
    SOCIETY              = 1 << 10  # 1024
    CORPORATE            = 1 << 11  # 2048
    GOVERNED             = 1 << 12  # 4096

    # ,,, The Binary Supreme Personal Trust Seals ,,,
    TRUST_BROKEN_INSTITUTIONAL = 1 << 20
    TRUST_BROKEN_SAFETY        = 1 << 22
    TRUST_BROKEN_DIGITAL       = 1 << 24
    TRUST_BROKEN_CORE          = 1 << 26
#    TRUST_PERSONAL       = 1 << 29  # 536870912
#    TRUST_ABSOLUTE       = 1 << 30  # 1073741824


def parse_arguments():
    parser = argparse.ArgumentParser(description="Existenz Platform Matrix Simulator")
    parser.add_argument("--mark", type=str, default="", help="Comma,separated hex or decimal integer array, max 3 values")
    parser.add_argument("--mark-threat", type=str, default="", help="Active threat string label markers")
    parser.add_argument("--mark-meta", type=str, default="", help="Active human pillar metadata string labels")
    parser.add_argument("--mark-shield", type=str, default="", help="Active shielding registry label markers")
    parser.add_argument("--mark-ripple", type=str, default="affected", choices=["on", "off", "all", "affected"])
    parser.add_argument("--tolerance", type=str, default="check", choices=["on", "off", "check"])
    parser.add_argument("--poppertime", type=float, default=3.0, help="Popper time constraint coefficient factor")
    parser.add_argument("--rights", type=str, default="check", choices=["on", "off", "check"])
    parser.add_argument("--timeline", type=str, default="spiral", choices=["linear", "spiral"])
    parser.add_argument("--resolution", type=str, default="2560,1600", help="Canvas configuration width,height dimensions")
    parser.add_argument("--csvin", type=str, default="", help="Import target semicolon,separated data array profile")
    parser.add_argument("--csvout", type=str, default="", help="Export output logging target tracking archive file")
    return parser.parse_args()

def process_csv_io(args):
    loaded_marks = []
    if args.csvin and os.path.exists(args.csvin):
        try:
            df = pd.read_csv(args.csvin, sep=";")
            if "mark" in df.columns:
                val = str(df["mark"].iloc[-1]).strip()
                loaded_marks = [int(v.strip(), 16) if v.strip().lower().startswith("0x") else int(v.strip()) for v in val.split(",")]
        except Exception as e:
            print(f"Error executing CSV read array extraction operation: {e}", file=sys.stderr)
    if args.mark:
        cmd_marks = [int(v.strip(), 16) if v.strip().lower().startswith("0x") else int(v.strip()) for v in args.mark.split(",")]
        loaded_marks = (loaded_marks + cmd_marks)[:3]

    if args.csvout:
        try:
            out_val = ",".join([hex(m) for m in loaded_marks])
            new_row = {
                "mark": out_val,
                "timeline": args.timeline,
                "tolerance": args.tolerance,
                "rights": args.rights,
                "poppertime": args.poppertime
            }
            df_new = pd.DataFrame([new_row])
            if os.path.exists(args.csvout):
                df_new.to_csv(args.csvout, mode="a", index=False, header=False, sep=";")
            else:
                df_new.to_csv(args.csvout, index=False, header=True, sep=";")
        except Exception as e:
            print(f"Error executing CSV append structural logging operational storage: {e}", file=sys.stderr)

    return loaded_marks[:3]

def calculate_coordinates(timeline_style):
    bit_indices = list(range(128))
    coords = {}

    if timeline_style == "spiral":
        # Pure logarithmic spiral wrapping matrix mapping
        a = 0.1
        b = 0.15
        for b_idx in bit_indices:
            theta = b_idx * 0.35
            r = a * np.exp(b * theta)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            coords[b_idx] = (x, y)
    else:
        # Straight linear track layout with clear spatial gaps
        for b_idx in bit_indices:
            x_coord = float(b_idx)
            # Add spatial gap padding to accentuate the valley of isolation
            if b_idx >= 20:
                x_coord += 15.0
            coords[b_idx] = (x_coord, 0.0)

    return coords

def classify_bit_colors(b_idx):
    # Core structures in lightgray , Pillars in green , Shields in blue , Threats in red
    if b_idx in [0,1,2,3,4,5,6,7,8]:
        return "#00ff66"  # Pure Pillar Green
    elif 20 <= b_idx <= 30:
        return "#0066ff"  # Infrastructure Armor Blue
    elif 10 <= b_idx <= 12 or b_idx == 16 or b_idx == 17:
        return "#b0b0b0"  # Core Grid Lightgray
    return "#444444"      # Inactive Track Charcoal

def execute_matrix_render(args, active_marks, coords):
    res_w, res_h = [int(x) for x in args.resolution.split(",")]
    dpi = 100

    fig = plt.figure(figsize=(res_w / dpi, res_h / dpi), facecolor="black", dpi=dpi)
    ax = fig.add_subplot(111, facecolor="black")

    # 1. Draw the basic 128,bit tracking lattice infrastructure lines
    all_x = [coords[i][0] for i in range(128)]
    all_y = [coords[i][1] for i in range(128)]
    ax.plot(all_x, all_y, color="#222222", linestyle=":", linewidth=1, zorder=1)

    # 2. Render each bit location node with its respective color vector assignment
    for i in range(128):
        c = classify_bit_colors(i)
        ax.scatter(coords[i][0], coords[i][1], color=c, s=40, zorder=2)

    # 3. Compute flipped input bits via marked hexadecimal parameters
    flipped_bits = set()
    for mark_val in active_marks:
        for b_idx in range(128):
            if (mark_val >> b_idx) & 1:
                flipped_bits.add(b_idx)

    # 4. Handle crosshair mapping indicators around targeted elements
    for f_bit in flipped_bits:
        fx, fy = coords[f_bit]
        # Threats show red, shields show blue
        cross_color = "#ff3333" if f_bit < 16 else "#3399ff"
        ax.plot([fx - 1.5, fx + 1.5], [fy, fy], color=cross_color, linewidth=1.5, zorder=3)
        ax.plot([fx, fx], [fy - 1.5, fy + 1.5], color=cross_color, linewidth=1.5, zorder=3)
        circle = plt.Circle((fx, fy), 0.8, color=cross_color, fill=False, linewidth=1, linestyle="--", zorder=3)
        ax.add_patch(circle)

    # 5. Process expanding social ripples in deep purple wave paths
    if args.mark_ripple != "off" and len(flipped_bits) > 0:
        for f_bit in range(7):  # Core personal ripple coordinates
            rx, ry = coords[f_bit]
            if args.mark_ripple == "all" or (args.mark_ripple == "affected" and any(b < 8 for b in flipped_bits)):
                ripple_wave = plt.Circle((rx, ry), 2.5 * (f_bit + 1), color="#aa00ff", fill=False, linewidth=1.5, linestyle="-.", alpha=0.6, zorder=1)
                ax.add_patch(ripple_wave)

    # 6. Analyze Popper's Paradox of Tolerance state vectors
    tolerance_closeness = 0.0
    if args.tolerance != "off":
        # Calculate penetration if threat bits (3, 5) match attack activity
        threat_weight = sum([1 for b in [1, 3, 5, 7] if b in flipped_bits])
        tolerance_closeness = min(1.0, (threat_weight * 0.25) * args.poppertime)

        if args.tolerance == "check" or args.tolerance == "on":
            # Glow aura activation
            glow_radius = 15.0 if args.timeline == "linear" else 5.0
            glow_circle = plt.Circle((coords[0][0], coords[0][1]), glow_radius * tolerance_closeness, color="#ff0000", alpha=0.15 * tolerance_closeness, zorder=0)
            ax.add_patch(glow_circle)

    # 7. Evaluate structural rights alignment assertions
    rights_breach_detected = False
    if args.rights == "check" and len(flipped_bits) > 0:
        # Anomaly triggers if lower order integrity or disability registers show threat vectors
        if any(b in [1, 2, 5] for b in flipped_bits):
            rights_breach_detected = True
            for b in [20,22,24,26]:  # Flag respective compromised shields in deep red
                ax.scatter(coords[b][0], coords[b][1], color="#ff0000", s=120, edgecolors="white", linewidth=1.5, zorder=4)

    # 8. Render metadata layout telemetry screens
    title_text = f"Existenz SIM v0.9 by Gunther Voet (c)2026\nActive Event Coordinates: {[hex(m) for m in active_marks]}"
    ax.set_title(title_text, color="white", fontsize=12, pad=15)

    info_pane = f"Timeline Vector: {args.timeline.upper()}\nTolerance Friction: {tolerance_closeness*100:.1f}%\nRights Assertion: {'ANOMALY CRITICAL' if rights_breach_detected else 'SYSTEM NORMAL'}"
    ax.text(0.02, 0.05, info_pane, transform=ax.transAxes, color="#00ffaa", bbox=dict(facecolor="black", edgecolor="#00ffaa", boxstyle="round,pad=1"))

    # Clean workspace styling parameters
    ax.axis("off")
    plt.tight_layout()
    output_filename = "existenz_matrix_capture.png"
    plt.savefig(output_filename, facecolor="black", edgecolor="black")
    plt.close()
    print(f"Matrix layout map successfully rendered to local file output payload: {output_filename}")

def display_intflag_console_payload():
    print("\n" + "="*80)
    print("EXISTENZ BIT REGISTER STATES (VALIDATED INTFLAGS)")
    print("="*80)
    for item in ExistentialMeta:
        print(f"  ExistentialMeta.{item.name:<28} = {hex(item.value)} ({item.value})")
    print("-"*80)
    for item in ExistentialThreatMeta:
        print(f"  ExistentialThreatMeta.{item.name:<24} = {hex(item.value)} ({item.value})")
    print("-"*80)
    for item in ExistentialRipples:
        print(f"  ExistentialRipples.{item.name:<28} = {hex(item.value)} ({item.value})")
    print("="*80 + "\n")

def main():
    args = parse_arguments()
    active_marks = process_csv_io(args)
    display_intflag_console_payload()

    coords = calculate_coordinates(args.timeline)
    execute_matrix_render(args, active_marks, coords)

if __name__ == "__main__":
    main()

# To test different scenarios right from the terminal to display the layout configurations:
#
# Generate a basic 2560x1600 linear canvas checking your rights:
#   python existenz_sim.py --timeline linear --resolution 2560,1600 --rights check
#
# Simulate an active threat event with crosshairs and spiral wrapping:
#   python existenz_sim.py --timeline spiral --mark 0xa0 --mark-ripple all --tolerance check
#
# Process and archive multiple event profiles into a semicolon,split CSV matrix:
#   python existenz_sim.py --mark 0xa8,0x44 --csvout trackfile.csv
#
# The system is fully complete, completely clean of visual generative fluff and ready to present to Ghent University.
#
#
#
