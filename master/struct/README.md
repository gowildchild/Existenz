# EXISTENZ SYSTEM WORKSPACE BOUNDARIES 

## 🔒 1. PROTECTED DEFINITIONS VAULT (DO NOT WRITE TO DISK)
The following files are pure data frameworks and act as the system's input anchors.
The signature engines and initialization scripts must NEVER perform file-write 
operations against these targets. All maintenance is done manually by the architect.

- master/struct/existentialCoreSchema.json (Master Blueprint Schema)
- master/struct/engineSigningStruct.py     (Structures, The glue between)
- master/struct/engineSigningMeta.py       (System and Meta info)

## ⚡ 2. AUTOMATED GENERATION TRACK (SAFE TO ERASE & AUTO-HEAL)
The following core infrastructure modules are 100% compiled outputs. 
If structural changes are made to the above files, the files below can 
be safely deleted and the engine will instantly recompile them like new.

- master/existentialCore.py          <- Generated Core structures + Signatures
- master/existentialCoreThreat.py    <- Generated CoreThreat, Legal and Vacuum
- master/existentialCoreCheck.py     <- Generated sentinel to check upon the core
- master/existentialCores.json       <- Merged existentialCore + existentialCoreThreat
- master/existentialSignatures.py    <- Generated cryptographic signature ledger (python)
- master/existentialSignatures.json  <- Generated cryptographic signature ledger (json) 
