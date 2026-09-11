# ==========================================================================
# EXISTENZ TEMPLATE master/struct/existenzSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {
    "MAGIC": {
        "TAG":                "Existenz:v0.76.18:EX25IMMUT32CORE7617",
        "TOKEN":              "3772c343abeb74234b7e8495fd42cfbd37773cc298ed11579a208400f99c7a19",
        "SIGNATURE":          "a3b2d5656db6b5f6c529d2e15100280b28678530a91db8afc49458a12d9e0aa9",
        "REALM":              "Existenz",
        "VERSION":            "v0.76.18",
        "AUTHOR":             "Gunther Voet"
    },
    "master": {
        "Core":               "{{HASH_CORE}}",
        "Check":              "{{HASH_CHECK}}",        
        "Schema":             "{{HASH_SCHEMA}}",
        "Cores":              "{{HASH_CORES}}",
        "Threat":             "{{HASH_THREAT}}",
        "ThreatLegal":        "{{HASH_THREAT_LEGAL}}",
        "ThreatShadowVacuum": "{{HASH_THREAT_VACUUM}}",
        "ThreatSigned":       "{{HASH_THREAT_SIGNED}}"
    },
    "chain": {
        "Core":               "",
        "CoresChain":         "",
        "Threat":             "",
    },
    "manifest": {
        "dist":               "dist",
        "tools":              "dist/tools",
        "build":              "master/build-tools",
        "master":             "master/struct"
    },
    "structs": {
        "KeysPublic":         "",
        "KeysHandler":        "",
        "KeysType":           "",
        "Locations":          ""
    },
    "engine": {
        "engineLogging":      "9e3383aa1d5773a56af938bac052b44efd4e8c739211c27debddd0798ae14bc6",
        "engineCrypto":       "4aa916e09879cb5cf6aec5f95c6b4673a037c8250f65ba01553e21d447a48821",
        "signingMeta":        "{{HASH_SIGNING_META}}",
        "signingStruct":      "{{HASH_SIGNING_STRUCT}}",
        "signingLibrary":     "{{HASH_SIGNING_LIBRARY}}",
        "builderLibrary":     "{{HASH_BUILDER_LIBRARY}}",
        "cliStateTest" :      "{{HASH_CLI_TEST}}",
        "cliStateInit" :      "{{HASH_CLI_INIT}}",
        "cliStateManifest":   "{{HASH_CLI_MANIFEST}}",
        "cliStateSign":       "{{HASH_CLI_SIGN}}",
        "cliStateVerify":     "{{HASH_CLI_VERIFY}}",
        "cliStateBuild":      "{{HASH_CLI_BUILD}}",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "cbf8f89315a91362a8dee86345534a4c0da56d8602fc2dcfb93904fd14a487cf"
    }
}
