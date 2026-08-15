# ==========================================================================
# EXISTENZ Platform v0.76g (Private Key Signer)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
# The glue, immutability,  protection part for a zero trust world.

existentialCoreVersion                       = "v0.76g"
existentialCoreCheckMagic                    = b"EX25IMMUT32CORE7617"
existentialCoreCheckSignature                = "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c"

class existentialCoreSignatures:
    existentialCore                              = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e"
    existentialCoreThreatRoot                    = "57c413f8531731df0d2f09a260ea36c7e49269348b553fdeeaa2dd11e7bc4bb9"
    existentialCoreThreatLegal                   = "6d07d97272d414f966ea7a9d7b2956b96541fecbcb9079f375408a62b3b6bd6e"
    existentialCoreThreat                        = "759533dfd2a276046bc62985b17df7cefb999a1c3a07b7b983e5ee278d80302d"
    existentialCoreCheck                         = "7c165b322566e304975917cdc92de03d3ab14e72d1edaefc2ea18f7444ac891c"

    existentialPublicKeys = (
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    )

    existentialCoreSigned = (
        ("Magic", "7faa8872", "existentialCoreMagicHash", "7faa88729e96e6a8795855c4e962d1cef3f9b8d2675819ba383f65e33daa0b9f6e46d27348e0670a6e4a90ebaf1266c3be28cf0412153501830d506c6f808909", 60, 0),
        ("Core", "1289de75", "existentialCoreHash", "1289de75fe9506e225779f2f9cfe530c231e81fd4b6d420ee657cfec6e6d3b3a7b0b009a2aad37b7549b8c81e972ff337b0db434f66a67e4d859ef7186467d07", 126, 0),
        ("CoreCheck", "7faa8872", "existentialCoreCheckHash", "7faa88729e96e6a8795855c4e962d1cef3f9b8d2675819ba383f65e33daa0b9f6e46d27348e0670a6e4a90ebaf1266c3be28cf0412153501830d506c6f808909", 62, 0),
        ("CoreThreatStruct", "cfac5173", "existentialCoreThreatStructHash", "cfac51731c4614745c0f3d6c867bb0f07b4f2c7144de8a26c0676c5ff93c2a92d64f11568b294e03d598aaf1fb0c647cc1f18cad0dc9e11ccb19054b76bf2c09", 31, 1),
        ("CoreThreatLegal", "afc8df8c", "existentialCoreThreatLegalHash", "afc8df8ce773f0a5dc492fcaf08686da15601de09ad58ed224284e2e96f5b29d17a4d4c1eb0eff3ed8863eea0e64af1c25be49999d3c5d6de552ad97dbe8ad09", 31, 2),
        ("CoreThreat", "158ca97c", "existentialCoreThreatHash", "158ca97cd218c2a45c1dcead0cf22ee4bfaf582ad02c5a74cd587059636331b0bd5a6043f9b27bd7c2b8889220aaaee1c9f49a730c79ae61a211633f05392f01", 127, 3),
        ("CoreChain", "7faa8872", "existentialCoreChainHash", "7faa88729e96e6a8795855c4e962d1cef3f9b8d2675819ba383f65e33daa0b9f6e46d27348e0670a6e4a90ebaf1266c3be28cf0412153501830d506c6f808909", 255, 9)
    )
