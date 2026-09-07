# ==========================================================================
# EXISTENZ  master/struct/engineSigningMeta.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
_HEADER = {
    "REALM":   b"Existenz",
    "VERSION": b"v0.76.17",
    "SECRET":  b"EX25IMMUT32CORE7617"
}

class existenzMeta:
    HEADER = _HEADER
    MAGIC = {
        "RAW":       f"{_HEADER['REALM'].decode()}:{_HEADER['VERSION'].decode()}:{_HEADER['SECRET'].decode()}",
        "TOKEN":     "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85",
        "SIGNATURE": "db33c3915f073fa8ff11e8557ee0f01ba329b3ae3f06e788bc4803afdf2674e1"        
    }
    META = {
        "AUTHOR":    "Gunther Voet"
    }

# del _HEADER

class existenzConfig:
    FINGERPRINT = {
        "Environment": "f5WWuJ5qDimvSlDycDgXtP2RIwAdLoLan48IK1knr/Y",
        "Platform":    "H2EyS1X5iw/eD88YSysuZbQZ4HH43hZBFWzF2ka4SXQ",
        "Developer":   "3cNVRAjalOpDV243r6xa+GRLV6KETZWc4Y47JfBPWmE",
        "Personal":    "IupL7H3fQINdH4aNFTAwfYvc2RD4LuXO+qsAjCfW1Ig"
    }
    DATA = {
        "SEPARATOR":   [",", ":"]
    }

existenzLocations = {
    "core": {
        "Core":          "master/existentialCore.py",
        "Check":         "master/existentialCoreCheck.py",
        "Schema":        "master/struct/existentialCoreSchema.json",
        "Cores":         "master/existentialCores.json",
        "Threat":        "master/existentialCoreThreat.py",
        "ThreatSigned":  "master/existentialCoreThreat.py",
        "Signatures":    "master/existentialSignatures.py"
    },
    "chain": {
        "CoresChain":    "",
        "ThreatSigned":  ""
    },
    "manifest": {
        "dist":     "dist",
        "tools":    "dist/tools",
        "build":    "master/build-tools",
        "master":   "master/struct"
    },
    "engine": {
        "engineLogging":     "master/struct/visualMixEngineLogging.py",
        "engineCrypto":      "master/struct/visualMixEngineCrypto.py",
        "signingMeta":       "master/struct/engineSigningMeta.py",
        "signingStruct":     "master/struct/engineSigningStruct.py",
        "signingLibrary":    "master/struct/engineSigningLibrary.py",
        "builderLibrary":    "master/struct/engineBuilderLibrary.py",
        "cliStateTest" :     "master/struct/module/cliStateTest.py",
        "cliStateInit" :     "master/struct/module/cliStateInit.py",
        "cliStateManifest":  "master/struct/module/cliStateManifest.py",
        "cliStateSign":      "master/struct/module/cliStateSign.py",
        "cliStateVerify":    "master/struct/module/cliStateVerify.py",
        "cliStateBuild":     "master/struct/module/cliStateBuild.py",
        "jsonConfig":        "master/existentialSigningConfig.json",
        "jsonSignatures":    "master/existentialSignatures.json",
        "jsonData":          "master/existentialSigningData.json",
        "jsonManifest":      "manifest.json",
        "jsonLocalConf":     "sign_integrity_config.json"
    }
}

existenzPublicKeys = (
    ("Environment", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16,  7,  31,  existenzConfig.FINGERPRINT["Environment"]),
    ("Platform",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",         32, 14,  46,  existenzConfig.FINGERPRINT["Platform"]),
    ("Developer",   "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net", 64,  8,  78,  existenzConfig.FINGERPRINT["Developer"]),
    ("Personal",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128,  8, 142,  existenzConfig.FINGERPRINT["Personal"])
)
