# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
# VERSION: v0.76a This file still has to be simulated for collisions
#
from enum import IntFlag
class ExistentialRipple(IntFlag):

    # The Social Blast Radius Expanded in Clean Base-2 Symmetry

    INDIVIDUAL         = 1 << 0  # 1    The Micro Core / The Sovereign Human
    PARTNER            = 1 << 1  # 2    Secondary Core Alliance / The One 
    HOUSEHOLD_MARRIAGE = 1 << 2  # 4    The Domestic Micro-Environment
    FAMILY             = 1 << 4  # 16   Biological and Selected Kinship Net
    FRIENDS            = 1 << 5  # 32   Voluntary Non-Kinship Alliances
    PEERS              = 1 << 6  # 64   Professional and Local Social Circle
    SUPPORT            = 1 << 7  # 128  Care frameworks

    # Macro Environments and Structural Network Horizons

    SOCIETY            = 1 << 10 # 1024 Local Cultural and Civic Population
    CORPORATE          = 1 << 11 # 2048 Commercial Conglomerates
    GOVERNED           = 1 << 12 # 4096 Public Infrastructure / National

    # Systemic Trust Layers (Contractual, Verifiable, Structural) 

    TRUST_SYSTEMIC    = 1 << 16 # 65536 Infrastructure verification
    TRUST_CONDITIONAL = 1 << 17 # 131072 Prof-contracts / Transactional 

    # The Cascading Trust-Breaker Matrix (Perfect 1:1 Shield Alignment) 

    TRUST_BROKEN_INSTITUTIONAL = 1 << 20 # 1048576 Minor breach of public trust
    TRUST_BROKEN_SAFETY        = 1 << 22 # 4194304 Breach of safety boundary
    TRUST_BROKEN_DIGITAL       = 1 << 24 # 16777216 Breach of online space
    TRUST_BROKEN_CORE          = 1 << 26 # 67108864 The Ultimate Personal Betrayal
    # The Forensic Dead-Bolt Activation Matrix (Calculated via Bitwise OR) 
    TRUST_BROKEN_LOCKOUT       = TRUST_BROKEN_CORE | TRUST_BROKEN_DIGITAL 

    # The Binary Supreme Personal Trust Seals (The Unassailable Core) 
    TRUST_PERSONAL = 1 << 29 # 536870912 Intuitive Human Validation 
    TRUST_ABSOLUTE = 1 << 30 # 1073741824 The Supreme Alliance Apex Bond
