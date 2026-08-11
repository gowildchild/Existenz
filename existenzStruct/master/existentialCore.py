# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76f
#
import hmac
import hashlib
from enum import IntFlag

class existentialCore(IntFlag):

    # THE LOWER 16-BITS:  IMMUTABLE   7 Human Pillars of existence!

    EXISTENCE               = 1 << 0    # 1     PILLAR  You, alive, with a body
    AUTONOMY                = 1 << 1    # 2     PILLAR  The Sovereign Right to Choose
    INTEGRITY               = 1 << 2    # 4     PILLAR  The Moral Axis of Personal Choice
    CANARY_1_SOVEREIGN      = 1 << 3    # 8     WATCHDOG
    PSYCHOLOGY              = 1 << 4    # 16    PILLAR  Cognitive Internal State and Mental Peace
    PHYSICAL                = 1 << 5    # 32    PILLAR  Physical Body Vessel and bio-state
    DISABILITY              = 1 << 6    # 64    PILLAR  Nature's way of checks and balances
    DEVELOPMENT             = 1 << 7    # 128   PILLAR  Evolutionary, Intellectual and Creative Growth
    PROPERTY                = 1 << 8    # 256   PILLAR  Material Assets and Income Protection
    CANARY_2_SOMATIC        = 1 << 9    # 512   WATCHDOG  WATCHDOG_SOMATIC
    PRESENCE                = 1 << 10   # 1024  PILLAR  Real-Time Spacetime Footprint
    CANARY_3_SYSTEMIC       = 1 << 13   # 8128  WATCHDOG  WATCHDOG_EVOLUTION
    CANARY_XV_STRUCT        = 1 << 15   # 32768 WATCHDOG  WATCHDOG_PILLARS
	
    # THE HIGHER 8-BITS:  IMMUTABLE   Legal SHIELDS by external defense factors

    CANARY_IV_PERSONAL      = 1 << 17   # 131072     CANARY  WATCHDOG_PERSONAL	
    SHIELD_RIGHTS_HUMAN     = 1 << 20   # 1048576    SHIELD-A  (Institutional)
    SHIELD_RIGHTS_INCLUSIVE = 1 << 22   # 4194304    SHIELD-A2 (Systemic)
    CANARY_V_RIGHTS         = 1 << 23   # 8388608    CANARY  WATCHDOG_RIGHTS
    SHIELD_RIGHTS_BASIC     = 1 << 24   # 16777216   SHIELD-B  (Institutional) 
    SHIELD_RIGHTS_ASYLUM    = 1 << 26   # 67108864   SHIELD-A3 (Institutional)
    CANARY_VI_CIVIC         = 1 << 27   # 134217728  CANARY  WATCHDOG_CIVILIAN
    SHIELD_IMMUTABLE_END    = 1 << 31   # 2147483648 END OF IMMUTABLE STRUCTURE

    # CANARIES FOR STRUCTURAL MANIPULATION

    CANARY_S_IMMUTABLE      = 0x80000401
    CANARY_S_STATE          = 0x055005f7
    CANARY_S_COLLIDE        = 0x8882a208
 
    # SIGNATURES FOR IMMUTABLE STRUCTURE, CORE STRUCTURE AND CHAINED SIGNATURE

    SIGN_CORE_EXISTENZ      = 0x5beba3df
    SIGN_CORE_IMMUTABLE     = 0x6d44968d
    SIGN_CORE_EXISTENTIAL   = 0x18641470
    SIGN_CORE_CANARY        = 0xc01eca1e
    SIGN_CORES_CHAINED	    = 0x48e65b5f
