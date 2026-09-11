# ==========================================================================
# EXISTENZ master/struct/engineSigningStruct.py 
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
from enum import IntFlag

from engineSigningMeta import existenzLocations, existenzMeta
from existentialSignatures import existentialToken

existenzIntegrityGlue = {
    "Magic":                  ( "existentialMagicSignature", 7671, 139777,  0x0100, existenzLocations["core"]["SignaturesPy"],  
                                                                               existentialToken.get("MAGIC", {}).get("SIGNATURE", "PENDING_SIGN")),
    "MagicCheck":             ( "existentialMagicToken",     7679, 139777,  0x0100, existenzLocations["core"]["SignaturesPy"],  
                                                                               existentialToken.get("MAGIC", {}).get("TOKEN", "PENDING_SIGN")),
    "Core":                   ( "existentialCore",           3327, 4625, 0x0201, existenzLocations["core"]["Core"],  
                                                                               existentialToken.get("master", {}).get("Core", "PENDING_SIGN")),
    "CorePolicy":             ( "existentialCorePolicy",     3326, 4626, 0x0202, existenzLocations["core"]["Core"],
                                                                               existentialToken.get("master", {}).get("CorePolicy", "PENDING_SIGN")),
    "CoreBitmask":            ( "existentialCoreBitmask",    3326, 4626, 0x0203, existenzLocations["core"]["Core"],
                                                                               existentialToken.get("master", {}).get("CoreBitmask", "PENDING_SIGN")),    
    "CoreChain":              ( "existentialCoreChain",      3582, 4642,  0x0204, existenzLocations["core"]["Core"],
                                                                               existentialToken.get("master", {}).get("CoreChain", "PENDING_SIGN")),   
    "CoreThreat":             ( "existentialCoreThreat",     3327, 4641, 0x0301, existenzLocations["core"]["Threat"],
                                                                               existentialToken.get("master", {}).get("Threat", "PENDING_SIGN")),
    "CoreThreatLegal":        ( "existentialCoreThreatLegal",3326, 4642, 0x0302, existenzLocations["core"]["Threat"],
                                                                               existentialToken.get("master", {}).get("ThreatLegal", "PENDING_SIGN")),
    "CoreThreatShadowVacuum": ( "existentialCoreThreatShadowVacuum", 3326, 4642, 0x0303, existenzLocations["core"]["Threat"],
                                                                               existentialToken.get("master", {}).get("ThreatShadowVacuum", "PENDING_SIGN")),
    "CoreThreatSigned":       ( "existentialCoreThreatSigned",3582, 4642,  0x0304, existenzLocations["core"]["Threat"],
                                                                               existentialToken.get("master", {}).get("ThreatSigned", "PENDING_SIGN")),       
    "CoreCheck":              ( "existentialCoreCheck",      3583, 4865, 0x0700, existenzLocations["core"]["Check"],  
                                                                               existentialToken.get("master", {}).get("Check", "PENDING_SIGN")),
    "Cores":                  ( "existentialCores",          3583, 5250, 0x0800, existenzLocations["core"]["Cores"],
                                                                               existentialToken.get("master", {}).get("Cores", "PENDING_SIGN")),
    "Schema":                 ( "existentialCoreSchema",      246, 9224, 0x0900, existenzLocations["core"]["Schema"],
                                                                               existentialToken.get("master", {}).get("Schema", "PENDING_SIGN")),  
    "CircleDist":             ( "existentialCircleDist",     2615, 33860,   0xF02F, existenzLocations["manifest"]["dist"],
                                                                               existentialToken.get("manifest", {}).get("dist", "PENDING_SIGN")),
    "CircleTools":            ( "existentialCircleTools",    2614, 33860,   0xF03F, existenzLocations["manifest"]["tools"],
                                                                               existentialToken.get("manifest", {}).get("tools", "PENDING_SIGN")),
    "CircleBuild":            ( "existentialCircleBuild",    2614, 33860,  0xF04F, existenzLocations["manifest"]["build"],
                                                                               existentialToken.get("manifest", {}).get("build", "PENDING_SIGN")),
    "CircleMaster":           ( "existentialCircleMaster",   2614, 33860,  0xF05F, existenzLocations["manifest"]["master"],
                                                                               existentialToken.get("manifest", {}).get("master", "PENDING_SIGN")),
    "CircleChain":            ( "existentialCircleSigned",   2870, 33860,  0xF09F, existenzLocations["engine"]["Manifest"],
                                                                               existentialToken.get("engine", {}).get("Manifest", "PENDING_SIGN"))
}

existenzStructureGlue = {
    "KeysPublic":             ( "existenzPublicKeys",           16887, 8705, 0x00, existenzLocations["engine"]["signingMeta"], 
                                                                               existentialToken.get("structs", {}).get("KeysPublic", "PENDING_SIGN")),
    "Config":                 ( "existenzConfig",               8695, 9217, 0x00, existenzLocations["engine"]["signingMeta"], 
                                                                               existentialToken.get("structs", {}).get("Config", "PENDING_SIGN")),
    "Locations":              ( "existenzLocations",            8695, 9217, 0x00, existenzLocations["engine"]["signingMeta"], 
                                                                               existentialToken.get("structs", {}).get("Locations", "PENDING_SIGN")),
    "Steps":                  ( "existenzSteps",                3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("Steps", "PENDING_SIGN")),
    "IntegrityReq":           ( "existenzIntegrityRequirements", 3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("IntegrityReq", "PENDING_SIGN")),
    "KeysHandler":            ( "existenzIntegrityKeysHandler", 3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("KeysHandler", "PENDING_SIGN")),
    "KeysIO":                 ( "existenzIntegrityKeysIO",      3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("KeysIO", "PENDING_SIGN")),
    "KeyStatus":              ( "existenzIntegrityKeyStatus",   3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("KeyStatus", "PENDING_SIGN")),
    "IntegrityState":         ( "existenzIntegrityState",       3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("IntegrityState", "PENDING_SIGN")),
    "CorePolicy":             ( "existenzCorePolicy",           3575, 8705, 0x00, existenzLocations["engine"]["signingStruct"], 
                                                                               existentialToken.get("structs", {}).get("CorePolicy", "PENDING_SIGN"))
}

class existenzIntegrityKeysHandler(IntFlag):
    """Opcode execution instructions governing the cryptographic pipeline."""
    SIGN_CHAIN_START     = 1
    SIGN_MAGIC_HASH      = 2
    SIGN_TYPE_COMMIT     = 4
    SIGN_TO_FILES        = 8
    SIGN_PVT_ENVIRONMENT = 16
    SIGN_PVT_PLATFORM    = 32
    SIGN_PVT_DEVELOPER   = 64
    SIGN_PVT_PERSONAL    = 128
    SIGN_CHAIN_END       = 256
    SIGN_TYPE_FILE       = 512
    SIGN_TYPE_KEYS       = 1024
    SIGN_TYPE_VALUES     = 2048
    SIGN_TYPE_STRING     = 4096
    SIGN_TYPE_DICT       = 8192
    SIGN_TYPE_TUPLE      = 16384
    SIGN_TYPE_GROUP      = 32768

class existenzIntegrityRequirements(IntFlag):
    """Opcode execution instructions governing the processes required before possible to enter data."""
    REQ_INIT             = 1
    REQ_BUILD            = 2
    REQ_PRE              = 4
    REQ_FILE             = 8
    REQ_CORE             = 16
    REQ_THREAT           = 32
    REQ_SIGNATURES       = 64
    REQ_CORES            = 128
    REQ_CORECHECK        = 256
    REQ_FORMAT_PYTHON    = 512
    REQ_FORMAT_JSON      = 1024
    REQ_LOC_MASTER       = 4096
    REQ_LOC_STRUCT       = 8192
    REQ_LOC_BUILD        = 16384
    REQ_LOC_DIST         = 32768        
    REQ_LOC_TOOLS        = 64535
    REQ_SIGNATURE        = 131072


class existenzSignatures:
    existentialImmutable = ()
    existentialCore = (
        ("Magic",                  existenzIntegrityGlue["Magic"],                  0),
        ("Core",                   existenzIntegrityGlue["Core"],                   0),
        ("CoreCheck",              existenzIntegrityGlue["CoreCheck"],              0),
        ("Cores",                  existenzIntegrityGlue["Cores"],                  2),
        ("Schema",                 existenzIntegrityGlue["Schema"],                 3),
        ("CoreThreat",             existenzIntegrityGlue["CoreThreat"],             6),
        ("CoreThreatLegal",        existenzIntegrityGlue["CoreThreatLegal"],        7),
        ("CoreThreatShadowVacuum", existenzIntegrityGlue["CoreThreatShadowVacuum"], 8),
        ("CoreThreatSigned",       existenzIntegrityGlue["CoreThreatSigned"],        9)
    )

    existentialStructures   = (
    )
    
    existentialManifest = (
        ("Magic",                  existenzIntegrityGlue["Magic"],                  0),
        ("CircleDist",             existenzIntegrityGlue["CircleDist"],             1),
        ("CircleTools",            existenzIntegrityGlue["CircleTools"],            2),
        ("CircleBuild",            existenzIntegrityGlue["CircleBuild"],            3),
        ("CircleMaster",           existenzIntegrityGlue["CircleMaster"],           4),
        ("CircleChain",            existenzIntegrityGlue["CircleChain"],            9)
    )

class existenzSteps(IntFlag):
    STEP_NONE               = 0
    STEP_TEST               = 1
    STEP_INIT               = 2
    STEP_COMMIT             = 4
    STEP_MANIFEST           = 8
    STEP_INTEGRITY          = 16
    STEP_VERIFY             = 32
    STEP_SIGN_PUBLIC        = 64
    STEP_SIGN_ENVIRONMENT   = 128
    STEP_SIGN_PRIVATE       = 256
    STEP_SIGN_WAITING       = 512
    STEP_SIGN_SUCCESS       = 1024
    STEP_VERITAS            = 8192
    STEP_BUILD_DIST         = 16384
    STEP_BUILD_TOOLS        = 32768
    STEP_BUILD_BUILD        = 65536
    STEP_BUILD_MASTER       = 131072
    STEP_BUILD_SUCCESS      = 262144
    STEP_SUCCESS            = 524288  # FIXED: Added definition matching power-of-two bits

existenzStepsSeq = [
    existenzSteps.STEP_TEST,
    existenzSteps.STEP_INIT,
    existenzSteps.STEP_COMMIT,
    existenzSteps.STEP_MANIFEST,
    existenzSteps.STEP_INTEGRITY,
    existenzSteps.STEP_VERIFY,
    existenzSteps.STEP_SIGN_PUBLIC,
    existenzSteps.STEP_SIGN_ENVIRONMENT,
    existenzSteps.STEP_SIGN_PRIVATE,
    existenzSteps.STEP_SIGN_WAITING,  # FIXED: Restored to step timeline track
    existenzSteps.STEP_SIGN_SUCCESS,
    existenzSteps.STEP_VERITAS,    
    existenzSteps.STEP_BUILD_DIST,
    existenzSteps.STEP_BUILD_TOOLS,
    existenzSteps.STEP_BUILD_BUILD,
    existenzSteps.STEP_BUILD_MASTER,
    existenzSteps.STEP_BUILD_SUCCESS,
    existenzSteps.STEP_SUCCESS
]

class existenzCorePolicy(IntFlag):
    CORE_NONE               = 0
    CORE_PILLAR             = 1      # is CORE Pillar (immutable)
    CORE_RIGHTS             = 2      # is CORE Rights (immutable)
    CORE_INTEGRITY          = 8      # Is a hash or signature
    CORE_CANARY             = 16     # Is a Canary Bird
    CORE_WATCHDOG           = 32     # Will always be reported by CORE
    USER_CANARY             = 64     # User can enable/disable canary
    USER_CUSTOMIZE          = 256    # Can be customized by user
    USER_READ               = 512    # Can be read/subscribed to by user
    USER_UPDATE             = 1024   # Can be updated/changed by user
    USER_DISABLE            = 2048   # Can be removed/disabled by user
    BIT_MASK                = 4096   # Field has bitmask (for canaries)
    BIT_SHIFT               = 8192   # Standard Left Shift (1 << x)
    BIT_SHIFT_RIGHT         = 16384  # Arithmetic Right Shift (x >> y)
    BIT_ZERO_FILL_RIGHT     = 32768  # Logical Right Shift (x >>> y)
    BIT_ROTATE_LEFT         = 65536  # Circular Left Rotation
    BIT_ROTATE_RIGHT        = 131072 # Circular Right Rotation
    CORE_IMMUTABLE          = 262144 # Pushed high to clear space

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
    KEY_STATE_SUCCESS      = 2048
    KEY_STATE_FAIL         = 4096
    
    KEY_IN_ENVIRONMENT     = KEY_IS_PUBLIC      | KEY_PVT_ENVIRONMENT
    KEY_OK_ENVIRONMENT     = KEY_IN_ENVIRONMENT | KEY_IS_COMMITTED
    KEY_DONE_ENVIRONMENT   = KEY_OK_ENVIRONMENT | KEY_STATE_SUCCESS

    KEY_IS_PLATFORM        = KEY_IS_PRIVATE     | KEY_PVT_PLATFORM
    KEY_OK_PLATFORM        = KEY_IS_PLATFORM    | KEY_IS_COMMITTED
    KEY_DONE_PLATFORM      = KEY_OK_PLATFORM    | KEY_STATE_SUCCESS
    
    KEY_IS_DEVELOPER       = KEY_IS_PRIVATE     | KEY_PVT_DEVELOPER
    KEY_OK_DEVELOPER       = KEY_IS_DEVELOPER   | KEY_IS_COMMITTED
    KEY_DONE_DEVELOPER     = KEY_OK_DEVELOPER   | KEY_STATE_SUCCESS
    
    KEY_IS_PERSONAL        = KEY_IS_PRIVATE     | KEY_PVT_PERSONAL
    KEY_OK_PERSONAL        = KEY_IS_PERSONAL    | KEY_IS_COMMITTED
    KEY_DONE_PERSONAL      = KEY_OK_PERSONAL    | KEY_STATE_SUCCESS

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

