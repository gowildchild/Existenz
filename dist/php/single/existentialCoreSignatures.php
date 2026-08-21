<?php
// ==========================================================================
// THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
// Version: v0.76i | Framework Namespace Lock
// Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
// Released under strict Non-Commercial Open-Source License terms.
// ==========================================================================

namespace existentialCoreSignatures;
class Signatures {
    const existentialCoreVersion = 'v0.76i';
    const existentialCoreCheckMagic = 'b'EX25IMMUT32CORE7617'';
    const existentialCoreCheckSignatures = 'c01eca1e594d2105da6d4484bc871ef494dbd424bc871ef494dbd425da6d4484';
    const existentialCore = '22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e';
    const existentialCoreThreatRoot = '1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca';
    const existentialCoreThreatLegal = '931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1';
    const existentialCoreThreatShadowVacuum = '9b1d1bcf4903c7c26a6b75dd2e0c341ddab3594c2514c99e5d8e6b4651bfcc69';
    const existentialCoreThreat = '23e9fbb89c801de638ddd73798b42f7c57af2bfde3e09a999f9527d9f27e39f3';
    const existentialCoreCheck = '8b4defb0aaf1eb9bcd7b382cf0b4db0aa093eb1b84b8e09d3cf0f73d5b2d37b6';

    public static $existentialPublicKeys = [
        ['Platform', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ4tfhIlXUXCKvFE/HOwkVFTEIjWknHayefpjqTVAwSs existenz@xsrv.net'],
        ['Developer', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGHTQAOnKU4zaM03kASAKmrsps4ROCx8xMQZ4m12Yo8U existenz-dev-gwc@xsrv.net'],
        ['Personal', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKn1/r+k9+T5OJyoIjcrkj0DBmLq//x0/sffNMJNWofK existenz-dev-gv@xsrv.net']
    ];

    public static $existentialPrivateSigned = [
        ['Magic', 'aa9bc01ee92ec2db4ce5a5f0aac07caa70a2019ee17511336b41747201ade17a'],
        ['Core', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreCheck', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreThreatStruct', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreThreatLegal', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreThreatShadowVacuum', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreThreat', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreChain', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d']
    ];
}
