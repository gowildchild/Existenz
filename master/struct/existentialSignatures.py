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
        "Core":                   "{{HASH_CORE}}",
        "CorePolicy":             "{{HASH_CORE_POLICY}}",
        "CoreBitmask":            "{{HASH_CORE_BITMASK}}",
        "CoreChained":            "{{HASH_CORE_CHAINED}}",
        "CoreThreat":             "{{HASH_CORE_THREAT}}",
        "CoreThreatLegal":        "{{HASH_CORE_THREAT_LEGAL}}",
        "CoreThreatShadowVacuum": "{{HASH_CORE_THREAT_SHADOW_VACUUM}}",
        "CoreThreatChained":      "{{HASH_CORE_THREAT_CHAINED}}",
        "CoreCheck":              "{{HASH_CORE_CHECK}}",
        "Cores":                  "{{HASH_CORES}}",
        "Schema":                 "{{HASH_SCHEMA}}"
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
        "Config":             "{{HASH_CONFIG}}",
        "Locations":          "{{HASH_LOCATIONS}}",
        "Steps":              "{{HASH_STEPS}}",
        "IntegrityReq":       "{{HASH_INTEGRITY_REQ}}",
        "KeysHandler":        "{{HASH_KEYS_HANDLER}}",
        "KeysIO":             "{{HASH_KEYS_I_O}}",
        "KeyStatus":          "{{HASH_KEY_STATUS}}",
        "IntegrityState":     "{{HASH_INTEGRITY_STATE}}",
        "CorePolicy":         "{{HASH_CORE_POLICY}}"
    },
    "engine": {
        "engineLogging":      "{{HASH_ENGINE_LOGGING}}",
        "engineCrypto":       "{{HASH_ENGINE_CRYPTO}}",
        "signingMeta":        "{{HASH_SIGNING_META}}",
        "signingStruct":      "{{HASH_SIGNING_STRUCT}}",
        "signingLibrary":     "{{HASH_SIGNING_LIBRARY}}",
        "builderLibrary":     "{{HASH_BUILDER_LIBRARY}}",
        "cliStateTest" :      "{{HASH_CLI_STATE_TEST}}",
        "cliStateInit" :      "{{HASH_CLI_STATE_INIT}}",
        "cliStateManifest":   "{{HASH_CLI_STATE_MANIFEST}}",
        "cliStateSign":       "{{HASH_CLI_STATE_SIGN}}",
        "cliStateVerify":     "{{HASH_CLI_STATE_VERIFY}}",
        "cliStateBuild":      "{{HASH_CLI_STATE_BUILD}}",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "{{HASH_MANIFEST_JSON}}"
    }
}
