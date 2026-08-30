// ==========================================================================
// EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler
// Version: v0.76.15 | Github Deployment
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

pub mod existential_core_signatures {
    pub const EXISTENTIAL_CORE_VERSION: &str = "v0.76.15";
    pub const EXISTENTIAL_CORE_CHECK_MAGIC: &[u8] = b"EX25IMMUT32CORE7617";
    pub const EXISTENTIAL_CORE_CHECK_SIGNATURES: &str = "NOT_SIGNED_YET";
    pub const EXISTENTIAL_CORE: &str = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e";
    pub const EXISTENTIAL_CORE_THREAT_ROOT: &str = "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca";
    pub const EXISTENTIAL_CORE_THREAT_LEGAL: &str = "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1";
    pub const EXISTENTIAL_CORE_THREAT_SHADOW_VACUUM: &str = "9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69";
    pub const EXISTENTIAL_CORE_THREAT: &str = "23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3";
    pub const EXISTENTIAL_CORE_CHECK: &str = "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85";

    pub const EXISTENTIAL_PUBLIC_KEYS: &[(&str, &str)] = &[
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    ];

    pub const EXISTENTIAL_PRIVATE_SIGNED: &[(&str, &str)] = &[
        ("Magic", "46145468df9a2178e371c9918cb7ba8d77f9970b4bdb5fdad8350daa646cf263"),
        ("Core", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreCheck", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreThreatStruct", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreThreatLegal", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreThreatShadowVacuum", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreThreat", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("Cores", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
        ("CoreChain", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad")
    ];
}
