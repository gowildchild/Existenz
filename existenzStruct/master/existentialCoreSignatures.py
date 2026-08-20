# ==========================================================================
# EXISTENZ Platform v0.76i (Private Key Signer)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
# The glue, immutability,  protection part for a zero trust world.

existentialCoreVersion                       = "v0.76i"
existentialCoreCheckMagic                    = b"EX25IMMUT32CORE7617"
existentialCoreCheckSignature                = "b45624fc09463f05d2e9359db32ae928e084aa81e47bbd33ecde0a58d66d0656"

class existentialCoreSignatures:
    existentialCore                              = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e"
    existentialCoreThreatRoot                    = "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca"
    existentialCoreThreatLegal                   = "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1"
    existentialCoreThreat                        = "90f9d7438a0497f54dbe065a64f5f5c111dee8c1184832c280d96c0bd2226689"
    existentialCoreCheck                         = "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c"

    existentialPublicKeys = (
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    )

    existentialCoreSigned = (
        ("Magic", "existentialCoreMagicSig", "existentialCoreMagicHash", "existentialCoreMagicSignature", 60, 0),
        ("Core", "existentialCoreSign", "existentialCoreHash", "existentialCoreSignature", 126, 0),
        ("CoreCheck", "existentialCoreCheckSign", "existentialCoreCheckHash", "existentialCoreCheckSignature", 62, 0),
        ("CoreThreatStruct", "existentialCoreThreatStructSign", "existentialCoreThreatStructHash", "existentialCoreThreatStructSignature", 31, 1),
        ("CoreThreatLegal", "existentialCoreThreatLegalSign", "existentialCoreThreatLegalHash", "existentialCoreThreatLegalSignature", 31, 2),
        ("CoreThreat", "existentialCoreThreatSign", "existentialCoreThreatHash", "existentialCoreThreatSignature", 127, 3),
        ("CoreChain", "existentialCoreChainSign", "existentialCoreChainHash", "existentialCoreChainSignature", 255, 9)
    )
