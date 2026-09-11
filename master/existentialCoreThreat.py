# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.20 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from enum import IntFlag

class existentialCoreThreat(IntFlag):
    THREAT_NONE                    = 0
    THREAT_EXISTENCE               = 1 << 0
    THREAT_AUTONOMY                = 1 << 1
    THREAT_INTEGRITY               = 1 << 2
    THREAT_PSYCHOLOGY              = 1 << 4
    THREAT_PHYSICAL                = 1 << 5
    THREAT_ABLEISM                 = 1 << 6
    THREAT_DEVELOPMENT             = 1 << 7
    THREAT_PROPERTY                = 1 << 8
    THREAT_PRESENCE                = 1 << 10
    THREAT_P_SAFE_OK               = 1 << 11
    THREAT_P_DURESS_OFF            = 1 << 12
    THREAT_USER_A                  = 1 << 14
    THREAT_USER_B                  = 1 << 15
    THREAT_USER_C                  = 1 << 16
    THREAT_RIGHTS_HUMAN            = 1 << 20
    THREAT_PRESENCE_SAFETY         = 1 << 21
    THREAT_RIGHTS_INCLUSIVE        = 1 << 22
    THREAT_RIGHTS_ASYLUM           = 1 << 23
    THREAT_RIGHTS_BASIC            = 1 << 24

existentialCoreThreatLegal = {
    existentialCoreThreat.THREAT_EXISTENCE: "LEGAL_CAT1_MURDER",
    existentialCoreThreat.THREAT_AUTONOMY: "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_INTEGRITY: "LEGAL_CAT3_COERCION",
    existentialCoreThreat.THREAT_PSYCHOLOGY: "LEGAL_CAT5_PSYCHOLOGICAL_INTIMIDATION",
    existentialCoreThreat.THREAT_PHYSICAL: "LEGAL_CAT2_PHYSICAL_VIOLATION",
    existentialCoreThreat.THREAT_ABLEISM: "LEGAL_CAT6_ABLEISM",
    existentialCoreThreat.THREAT_DEVELOPMENT: "LEGAL_CAT8_INTELLECTUAL_PIRACY",
    existentialCoreThreat.THREAT_PROPERTY: "LEGAL_CAT9_THEFT",
    existentialCoreThreat.THREAT_RIGHTS_HUMAN: "LEGAL_CAN3_HUMAN",
    existentialCoreThreat.THREAT_RIGHTS_INCLUSIVE: "LEGAL_CAN4_INCLUSION",
}

existentialCoreThreatShadowVacuum = {
    existentialCoreThreat.THREAT_EXISTENCE: "VACUUM_DEHUMANISATION",
    existentialCoreThreat.THREAT_AUTONOMY: "VACUUM_DISFRANCHISEMENT",
    existentialCoreThreat.THREAT_INTEGRITY: "VACUUM_CORRUPTION",
    existentialCoreThreat.THREAT_PSYCHOLOGY: "VACUUM_ATTRITION_PSYCHOLOGY",
    existentialCoreThreat.THREAT_PHYSICAL: "VACUUM_SOMATIC_DRAIN",
    existentialCoreThreat.THREAT_ABLEISM: "VACUUM_NEURONORMATIVITY",
    existentialCoreThreat.THREAT_DEVELOPMENT: "VACUUM_ATTRITION_INSTITUTIONAL",
    existentialCoreThreat.THREAT_PROPERTY: "VACUUM_SYSTEMIC_DESPOILMENT",
    existentialCoreThreat.THREAT_PRESENCE: "VACUUM_PANOPTICISM",
    existentialCoreThreat.THREAT_RIGHTS_HUMAN: "VACUUM_INVERT_COMPLIANCE",
    existentialCoreThreat.THREAT_RIGHTS_INCLUSIVE: "VACUUM_INVERT_NORMALIZATION",
    existentialCoreThreat.THREAT_RIGHTS_BASIC: "VACUUM_INVERT_INERTIA",
}

# ==========================================================================
# EXISTENZ IMMUTABLE INTEGRITY
# ==========================================================================
existenzIntegrity = {
    "existentialCoreThreat": {
        "Version": "Existenz:v0.76.20",
        "Update":  "20260911 18:05"
    },
    "PublicKeys": (
        ("Environment"  , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16),
        ("Platform"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",  32),
        ("Developer"    , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net",  64),
        ("Personal"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128)
    ),
    "Signatures": (
        ("existentialCoreThreatMeta"           ,   3581, "ae4e971368a64cd24d83215eb0f99dfe5d5730661734782460d75598dd232b06", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreat"               ,   3327, "437b7e65e075ae5536f8d358aa875c616015e265b4ed919d6a528d2b7b71ea29", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatLegal"          ,   3326, "4de26079eb1d3dc806b2b725b5d174dfb6bb0ee4fecdd4cf181221f96e8f7e57", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatShadowVacuum"   ,   3326, "6da055dcd10b920674ee114ed8050837174b838930e03e5dbf3fbd1464cef16d", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatSigned"         ,   3582, "ba2f11f792bf23128a8b210b2985e4e2ae7ffbb4393dcfc79ca32884f333bf77", "PENDING_PRIVATE_KEY_SIGNATURE")
    )
}
