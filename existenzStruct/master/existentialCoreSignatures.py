# ==========================================================================
# EXISTENZ CORE MASTER Private Key Signer v0.76.15
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

existentialCoreVersion                       = "v0.76.15"
existentialCoreCheckMagic                    = b"EX25IMMUT32CORE7617"
existentialCoreCheckSignature                = "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"

class existentialCoreSignatures:
    existentialCore                              = "22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e"
    existentialCores                             = "18d3aeb347a36d7033dd2555b7ddfdde67b289e662ff2c6a8fb03d9562063ab6"    
    existentialCoreThreatRoot                    = "1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca"
    existentialCoreThreatLegal                   = "931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1"
    existentialCoreThreatShadowVacuum            = "9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69"
    existentialCoreThreat                        = "23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3"
    existentialCoreCheck                         = "b36d1e03858491d3b12ddd1f4f3043458be6065befb6f25622475b8bc909fd85"

    existentialPublicKeys = (
        ("Platform", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net"),
        ("Developer", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net"),
        ("Personal", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net")
    )

    existentialCoreSigned = (
        ("Magic", "8be84a05", "existentialCoreMagicHash", "3762486323846fee46338ee354c51f8bd8cbb2f21fe935a71bed8737547a58ebd3afe665578fa4636258fd8414cc0043116897b08f332b78bcdf04033695ea06:9274683b92177e0d98c103cc455254ed81408bbe36e487a1933da77e393bcb6103b5945d46e9506f99670ca94713b1e090a544c2ce4040040db29e6013c97c05:8be84a05e863b1c741ebeeaaf46152c57dcbcbc7ee20e4e2260ca302a745679488dddc0002c32f732403178c1e01155c01e252a8f5fb503f67ccf015cd090c03", 60, 0),
        ("Core", "1289de75", "existentialCoreHash", "20cd9dfaa678b889aec0abd1c519a3d48889e7870fbdec76bcdac7d0a93edf86e3136df898f37b360387fd2ad0ae4218798d55513b9ea0279af781a1c8944e03:bc3cb76c41d37e5ce466f30ce67084fcad3f4b19198bb393918fc851beeda236aa623ca9594552c9112d91635dc836fbcb1aeb69e9cb681388adb2048c1aa501:1289de75fe9506e225779f2f9cfe530c231e81fd4b6d420ee657cfec6e6d3b3a7b0b009a2aad37b7549b8c81e972ff337b0db434f66a67e4d859ef7186467d07", 126, 0),
        ("Cores", "18d3aeb3", "existentialCoresHash", "3762486323846fee46338ee354c51f8bd8cbb2f21fe935a71bed8737547a58ebd3afe665578fa4636258fd8414cc0043116897b08f332b78bcdf04033695ea06:9274683b92177e0d98c103cc455254ed81408bbe36e487a1933da77e393bcb6103b5945d46e9506f99670ca94713b1e090a544c2ce4040040db29e6013c97c05:8be84a05e863b1c741ebeeaaf46152c57dcbcbc7ee20e4e2260ca302a745679488dddc0002c32f732403178c1e01155c01e252a8f5fb503f67ccf015cd090c03", 52, 1),
        ("CoreCheck", "8be84a05", "existentialCoreCheckHash", "3762486323846fee46338ee354c51f8bd8cbb2f21fe935a71bed8737547a58ebd3afe665578fa4636258fd8414cc0043116897b08f332b78bcdf04033695ea06:9274683b92177e0d98c103cc455254ed81408bbe36e487a1933da77e393bcb6103b5945d46e9506f99670ca94713b1e090a544c2ce4040040db29e6013c97c05:8be84a05e863b1c741ebeeaaf46152c57dcbcbc7ee20e4e2260ca302a745679488dddc0002c32f732403178c1e01155c01e252a8f5fb503f67ccf015cd090c03", 62, 0),
        ("CoreThreatStruct", "aa808a1f", "existentialCoreThreatStructHash", "80994652037d103a7ba5fd4bf68c250af3dd34602dacd1c7697271ec8c955bb55b7d79ac17ce5aeb9ea9e584efedae16c2b7e46d221af4ddfa96443e8041c800:aa808a1f4a6f73281378d2875fda658f0866048da37419013c0ebfd846a14a0fda859c5d6d657ce2ab1efec0c07d83320d7d4d437a4aee01e1c83d7893675903", 31, 2),
        ("CoreThreatLegal", "cf73b021", "existentialCoreThreatLegalHash", "59ea882415e457ac29bf430a12db7568a0a6dba8f39f2254798a17f6225bc8bd6451dac659fa8c491276795fc5e5fb33695cb8b58700550b5fb61f0cc481f103:cf73b021381f426ad53910a83a1a5ce15ab6c3ea200e6e6818a805ca22328b13c7aacfc8a9cb5083abd633687e7693cc2c38310d026a36e59dfbd75cf592eb0b", 31, 3),
        ("CoreThreatShadowVacuum", "d7045a03", "existentialCoreThreatShadowVacuumHash", "911c52a9e2d100453c744593a8ea0f66ef64cf04f3836a9830647e9fb108daa7e56657812cb5e2058040b63f3835c54d68478c318e325a2c77034e1452ed9d04:d7045a039acd2e395f9b9c7f5e805cf51162db517a2459df01538ddf2163cd5942c8b9de52cdcf6493f49a8bb2d954e93f0f9145b6bab2a8ed0c366e69d31a04", 31, 4),
        ("CoreThreat", "79b1e69e", "existentialCoreThreatHash", "0accb707d6053eacdf1aff586bc2a463e357be37103ef17dabada0e0ba366007a8ff4867ad84c19addf6111cd6f115deb89ce2b010b36aeaaa9a9c98519fb908:664c217a226ad95906f9d68e7f4432e38096dfa50c7a36c048753c3c24e7109148fbe500458880501f04139345a2cb6ecf9ba01712d743f1fe27493ea1d90608:79b1e69ed3a999fc6ed1d92c92f90f920d1052c4b5d93d17bed0ec90ed0bac6833aaa16301c843f70ac7a959e462a1efccbdb7958b610501d9f7c4c4bb07200b", 127, 5),
        ("CoreChain", "a8d3c480", "existentialCoreChainHash", "462e5a3fca4d13edb5759cd4e2e42022a25ff7ca09b3d73ff4bac268839480ce7afa1772f2e073c5b25aedff02cb9566dda5732c734e411e45008b9b25b29f07:a4a48839fab6600d452ca11ca5af0369b5aead11ee1f87f644e3d57eb66c3bd41dc7f48dc48eb86471c50bd7c69faa5bcb552d4b13835e7ed7dea0adeb4c0d07:a8d3c480e44420911de2444095a60ace8807741e03903a8221b42b613716e9eca093ce765d16fa334fda4c75eb76934d49db06cafc9ff442047addc9a2fb820e", 255, 9)
    )
