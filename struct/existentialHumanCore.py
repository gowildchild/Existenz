####
## You don't have to agree with my coding, but atleast you could agree upon the framework. Atleast, I tried. 
####

from enum import IntFlag
class ExistentialHumanCore(IntFlag):

    # THE LOWER 16-BITS:  IMMUTABLE   7 Human Pillars of existence!

    EXISTENCE               = 1 << 0    # 1     PILLAR  You, alive, with a body
    AUTONOMY                = 1 << 1    # 2     PILLAR  The Sovereign Right to Choose
    INTEGRITY               = 1 << 2    # 4     PILLAR  The Moral Axis of Personal Choice
    PSYCHOLOGY              = 1 << 4    # 16    PILLAR  Cognitive Internal State and Mental Peace
    PHYSICAL                = 1 << 5    # 32    PILLAR  Physical Body Vessel and bio-state
    DISABILITY              = 1 << 6    # 64    PILLAR  Nature's way of checks and balances
    DEVELOPMENT             = 1 << 7    # 128   PILLAR  Evolutionary, Intellectual and Creative Growth
    PROPERTY                = 1 << 8    # 256   PILLAR  Material Assets and Income Protection
    PRESENCE                = 1 << 10   # 1024  PILLAR  Real-Time Spacetime Footprint
    EXISTENCE_IMMUTABLE_END = 1 << 12   # 4096  END OF IMMUTABLE BLOCK OF [PILLARS]

    # THE HIGHER 8-BITS:  IMMUTABLE for every human being, LOWER 8-BITS: legal SHIELDS by external factors

    SHIELD_RIGHTS_HUMAN     = 1 << 20   # 1048576    SHIELD-A  (Institutional)
    SHIELD_RIGHTS_INCLUSIVE = 1 << 22   # 4194304    SHIELD-A2 (Systemic)
    SHIELD_RIGHTS_BASIC     = 1 << 24   # 16777216   SHIELD-B  (Institutional) 
    SHIELD_RIGHTS_ASYLUM    = 1 << 26   # 67108864   SHIELD-A3 (Institutional)
    SHIELD_IMMUTABLE_END    = 1 << 27   # 2147483648 END OF IMMUTABLE BLOCK [HUMAN RIGHTS]  
    EXISTENZ_IMMUTABLE_END  = 1 << 31   # 2147483648 END OF IMMUTABLE BLOCK [HUMAN FRAMEWORK]
