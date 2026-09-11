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
        "Core":               "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",
        "Check":              "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",        
        "Schema":             "f40e5ab470587730f2a8bf04ea640504f996e96084ab3c4b2f5d9983692b2e05",
        "Cores":              "e604203d78d1f34f07c36d2a96035261093725a1776303427fa1b73c36ca3811",
        "Threat":             "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",
        "ThreatLegal":        "2cd5a860c19c586e1a6a18fe158480549831b5bedcae77033385d19f557b91cc",
        "ThreatShadowVacuum": "791be6e47d491e9f3c8d6a8fa3b4b5032048bda63c8b2d6ff39d908527781b61",
        "ThreatSigned":       "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc"
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
        "KeysPublic":         "3b574f18e912ce1429004bef31d5ecfab1ac12df4831e856862655b232070abb",
        "KeysHandler":        "3b574f18e912ce1429004bef31d5ecfab1ac12df4831e856862655b232070abb",
        "KeysType":           "3b574f18e912ce1429004bef31d5ecfab1ac12df4831e856862655b232070abb",
        "Locations":          "3b574f18e912ce1429004bef31d5ecfab1ac12df4831e856862655b232070abb"
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
        "Manifest":           "93588c82801073aef9867ecbd99de5d33191717e608a5864c76e041cf8bffea1"
    }
}
