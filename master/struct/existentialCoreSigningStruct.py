# ==========================================================================
# EXISTENZ Existential build-tools & libraries (engineStructure.py v0.76.16)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
from enum import IntFlag

from existentialCoreSigning import existenzLocations, existenzSigned

existenzIntegrityStructure = {
    "Magic":                  (
        "existentialMagicSignature", 3583, 118,  0x00, existenzLocations["core"]["Signatures"],  existenzSigned.MAGIC["SIGNATURE"]),
    "MagicCheck":             (
        "existentialMagicToken",     3575, 110,  0x00, existenzLocations["core"]["Signatures"],  existenzSigned.MAGIC["TOKEN"]),
    "Core":                   (
        "existentialCore",           3575, 1790, 0x00, existenzLocations["core"]["Core"],  existenzSigned.CORE["existentialCore"]),
    "CoreCheck":              (
        "existentialCoreCheck",      3575, 4222, 0x00, existenzLocations["core"]["Check"],  existenzSigned.CORE["existentialCoreCheck"]),
    "Cores":                  (
        "existentialCores",          3575, 1558, 0x01, existenzLocations["core"]["Cores"],  existenzSigned.CORE["existentialCores"]),
    "CoreThreat":             (
        "existentialCoreThreat",     3575, 1599, 0x02, existenzLocations["core"]["Threat"],  existenzSigned.CORE["existentialCoreThreat"]),
    "CoreThreatLegal":        (
        "existentialCoreThreatLegal",3575, 1599, 0x03, existenzLocationsp["core"]["Threat"],  existenzSigned.CORE["existentialCoreThreatLegal"]),
    "CoreThreatShadowVacuum": (
        "existentialCoreThreatShadowVacuum", 3575, 1599, 0x04, existenzLocations["core"]["Threat"],  existenzSigned.CORE["existentialCoreThreatShadowVacuum"]),
    "CoreThreatChain":        (
        "existentialCoreThreatChain",3583, 382,  0x05, existenzLocations["core"]["Threat"], existenzSigned.CORE["existentialCoreThreatChain"]),
    "CoreSigned":             (
        "existentialCoreSigned",     3583, 511,  0x09, existenzLocations["core"]["Signatures"],  existenzSigned.CORE["existentialCore"]),
    "CircleDist":             (
        "existentialCircleDist",     2615, 23,   0x2F, existenzLocations["manifest"]["dist"],  existenzSigned.CIRCLE["CircleDist"]),
    "CircleTools":            (
        "existentialCircleTools",    2814, 22,   0x3F, existenzLocations["manifest"]["tools"],  existenzSigned.CIRCLE["CircleTools"]),
    "CircleBuild":            (
        "existentialCircleBuild",    2815, 126,  0x4F, existenzLocations["manifest"]["build"],  existenzSigned.CIRCLE["CircleBuild"]),
    "CircleMaster":           (
        "existentialCircleMaster",   2815, 255,  0x5F, existenzLocations["manifest"]["master"],  existenzSigned.CIRCLE["CircleMaster"]),
    "CircleChain":            (
        "existentialCircleSigned",   3839, 511,  0x9F, existenzLocations["manifest"]["manifest"],  existenzSigned.CHAIN["CORE"])
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

class existenzIntegrityKeyStatus(IntFlag):
    """Bitmask operated registration flags for public/private key verification states."""
    KEY_NONE               = 0
    KEY_IS_PUBLIC          = 1
    KEY_IS_VERIFIED        = 2
    KEY_IS_COMMITTED       = 4
    KEY_IS_PRIVATE         = 8
    KEY_PVT_ENVIRONMENT    = 16
    KEY_PVT_PLATFORM       = 32
    KEY_PVT_DEVELOPER      = 64
    KEY_PVT_PERSONAL       = 128
    KEY_OK_HASHED          = 256
    KEY_IS_CHAINED         = 512
    KEY_STATE_WAIT         = 1024
    KEY_STATE_SUCCES       = 2048
    KEY_STATE_FAIL         = 4096
    
    KEY_IN_ENVIRONMENT     = KEY_IS_PUBLIC      | KEY_PVT_ENVIRONMENT
    KEY_OK_ENVIRONMENT     = KEY_IN_ENVIRONMENT | KEY_IS_COMMITTED
    KEY_DONE_ENVIRONMENT   = KEY_OK_ENVIRONMENT | KEY_STATE_SUCCES

    KEY_IS_PLATFORM        = KEY_IS_PRIVATE     | KEY_PVT_PLATFORM
    KEY_OK_PLATFORM        = KEY_IS_PLATFORM    | KEY_IS_COMMITTED
    KEY_DONE_PLATFORM      = KEY_OK_PLATFORM    | KEY_STATE_SUCCES
    
    KEY_IS_DEVELOPER       = KEY_IS_PRIVATE     | KEY_PVT_DEVELOPER
    KEY_OK_DEVELOPER       = KEY_IS_DEVELOPER   | KEY_IS_COMMITTED
    KEY_DONE_DEVELOPER     = KEY_OK_DEVELOPER   | KEY_STATE_SUCCES
    
    KEY_IS_PERSONAL        = KEY_IS_PRIVATE     | KEY_PVT_PERSONAL
    KEY_OK_PERSONAL        = KEY_IS_PERSONAL    | KEY_IS_COMMITTED
    KEY_DONE_PERSONAL      = KEY_OK_PERSONAL    | KEY_STATE_SUCCES

class existenzIntegrityKeysHandler(IntFlag):
    """Opcode execution instructions governing the cryptographic pipeline."""
    SIGN_CHAIN_START     = 1
    SIGN_MAGIC_HASH      = 2
    SIGN_TYPE_COMMIT     = 4
    SIGN_TYPE_PRIVATE    = 8
    SIGN_PVT_ENVIRONMENT = 16
    SIGN_PVT_PLATFORM    = 32
    SIGN_PVT_DEVELOPER   = 64
    SIGN_PVT_PERSONAL    = 128
    SIGN_CHAIN_END       = 256
    SIGN_TYPE_FILE       = 512
    SIGN_TYPE_KEYS       = 1025
    SIGN_TYPE_VALUES     = 2048
    SIGN_TYPE_STRING     = 4096

class existenzIntegrityKeysIO(IntFlag):
    """IO tracking bitcodes defining directory and file storage boundaries."""
    FILE_CREATE            = 1
    FILE_READ              = 2
    FILE_UPDATE            = 4
    FILE_DELETE            = 8
    FILE_WRITE_VERIFIED    = 16
    FILE_NEEDS_AUDITED     = 32
    FILE_NEEDS_HUMAN       = 64
    FILE_NEEDS_KEY         = 128
    FILE_IN_CORE           = 256
    FILE_IN_MANIFEST       = 512
    FILE_IN_SIGNATURES     = 1024
    FILE_IS_REQUIRED       = 2048

class existenzIntegrityState(IntFlag):
    STATE_NEW                 = existenzIntegrityKeysIO.FILE_CREATE
    STATE_READ                = existenzIntegrityKeysIO.FILE_READ
    STATE_UPDATED             = existenzIntegrityKeysIO.FILE_UPDATE
    STATE_WRITE               = existenzIntegrityKeysIO.FILE_WRITE_VERIFIED
    STATE_PROVISIONED         = existenzIntegrityKeysIO.FILE_WRITE_VERIFIED | existenzIntegrityKeysIO.FILE_UPDATE
    STATE_SIGN_HASH           = existenzIntegrityKeysIO.FILE_NEEDS_AUDITED
    STATE_SIGN_HUMAN          = existenzIntegrityKeysIO.FILE_NEEDS_HUMAN
    STATE_SUCCESS_PRIVATE     = existenzIntegrityKeysIO.FILE_NEEDS_KEY
    STATE_SUCCESS_CORE        = existenzIntegrityKeysIO.FILE_IN_CORE
    STATE_SUCCESS_MANIFEST    = existenzIntegrityKeysIO.FILE_IN_MANIFEST
    STATE_SUCCESS_SIGNATURES  = existenzIntegrityKeysIO.FILE_IN_SIGNATURES
    STATE_SUCCESS_DONE        = existenzIntegrityKeysIO.FILE_IS_REQUIRED

