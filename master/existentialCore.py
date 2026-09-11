# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.20 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

from enum import IntFlag

class existentialCore(IntFlag):
    NONE                           = 0  # No Record
    EXISTENCE                      = 1 << 0  # You, alive, with a body
    AUTONOMY                       = 1 << 1  # The Sovereign Right to Choose
    INTEGRITY                      = 1 << 2  # The Moral Axis of Personal Choice
    CANARY_1_SOVEREIGN             = 1 << 3  # WATCHDOG_SOVEREIGN
    PSYCHOLOGY                     = 1 << 4  # Cognitive Mental State and Peace
    PHYSICAL                       = 1 << 5  # Physical Body Vessel and bio-state
    DISABILITY                     = 1 << 6  # Nature's way of checks and balances
    DEVELOPMENT                    = 1 << 7  # Evolutionary, Intellectual, Growth
    PROPERTY                       = 1 << 8  # Material Assets and Income Protection
    CANARY_2_SOMATIC               = 1 << 9  # WATCHDOG_SOMATIC
    PRESENCE                       = 1 << 10  # Real-Time Spacetime Footprint
    CANARY_P_SAFE                  = 1 << 11  # WATCHDOG_PRESENCE_SAFE
    CANARY_P_DURESS                = 1 << 12  # WATCHDOG_PRESENCE_NO_DURESS
    CANARY_3_ABLEISM               = 1 << 13  # WATCHDOG_ABLEISM
    CANARY_USER_A                  = 1 << 14  # WATCHDOG_USER_DEFINABLE_A
    CANARY_USER_B                  = 1 << 15  # WATCHDOG_USER_DEFINABLE_B
    CANARY_USER_C                  = 1 << 16  # WATCHDOG_USER_DEFINABLE_C
    CANARY_4_FOOTPRINT             = 1 << 17  # WATCHDOG_FOOTPRINT
    CANARY_IV_PRESENCE             = 1 << 18  # WATCHDOG_PRESENCE_OK
    SHIELD_RIGHTS_HUMAN            = 1 << 20  # SHIELD-A (Institutional)
    CANARY_P_SAFETY                = 1 << 21  # WATCHDOG_PRESENCE_SAFETY
    SHIELD_RIGHTS_INCLUSIVE        = 1 << 22  # SHIELD-A2 (Systemic)
    SHIELD_RIGHTS_ASYLUM           = 1 << 23  # SHIELD-A3 (Asylum Seekers)
    SHIELD_RIGHTS_BASIC            = 1 << 24  # SHIELD-B (Institutional)
    CANARY_5_METRICS               = 1 << 25  # WATCHDOG_METRICS
    CANARY_V_RIGHTS                = 1 << 26  # WATCHDOG_RIGHTS
    CANARY_VI_SYSTEMIC             = 1 << 29  # WATCHDOG_SYSTEMIC
    CANARY_6_IMMUTABLE             = 1 << 31  # WATCHDOG_IMMUTABLE

    IMMUTABLE_PILLARS = (
        EXISTENCE |
        AUTONOMY |
        INTEGRITY |
        PSYCHOLOGY |
        PHYSICAL |
        DISABILITY |
        DEVELOPMENT |
        PROPERTY |
        PRESENCE
    )

    IMMUTABLE_RIGHTS = (
        SHIELD_RIGHTS_HUMAN |
        SHIELD_RIGHTS_INCLUSIVE |
        SHIELD_RIGHTS_BASIC |
        SHIELD_RIGHTS_ASYLUM
    )

existentialCoreBitmask = {
    existentialCore.CANARY_1_SOVEREIGN       : "0x7",
    existentialCore.CANARY_2_SOMATIC         : "0x3f",
    existentialCore.CANARY_3_ABLEISM         : "0x27f",
    existentialCore.CANARY_4_FOOTPRINT       : "0x33f",
    existentialCore.CANARY_IV_PRESENCE       : "0x7ff",
    existentialCore.CANARY_P_SAFETY          : "0x63fff",
    existentialCore.CANARY_5_METRICS         : "0x263fff",
    existentialCore.CANARY_V_RIGHTS          : "0x3f63fff",
    existentialCore.CANARY_VI_SYSTEMIC       : "0xc000",
    existentialCore.CANARY_6_IMMUTABLE       : "0x26262208",
}

existentialCorePolicy = {
    existentialCore.NONE                     : "0x422c1",
    existentialCore.EXISTENCE                : "0x422c1",
    existentialCore.AUTONOMY                 : "0x422c1",
    existentialCore.INTEGRITY                : "0x422c1",
    existentialCore.CANARY_1_SOVEREIGN       : "0x43230",
    existentialCore.PSYCHOLOGY               : "0x422c1",
    existentialCore.PHYSICAL                 : "0x422c1",
    existentialCore.DISABILITY               : "0x422c1",
    existentialCore.DEVELOPMENT              : "0x422c1",
    existentialCore.PROPERTY                 : "0x422c1",
    existentialCore.CANARY_2_SOMATIC         : "0x43230",
    existentialCore.PRESENCE                 : "0x422c1",
    existentialCore.CANARY_P_SAFE            : "0x3fc0",
    existentialCore.CANARY_P_DURESS          : "0x3fc0",
    existentialCore.CANARY_3_ABLEISM         : "0x43230",
    existentialCore.CANARY_USER_A            : "0x1fc4",
    existentialCore.CANARY_USER_B            : "0x1fc4",
    existentialCore.CANARY_USER_C            : "0x1fc4",
    existentialCore.CANARY_4_FOOTPRINT       : "0x43230",
    existentialCore.CANARY_IV_PRESENCE       : "0x43230",
    existentialCore.SHIELD_RIGHTS_HUMAN      : "0x422c2",
    existentialCore.CANARY_P_SAFETY          : "0x3fc0",
    existentialCore.SHIELD_RIGHTS_INCLUSIVE  : "0x422c2",
    existentialCore.SHIELD_RIGHTS_ASYLUM     : "0x422c2",
    existentialCore.SHIELD_RIGHTS_BASIC      : "0x422c2",
    existentialCore.CANARY_5_METRICS         : "0x43230",
    existentialCore.CANARY_V_RIGHTS          : "0x43230",
    existentialCore.CANARY_VI_SYSTEMIC       : "0x43230",
    existentialCore.CANARY_6_IMMUTABLE       : "0x43230",
}

# ==========================================================================
# EXISTENZ IMMUTABLE INTEGRITY
# ==========================================================================
existenzIntegrity = {
    "existentialCore": {
        "Version": "Existenz:v0.76.20",
        "Update":  "20260911 20:08"
    },
    "PublicKeys": (
        ("Environment"  , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPjuPmZWZS4tAjCxF1FkKtMfEroVnEThd+IIMXws9swd existenz-dev-gh@xsrv.net",  16),
        ("Platform"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net",  32),
        ("Developer"    , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net",  64),
        ("Personal"     , "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net", 128)
    ),
    "Signatures": (
        ("existentialCore"                     ,   3327, "76a3ef007f8c735e28e582c90ef017061621f401a7138d992f47030005cc95ff", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreBitmask"              ,   3326, "2263f32f11f95084c7560c2ce5013fe9cffa3b4cc16638c9037742edf4f0675d", "PENDING_PRIVATE_KEY_SIGNATURE"),
        ("existentialCoreChained"              ,   3582, "24e3bd7dac27419db91e39025600d9b0dfeda3555bb841fbb8942528db3ac30e", "PENDING_PRIVATE_KEY_SIGNATURE")
    )
}
