# NIP-Existenz
## Dual-Horizon Encrypted Forensic Capsules, Systemic Human Rights Abuses and Attribute-Based Threat Ledgers
`draft` `optional` `author: Existenz`

This NIP specification defines sub-milliwat 128-bit human rights protocol protocol for establishing human rights violations, transmitting human rights metrics while keeping important data entirely under the users control, without leaking sender identity, location data or network topology. The specification has 3 modes of operation. The user controls how he wishes to be shielded, how violations are stored and if any further forensic evidence is required. 

**PUBLIC** : Reports human rights violations anonymously and statistically. It exposes only regional/city data for public census counting without collecting local user tracking data.
**BASIC**  : Provides the public statistical broadcast while packing an encrypted, high-entropy ciphertext interior containing the precise location and timestamp of the incident. Designed for one-time, unexpected or out-of-the-ordinary encounters.
*FORENSIC* : Includes all Mode 1 and Mode 2 parameters, but converts the interior into an append-only, chained Dual-Horizon Forensic Capsule ready to be claimed with verifiable evidentiary attachments (e.g., photos). Designed for recurring structural tracking, stalkers, and high-end crimes.

### The Problem
Traditional metadata encryption leaves routing signatures, precise location telemetry and relationship graphs vulnerable to side-channel traffic analysis and data harvesting. With this standard, the user is in full control of the shields and what happens to violations, while human rights are non-negotionable. As a matter of fact, the existentialCore, existentialCoreThreat and existentialCoreThreatLegal structures are immutable. This algorithm is designed to spot and report human rights violations on the spot.

### The Solution: Kind 15430
This NIP introduces a specialized, dual-zone event class: `kind: 31543`. 
The packet structures data into an publically anonymous, exploded public metadata header (for global consensus tracking) with the tags of the violations like "+THREAT_ABLEISM +THREAT_VIOLENCE @BE" and an opaque, symmetric ciphertext interior (for secure, offline forensic auditing) containing the lon, lat, time and internal message or file attached. 

### Event Layout
Used for continuous, low-power global census counting. It maps events to standard Regular Kind behaviors and is permanently append-only.
A `kind: 15400` event follows this strict JSON schema:

```json
// --- MODE 1: PUBLIC STATISTICAL BROADCAST ---
{
  "kind": 15400,
  "tags": [
    ["m", "1:<COUNTS_OF_THREAT>"],
    ["c", "<ABSTRACTED_REGIONAL_CITY_CODE> <ABSTRACTED_REGIONAL_COUNTRY_CODE>"],
    ["core_threat", "+THREAT_ABLEISM +THREAT_VIOLENCE"] 
  ],
  "content": "<signature_of_the_internal_report_only>",
  "pubkey": "...", "sig": "..."
}
```
A `kind: 15430` event follows this strict JSON schema:
Handles Mode 2 and Mode 3 actions. These events map directly to standard Regular Kind behaviors. They cannot be overwritten or replaced by relays once broadcasted.
```json
// --- MODE 2: BASIC BROADCAST ---
// For one-time encounters, out of the ordinary
// This capsule can be claimed for release
{
  "id": <32-byte-hex-of-serialized-event>,
  "created_at": <unix-timestamp>,
  "kind": 15430,
  "tags": [
    ["m", "2:<COUNTS_OF_THREAT>"],
    ["c", "<ABSTRACTED_REGIONAL_CITY_CODE> <ABSTRACTED_REGIONAL_COUNTRY_CODE>"],
    ["existenz","<32-BIT THREAT BITMASK>"],
    ["core_threat", "+THREAT_ABLEISM +THREAT_VIOLENCE +THREAT_PROPERTY"],
    ["core_legal", "+LEGAL_CAT6_ABLEISM +LEGAL_CAT9_THEFTH"],
    ["core_note", "<ABSTRACTED_SMALL_PUBLIC_NOTE>"],
    ["nonce", "<string>", "<target_difficulty_bits>"]
  ],
  "content": "{\"n\": "<private_notice>, \"x\": 4.8951, \"y\": 52.3702, \"t\": 1783910000, \"signed_client\": \"<client_sig>\"}",
  "pubkey": "...", "sig": "..."
}

// --- MODE 3: BASIC BROADCAST + FORENSICS ---
// For multiple encounters, stalkers, high-end crime
{
  "id": <32-byte-hex-of-serialized-event>,
  "created_at": <unix-timestamp>,
  "kind": 15430,
  "tags": [
    ["m", "3:<COUNTS_OF_THREAT>"],
    ["c", "<ABSTRACTED_REGIONAL_CITY_CODE> <ABSTRACTED_REGIONAL_COUNTRY_CODE>"],
    ["existenz","<32-BIT THREAT BITMASK>:<ABSTRACTED_MODE_FLAGS>"],
    ["sign_threat_previous", "<sha256_of_prior_violation_event_when_recurring>"],
    ["sign_threat_chain", "0xa62b1b36"]
    ["core_threat", "+THREAT_ABLEISM +THREAT_VIOLENCE +THREAT_PROPERTY"],
    ["core_legal", "+LEGAL_CAT6_ABLEISM +LEGAL_CAT9_THEFTH"],
    ["core_note", "<ABSTRACTED_SMALL_PUBLIC_NOTE>"],
    ["nonce", "<string>", "<target_difficulty_bits>"]
  ],
  "content": "{\"forensic_capsule\": \"<encrypted_binary_payload>\", \"attachments\": [{\"type\": \"photo\", \"hash\": \"<sha256_of_image_file>\", \"n\": \"<private_notice>\"}]}",
  "pubkey": "...", "sig": "..."
}
```

## Core Structures & Integration

To achieve semantic compatibility with the Existenz framework, client and relay developers can import or reference the immutable 32-bit/128-bit register structures provided in this repository. 

#### Tag Specifications
* `m`: Mode Selection flag followed by a string-delimited integer tracking the aggregated threat count.
* `c`: Coarse spatial telemetry. Restricts public mapping resolution to 1 or 2 decimal places to enforce a strict geographic blur radius (1.1km to 11km) for absolute physical anonymity.
* `existenz`: Contains the immutable 32-bit ExistentialCore threat register bitmask encoded as an analytical hex string. In Mode 3, includes an appended string modifier for abstracted mode operational flags.
* `core_threat`: Space-delimited string representing the active bitrange vectors.
* `core_legal`: Systemic classification of violations mapped to recognized legal statutes and frameworks.
* `core_note`: A sanitized, non-identifying public annotation.
* `chain_threat_previous` / `sign_threat_chain`: Cryptographic threading parameters used to build unalterable, linear histories of recurring or systemic violations over time.
* `nonce`: Enforces NIP-13 Proof of Work. This mitigates spam, ensures high-priority relay retention, and programmatically blocks adversarial deletion or throttling loops.

#### Content Specification
The `content` block must remain a completely high-entropy ciphertext payload. It is encrypted locally inside the client's RAM using an Ephemeral Derivative Key derived from the threat's unique binary footprint mixed with an offline, un-shared local salt vector. The payload holds the pristine 4-decimal coordinates (`x,y`), timestamps (`t`), encrypted_binary_payload (`attachments`) and a private note as memo (`n`), 

### Prefix Notation Rules
The `core_threat` field enforces a standardized single-character prefix shorthand to streamline client parsing engines:
* `+` : Active Presence / Metric Injected
* `-` : Lost Parameter / Boundary Degraded
* `!` : Emergency / Immediate Attention Trigger Active
* `?` : Unknown Circumstance Under Automated Review
* `=` : Ongoing / In Progress Event Tracking
