# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.18 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

# ==========================================================================
# EXISTENZ CORE SIGNATURE CONTEXT
# ==========================================================================
CoreMagicRaw = "CoreRealm:CoreVersion:CoreMagic"
CoreMagicTag = "Existenz:v0.76.18:EX25IMMUT32CORE7617"

from enum import IntFlag

class existentialCoreThreat(IntFlag):
    THREAT_NONE                    = 0
    THREAT_EXISTENCE               = 1 << 0
    THREAT_AUTONOMY                = 1 << 1
    THREAT_INTEGRITY               = 1 << 2
    THREAT_PSYCHOLOGY              = 1 << 4
    THREAT_PHYSICAL                = 1 << 5
    THREAT_ABLEISM                 = 1 << 6
    THREAT_DEVELOPMENT             = 1 << 7
    THREAT_PROPERTY                = 1 << 8
    THREAT_PRESENCE                = 1 << 10
    THREAT_P_SAFE_OK               = 1 << 11
    THREAT_P_DURESS_OFF            = 1 << 12
    THREAT_USER_A                  = 1 << 14
    THREAT_USER_B                  = 1 << 15
    THREAT_USER_C                  = 1 << 16
    THREAT_RIGHTS_HUMAN            = 1 << 20
    THREAT_PRESENCE_SAFETY         = 1 << 21
    THREAT_RIGHTS_INCLUSIVE        = 1 << 22
    THREAT_RIGHTS_ASYLUM           = 1 << 23
    THREAT_RIGHTS_BASIC            = 1 << 24

existentialCoreThreatLegal = {
    existentialCoreThreat.THREAT_EXISTENCE: "LEGAL_CAT1_MURDER",
    existentialCoreThreat.THREAT_AUTONOMY: "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_INTEGRITY: "LEGAL_CAT3_COERCION",
    existentialCoreThreat.THREAT_PSYCHOLOGY: "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION",
    existentialCoreThreat.THREAT_PHYSICAL: "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_ABLEISM: "LEGAL_CAT6_ABLEISM",
    existentialCoreThreat.THREAT_DEVELOPMENT: "LEGAL_CAT8_INTELLECTUAL_PIRACY",
    existentialCoreThreat.THREAT_PROPERTY: "LEGAL_CAT9_THEFT",
    existentialCoreThreat.THREAT_RIGHTS_HUMAN: "LEGAL_CAN3_HUMAN",
    existentialCoreThreat.THREAT_RIGHTS_INCLUSIVE: "LEGAL_CAN4_INCLUSION",
}

existentialCoreThreatShadowVacuum = {
    existentialCoreThreat.THREAT_EXISTENCE: "VACUUM_DEHUMANISATION",
    existentialCoreThreat.THREAT_AUTONOMY: "VACUUM_DISFRANCHISEMENT",
    existentialCoreThreat.THREAT_INTEGRITY: "VACUUM_CORRUPTION",
    existentialCoreThreat.THREAT_PSYCHOLOGY: "VACUUM_ATTRITION_PSYCHOLOGY",
    existentialCoreThreat.THREAT_PHYSICAL: "VACUUM_SOMATIC_DRAIN",
    existentialCoreThreat.THREAT_ABLEISM: "VACUUM_NEURONORMATIVITY",
    existentialCoreThreat.THREAT_DEVELOPMENT: "VACUUM_ATTRITION_INSTITUTIONAL",
    existentialCoreThreat.THREAT_PROPERTY: "VACUUM_SYSTEMIC_DESPOILMENT",
    existentialCoreThreat.THREAT_PRESENCE: "VACUUM_PANOPTICISM",
    existentialCoreThreat.THREAT_RIGHTS_HUMAN: "VACUUM_INVERT_COMPLIANCE",
    existentialCoreThreat.THREAT_RIGHTS_INCLUSIVE: "VACUUM_INVERT_NORMALIZATION",
    existentialCoreThreat.THREAT_RIGHTS_BASIC: "VACUUM_INVERT_INERTIA",
}
