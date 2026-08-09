# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76b
#
from enum import IntFlag
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
    def verify_legal_map_integrity(cls) -> bool:
        """
        Deterministically verifies that the forensic translation map has not 
        been altered by external code injection or memory manipulation.
        Executes entirely in constant time.
        """
        # 1. Flatten the map into a deterministic, unspaced string
        serialized_map = "".join(f"{k}:{v}" for k, v in sorted(cls.THREAT_RIGHTS_LEGAL.items()))
        payload_bytes = serialized_map.encode('utf-8')
        
        # 2. Use the framework master key anchor as the signature salt
        anchor_key = b"EX25IMMUT32CORE7617"
        computed_hash = hmac.new(anchor_key, payload_bytes, hashlib.sha256).digest()
        computed_token = computed_hash[:4].hex()
        
        # 3. Verify against the cold-compiled literal constant
        expected_token = hex(cls.SIGN_THREAT_RIGHTS_LEGAL)[2:]
        return hmac.compare_digest(computed_token, expected_token)


class existentialCoreThreatBirds(IntFlag):
    CANARY_1_SOVEREIGN      = 1 << 3
    CANARY_2_SOMATIC        = 1 << 9
    CANARY_3_SYSTEMIC       = 1 << 13
    CANARY_4_PERSONAL       = 1 << 17
    CANARY_5_RIGHTS         = 1 << 23
    CANARY_6_CIVIC          = 1 << 27

