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
        "Check":              "",        
        "Schema":             "3960a13aa0fb0893ae905a6bbb2330d4a937e496f98a9f0b372f39b40653979c",
        "Cores":              "",
        "Threat":             "",
        "ThreatLegal":        "2cd5a860c19c586e1a6a18fe158480549831b5bedcae77033385d19f557b91cc",
        "ThreatShadowVacuum": "791be6e47d491e9f3c8d6a8fa3b4b5032048bda63c8b2d6ff39d908527781b61",
        "ThreatSigned":       ""
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
        "Locations":          "07a453f78f6e8aa4b39b4af896a07328c544058d3fbb53bf5af17c93f2e2c27d"
    },
    "engine": {
        "engineLogging":      "{{HASH_LOGGING}}",
        "engineCrypto":       "{{HASH_CRYPTO}}",
        "signingMeta":        "07a453f78f6e8aa4b39b4af896a07328c544058d3fbb53bf5af17c93f2e2c27d",
        "signingStruct":      "c75c4f815091e377a7e9fd079e7a3ca922eaedde3e6351cdffa67c7083201915",
        "signingLibrary":     "6658b1d37301dca936929927bb7e54898d857e5204959038aad1c3627b803cf6",
        "builderLibrary":     "1fca33e2740b4327f792a042adb5afef89356b6a08b7ff277bae386d1737319a",
        "cliStateTest" :      "{{HASH_CLI_TEST}}",
        "cliStateInit" :      "{{HASH_CLI_INIT}}",
        "cliStateManifest":   "{{HASH_CLI_MANIFEST}}",
        "cliStateSign":       "{{HASH_CLI_SIGN}}",
        "cliStateVerify":     "{{HASH_CLI_VERIFY}}",
        "cliStateBuild":      "{{HASH_CLI_BUILD}}",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "e07d2ac1090440f21a497a439179d654f2ca2c3e4e404ca89f2e71da94720c4a"
    }
}
