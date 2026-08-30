# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
# Version: v0.76.15 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

class existentialCoreThreat:
    THREAT_NONE = 0                        # 
    THREAT_EXISTENCE = 1 << 0              # 
    THREAT_AUTONOMY = 1 << 1               # 
    THREAT_INTEGRITY = 1 << 2              # 
    CANARY_1_SOVEREIGN = 1 << 3            # WATCHDOG_SOVEREIGN
    THREAT_PSYCHOLOGY = 1 << 4             # 
    THREAT_PHYSICAL = 1 << 5               # 
    THREAT_ABLEISM = 1 << 6                # 
    THREAT_DEVELOPMENT = 1 << 7            # 
    THREAT_PROPERTY = 1 << 8               # 
    CANARY_2_SOMATIC = 1 << 9              # WATCHDOG_SOMATIC
    THREAT_PRESENCE = 1 << 10              # 
    CANARY_3_SYSTEMIC = 1 << 13            # WATCHDOG_EVOLUTION
    CANARY_4_PERSONAL = 1 << 17            # 
    THREAT_RIGHTS_HUMAN = 1 << 20          # 
    THREAT_RIGHTS_INCLUSIVE = 1 << 22      # 
    CANARY_5_RIGHTS = 1 << 23              # 
    THREAT_RIGHTS_BASIC = 1 << 24          # 
    THREAT_RIGHTS_ASYLUM = 1 << 26         # 
    CANARY_7_EXPLOITATION = 0x055005f7     # 
    CANARY_6_CIVIC = 1 << 27               # 
    SIGN_THREAT_EXISTENTIAL = 0x18641470   # 
    SIGN_THREAT_EXISTENZ = 0x5beba3df      # 
    SIGN_THREAT_RIGHTS_LEGAL = 0x6d07d972  # 
    SIGN_THREAT_IMMUTABLE = 0x6d44968d     # 
    THREAT_IMMUTABLE_END = 1 << 31         # 
    CANARY_8_PREDATORY = 0x8882a608        # 
    SIGN_THREAT_CANARY = 0xc01eca1e        # 

    existentialCoreThreatLegal = {
        1: "LEGAL_CAT1_MURDER",
        2: "LEGAL_CAT2_PHYSICAL_VIOLATION",
        4: "LEGAL_CAT3_COERCION",
        8: "LEGAL_CAT4_CHARACTER_ASSASSINATION",
        16: "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION",
        32: "LEGAL_CAT2_PHYSICAL_VIOLATION",
        64: "LEGAL_CAT6_ABLEISM",
        128: "LEGAL_CAT8_INTELLECTUAL_PIRACY",
        256: "LEGAL_CAT9_THEFT",
        8192: "LEGAL_CAN1_SYSTEMCRISIS",
        1048576: "LEGAL_CAN3_HUMAN",
        4194304: "LEGAL_CAN4_INCLUSION",
        89130487: "LEGAL_CAN2_EXPLOITATION",
        2290263560: "LEGAL_CAN5_PREDATORY"
    }

    existentialCoreThreatShadowVacuum = {
        1: "VACUUM_DEHUMANISATION",
        2: "VACUUM_DISFRANCHISEMENT",
        4: "VACUUM_CORRUPTION",
        8: "VACUUM_DRIFT_SOVEREIGN",
        16: "VACUUM_ATTRITION_PSYCHOLOGY",
        32: "VACUUM_SOMATIC_DRAIN",
        64: "VACUUM_NEURONORMATIVITY",
        128: "VACUUM_ATTRITION_INSTITUTIONAL",
        256: "VACUUM_SYSTEMIC_DESPOILMENT",
        512: "VACUUM_DRIFT_SOMATIC",
        1024: "VACUUM_PANOPTICISM",
        8192: "VACUUM_DRIFT_SYSTEMIC",
        1048576: "VACUUM_INVERT_COMPLIANCE",
        4194304: "VACUUM_INVERT_NORMALIZATION",
        16777216: "VACUUM_INVERT_INERTIA",
        89130487: "VACUUM_PARASITISM",
        2290263560: "VACUUM_HARVESTING"
    }
