# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.21 | Github Deployment
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
        "Version": "Existenz:v0.76.21",
        "Update":  "20260912 17:36"
    },
    "PublicKeys": (
        ("Environment"  , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16),
        ("Platform"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",  32),
        ("Developer"    , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net",  64),
        ("Personal"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128)
    ),
    "Signatures": (
        ("existentialCoreThreat"               ,   3327, "48a4c574379c6fe9a2a27d005a4fcef50b1d2443f3385c9255515ce98de8561c", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatLegal"          ,   3326, "954792f0c8b2097ca8bd6c878c9def378df9e069beb9484f35e09c3dbb4df0b5", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatShadowVacuum"   ,   3326, "d5ef39294f99e9e4994517d2f8026b233b852bda8eaee0dd90c58b24a4a60853", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreThreatChained"        ,   3582, "4d224d1578b5690fd307753780d0db2d595e42ed5085918aec7a7e62290ed1f4", "PENDING_PRIVATE_KEY_SIGNATURE")
    )
}
