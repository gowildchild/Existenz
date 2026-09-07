# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# Commercial use requires immediate written license and explicit payment.
# ==========================================================================
from enum import IntFlag
class ExistentialMeta(IntFlag):
    # The 7 Natural Human Pillars (The Foundational Coordinates) 
    EXISTENCE   = 1 << 0  # 1   You, alive, with a body
    AUTONOMY    = 1 << 1  # 2   The Sovereign Right to Choose
    INTEGRITY   = 1 << 2  # 4   The Moral Axis of Personal Choice 
    PSYCHOLOGY  = 1 << 3  # 8   Cognitive Internal State and Mental Peace
    PHYSICAL    = 1 << 4  # 16  Physical Body Vessel and bio-state
    DISABILITY  = 1 << 5  # 32  Nature's way of checks and balances
    DEVELOPMENT = 1 << 6  # 64  Evolutionary, Intellectual and Creative Growth
    PROPERTY    = 1 << 7  # 128 Material Assets and Income Protection
    PRESENCE    = 1 << 8  # 256 Real-Time Spacetime Footprint

    # The external defense factors, protected SHIELD structures
    SHIELD_HUMAN_RIGHTS          = 1 << 20 # 1048576 Shield A (Institutional)
    SHIELD_BASIC_RIGHTS          = 1 << 21 # 2097152 Shield B (Institutional)
    SHIELD_ASYLUM_RIGHTS         = 1 << 22 # 4194304 Shield B2 (Sovereign)
    SHIELD_DISCRIMINATION_RIGHTS = 1 << 23 # 8388608 Shield B3 (Systemic)
    # The acquired micro-structural SHIELDS
    SHIELD_ONLINE_RIGHTS         = 1 << 24 # 16777216 Shield C (Systemic Risks)
    SHIELD_EXPLOITATION_RIGHTS   = 1 << 25 # 33554432 Shield C2 (Anti-Exploitation)
    SHIELD_AQUIRED_RIGHTS        = 1 << 26 # 67108864 Shield D (Acquired by alliance)
    # Forensic and Trust Shields
    SHIELD_FORENSIC_RIGHTS       = 1 << 28 # 268435456 Shield D2 (Immutable records)
    SHIELD_AQUIRED_TRUST         = 1 << 30 # 1073741824 Shield E (Human Action)

class ExistentialThreatMeta(IntFlag):
    # 100% Mathematically Honest Threat Matrix (Flawless 1:1 Mirror Alignment)
    THREAT_EXISTENCE   = 1 << 0  # 1   direct life / mercenary violence
    THREAT_AUTONOMY    = 1 << 1  # 2   choice / administrative coercion
    THREAT_INTEGRITY   = 1 << 2  # 4   moral axis / character assassination
    THREAT_PSYCHOLOGY  = 1 << 3  # 8   mental peace / cyber-bullying
    THREAT_PHYSICAL    = 1 << 4  # 16  bodily safety / hired physical agents
    THREAT_ABLEISM     = 1 << 5  # 32  hostile counter-attack against DISABILITY
    THREAT_DEVELOPMENT = 1 << 6  # 64  growth / algorithmic mining / asset stripping
    THREAT_PROPERTY    = 1 << 7  # 128 assets / capitalistic resource locks

    # Advanced Composite State Triggers
    TRIGGER_EXPLOITATION   = THREAT_ABLEISM | THREAT_PROPERTY
    TRIGGER_PREDATORY       = THREAT_PSYCHOLOGY | THREAT_AUTONOMY
    TRIGGER_SYSTEMSCRISIS  = THREAT_AUTONOMY | THREAT_PSYCHOLOGY | THREAT_PROPERTY

class ExistentialRipples(IntFlag):
    # The Social Blast Radius Expanded in Clean Base-2 Symmetry
    INDIVIDUAL         = 1 << 0  # 1   The Micro Core / The Sovereign Human
    PARTNER            = 1 << 1  # 2   Secondary Core Alliance / The One 
    HOUSEHOLD_MARRIAGE = 1 << 2  # 4   The Domestic Micro-Environment
    FAMILY             = 1 << 3  # 8   Biological and Selected Kinship Net
    FRIENDS            = 1 << 4  # 16  Voluntary Non-Kinship Alliances
    PEERS              = 1 << 5  # 32  Professional and Local Social Circle
    SUPPORT            = 1 << 6  # 64  Care frameworks

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
