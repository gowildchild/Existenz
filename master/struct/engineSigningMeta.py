# ==========================================================================
# EXISTENZ  master/struct/engineSigningMeta.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from emgomeSigning import existenzLocations

class existenzMeta:
    HEADER = {
        "REALM":   b"Existenz",
        "VERSION": b"v0.76.16",
        "SECRET":  b"EX25IMMUT32CORE7617"
    }
    MAGIC = {
        "RAW":       f"{HEADER['REALM'].decode()}:{HEADER['VERSION'].decode()}:{HEADER['SECRET'].decode()}",
        "TOKEN":     "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85",
        "SIGNATURE": "db33c3915f073fa8ff11e8557ee0f01ba329b3ae3f06e788bc4803afdf2674e1"        
    }
    META = {
        "Author":    "Gunther Voet"
    }

class existenzConfig:
    FINGERPRINT = {
        "Environment": "f5WWuJ5qDimvSlDycDgXtP2RIwAdLoLan48IK1knr/Y",
        "Platform":    "H2EyS1X5iw/eD88YSysuZbQZ4HH43hZBFWzF2ka4SXQ",
        "Developer":   "3cNVRAjalOpDV243r6xa+GRLV6KETZWc4Y47JfBPWmE",
        "Personal":    "IupL7H3fQINdH4aNFTAwfYvc2RD4LuXO+qsAjCfW1Ig"
    }
    DATA = {
        "SEPARATOR" = [",", ":"]
    }

existenzLocations = {
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
    "sign": {
        "engineStruct":   "master/build-tools/engineStructure.py",
        "engineLibrary":  "master/build-tools/engineLibrary.py",
        "engineData":     "master/build-tools/engineData.py",
        "structures":     "master/build-tools/engineStruct.py",
        "jsonConfig":     "master/existentialSigningConfig.json",
        "jsonSignatures": "master/existentialSignatures.json",
        "jsonData":       "master/existentialSigningData.json",
        "jsonManifest":   "manifest.json",
        "jsonLocalConf":  "sign_integrity_config.json"
    }
}

existenzPublicKeys = (
    ("Environment", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16,  7,  31,  existenzConfig.FINGERPRINT["Environment"]),
    ("Platform",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",         32, 14,  46,  existenzConfig.FINGERPRINT["Platform"]),
    ("Developer",   "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net", 64,  8,  78,  existenzConfig.FINGERPRINT["Developer"]),
    ("Personal",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128,  8, 142,  existenzConfig.FINGERPRINT["Personal"])
)
