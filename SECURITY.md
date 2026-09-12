# Security Policy

## Supported Versions

The old build has been deprecated because it was not safe in a zero-trust environment.

| Version | Supported          |
| ------- | ------------------ |
| 0.76.x  | :white_check_mark: |
| < 0.75  | :x:                |

## Reporting a Vulnerability

The old build did not have check-bits to have canaries checking for human right violations.
The new structures have checkbits on bit-3, bit-9, bit-13, bit-17 and so on. 

They will additionally get signed with sha-256 hashes and private keys for the best protection against malicious tampering.
