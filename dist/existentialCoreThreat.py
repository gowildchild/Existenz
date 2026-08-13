# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76g
#
from enum import IntFlag
class existentialCoreThreat(IntFlag):
    """
    1:1 Symmetrical Mirror of ExistentialCore.
    Defines immediate critical attacks and their corresponding system watchdogs.
    """
    THREAT_NONE             = 0
    THREAT_EXISTENCE        = 1 << 0
    THREAT_AUTONOMY         = 1 << 1
    THREAT_INTEGRITY        = 1 << 2
    THREAT_PSYCHOLOGY       = 1 << 4
    THREAT_PHYSICAL         = 1 << 5
    THREAT_ABLEISM          = 1 << 6
    THREAT_DEVELOPMENT      = 1 << 7
    THREAT_PROPERTY         = 1 << 8
    THREAT_PRESENCE         = 1 << 10

    THREAT_RIGHTS_HUMAN     = 1 << 20
    THREAT_RIGHTS_INCLUSIVE = 1 << 22
    THREAT_RIGHTS_BASIC     = 1 << 24
    THREAT_RIGHTS_ASYLUM    = 1 << 26
    THREAT_IMMUTABLE_END    = 1 << 31

    CANARY_1_SOVEREIGN      = 1 << 3
    CANARY_2_SOMATIC        = 1 << 9
    CANARY_3_SYSTEMIC       = 1 << 13
    CANARY_4_PERSONAL       = 1 << 17
    CANARY_5_RIGHTS         = 1 << 23
    CANARY_6_CIVIC          = 1 << 27

    SIGN_THREAT_RIGHTS_LEGAL = 0x6d07d972
    SIGN_THREAT_EXISTENZ     = 0x5beba3df
    SIGN_THREAT_IMMUTABLE    = 0x6d44968d
    SIGN_THREAT_EXISTENTIAL  = 0x18641470
    SIGN_THREAT_CANARY       = 0xc01eca1e

existentialCoreThreatLegal = {
    existentialCoreThreat.THREAT_EXISTENCE:        "LEGAL_CAT1_MURDER",
    existentialCoreThreat.THREAT_AUTONOMY:         "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_INTEGRITY:        "LEGAL_CAT3_COERSION",
    existentialCoreThreat.CANARY_1_SOVEREIGN:      "LEGAL_CAT4_CHARACTER_ASSASINATION",
    existentialCoreThreat.THREAT_PSYCHOLOGY:       "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION",
    existentialCoreThreat.THREAT_PHYSICAL:         "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_ABLEISM:          "LEGAL_CAT6_ABLEISM",
    existentialCoreThreat.THREAT_DEVELOPMENT:      "LEGAL_CAT8_INTELLECTUAL_PIRACY",
    existentialCoreThreat.THREAT_PROPERTY:         "LEGAL_CAT9_THEFTH",
    existentialCoreThreat.CANARY_3_SYSTEMIC:       "LEGAL_CAN1_SYSTEMCRISIS",
    1 << 14:                                       "LEGAL_CAN2_EXPLOITATION",
    existentialCoreThreat.THREAT_RIGHTS_HUMAN:     "LEGAL_CAN3_HUMAN",
    existentialCoreThreat.THREAT_RIGHTS_INCLUSIVE: "LEGAL_CAN4_INCLUSION",
    1 << 40:                                       "LEGAL_CAN5_PREDATORY"
}


# ==========================================================================
# UNIVERSAL CRYPTOGRAPHIC BOUNDARY VAULT (CONSOLIDATED STRUCTURE)
# ==========================================================================
class existentialCoreThreatSignatures:
    """Consolidated hardware-salted cryptographic locks for the threat ecosystem."""
    existentialCoreThreatSign                = 0x57c413f8
    existentialCoreThreatSignature           = "57c413f8531731df0d2f09a260ea36c7e49269348b553fdeeaa2dd11e7bc4bb9"
    existentialCoreThreatLegalSign           = 0x6d07d972
    existentialCoreThreatLegalSignature      = "6d07d97272d414f966ea7a9d7b2956b96541fecbcb9079f375408a62b3b6bd6e"
    existentialCoreThreatStructuresSign      = 0x759533df
    existentialCoreThreatStructuresSignature = "759533dfd2a276046bc62985b17df7cefb999a1c3a07b7b983e5ee278d80302d"


