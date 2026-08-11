# ==========================================================================
# THE EXISTENZ PLATFORM (PUBLIC SECURITY INTEGRITY CHECK)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
# v0.76f
# Veritas - Public Security Guardian - final Check.
import hmac
import hashlib
from existentialCore import existentialCore
from existentialCoreThreat import existentialCoreThreat

# ==========================================================================
# CRITICAL FILE-GLOBAL ARCHITECTURAL ANCHORS
# ==========================================================================
PLATFORM_VERSION        = "v0.76f"
PLATFORM_ANCHOR_KEY     = b"EX25IMMUT32CORE7617"
SIGNATURE_CORE_EXISTENZ = "5beba3df6d44968d18641470c01eca1eca3e7ec2"


class existentialCoreCheck:
    """
    Public-facing validation gatekeeper. Cross-examines live register states
    against the clean room master structure definitions.
    """
    
    @classmethod
    def check_integrity_core(cls, active_register_state: int) -> int:
        """
        Active State Modifier (Mutator). Applies NAND logic to active pairs.
        """
        has_existence   = bool(active_register_state & existentialCore.EXISTENCE)
        has_autonomy    = bool(active_register_state & existentialCore.AUTONOMY)
        has_integrity   = bool(active_register_state & existentialCore.INTEGRITY)
        has_psychology  = bool(active_register_state & existentialCore.PSYCHOLOGY)
        has_physical    = bool(active_register_state & existentialCore.PHYSICAL)
        has_development = bool(active_register_state & existentialCore.DEVELOPMENT)
        has_property    = bool(active_register_state & existentialCore.PROPERTY)

        cleared_mask = ~(existentialCore.CANARY_1_SOVEREIGN | existentialCore.CANARY_2_SOMATIC | 
                         existentialCore.CANARY_3_SYSTEMIC | existentialCore.CANARY_XV_STRUCT)
        evaluated_state = active_register_state & cleared_mask

        if not (has_autonomy and has_integrity):
            evaluated_state |= existentialCore.CANARY_1_SOVEREIGN
        if not (has_psychology and has_physical):
            evaluated_state |= existentialCore.CANARY_2_SOMATIC
        if not (has_development and has_property):
            evaluated_state |= existentialCore.CANARY_3_SYSTEMIC
        if not has_existence:
            evaluated_state |= existentialCore.CANARY_1_SOVEREIGN

        running_parity = 0
        for bit_index in range(15):
            if evaluated_state & (1 << bit_index):
                running_parity ^= 1

        if running_parity == 1:
            evaluated_state |= existentialCore.CANARY_XV_STRUCT

        return evaluated_state

    @classmethod
    def check_integrity_pillars(cls, active_register_state: int) -> bool:
        """
        State Validator (Inspector). Zero-loop, constant-time validation using CANARY_S_STATE.
        """
        raw_pillars = active_register_state & (existentialCore.CANARY_S_STATE & 0x0FFF)
        has_existence   = bool(raw_pillars & existentialCore.EXISTENCE)
        has_autonomy    = bool(raw_pillars & existentialCore.AUTONOMY)
        has_integrity   = bool(raw_pillars & existentialCore.INTEGRITY)
        has_psychology  = bool(raw_pillars & existentialCore.PSYCHOLOGY)
        has_physical    = bool(raw_pillars & existentialCore.PHYSICAL)
        has_development = bool(raw_pillars & existentialCore.DEVELOPMENT)
        has_property    = bool(raw_pillars & existentialCore.PROPERTY)

        expected_canary_1 = (not (has_autonomy and has_integrity) or not has_existence) << 3
        expected_canary_2 = (not (has_psychology and has_physical)) << 9
        expected_canary_3 = (not (has_development and has_property)) << 13

        expected_canaries_vector = expected_canary_1 | expected_canary_2 | expected_canary_3
        claimed_canaries_vector = active_register_state & (existentialCore.CANARY_1_SOVEREIGN | 
                                                            existentialCore.CANARY_2_SOMATIC | 
                                                            existentialCore.CANARY_3_SYSTEMIC)

        if claimed_canaries_vector != expected_canaries_vector:
            return False

        lower_15_bits = active_register_state & 0x7FFF
        canaries_mask = existentialCore.CANARY_1_SOVEREIGN | existentialCore.CANARY_2_SOMATIC | existentialCore.CANARY_3_SYSTEMIC
        pristine_parity_track = lower_15_bits & ~canaries_mask
        running_parity = bin(pristine_parity_track).count("1") % 2
        
        expected_checksum = existentialCore.CANARY_XV_STRUCT if running_parity == 1 else 0
        claimed_checksum = active_register_state & existentialCore.CANARY_XV_STRUCT

        return claimed_checksum == expected_checksum

    @classmethod
    def check_integrity(cls, active_register_state: int) -> bool:
        """
        Sentinel Master Firewall. Keeps the full string signatures 
        directly inside the method code segment to protect them from memory hacks.
        """
        sign_existenz        = "5beba3df48dfcb7cf800c14fba00a297e594d2105da6d4484bc871ef494dbd42"
        sign_immutable       = "18641470fa93489814467d58fa05ef44c35c3b99912788e0b67277d33d9691b0"
        sign_structure       = "6d44968d7d1d9d85546928e57d9924f7ab5cf0682bfd7e1d7de690e086347438"
        sign_canary          = "c01eca1e594d2105da6d4484bc871ef494dbd424bc871ef494dbd425da6d4484"
        sign_corechain       = "ca3e7ec2441ca7641ae32cbe9b1b6890fe21f80f325fe9bb45349502526465ae"

        if (active_register_state & existentialCore.CANARY_S_COLLIDE) != 0:
            return False
        if not cls.check_integrity_pillars(active_register_state):
            return False
        return active_register_state == existentialCore.CANARY_S_STATE

    @classmethod
    def check_integrity_legal(cls) -> bool:
        """
        Deterministically verifies the threat map has not been tampered with.
        """
        serialized_map = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreat.THREAT_RIGHTS_LEGAL.items()))
        payload_bytes = serialized_map.encode('utf-8')
        
        # Explicit reference loop to capture file-global scope configuration value safely
        anchor_salt = PLATFORM_ANCHOR_KEY
        computed_hash = hmac.new(anchor_salt, payload_bytes, hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        expected_token = hex(existentialCoreThreat.SIGN_THREAT_RIGHTS_LEGAL)[2:]
        return hmac.compare_digest(computed_token, expected_token)
