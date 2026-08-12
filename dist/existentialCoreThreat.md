# Existenz Blueprint: existentialCoreThreat

> ==========================================================================
> THE EXISTENZ PLATFORM (AUTOMATED BLUEPRINT COMPILATION)
> Version: v0.76g | Framework Namespace Lock
> Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
> Released under strict Non-Commercial Open-Source License terms.
> ==========================================================================

| Property Element | Register Integer | Bitmask Equation | Struct Type | Context Reference Description |
| :--- | :--- | :--- | :--- | :--- |
| `THREAT_NONE` | `0` | `0` | `SIGNATURE` |  |
| `THREAT_EXISTENCE` | `1` | `1 << 0` | `THREAT` |  |
| `THREAT_AUTONOMY` | `2` | `1 << 1` | `THREAT` |  |
| `THREAT_INTEGRITY` | `4` | `1 << 2` | `THREAT` |  |
| `CANARY_1_SOVEREIGN` | `8` | `1 << 3` | `CANARY` | WATCHDOG_SOVEREIGN |
| `THREAT_PSYCHOLOGY` | `16` | `1 << 4` | `THREAT` |  |
| `THREAT_PHYSICAL` | `32` | `1 << 5` | `THREAT` |  |
| `THREAT_ABLEISM` | `64` | `1 << 6` | `THREAT` |  |
| `THREAT_DEVELOPMENT` | `128` | `1 << 7` | `THREAT` |  |
| `THREAT_PROPERTY` | `256` | `1 << 8` | `THREAT` |  |
| `CANARY_2_SOMATIC` | `512` | `1 << 9` | `CANARY` | WATCHDOG_SOMATIC |
| `THREAT_PRESENCE` | `1024` | `1 << 10` | `THREAT` |  |
| `CANARY_3_SYSTEMIC` | `8192` | `1 << 13` | `CANARY` | WATCHDOG_EVOLUTION |
| `CANARY_4_PERSONAL` | `131072` | `1 << 17` | `CANARY` |  |
| `THREAT_RIGHTS_HUMAN` | `1048576` | `1 << 20` | `RIGHTS` |  |
| `THREAT_RIGHTS_INCLUSIVE` | `4194304` | `1 << 22` | `RIGHTS` |  |
| `CANARY_5_RIGHTS` | `8388608` | `1 << 23` | `RIGHTS` |  |
| `THREAT_RIGHTS_BASIC` | `16777216` | `1 << 24` | `RIGHTS` |  |
| `THREAT_RIGHTS_ASYLUM` | `67108864` | `1 << 26` | `RIGHTS` |  |
| `CANARY_6_CIVIC` | `134217728` | `1 << 27` | `CANARY` |  |
| `SIGN_THREAT_EXISTENTIAL` | `409212016` | `0x18641470` | `SIGNATURE` |  |
| `SIGN_THREAT_EXISTENZ` | `1542169567` | `0x5beba3df` | `SIGNATURE` |  |
| `SIGN_THREAT_RIGHTS_LEGAL` | `1829230962` | `0x6d07d972` | `RIGHTS` |  |
| `SIGN_THREAT_IMMUTABLE` | `1833211533` | `0x6d44968d` | `SIGNATURE` |  |
| `THREAT_IMMUTABLE_END` | `2147483648` | `1 << 31` | `THREAT` |  |
| `SIGN_THREAT_CANARY` | `3223243294` | `0xc01eca1e` | `SIGNATURE` |  |
