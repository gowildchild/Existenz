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
        "Core":               "459184d4d181e544882fd6eb62f17bcfd27f5275c1ea1ed2540f3870df9c5c93",
        "Check":              "a3c35f3f710d68fc1c546f68c6887ab65a640da99c3c3b68ac854ea5889d0990",        
        "Schema":             "3960a13aa0fb0893ae905a6bbb2330d4a937e496f98a9f0b372f39b40653979c",
        "Cores":              "7cbdc0fd0ee79b3e5d5f488e74e7addf87a416a4f0271df67dc5c32c810fa4e3",
        "Threat":             "45eca7b6496c7b566ce3fbec41165758484a40c8c466ee70dba8ef89dd833a63",
        "ThreatLegal":        "45eca7b6496c7b566ce3fbec41165758484a40c8c466ee70dba8ef89dd833a63",
        "ThreatShadowVacuum": "45eca7b6496c7b566ce3fbec41165758484a40c8c466ee70dba8ef89dd833a63",
        "ThreatSigned":       "45eca7b6496c7b566ce3fbec41165758484a40c8c466ee70dba8ef89dd833a63"
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
        "signingMeta":        "07a453f78f6e8aa4b39b4af896a07328c544058d3fbb53bf5af17c93f2e2c27d",
        "signingStruct":      "c75c4f815091e377a7e9fd079e7a3ca922eaedde3e6351cdffa67c7083201915",
        "signingLibrary":     "99facb0a43f1b532999ed31f5fd47a1fa7e91538d5a07a8f2eb2fbe2501b7ad2",
        "builderLibrary":     "1fca33e2740b4327f792a042adb5afef89356b6a08b7ff277bae386d1737319a",
        "cliStateTest" :      "ddd9487cce4fbeb919bf9f0a362c135f816a8b5e1c179b6a929cfd5bb7a2c062",
        "cliStateInit" :      "ce49a87b2bbbd3928555415df32a81c976e66f4e188cb025c80f55b6a037fb77",
        "cliStateManifest":   "5fe783ec0ade53510ef630b77bf95c0e8de7bfac56d15ade6702bc91eb12d0e7",
        "cliStateSign":       "2c448384308d481774b6c8f2f31f23d6b39b94fd41d22352e48920103a3daca0",
        "cliStateVerify":     "5811e788c0823c056e746060de553ce94105a1c04cf33789409acbc9cb91a4bb",
        "cliStateBuild":      "f9b9f6bf74d195106b753561cf27b498e874e9eca37d56e7d4de0e7995d82f33",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "4c8cdbdd9c4d1f9177848cb47fc1650db8c046fa05af76fdab4dc1db85cabf59"
    }
}
