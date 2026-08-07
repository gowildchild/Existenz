/**
 * THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
 * Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
 */

export const ExistentialCore = Object.freeze({
    // The 7 Natural Human Pillars (The Foundational Coordinates)
    EXISTENCE:   1 << 0,   // 1
    AUTONOMY:    1 << 1,   // 2
    INTEGRITY:   1 << 2,   // 4
    PSYCHOLOGY:  1 << 3,   // 8
    PHYSICAL:    1 << 4,   // 16
    DISABILITY:  1 << 5,   // 32
    DEVELOPMENT: 1 << 6,   // 64
    PROPERTY:    1 << 7,   // 128
    PRESENCE:    1 << 8,   // 256

    // The external defense factors, protected SHIELD structures
    SHIELD_HUMAN_RIGHTS:          1 << 20, // 1048576
    SHIELD_DISCRIMINATION_RIGHTS: 1 << 22, // 8388608
    SHIELD_BASIC_RIGHTS:          1 << 24, // 2097152
    
    // The acquired micro-structural SHIELDS
    SHIELD_AQUIRED_RIGHTS:        1 << 26, // 67108864
    SHIELD_AQUIRED_TRUST:         1 << 30  // 1073741824
});

export const ExistentialThreat = Object.freeze({
    // 100% Mathematically Honest Threat Matrix (Flawless 1:1 Mirror Alignment)
    THREAT_EXISTENCE:   1 << 0,   // 1
    THREAT_AUTONOMY:    1 << 1,   // 2
    THREAT_INTEGRITY:   1 << 2,   // 4
    THREAT_PSYCHOLOGY:  1 << 3,   // 8
    THREAT_PHYSICAL:    1 << 4,   // 16
    THREAT_ABLEISM:     1 << 5,   // 32
    THREAT_DEVELOPMENT: 1 << 6,   // 64
    THREAT_PROPERTY:    1 << 7,   // 128

    // Advanced Composite State Triggers
    get TRIGGER_EXPLOITATION() { return this.THREAT_ABLEISM | this.THREAT_PROPERTY; },
    get TRIGGER_PREDATORY() { return this.THREAT_PSYCHOLOGY | this.THREAT_AUTONOMY; },
    get TRIGGER_SYSTEMSCRISIS() { return this.THREAT_AUTONOMY | this.THREAT_PSYCHOLOGY | this.THREAT_PROPERTY; }
});

export const ExistentialRipple = Object.freeze({
    // The Social Blast Radius Expanded in Clean Base-2 Symmetry
    INDIVIDUAL:         1 << 0,   // 1
    PARTNER:            1 << 1,   // 2
    HOUSEHOLD_MARRIAGE: 1 << 2,   // 4
    FAMILY:             1 << 3,   // 8
    FRIENDS:            1 << 4,   // 16
    PEERS:              1 << 5,   // 32
    SUPPORT:            1 << 6,   // 64

    // Macro Environments and Structural Network Horizons
    SOCIETY:            1 << 10,  // 1024
    CORPORATE:          1 << 11,  // 2048
    GOVERNED:           1 << 12,  // 4096

    // Systemic Trust Layers (Contractual, Verifiable, Structural)
    TRUST_SYSTEMIC:     1 << 16,  // 65536
    TRUST_CONDITIONAL:  1 << 17,  // 131072
    
    // The Cascading Trust-Breaker Matrix (Perfect 1:1 Shield Alignment)
    TRUST_BROKEN_INSTITUTIONAL: 1 << 20, // 1048576
    TRUST_BROKEN_SAFETY:        1 << 22, // 4194304
    TRUST_BROKEN_DIGITAL:       1 << 24, // 16777216
    TRUST_BROKEN_CORE:          1 << 26, // 67108864
    
    // The Forensic Dead-Bolt Activation Matrix (Calculated via Bitwise OR)
    get TRUST_BROKEN_LOCKOUT() { return this.TRUST_BROKEN_CORE | this.TRUST_BROKEN_DIGITAL; },

    // The Binary Supreme Personal Trust Seals (The Unassailable Core)
    TRUST_PERSONAL:     1 << 29,  // 536870912
    TRUST_ABSOLUTE:     1 << 30   // 1073741824
});
