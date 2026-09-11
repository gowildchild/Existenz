# ==========================================================================
# EXISTENZ TEMPLATE master/struct/existenzSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {
    "MAGIC": {
        "TAG":                "Existenz:v0.76.20:EX25IMMUT32CORE7617",
        "TOKEN":              "f8f798f97efd50ead75e8f187d99d9b2e5c2d3c14bbc34e97c09f5b9fd7f3c92",
        "SIGNATURE":          "123ebc37b9f67191556535aa1dba970c62daac63ded74ffb6ba9ecbdb87a1d88",
        "REALM":              "Existenz",
        "VERSION":            "v0.76.20",
        "AUTHOR":             "Gunther Voet"
    },
    "master": {
        "Core":               "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",
        "Check":              "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",        
        "Schema":             "4dfd575a306fad32e996e274269c9c9ea1f71736229e94a3461a72bca9218847",
        "Cores":              "8e451ce586b9a0e8d43dd7a3809ba78eb12edb7878af54f4252c001fc35b7f4c",
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
        "KeysPublic":         "18521587bc16c25a754a08c0ae4670c4566e88225c4ff5a1f76e4e8d2c07a9ae",
        "KeysHandler":        "469f718d4d1f57246fd3fe56a7b13a2b149685b3a44da19ca64bf3cfde60e1cc",
        "KeysType":           "{{HASH_KEYS_TYPE}}",
        "Locations":          "5c45798c6743b991dc511ebdc913c38ef9604bd86cca06393b12c10f9a5ae13d"
    },
    "engine": {
        "engineLogging":      "9e3383aa1d5773a56af938bac052b44efd4e8c739211c27debddd0798ae14bc6",
        "engineCrypto":       "4aa916e09879cb5cf6aec5f95c6b4673a037c8250f65ba01553e21d447a48821",
        "signingMeta":        "07a453f78f6e8aa4b39b4af896a07328c544058d3fbb53bf5af17c93f2e2c27d",
        "signingStruct":      "e4f1f325c163ea339b3be43e2fef739180645593b2c09eab798123e15f21857f",
        "signingLibrary":     "b93ecba452ddefd1bcd77ab9ad818d14d7e78ab1ea5d24f49ab4f2a9d779c533",
        "builderLibrary":     "1fca33e2740b4327f792a042adb5afef89356b6a08b7ff277bae386d1737319a",
        "cliStateTest" :      "{{HASH_CLI_TEST}}",
        "cliStateInit" :      "{{HASH_CLI_INIT}}",
        "cliStateManifest":   "{{HASH_CLI_MANIFEST}}",
        "cliStateSign":       "{{HASH_CLI_SIGN}}",
        "cliStateVerify":     "{{HASH_CLI_VERIFY}}",
        "cliStateBuild":      "{{HASH_CLI_BUILD}}",
        "Signatures":         "{{HASH_SIGNATURES_JSON}}",
        "Manifest":           "fec8ee7efb3a8f14bf68d40cf62a2f68d1472a799bc8de12726f8acd30766b2b"
    }
}
