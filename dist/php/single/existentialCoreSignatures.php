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
    const existentialCoreCheckSignatures = 'b45624fc09463f05d2e9359db32ae928e084aa81e47bbd33ecde0a58d66d0656';
    const existentialCore = '22023c142c21687803a3cdedb82684973d7ab5bb601b2b35d0bd8b448e26f99e';
    const existentialCoreThreatRoot = '1f95497bb174e069c2b727d8b72a7d556a03c0db451dcf2bac6b00bf191291ca';
    const existentialCoreThreatLegal = '931547edaba6ec457f2b6a22ef1961d56c08a765983036cb95642aa75fbd0ab1';
    const existentialCoreThreat = '90f9d7438a0497f54dbe065a64f5f5c111dee8c1184832c280d96c0bd2226689';
    const existentialCoreCheck = 'b45624fc09463f05d2e9359db32ae928e084aa81e47bbd33ecde0a58d66d0656';

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
        ['CoreThreat', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d'],
        ['CoreChain', 'faddd14fdefb46154f26bdc052e457e0a63edd9c619af12b2e1aad55f8a7a14d']
    ];
}
