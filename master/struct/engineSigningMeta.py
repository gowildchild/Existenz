# ==========================================================================
# EXISTENZ  master/struct/engineSigningMeta.py
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import json
import hashlib

# 1. Resolve the blueprint path and ingest master configurations dynamically
_current_dir = os.path.dirname(os.path.abspath(__file__))
_schema_path = os.path.abspath(os.path.join(_current_dir, "existentialCoreSchema.json"))

try:
    with open(_schema_path, "r", encoding="utf-8") as _f:
        _blueprint_data = json.load(_f)
    _meta = _blueprint_data.get("existentialMeta", {})
except Exception:
    # Safe fallback matching your baseline configuration
    _meta = {
        "CoreRealm": "Existenz",
        "CoreVersion": "v0.76.15",
        "CoreMagic": "EX25IMMUT32CORE7617",
        "CoreMagicRaw": "CoreRealm:CoreVersion:CoreMagic",
        "CoreAuthor": "Gunther Voet"
    }

# 2. Dynamically build the magic tag matching your structural rules
_magic_raw_template = str(_meta.get("CoreMagicRaw", "CoreRealm:CoreVersion:CoreMagic"))
try:
    _fields = _magic_raw_template.split(":")
    _magic_tag = ":".join([str(_meta.get(_field, "UNKNOWN")) for _field in _fields])
except Exception:
    _magic_tag = "Existenz:v0.76.15:EX25IMMUT32CORE7617"

# 3. Compute live token and signature hashes on the fly from the JSON keys
_dynamic_token_hash = hashlib.sha256(_magic_tag.encode("utf-8")).hexdigest()
_live_author = str(_meta.get("CoreAuthor", "Gunther Voet"))
_chain_seed_string = f"{_dynamic_token_hash}:{_live_author}"
_dynamic_signature_hash = hashlib.sha256(_chain_seed_string.encode("utf-8")).hexdigest()

# 4. Populate headers keeping 1:1 backward compatibility with your binary keys
_HEADER = {
    "REALM":   str(_meta.get("CoreRealm", "Existenz")).encode(),
    "VERSION": str(_meta.get("CoreVersion", "v0.76.15")).encode(),
    "SECRET":  str(_meta.get("CoreMagic", "EX25IMMUT32CORE7617")).encode()
}

class existenzMeta:
    HEADER = _HEADER
    MAGIC = {
        "RAW_TEMPLATE": _magic_raw_template,
        "RAW":          _magic_tag,
        "TOKEN":        _dynamic_token_hash,
        "SIGNATURE":    _dynamic_signature_hash
    }
    META = {
        "AUTHOR":       _live_author
    }

# Clean up local temporary builder scope variables safely
del _current_dir, _schema_path, _blueprint_data, _meta, _magic_raw_template, _fields, _magic_tag, _dynamic_token_hash, _live_author, _chain_seed_string, _dynamic_signature_hash, _HEADER

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
        "Schema":        "master/struct/existentialCoreSchema.json",        
        "Cores":         "master/existentialCores.json",
        "Core":          "master/existentialCore.py",
        "Check":         "master/existentialCoreCheck.py",
        "Threat":        "master/existentialCoreThreat.py",
        "SignaturesPy":  "master/existentialSignatures.py",
        "SignaturesJson":  "master/existentialSignatures.json"
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
        "Manifest":          "manifest.json"
    }
}

existenzPublicKeys = (
    ("Environment", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16,  7,  31,  existenzConfig.FINGERPRINT["Environment"]),
    ("Platform",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",         32, 14,  46,  existenzConfig.FINGERPRINT["Platform"]),
    ("Developer",   "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net", 64,  8,  78,  existenzConfig.FINGERPRINT["Developer"]),
    ("Personal",    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128,  8, 142,  existenzConfig.FINGERPRINT["Personal"])
)
