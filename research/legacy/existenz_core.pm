package struct::existenz_core;

# ==========================================================================
# THE EXISTENZ PLATFORM (PROTOTYPE ARCHITECTURE CORE, 128-BIT MATRIX)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# ==========================================================================

use strict;
use warnings;
use Hash::Util qw(lock_hash);

use Exporter 'import';
our @EXPORT_OK = qw(
    $EXISTENTIAL_CORE 
    $EXISTENTIAL_THREAT 
    $EXISTENTIAL_RIPPLE
);

# 1. ExistentialCore Constants Map
our $EXISTENTIAL_CORE = {
    EXISTENCE                    => 1 << 0,
    AUTONOMY                     => 1 << 1,
    INTEGRITY                    => 1 << 2,
    PSYCHOLOGY                   => 1 << 3,
    PHYSICAL                     => 1 << 4,
    DISABILITY                   => 1 << 5,
    DEVELOPMENT                  => 1 << 6,
    PROPERTY                     => 1 << 7,
    PRESENCE                     => 1 << 8,
    SHIELD_HUMAN_RIGHTS          => 1 << 20,
    SHIELD_DISCRIMINATION_RIGHTS => 1 << 22,
    SHIELD_BASIC_RIGHTS          => 1 << 24,
    SHIELD_AQUIRED_RIGHTS        => 1 << 26,
    SHIELD_AQUIRED_TRUST         => 1 << 30
};
lock_hash(%$EXISTENTIAL_CORE);

# 2. ExistentialThreat Constants Map
our $EXISTENTIAL_THREAT = {
    THREAT_EXISTENCE   => 1 << 0,
    THREAT_AUTONOMY    => 1 << 1,
    THREAT_INTEGRITY   => 1 << 2,
    THREAT_PSYCHOLOGY  => 1 << 3,
    THREAT_PHYSICAL    => 1 << 4,
    THREAT_ABLEISM     => 1 << 5,
    THREAT_DEVELOPMENT => 1 << 6,
    THREAT_PROPERTY    => 1 << 7,
};

# Generate Advanced Composite State Triggers dynamically
$EXISTENTIAL_THREAT->{TRIGGER_EXPLOITATION}  = $EXISTENTIAL_THREAT->{THREAT_ABLEISM} | $EXISTENTIAL_THREAT->{THREAT_PROPERTY};
$EXISTENTIAL_THREAT->{TRIGGER_PREDATORY}      = $EXISTENTIAL_THREAT->{THREAT_PSYCHOLOGY} | $EXISTENTIAL_THREAT->{THREAT_AUTONOMY};
$EXISTENTIAL_THREAT->{TRIGGER_SYSTEMSCRISIS}  = $EXISTENTIAL_THREAT->{THREAT_AUTONOMY} | $EXISTENTIAL_THREAT->{THREAT_PSYCHOLOGY} | $EXISTENTIAL_THREAT->{THREAT_PROPERTY};
lock_hash(%$EXISTENTIAL_THREAT);

# 3. ExistentialRipple Constants Map
our $EXISTENTIAL_RIPPLE = {
    INDIVIDUAL                 => 1 << 0,
    PARTNER                    => 1 << 1,
    HOUSEHOLD_MARRIAGE         => 1 << 2,
    FAMILY                     => 1 << 3,
    FRIENDS                    => 1 << 4,
    PEERS                      => 1 << 5,
    SUPPORT                    => 1 << 6,
    SOCIETY                    => 1 << 10,
    CORPORATE                  => 1 << 11,
    GOVERNED                   => 1 << 12,
    TRUST_SYSTEMIC             => 1 << 16,
    TRUST_CONDITIONAL          => 1 << 17,
    TRUST_BROKEN_INSTITUTIONAL => 1 << 20,
    TRUST_BROKEN_SAFETY        => 1 << 22,
    TRUST_BROKEN_DIGITAL       => 1 << 24,
    TRUST_BROKEN_CORE          => 1 << 26,
    TRUST_PERSONAL             => 1 << 29,
    TRUST_ABSOLUTE             => 1 << 30
};

# Generate Forensic Dead-Bolt Activation Matrix dynamically
$EXISTENTIAL_RIPPLE->{TRUST_BROKEN_LOCKOUT} = $EXISTENTIAL_RIPPLE->{TRUST_BROKEN_CORE} | $EXISTENTIAL_RIPPLE->{TRUST_BROKEN_DIGITAL};
lock_hash(%$EXISTENTIAL_RIPPLE);

1; # Return the absolute compliance execution bit
