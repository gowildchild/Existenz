# ==========================================================================
# EXISTENZ TEMPLATE master/struct/existenzSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {
    "MAGIC": {
        "TAG":                "{{MAGIC_TAG}}",
        "TOKEN":              "3772c343abeb74234b7e8495fd42cfbd37773cc298ed11579a208400f99c7a19",
        "SIGNATURE":          "a3b2d5656db6b5f6c529d2e15100280b28678530a91db8afc49458a12d9e0aa9",
        "REALM":              "Existenz",
        "VERSION":            "v0.76.18",
        "AUTHOR":             "Gunther Voet"
    },
    "master": {
        "Core":               "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",
        "Check":              "{{HASH_CHECK}}",        
        "Schema":             "3960a13aa0fb0893ae905a6bbb2330d4a937e496f98a9f0b372f39b40653979c",
        "Cores":              "",
        "Threat":             "",
        "ThreatLegal":        "2cd5a860c19c586e1a6a18fe158480549831b5bedcae77033385d19f557b91cc",
        "ThreatShadowVacuum": "{{HASH_THREAT_VACUUM}}",
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
        "KeysPublic":         "{{HASH_KEYS_PUBLIC}}",
        "KeysHandler":        "{{HASH_KEYS_HANDLER}}",
        "KeysType":           "{{HASH_KEYS_TYPE}}",
        "Locations":          "{{HASH_LOCATIONS}}"
    },
    "engine": {
        "engineLogging":      "9e3383aa1d5773a56af938bac052b44efd4e8c739211c27debddd0798ae14bc6",
        "engineCrypto":       "4aa916e09879cb5cf6aec5f95c6b4673a037c8250f65ba01553e21d447a48821",
        "signingMeta":        "07a453f78f6e8aa4b39b4af896a07328c544058d3fbb53bf5af17c93f2e2c27d",
        "signingStruct":      "c75c4f815091e377a7e9fd079e7a3ca922eaedde3e6351cdffa67c7083201915",
        "signingLibrary":     "0de24933d877d104c9c1a03f8e1a9105c596a1818b977491ed2fe4b7e07ba419",
        "builderLibrary":     "1fca33e2740b4327f792a042adb5afef89356b6a08b7ff277bae386d1737319a",
        "cliStateTest" :      "ddd9487cce4fbeb919bf9f0a362c135f816a8b5e1c179b6a929cfd5bb7a2c062",
        "cliStateInit" :      "8145cda113cb4e5c5f1aa61f26676e85a0aa70d1e0210fe1e92d448ef193d6f7",
        "cliStateManifest":   "5fe783ec0ade53510ef630b77bf95c0e8de7bfac56d15ade6702bc91eb12d0e7",
        "cliStateSign":       "2c448384308d481774b6c8f2f31f23d6b39b94fd41d22352e48920103a3daca0",
        "cliStateVerify":     "5811e788c0823c056e746060de553ce94105a1c04cf33789409acbc9cb91a4bb",
        "cliStateBuild":      "f9b9f6bf74d195106b753561cf27b498e874e9eca37d56e7d4de0e7995d82f33",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "b3afa47fd2b4d0fe436d414eef0e3ba59c38de5cec55a9772ae8533ea1efc4e5"
    }
}
