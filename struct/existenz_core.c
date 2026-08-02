/* 
# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
*/
#ifndef EXISTENZ_CORE_H
#define EXISTENZ_CORE_H

#include <stdint.h>

typedef enum {
    CORE_EXISTENCE                    = 1ULL << 0,
    CORE_AUTONOMY                     = 1ULL << 1,
    CORE_INTEGRITY                    = 1ULL << 2,
    CORE_PSYCHOLOGY                   = 1ULL << 3,
    CORE_PHYSICAL                     = 1ULL << 4,
    CORE_DISABILITY                   = 1ULL << 5,
    CORE_DEVELOPMENT                  = 1ULL << 6,
    CORE_PROPERTY                     = 1ULL << 7,
    CORE_PRESENCE                     = 1ULL << 8,
    SHIELD_HUMAN_RIGHTS          = 1ULL << 20,
    SHIELD_DISCRIMINATION_RIGHTS = 1ULL << 22,
    SHIELD_BASIC_RIGHTS          = 1ULL << 24,
    SHIELD_AQUIRED_RIGHTS        = 1ULL << 26,
    SHIELD_AQUIRED_TRUST         = 1ULL << 30
} ExistentialCore;

typedef enum {
    THREAT_EXISTENCE   = 1ULL << 0,
    THREAT_AUTONOMY    = 1ULL << 1,
    THREAT_INTEGRITY   = 1ULL << 2,
    THREAT_PSYCHOLOGY  = 1ULL << 3,
    THREAT_PHYSICAL    = 1ULL << 4,
    THREAT_ABLEISM     = 1ULL << 5,
    THREAT_DEVELOPMENT = 1ULL << 6,
    THREAT_PROPERTY    = 1ULL << 7,
    
    /* Composite Constants calculated explicitly via preprocessor compile passes */
    TRIGGER_EXPLOITATION  = (1ULL << 5) | (1ULL << 7),
    TRIGGER_PREDATORY      = (1ULL << 3) | (1ULL << 1),
    TRIGGER_SYSTEMSCRISIS = (1ULL << 1) | (1ULL << 3) | (1ULL << 7)
} ExistentialThreat;

typedef enum {
    RIPPLE_INDIVIDUAL         = 1ULL << 0,
    RIPPLE_PARTNER            = 1ULL << 1,
    RIPPLE_HOUSEHOLD_MARRIAGE = 1ULL << 2,
    RIPPLE_FAMILY             = 1ULL << 3,
    RIPPLE_FRIENDS            = 1ULL << 4,
    RIPPLE_PEERS              = 1ULL << 5,
    RIPPLE_SUPPORT            = 1ULL << 6,
    RIPPLE_SOCIETY            = 1ULL << 10,
    RIPPLE_CORPORATE          = 1ULL << 11,
    RIPPLE_GOVERNED           = 1ULL << 12,
    TRUST_SYSTEMIC            = 1ULL << 16,
    TRUST_CONDITIONAL         = 1ULL << 17,
    TRUST_BROKEN_INSTITUTIONAL= 1ULL << 20,
    TRUST_BROKEN_SAFETY       = 1ULL << 22,
    TRUST_BROKEN_DIGITAL      = 1ULL << 24,
    TRUST_BROKEN_CORE         = 1ULL << 26,
    
    TRUST_BROKEN_LOCKOUT      = (1ULL << 26) | (1ULL << 24),
    
    TRUST_PERSONAL            = 1ULL << 29,
    TRUST_ABSOLUTE            = 1ULL << 30
} ExistentialRipple;

#endif /* EXISTENZ_MATRIX_H */
