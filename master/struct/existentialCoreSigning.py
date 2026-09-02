# ==========================================================================
# EXISTENZ Existential structures (engine.py v0.76.16)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from existentialCore import existenzIntegrityFileMap

class existenzMeta:
    HEADER = {
        "REALM":   b"Existenz",
        "VERSION": b"v0.76.16",
        "SECRET":  b"EX25IMMUT32CORE7617"
    }
    MAGIC = {
        "SEPARATOR": [",", ":"],
        "TOKEN":     f"{HEADER['REALM'].decode()}:{HEADER['VERSION'].decode()}:{HEADER['SECRET'].decode()}"
    }
    META = {
        "Author":    "Gunther Voet"
    }

class existenzSigned:
    tokens = {
        "MAGIC": "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"
    }
    MAGIC = {
        "TOKEN":     "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85",
        "SIGNATURE": "db33c3915f073fa8ff11e8557ee0f01ba329b3ae3f06e788bc4803afdf2674e1"
    }
    CORE = {
        "existentialCore":                   "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e",
        "existentialCores":                  "bb11656cb916db4245e1ac23cf9b04f03fddcc492faf420e9d0ecf54e4384af8",
        "existentialCoreThreat":             "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca",
        "existentialCoreThreatLegal":        "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1",
        "existentialCoreThreatShadowVacuum": "9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69",
        "existentialCoreThreatChain":        "23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3",
        "existentialCoreCheck":              "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"
    }
    CIRCLE = {
        "CircleDist":   "",
        "CircleTools":  "",
        "CircleBuild":  "",
        "CircleMaster": ""
    }
    CHAIN = {
        "CORE": "77fb563be33179d9658ac77fad0c791d08202c0c32488ea52a098c8af118cef5"
    }
    BUILD = {
        "existenzIntegrityKeysPublic":  "40cc0fb5fe8bebcbd871f3089d701df607d727b689aa21ff2ec18350b91e1cc1",
        "existenzIntegrityKeysHandler": "b69be327173e6598c19958742a03eef59ed912574e92a106f2df6b1897d9fc48",
        "existenzIntegrityKeysType":    "4336c5df5ba3017f8a706591fae29ec6ea38993cc653a165f6c8ae3181822557",
        "existenzIntegrityKeysPolicy":  "",
        "existenzIntegrityKeysState":   "",
        "existenzIntegrityMap":         "ad0e774f35ff2000eaeb3f6063be74c3e86c043ed6a04bfd45b7ff2f6460bfa4"
    }
    FINGERPRINT = {
        "Environment": "f5WWuJ5qDimvSlDycDgXtP2RIwAdLoLan48IK1knr/Y",
        "Platform":    "H2EyS1X5iw/eD88YSysuZbQZ4HH43hZBFWzF2ka4SXQ",
        "Developer":   "3cNVRAjalOpDV243r6xa+GRLV6KETZWc4Y47JfBPWmE",
        "Personal":    "IupL7H3fQINdH4aNFTAwfYvc2RD4LuXO+qsAjCfW1Ig"
    }

existenzIntegrityKeysPublic = (
    ("Environment", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16,  7,  31,  FINGERPRINT["Environment"]),
    ("Platform",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",         32, 14,  46,  FINGERPRINT["Platform"]),
    ("Developer",   "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net", 64,  8,  78,  FINGERPRINT["Developer"]),
    ("Personal",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128,  8, 142,  FINGERPRINT["Personal"])
)

existenzIntegrityStructure = {
    "Magic":                  ("existentialMagicSignature",         3583, 118,  0x00, existenzIntegrityFileMap["core"]["Signatures"],           MAGIC["SIGNATURE"]),
    "MagicCheck":             ("existentialMagicToken",             3575, 110,  0x00, existenzIntegrityFileMap["core"]["Signatures"],           MAGIC["TOKEN"]),
    "Core":                   ("existentialCore",                   3575, 1790, 0x00, existenzIntegrityFileMap["core"]["Core"],                 CORE["existentialCore"]),
    "CoreCheck":              ("existentialCoreCheck",              3575, 4222, 0x00, existenzIntegrityFileMap["core"]["Check"],                CORE["existentialCoreCheck"]),
    "Cores":                  ("existentialCores",                  3575, 1558, 0x01, existenzIntegrityFileMap["core"]["Cores"],                CORE["existentialCores"]),
    "CoreThreat":             ("existentialCoreThreat",             3575, 1599, 0x02, existenzIntegrityFileMap["core"]["Threat"],               CORE["existentialCoreThreat"]),
    "CoreThreatLegal":        ("existentialCoreThreatLegal",        3575, 1599, 0x03, existenzIntegrityFileMap["core"]["Threat"],               CORE["existentialCoreThreatLegal"]),
    "CoreThreatShadowVacuum": ("existentialCoreThreatShadowVacuum", 3575, 1599, 0x04, existenzIntegrityFileMap["core"]["Threat"],               CORE["existentialCoreThreatShadowVacuum"]),
    "CoreThreatChain":        ("existentialCoreThreatChain",        3583, 382,  0x05, existenzIntegrityFileMap["core"]["Threat"],               CORE["existentialCoreThreatChain"]),
    "CoreSigned":             ("existentialCoreSigned",             3583, 511,  0x09, existenzIntegrityFileMap["core"]["Signatures"],           CORE["existentialCore"]),
    "CircleDist":             ("existentialCircleDist",             2615, 23,   0x2F, existenzIntegrityFileMap["manifest"]["dist"],             CIRCLE["CircleDist"]),
    "CircleTools":            ("existentialCircleTools",            2814, 22,   0x3F, existenzIntegrityFileMap["manifest"]["tools"],            CIRCLE["CircleTools"]),
    "CircleBuild":            ("existentialCircleBuild",            2815, 126,  0x4F, existenzIntegrityFileMap["manifest"]["build"],            CIRCLE["CircleBuild"]),
    "CircleMaster":           ("existentialCircleMaster",           2815, 255,  0x5F, existenzIntegrityFileMap["manifest"]["master"],           CIRCLE["CircleMaster"]),
    "CircleChain":            ("existentialCircleSigned",           3839, 511,  0x9F, existenzIntegrityFileMap["manifest"]["manifest"],        CHAIN["CORE"])
}

class existenzSignatures:
    existentialImmutable = ()

    existentialCore = (
        ("Magic",                  existenzIntegrityStructure["Magic"],                  0),
        ("Core",                   existenzIntegrityStructure["Core"],                   1),
        ("CoreCheck",              existenzIntegrityStructure["CoreCheck"],              2),
        ("Cores",                  existenzIntegrityStructure["Cores"],                  4),
        ("CoreThreat",             existenzIntegrityStructure["CoreThreat"],             6),
        ("CoreThreatLegal",        existenzIntegrityStructure["CoreThreatLegal"],        7),
        ("CoreThreatShadowVacuum", existenzIntegrityStructure["CoreThreatShadowVacuum"], 8),
        ("CoreThreatChain",        existenzIntegrityStructure["CoreThreatChain"],        10)
    )

    existentialManifest = (
        ("Magic",                  existenzIntegrityStructure["Magic"],                  0),
        ("CircleDist",             existenzIntegrityStructure["CircleDist"],             1),
        ("CircleTools",            existenzIntegrityStructure["CircleTools"],            2),
        ("CircleBuild",            existenzIntegrityStructure["CircleBuild"],            3),
        ("CircleMaster",           existenzIntegrityStructure["CircleMaster"],           4),
        ("CircleChain",            existenzIntegrityStructure["CircleChain"],            9)
    )
