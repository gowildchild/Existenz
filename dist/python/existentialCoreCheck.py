# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76i | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

import hmac
import hashlib
from single.existentialCore import existentialCore
from single.existentialCoreThreat import existentialCoreThreat, existentialCoreThreatLegal
from single.existentialCoreSignatures import existentialCoreSignatures

existentialCoreCheckVersion    = "{existentialCoreVersion}"
existentialCoreCheckMagic      = b"{existentialCoreCheckMagic}"
existentialCoreCheckSign       = 0x7c165b32
existentialCoreCheckSignature  = "{sigs['existentialCoreCheck']}"

class existentialCoreCheck:
    @classmethod
    def check_integrity_core(cls, active_register_state: int) -> int:
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

        if not (has_autonomy and has_integrity): evaluated_state |= existentialCore.CANARY_1_SOVEREIGN
        if not (has_psychology and has_physical): evaluated_state |= existentialCore.CANARY_2_SOMATIC
        if not (has_development and has_property): evaluated_state |= existentialCore.CANARY_3_SYSTEMIC
        if not has_existence: evaluated_state |= existentialCore.CANARY_1_SOVEREIGN

        running_parity = 0
        for bit_index in range(15):
            if evaluated_state & (1 << bit_index): running_parity ^= 1
        if running_parity == 1: evaluated_state |= existentialCore.CANARY_XV_STRUCT
        return evaluated_state

    @classmethod
    def check_integrity_pillars(cls, active_register_state: int) -> bool:
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
        if claimed_canaries_vector != expected_canaries_vector: return False

        lower_15_bits = active_register_state & 0x7FFF
        canaries_mask = existentialCore.CANARY_1_SOVEREIGN | existentialCore.CANARY_2_SOMATIC | existentialCore.CANARY_3_SYSTEMIC
        pristine_parity_track = lower_15_bits & ~canaries_mask
        running_parity = bin(pristine_parity_track).count("1") % 2
        
        expected_checksum = existentialCore.CANARY_XV_STRUCT if running_parity == 1 else 0
        claimed_checksum = active_register_state & existentialCore.CANARY_XV_STRUCT
        return claimed_checksum == expected_checksum

    @classmethod
    def check_integrity(cls, active_register_state: int) -> bool:
        if (active_register_state & existentialCore.CANARY_S_COLLIDE) != 0: return False
        if not cls.check_integrity_pillars(active_register_state): return False
        return active_register_state == existentialCore.CANARY_S_STATE

    @classmethod
    def check_integrity_legal(cls) -> bool:
        serialized_map = "".join(f"{k}:{v}" for k, v in sorted(existentialCoreThreatLegal.items()))
        computed_hash = hmac.new(existentialCoreCheckMagic, serialized_map.encode('utf-8'), hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        expected_token = existentialCoreSignatures.existentialCoreThreatLegal[-8:].lower()
        return hmac.compare_digest(computed_token, expected_token)
