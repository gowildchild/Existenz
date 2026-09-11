# ==========================================================================
# EXISTENZ master/struct/engineSigningDefaults.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

# 1. CORE REALM FALLBACK BLUEPRINT METADATA
# Preserves baseline authority schemas if the primary json schema is dropped.
DEFAULT_META = {
    "CoreRealm": "Existenz",
    "CoreVersion": "v0.76.20",
    "CoreMagic": "EX25IMMUT32CORE7617",
    "CoreMagicRaw": "CoreRealm:CoreVersion:CoreMagic",
    "CoreAuthor": "Gunther Voet",
    "CoreDate": "20260912",
    "CoreWeb": "://github.com"
}

# 2. STRATEGIC IMMUTABILITY CONSTRAINTS
# Holds structural nodes for fallback token map rendering validation passes.
DEFAULT_IMMUTABLE = {
    "PILLARS": "EXISTENCE | AUTONOMY | INTEGRITY | PSYCHOLOGY | PHYSICAL | DISABILITY | DEVELOPMENT | PROPERTY | PRESENCE",
    "RIGHTS": "SHIELD_RIGHTS_HUMAN | SHIELD_RIGHTS_INCLUSIVE | SHIELD_RIGHTS_BASIC | SHIELD_RIGHTS_ASYLUM"
}

# 3. CRUTIAL SYSTEM CRYPTOGRAPHIC RE-COMPILATION TEMPLATE
# Acts as the authoritative baseline backup string for magic tag salting calculations.
DEFAULT_MAGIC_TAG = "Existenz:v0.76.20:EX25IMMUT32CORE7617"

# 4. SYSTEM FATAL GATING FLAG
# True  -> Immediately raises exceptions and halts execution if master schema drops out.
# False -> Emits a warning log indicator and gracefully drops back to these tracking profiles.
HALT_ON_SCHEMA_DRIFT = False
