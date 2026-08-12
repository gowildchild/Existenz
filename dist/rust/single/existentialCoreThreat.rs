// ==========================================================================
// THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
// Version: v0.76g | Framework Namespace Lock
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

pub mod existential_core_threat {
    pub const THREAT_NONE: u64 = 0; // 
    pub const THREAT_EXISTENCE: u64 = 1 << 0; // 
    pub const THREAT_AUTONOMY: u64 = 1 << 1; // 
    pub const THREAT_INTEGRITY: u64 = 1 << 2; // 
    pub const CANARY_1_SOVEREIGN: u64 = 1 << 3; // WATCHDOG_SOVEREIGN
    pub const THREAT_PSYCHOLOGY: u64 = 1 << 4; // 
    pub const THREAT_PHYSICAL: u64 = 1 << 5; // 
    pub const THREAT_ABLEISM: u64 = 1 << 6; // 
    pub const THREAT_DEVELOPMENT: u64 = 1 << 7; // 
    pub const THREAT_PROPERTY: u64 = 1 << 8; // 
    pub const CANARY_2_SOMATIC: u64 = 1 << 9; // WATCHDOG_SOMATIC
    pub const THREAT_PRESENCE: u64 = 1 << 10; // 
    pub const CANARY_3_SYSTEMIC: u64 = 1 << 13; // WATCHDOG_EVOLUTION
    pub const CANARY_4_PERSONAL: u64 = 1 << 17; // 
    pub const THREAT_RIGHTS_HUMAN: u64 = 1 << 20; // 
    pub const THREAT_RIGHTS_INCLUSIVE: u64 = 1 << 22; // 
    pub const CANARY_5_RIGHTS: u64 = 1 << 23; // 
    pub const THREAT_RIGHTS_BASIC: u64 = 1 << 24; // 
    pub const THREAT_RIGHTS_ASYLUM: u64 = 1 << 26; // 
    pub const CANARY_6_CIVIC: u64 = 1 << 27; // 
    pub const SIGN_THREAT_EXISTENTIAL: u64 = 0x18641470; // 
    pub const SIGN_THREAT_EXISTENZ: u64 = 0x5beba3df; // 
    pub const SIGN_THREAT_RIGHTS_LEGAL: u64 = 0x6d07d972; // 
    pub const SIGN_THREAT_IMMUTABLE: u64 = 0x6d44968d; // 
    pub const THREAT_IMMUTABLE_END: u64 = 1 << 31; // 
    pub const SIGN_THREAT_CANARY: u64 = 0xc01eca1e; // 

    pub const existential_core_threat_legal: &[(u64, &str)] = &[
        (1, "LEGAL_CAT1_MURDER"),
        (2, "LEGAL_CAT2_PHYSICAL_VIOLATION"),
        (4, "LEGAL_CAT3_COERSION"),
        (8, "LEGAL_CAT4_CHARACTER_ASSASINATION"),
        (16, "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION"),
        (32, "LEGAL_CAT2_PHYSICAL_VIOLATION"),
        (64, "LEGAL_CAT6_ABLEISM"),
        (128, "LEGAL_CAT8_INTELLECTUAL_PIRACY"),
        (256, "LEGAL_CAT9_THEFTH"),
        (8192, "LEGAL_CAN1_SYSTEMCRISIS"),
        (16384, "LEGAL_CAN2_EXPLOITATION"),
        (1048576, "LEGAL_CAN3_HUMAN"),
        (4194304, "LEGAL_CAN4_INCLUSION"),
        (1099511627776, "LEGAL_CAN5_PREDATORY")
    ];
}
