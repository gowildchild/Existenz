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
        "Core":               "852f356dedaaf46ba3029243b1ba6bff321d963a05e2e2f9013f8f8cfd5d519a",
        "Check":              "{{HASH_CHECK}}",        
        "Schema":             "b7719b3671077f9d19913a13d2f5f992576ea2ed15a684289975b1e54f8b69f5",
        "Cores":              "24a345a460e123e67e23e2d4959b015e41c1a41287ae1cabdb69545f58b49115",
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
        "KeysPublic":         "{{HASH_KEYS_PUBLIC}}",
        "KeysHandler":        "{{HASH_KEYS_HANDLER}}",
        "KeysType":           "{{HASH_KEYS_TYPE}}",
        "Locations":          "{{HASH_LOCATIONS}}"
    },
    "engine": {
        "engineLogging":      "{{HASH_LOGGING}}",
        "engineCrypto":       "{{HASH_CRYPTO}}",
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
        "Manifest":           "{{HASH_MANIFEST_JSON}}"
    }
}
