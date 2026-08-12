#!/usr/bin/env python3
# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED MULTI-GATE UNIT TEST)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: struct/existentialCoreTest.py
#
import sys
import os

# Ensure the parent / local directory is in the lookup path for clean imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

try:
    # We step in directly using your short package interface entry point
    from struct.existentialCores import (
        existentialCore,
        existentialCoreThreat,
        existentialCoreCheck,
        PLATFORM_VERSION
    )
except ImportError as e:
    print(f"[-] Architecture Import Failure: {e}")
    sys.exit(1)


def run_architecture_suite():
    print(f"==================================================================")
    print(f"[*] RUNNING EXISTENZ CORE TEST [{PLATFORM_VERSION}]")
    print(f"==================================================================")
    
    tests_passed = 0
    total_tests = 5

    # ----------------------------------------------------------------------
    # TEST 1: Absolute File-Global Static Environment Validation
    # ----------------------------------------------------------------------
    print("[*] Test 1: Verifying File-Global Map and Structure Integrity Seals...")
    try:
        assert existentialCoreCheck.check_integrity_legal() == True, "Legal map signature mismatch!"
        print("  [+] Passed: Threat Legal translation tables match cold-compiled HMAC signatures.")
        tests_passed += 1
    except AssertionError as msg:
        print(f"  [-] Failed: {msg}")

    # ----------------------------------------------------------------------
    # TEST 2: Pristine Rest State Environment Assurance
    # ----------------------------------------------------------------------
    print("[*] Test 2: Asserting Pristine Baseline Environmental Sanctuary...")
    try:
        pristine_register = existentialCore.CANARY_S_STATE
        assert existentialCoreCheck.check_integrity(pristine_register) == True, "Pristine state broken!"
        print("  [+] Passed: Clean state satisfies multi-gate firewalls and XOR checkbits.")
        tests_passed += 1
    except AssertionError as msg:
        print(f"  [-] Failed: {msg}")

    # ----------------------------------------------------------------------
    # TEST 3: Active-High NAND Canary Vulnerability Trap Evaluation
    # ----------------------------------------------------------------------
    print("[*] Test 3: Testing NAND Watchdog Tripwires on Simulated Core Puncture...")
    try:
        # Simulate a hostile event: Drop INTEGRITY (Bit 2) from 1 down to 0
        compromised_state = existentialCore.CANARY_S_STATE & ~existentialCore.INTEGRITY
        
        # Pass the damaged state into the mutator to calculate expected alerts
        recalculated_state = existentialCoreCheck.check_integrity_core(compromised_state)
        
        # Verify that CANARY_1_SOVEREIGN (Bit 3) was successfully injected into the matrix
        assert (recalculated_state & existentialCore.CANARY_1_SOVEREIGN) != 0, "Sovereign Watchdog failed to trip!"
        print("  [+] Passed: NAND gate successfully trapped local attribute suppression.")
        tests_passed += 1
    except AssertionError as msg:
        print(f"  [-] Failed: {msg}")

    # ----------------------------------------------------------------------
    # TEST 4: Dead-Man's Void State Trigger Logic
    # ----------------------------------------------------------------------
    print("[*] Test 4: Testing Dead-Man's Switch Logic on Forced Memory Wiping...")
    try:
        # Simulate a severe attack: Zero out the entire lower 16-bit register tracking plane
        wiped_state = 0x00000000
        
        # The mutator must look into the void, realize EXISTENCE is missing, and activate flags
        recalculated_state = existentialCoreCheck.check_integrity_core(wiped_state)
        
        assert (recalculated_state & existentialCore.CANARY_1_SOVEREIGN) != 0, "Void trap failed!"
        print("  [+] Passed: Dead-Man's switch successfully fired on total memory erasure (0+0=1).")
        tests_passed += 1
    except AssertionError as msg:
        print(f"  [-] Failed: {msg}")

    # ----------------------------------------------------------------------
    # TEST 5: Collision Gate Banishment Check
    # ----------------------------------------------------------------------
    print("[*] Test 5: Testing Collision Mask Defenses Against Malicious Bit Spills...")
    try:
        # Inject noise directly into forbidden boundary zones covered by CANARY_S_COLLIDE
        tainted_state = existentialCore.CANARY_S_STATE | (1 << 31)
        
        # The master firewall must intercept this immediately at Gate 1
        assert existentialCoreCheck.check_integrity(tainted_state) == False, "Collision went undetected!"
        print("  [+] Passed: Master sentinel instantly blacklisted forbidden memory boundary overlap.")
        tests_passed += 1
    except AssertionError as msg:
        print(f"  [-] Failed: {msg}")

    # ----------------------------------------------------------------------
    # FINAL METRIC EVALUATION SUMMARY
    # ----------------------------------------------------------------------
    print(f"==================================================================")
    print(f"[+] AUDIT COMPLETE: Passed {tests_passed} of {total_tests} structural tests.")
    print(f"==================================================================")
    
    if tests_passed == total_tests:
        print("[+] PLATFORM STATUS: SECURE. All systems match Existenz parameters.")
        return True
    else:
        print("[-] PLATFORM STATUS: COMPROMISED. Do not build release distributions.")
        return False


if __name__ == "__main__":
    success = run_architecture_suite()
    sys.exit(0 if success else 1)
