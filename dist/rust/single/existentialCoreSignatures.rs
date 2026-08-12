// ==========================================================================
// THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
// Version: v0.76g | Framework Namespace Lock
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

pub mod existential_core_signatures {
    pub const EXISTENTIAL_CORE_VERSION: &str = "v0.76g";
    pub const EXISTENTIAL_CORE_CHECK_MAGIC: &[u8] = b"EX25IMMUT32CORE7617";
    pub const EXISTENTIAL_CORE_CHECK_SIGNATURES: &str = "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c";
    pub const EXISTENTIAL_CORE: &str = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e";
    pub const EXISTENTIAL_CORE_THREAT_ROOT: &str = "57c413f8531731df0d2f09a260ea36c7e49269348b553fdeeaa2dd11e7bc4bb9";
    pub const EXISTENTIAL_CORE_THREAT_LEGAL: &str = "6d07d97272d414f966ea7a9d7b2956b96541fecbcb9079f375408a62b3b6bd6e";
    pub const EXISTENTIAL_CORE_THREAT: &str = "759533dfd2a276046bc62985b17df7cefb999a1c3a07b7b983e5ee278d80302d";
    pub const EXISTENTIAL_CORE_CHECK: &str = "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c";

    pub const EXISTENTIAL_PUBLIC_KEYS: &[(&str, &str)] = &[
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    ];

    pub const EXISTENTIAL_PRIVATE_SIGNED: &[(&str, &str)] = &[
        ("Magic", "aa9bc01ee92ec2db4ce5a5f0aac07caa70a2019ee17511336b41747201ade17a"),
        ("Core", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d"),
        ("CoreCheck", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d"),
        ("CoreThreatStruct", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d"),
        ("CoreThreatLegal", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d"),
        ("CoreThreat", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d"),
        ("CoreChain", "faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d")
    ];
}
