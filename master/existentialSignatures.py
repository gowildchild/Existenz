# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.18 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

existentialNeta = "{'CoreVersion': 'v0.76.18', 'CoreRealm': 'Existenz', 'CoreMagic': 'EX25IMMUT32CORE7617', 'CoreMagicRaw': 'CoreRealm:CoreVersion:CoreMagic', 'CoreAuthor': 'Gunther Voet', 'CoreDate': '20260910', 'CoreWeb': 'github.com/gowildchild/Existenz/', 'immutable': {'PILLARS': 'EXISTENCE | AUTONOMY | INTEGRITY | PSYCHOLOGY | PHYSICAL | DISABILITY | DEVELOPMENT | PROPERTY | PRESENCE', 'RIGHTS': 'SHIELD_RIGHTS_HUMAN | SHIELD_RIGHTS_INCLUSIVE | SHIELD_RIGHTS_BASIC | SHIELD_RIGHTS_ASYLUM'}}"
existentialCoreCheckMagic = b"EX25IMMUT32CORE7617"

class existentialCoreSignatures:
    existentialCoreSigned = (
        ("Magic", "magic", "existentialCoreMagicHash", "", 2, 0),
        ("Core", "core", "existentialCoreHash", "", 12, 1),
    )
