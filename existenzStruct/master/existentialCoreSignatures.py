# ==========================================================================
# THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
# Version: v0.76 | Framework Namespace Lock
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

existentialCoreVersion                       = "v0.76.13"
existentialCoreCheckMagic                    = b"EX25IMMUT32CORE7617"
existentialCoreCheckSignatures               = "8b4defb0aaf1eb9bcd7b382cf0b4db0aa093eb1b84b8e09d3cf0f73d5b2d37b6"

class existentialCoreSignatures:
    existentialCore                              = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e"
    existentialCoreThreatRoot                    = "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca"
    existentialCoreThreatLegal                   = "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1"
    existentialCoreThreatShadowVacuum            = "9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69"
    existentialCoreThreat                        = "23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3"
    existentialCoreCheck                         = "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"
    existentialCores                             = "18d3aeb347a36d7033dd2555b7ddfdde67b289e662ff2c6a8fb03d9562063ab6"

    existentialPublicKeys = (
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    )

    existentialCoreSigned = (
        ("Magic", "11c39300", "existentialCoreMagicHash", "11c393009d3f0dca9fc83c0c76c02a89737cfffbbcbb974cf2632d8d797e4dd42616ec3b8b625718314bbc146792259884300beae923af01cc26ab6713472308", 60, 0),
        ("Core", "1289de75", "existentialCoreHash", "1289de75fe9506e225779f2f9cfe530c231e81fd4b6d420ee657cfec6e6d3b3a7b0b009a2aad37b7549b8c81e972ff337b0db434f66a67e4d859ef7186467d07", 126, 0),
        ("CoreCheck", "11c39300", "existentialCoreCheckHash", "11c393009d3f0dca9fc83c0c76c02a89737cfffbbcbb974cf2632d8d797e4dd42616ec3b8b625718314bbc146792259884300beae923af01cc26ab6713472308", 62, 0),
        ("CoreThreatStruct", "aa808a1f", "existentialCoreThreatStructHash", "aa808a1f4a6f73281378d2875fda658f0866048da37419013c0ebfd846a14a0fda859c5d6d657ce2ab1efec0c07d83320d7d4d437a4aee01e1c83d7893675903", 31, 2),
        ("CoreThreatLegal", "cf73b021", "existentialCoreThreatLegalHash", "cf73b021381f426ad53910a83a1a5ce15ab6c3ea200e6e6818a805ca22328b13c7aacfc8a9cb5083abd633687e7693cc2c38310d026a36e59dfbd75cf592eb0b", 31, 3),
        ("CoreThreatShadowVacuum", "4f42af6a", "existentialCoreThreatShadowVacuumHash", "4f42af6a6be5078c95f186936058f8872553d523879b287e575f77e4180e4fc9a215e6bb30a6fd744ed85880945c133509ecf318ce4ca79caad6b7e1a50c1d01", 31, 4),
        ("CoreThreat", "79b1e69e", "existentialCoreThreatHash", "79b1e69ed3a999fc6ed1d92c92f90f920d1052c4b5d93d17bed0ec90ed0bac6833aaa16301c843f70ac7a959e462a1efccbdb7958b610501d9f7c4c4bb07200b", 127, 5),
        ("Cores", "existentialCoresSign", "existentialCoresHash", "existentialCoresSignature", 31, 7),
        ("CoreChain", "11c39300", "existentialCoreChainHash", "11c393009d3f0dca9fc83c0c76c02a89737cfffbbcbb974cf2632d8d797e4dd42616ec3b8b625718314bbc146792259884300beae923af01cc26ab6713472308", 255, 9)
    )
