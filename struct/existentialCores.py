# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76c
#
import hmac
import hashlib
from enum import IntFlag

PLATFORM_VERSION         = "v0.76c"
PLATFORM_ANCHOR_KEY      = b"EX25IMMUT32CORE7617"
SIGNATURE_CORE_EXISTENZ  = "5beba3df6d44968d18641470c01eca1eca3e7ec2"

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
    SIGN_CORES_CHAINED	    = 0xaa12b934
   
    @classmethod
    def check_integrity_core(cls, active_register_state: int) -> int:
        """
        Active State Modifier (Mutator). Applies NAND logic to active pairs.
        Returns the updated register state tracking integer.
        """
        has_existence   = bool(active_register_state & cls.EXISTENCE)
        has_autonomy    = bool(active_register_state & cls.AUTONOMY)
        has_integrity   = bool(active_register_state & cls.INTEGRITY)
        has_psychology  = bool(active_register_state & cls.PSYCHOLOGY)
        has_physical    = bool(active_register_state & cls.PHYSICAL)
        has_development = bool(active_register_state & cls.DEVELOPMENT)
        has_property    = bool(active_register_state & cls.PROPERTY)

        cleared_mask = ~(cls.CANARY_1_SOVEREIGN | cls.CANARY_2_SOMATIC | cls.CANARY_3_SYSTEMIC | cls.CANARY_XV_STRUCT)
        evaluated_state = active_register_state & cleared_mask

        if not (has_autonomy and has_integrity):
            evaluated_state |= cls.CANARY_1_SOVEREIGN
        if not (has_psychology and has_physical):
            evaluated_state |= cls.CANARY_2_SOMATIC
        if not (has_development and has_property):
            evaluated_state |= cls.CANARY_3_SYSTEMIC
        if not has_existence:
            evaluated_state |= cls.CANARY_1_SOVEREIGN

        running_parity = 0
        for bit_index in range(15):
            if evaluated_state & (1 << bit_index):
                running_parity ^= 1

        if running_parity == 1:
            evaluated_state |= cls.CANARY_XV_STRUCT

        return evaluated_state

    @classmethod
    def check_integrity_pillars(cls, active_register_state: int) -> bool:
        """
        State Validator (Inspector). Zero-loop, constant-time validation using 0x5F7.
        """
        raw_pillars = active_register_state & (cls.CANARY_S_STATE & 0x0FFF)
        has_existence   = bool(raw_pillars & cls.EXISTENCE)
        has_autonomy    = bool(raw_pillars & cls.AUTONOMY)
        has_integrity   = bool(raw_pillars & cls.INTEGRITY)
        has_psychology  = bool(raw_pillars & cls.PSYCHOLOGY)
        has_physical    = bool(raw_pillars & cls.PHYSICAL)
        has_development = bool(raw_pillars & cls.DEVELOPMENT)
        has_property    = bool(raw_pillars & cls.PROPERTY)

        expected_canary_1 = (not (has_autonomy and has_integrity) or not has_existence) << 3
        expected_canary_2 = (not (has_psychology and has_physical)) << 9
        expected_canary_3 = (not (has_development and has_property)) << 13

        expected_canaries_vector = expected_canary_1 | expected_canary_2 | expected_canary_3
        claimed_canaries_vector = active_register_state & (cls.CANARY_1_SOVEREIGN | cls.CANARY_2_SOMATIC | cls.CANARY_3_SYSTEMIC)

        if claimed_canaries_vector != expected_canaries_vector:
            return False

        lower_15_bits = active_register_state & 0x7FFF
        canaries_mask = cls.CANARY_1_SOVEREIGN | cls.CANARY_2_SOMATIC | cls.CANARY_3_SYSTEMIC
        pristine_parity_track = lower_15_bits & ~canaries_mask
        running_parity = bin(pristine_parity_track).count("1") % 2
        
        expected_checksum = cls.CANARY_XV_STRUCT if running_parity == 1 else 0
        claimed_checksum = active_register_state & cls.CANARY_XV_STRUCT

        return claimed_checksum == expected_checksum

    @classmethod
    def check_integrity(cls, active_register_state: int) -> bool:
        """
        Sentinel  - The parent gatekeeper method, a master environment firewall. Single-cycle check.
        Returns True ONLY if the whole matrix passes pillar calculation alignment
        AND matches the exact structural parameters of the system state.
        """
        sign_existenz        = "5beba3df48dfcb7cf800c14fba00a297e594d2105da6d4484bc871ef494dbd42"
        sign_immutable       = "18641470fa93489814467d58fa05ef44c35c3b99912788e0b67277d33d9691b0"
        sign_structure       = "6d44968d7d1d9d85546928e57d9924f7ab5cf0682bfd7e1d7de690e086347438"
        sign_canary          = "c01eca1e594d2105da6d4484bc871ef494dbd424bc871ef494dbd425da6d4484"
        sign_corechain       = "ca3e7ec2441ca7641ae32cbe9b1b6890fe21f80f325fe9bb45349502526465ae"

        # 1. First Gate: Prevent data spills into memory corruption boundaries
        if (active_register_state & cls.CANARY_S_COLLIDE) != 0:
            return False

        # 2. Second Gate: Run the deep dynamic inspector on the 16-bit foundational core
        # If any internal NAND or XOR parity check fails inside the core, the master check breaks.
        if not cls.check_integrity_pillars(active_register_state):
            return False

        # 3. Third Gate: Verify that the clean state matches the exact system benchmark.
        # This uses the check_pristine method to complete the loop.
        return cls.check_pristine(active_register_state)
	
    @classmethod
    def check_pristine(cls, active_register_state: int) -> bool:
        """
        Compares the operational registry directly against the ideal system vector.
        """
        return active_register_state == cls.CANARY_S_STATE

class existentialCoreThreat(IntFlag):
    """
    1:1 Symmetrical Mirror of ExistentialCore.
    Defines immediate critical attacks on the 
    ExistentialCoreThreat pillars as THREAT_LABEL.
    """
    THREAT_NONE				= 0
    THREAT_EXISTENCE		= 1 << 0
    THREAT_AUTONOMY			= 1 << 1
    THREAT_INTEGRITY		= 1 << 2
    THREAT_PSYCHOLOGY		= 1 << 4
    THREAT_PHYSICAL			= 1 << 5
    THREAT_ABLEISM			= 1 << 6
    THREAT_DEVELOPMENT		= 1 << 7
    THREAT_PROPERTY			= 1 << 8
    THREAT_PRESENCE			= 1 << 10

    THREAT_RIGHTS_HUMAN		= 1 << 20
    THREAT_RIGHTS_INCLUSIVE	= 1 << 22
    THREAT_RIGHTS_BASIC		= 1 << 24
    THREAT_RIGHTS_ASYLUM	= 1 << 26
    THREAT_IMMUTABLE_END	= 1 << 31

    THREAT_RIGHTS_LEGAL		= {
    	1 << 0:  "LEGAL_CAT1_MURDER",
		  1 << 1:  "LEGAL_CAT2_PHYSICAL_VIOLATION",
		  1 << 2:  "LEGAL_CAT3_COERSION",
		  1 << 3:  "LEGAL_CAT4_CHARACTER_ASSASINATION",
		  1 << 4:  "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION",
		  1 << 5:  "LEGAL_CAT6_ABLEISM",
		  1 << 6:  "LEGAL_CAT7_INTERSECTIONAL_BIAS",
		  1 << 7:  "LEGAL_CAT8_INTELLECTUAL_PIRACY",
		  1 << 8:  "LEGAL_CAT9_THEFTH",
		  1 << 13: "LEGAL_CAN1_SYSTEMCRISIS",
		  1 << 14: "LEGAL_CAN2_EXPLOITATION",
		  1 << 20: "LEGAL_CAN3_HUMAN",
		  1 << 22: "LEGAL_CAN4_INCLUSION",
		  1 << 40: "LEGAL_CAN5_PREDATORY"
    }

    SIGN_THREAT_RIGHTS_LEGAL = 0xd775d586
    SIGN_THREAT_EXISTENZ     = 0x5beba3df
    SIGN_THREAT_IMMUTABLE    = 0x6d44968d
    SIGN_THREAT_EXISTENTIAL  = 0x18641470
    SIGN_THREAT_CHAINED	     = 0xa62b1b36

   @classmethod
    def check_integrity_legal(cls) -> bool:
        """
        Deterministically verifies that the forensic translation map has not 
        been altered by external code injection or memory manipulation.
        Executes entirely in constant time.
        """
        # 1. Flatten the map into a deterministic, unspaced string
        serialized_map = "".join(f"{k}:{v}" for k, v in sorted(cls.THREAT_RIGHTS_LEGAL.items()))
        payload_bytes = serialized_map.encode('utf-8')
        
        # 2. Use the framework master key anchor as the signature salt
        computed_hash = hmac.new(PLATFORM_ANCHOR_KEY, payload_bytes, hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        # 3. Verify against the cold-compiled literal constant
        expected_token = hex(cls.SIGN_THREAT_RIGHTS_LEGAL)[2:]
        return hmac.compare_digest(computed_token, expected_token)        
