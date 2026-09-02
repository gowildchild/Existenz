# ==========================================================================
# EXISTENZ master/struct/existenzSignatures.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from engineSigningMeta import existenzLocations, existenzMeta

existentialToken = {
    "MAGIC": {
        "TAG":                existenzMeta.MAGIC["RAW"],
        "TOKEN":              existenzMeta.MAGIC["TOKEN"],
        "SIGNATURE":          existenzMeta.MAGIC["SIGNATURE"],
        "REALM":              existenzMeta.HEADER["REALM"],
        "VERSION":            existenzMeta.HEADER["VERSION"],
        "AUTHOR":             existenzMeta.META["AUTHOR"]
    },
    "master": {
        "Core":               "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e",
        "Cores":              "bb11656cb916db4245e1ac23cf9b04f03fddcc492faf420e9d0ecf54e4384af8",
        "Threat":             "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca",
        "ThreatLegal":        "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1",
        "ThreatShadowVacuum": "9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69",
        "ThreatChain":        "23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3",
        "Check":              "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"
    },
    "chain": {
        "manifest":           "",
        "core":               "",
        "Threat":             "",
    },
    "manifest": {
        "dist":               "dist",
        "tools":              "dist/tools",
        "build":              "master/build-tools",
        "master":             "master/struct"
    },
    "structs": {
        "KeysPublic":         "40cc0fb5fe8bebcbd871f3089d701df607d727b689aa21ff2ec18350b91e1cc1",
        "KeysHandler":        "b69be327173e6598c19958742a03eef59ed912574e92a106f2df6b1897d9fc48",
        "KeysType":           "4336c5df5ba3017f8a706591fae29ec6ea38993cc653a165f6c8ae3181822557",
        "Locations":          "ad0e774f35ff2000eaeb3f6063be74c3e86c043ed6a04bfd45b7ff2f6460bfa4"
    },
    "engine": {
        "signingMeta":     "master/struct/engineSigningMeta.py",
        "signingStruct":   "master/struct/engineSigningStruct.py",
        "signingLibrary":  "master/struct/engineSigningLibrary.py",
        "signingRoutine":  "master/struct/engineSigningRoutine.py",
        "signingFlow":     "master/struct/engineSigningFlow.py",
        "jsonConfig":      "master/existentialSigningConfig.json",
        "jsonSignatures":  "master/existentialSignatures.json",
        "jsonData":        "master/existentialSigningData.json",
        "jsonManifest":    "manifest.json",
        "jsonLocalConf":   "sign_integrity_config.json"
    }
}

existentialSignature = {
    "core": {
        "Core":       "master/struct/existentialCore.py",
        "Threat":     "master/struct/existentialCoreThreat.py",
        "Signatures": "master/struct/existentialCoreSignatures.py",
        "Check":      "master/existentialCoreCheck.py",
        "Cores":      "master/existentialCores.json"
    },
    "manifest": {
        "dist":   "dist",
        "tools":  "dist/tools",
        "build":  "master/build-tools",
        "master": "master/struct"
    },
    "engine": {
        "signingMeta":     "master/struct/engineSigningMeta.py",
        "signingStruct":   "master/struct/engineSigningStruct.py",
        "signingLibrary":  "master/struct/engineSigningLibrary.py",
        "signingRoutine":  "master/struct/engineSigningRoutine.py",
        "signingFlow":     "master/struct/engineSigningFlow.py",
        "jsonConfig":      "master/existentialSigningConfig.json",
        "jsonSignatures":  "master/existentialSignatures.json",
        "jsonData":        "master/existentialSigningData.json",
        "jsonManifest":    "manifest.json",
        "jsonLocalConf":   "sign_integrity_config.json"
    }
}
