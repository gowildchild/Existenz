# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
# Version: v0.76.15 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

package existentialCore;
our %existentialCore = (
    'EXISTENCE' => 1 << 0,                  # You, alive, with a body
    'AUTONOMY' => 1 << 1,                   # The Sovereign Right to Choose
    'INTEGRITY' => 1 << 2,                  # The Moral Axis of Personal Choice
    'CANARY_1_SOVEREIGN' => 1 << 3,         # WATCHDOG_SOVEREIGN
    'PSYCHOLOGY' => 1 << 4,                 # Cognitive Internal State and Mental Peace
    'PHYSICAL' => 1 << 5,                   # Physical Body Vessel and bio-state
    'DISABILITY' => 1 << 6,                 # Nature's way of checks and balances
    'DEVELOPMENT' => 1 << 7,                # Evolutionary, Intellectual and Creative Growth
    'PROPERTY' => 1 << 8,                   # Material Assets and Income Protection
    'CANARY_2_SOMATIC' => 1 << 9,           # WATCHDOG_SOMATIC
    'PRESENCE' => 1 << 10,                  # Real-Time Spacetime Footprint
    'CANARY_3_SYSTEMIC' => 1 << 13,         # WATCHDOG_EVOLUTION
    'CANARY_XV_STRUCT' => 1 << 15,          # WATCHDOG_PILLARS
    'CANARY_IV_PERSONAL' => 1 << 17,        # WATCHDOG_PERSONAL
    'SHIELD_RIGHTS_HUMAN' => 1 << 20,       # SHIELD-A (Institutional)
    'SHIELD_RIGHTS_INCLUSIVE' => 1 << 22,   # SHIELD-A2 (Systemic)
    'CANARY_V_RIGHTS' => 1 << 23,           # WATCHDOG_RIGHTS
    'SHIELD_RIGHTS_BASIC' => 1 << 24,       # SHIELD-B (Institutional)
    'SHIELD_RIGHTS_ASYLUM' => 1 << 26,      # SHIELD-A3 (Institutional)
    'CANARY_S_STATE' => 0x055005f7,         # 
    'CANARY_VI_CIVIC' => 1 << 27,           # WATCHDOG_CIVILIAN
    'SIGN_CORE_EXISTENTIAL' => 0x18641470,  # 
    'SIGN_CORE_EXISTENZ' => 0x5beba3df,     # 
    'SIGN_CORE_IMMUTABLE' => 0x6d44968d,    # 
    'SHIELD_IMMUTABLE_END' => 1 << 31,      # END OF IMMUTABLE STRUCTURE
    'CANARY_S_IMMUTABLE' => 0x80000401,     # 
    'CANARY_S_COLLIDE' => 0x8882a208,       # 
    'SIGN_CORE_CANARY' => 0xc01eca1e,       # 
);
1;
