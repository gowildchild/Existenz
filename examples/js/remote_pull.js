// From inside your runtime web application dashboard controller:
import { ExistentialCore, ExistentialThreat, ExistentialRipple } from 'https://cdn.jsdelivr.net/gh/gowildchild/Existenz@master/struct/existenz_core.js';

// Bitwise Mask Match Assertions
let activeThreat = ExistentialThreat.THREAT_PSYCHOLOGY | ExistentialThreat.THREAT_AUTONOMY;
if (activeThreat === ExistentialThreat.TRIGGER_PREDATORY) {
    console.log("Forensic flag active: Predatory tracking vector triggered.");
}
