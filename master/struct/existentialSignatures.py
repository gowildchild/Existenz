# ==========================================================================
# EXISTENZ TEMPLATE master/struct/existenzSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {
    "MAGIC": {
        "TAG":                "{{MAGIC_TAG}}",
        "TOKEN":              "{{DYNAMIC_TOKEN}}",
        "SIGNATURE":          "{{DYNAMIC_SIGNATURE}}",
        "REALM":              "{{LIVE_REALM}}",
        "VERSION":            "{{LIVE_VERSION}}",
        "AUTHOR":             "{{LIVE_AUTHOR}}"
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
