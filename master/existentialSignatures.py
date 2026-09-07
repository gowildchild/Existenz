# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.16 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

existentialNeta = "{'CoreVersion': 'v0.76.16', 'CoreAuthor': 'Gunther Voet', 'CoreWeb': 'github.com/gowildchild/Existenz/', 'CoreDate': '20260906'}"
existentialCoreCheckMagic = b"EX25IMMUT32CORE7617"

class existentialCoreSignatures:
    existentialCoreSigned = (
        ("Magic", "magic", "existentialCoreMagicHash", "", 2, 0),
        ("Core", "core", "existentialCoreHash", "", 12, 1),
    )
