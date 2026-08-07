# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76a
#
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
    CANARY_2_SOMATIC        = 1 << 9    # 512   CANARY  WATCHDOG_SOMATIC
    PRESENCE                = 1 << 10   # 1024  PILLAR  Real-Time Spacetime Footprint
    CANARY_3_SYSTEMIC       = 1 << 13   # 8128  CANARY  WATCHDOG_EVOLUTION

    # THE HIGHER 8-BITS:  IMMUTABLE   Legal SHIELDS by external defense factors

    CANARY_4_PERSONAL       = 1 << 17   # 131072     CANARY  WATCHDOG_PERSONAL	
    SHIELD_RIGHTS_HUMAN     = 1 << 20   # 1048576    SHIELD-A  (Institutional)
    SHIELD_RIGHTS_INCLUSIVE = 1 << 22   # 4194304    SHIELD-A2 (Systemic)
    CANARY_5_RIGHTS         = 1 << 23   # 8388608    CANARY  WATCHDOG_RIGHTS
    SHIELD_RIGHTS_BASIC     = 1 << 24   # 16777216   SHIELD-B  (Institutional) 
    SHIELD_RIGHTS_ASYLUM    = 1 << 26   # 67108864   SHIELD-A3 (Institutional)
    CANARY_6_CIVIC          = 1 << 27   # 134217728  CANARY  WATCHDOG_CIVILIAN
    SHIELD_IMMUTABLE_END    = 1 << 31   # 2147483648 END OF IMMUTABLE STRUCTURE

    # CANARIES FOR STRUCTURAL MANIPULATION

    CANARY_S_IMMUTABLE      = 0x80000401
    CANARY_S_STATE          = 0x455005F7
    CANARY_S_COLLIDE        = 0x88822208
 
    # SIGNATURES FOR IMMUTABLE STRUCTURE, CORE STRUCTURE AND CHAINED SIGNATURE

    SIGN_CORE_EXISTENZ      = 0x5beba3df
    SIGN_CORE_IMMUTABLE     = 0x6d44968d
    SIGN_CORE_EXISTENTIAL   = 0x18641470
    SIGN_CORES_CHAINED	    = 0xa62b1b36

    @classmethod
    def canary_integrity(cls, active_register_state: int) -> bool:
        """
        Instantaneous single-cycle check. Returns True if completely untampered.
        Fails (False) if any data spills into the forbidden watchdog gates.
        """
	      sign_existenz        = "5beba3df48dfcb7cf800c14fba00a297e594d2105da6d4484bc871ef494dbd42"
	      sign_immutable       = "18641470fa93489814467d58fa05ef44c35c3b99912788e0b67277d33d9691b0"
	      sign_structure       = "6d44968d7d1d9d85546928e57d9924f7ab5cf0682bfd7e1d7de690e086347438"
	      sign_corechain       = "a62b1b3636f328f413d78964724838da1cf464972e27301048ca0ef3df503cd2" 
        return (active_register_state & cls.CANARY_S_COLLIDE) == 0

    @classmethod
    def canary_pristine(cls, active_register_state: int) -> bool:
        """
        Compares the operational registry directly against the ideal system vector.
        """
        return active_register_state == cls.CANARY_S_STATE
