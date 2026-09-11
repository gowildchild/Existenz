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
        "Check":              "e7b23aa0578b95efa87da64a394959fb3d1a321f369263e06a4f08a382c3cac8",        
        "Schema":             "b7719b3671077f9d19913a13d2f5f992576ea2ed15a684289975b1e54f8b69f5",
        "Cores":              "24a345a460e123e67e23e2d4959b015e41c1a41287ae1cabdb69545f58b49115",
        "Threat":             "2b2bae96d3e91b2693d45025803b175bb721a7c42ffc610680e7a6641b0ae701",
        "ThreatLegal":        "2b2bae96d3e91b2693d45025803b175bb721a7c42ffc610680e7a6641b0ae701",
        "ThreatShadowVacuum": "2b2bae96d3e91b2693d45025803b175bb721a7c42ffc610680e7a6641b0ae701",
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
        "KeysPublic":         "a91809578a7e3e5157187282926b84dd40e9b8aa9d7c4a998ff23b1b8b96fc35",
        "KeysHandler":        "a91809578a7e3e5157187282926b84dd40e9b8aa9d7c4a998ff23b1b8b96fc35",
        "KeysType":           "a91809578a7e3e5157187282926b84dd40e9b8aa9d7c4a998ff23b1b8b96fc35",
        "Locations":          "10debe34bdf1c6a1edd881b8e37a959f805c259ca9fdfb5bf28682059d21ce59"
    },
    "engine": {
        "engineLogging":      "74864a58243b75cf8c0accb2434e331ec880047a130085d974954ea597f5267a",
        "engineCrypto":       "57c64c849300aba3adbddffc423d526a8497c99666a0793248c58e4fc47c7424",
        "signingMeta":        "10debe34bdf1c6a1edd881b8e37a959f805c259ca9fdfb5bf28682059d21ce59",
        "signingStruct":      "a91809578a7e3e5157187282926b84dd40e9b8aa9d7c4a998ff23b1b8b96fc35",
        "signingLibrary":     "4c48189239d09274bc38c79edb116822e1d3769b7f094878fc6b3fcffba10dc5",
        "builderLibrary":     "9211c574180c36699e74d2542dfacd3b9cf75e6696b3d8e590446bdbdd144430",
        "cliStateTest" :      "e8a6c64754e74904994a5e7f73250d1e10c0bc8a6f7bf53e6be0a24505456417",
        "cliStateInit" :      "db762cac6cf919a432f3a0408953cd3d7e9fd86a6bd0fbadad20c34e44def054",
        "cliStateManifest":   "e12805015a864947f13700702a2719783ee4e7867b2431937b7bc217087ba2ab",
        "cliStateSign":       "c23d384c7b567124bfdac030910ed2289a88e731813d89d669516bca4adb25ee",
        "cliStateVerify":     "782c64b8d9a46da4151c6848eb128264fa26ff0a7667a496209c328053f1a237",
        "cliStateBuild":      "612f1c5128c06e02da8649777e5e40827ee76ee377e815a90be938578636cf12",
        "Signatures":         "bcd8f5d3a45ccbc70c1685e3b81c7e6998b051188c0900e1575dd59acb5b2015",
        "Manifest":           "3b0573e7143512e84e21f7ae3e37b648ec7fae6caa2d65235d1d7c27de9b4e63"
    }
}
