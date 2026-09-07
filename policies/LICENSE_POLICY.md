# Software Factory — Open-Source License Governance Policy

## 1. Approved Permissive Licenses (Safe to Integrate)
- **MIT**, **Apache-2.0**, **BSD-2-Clause**, **BSD-3-Clause**, **ISC**.
- Full integration, sublicensing, and modification permitted. Attribution preserved.

## 2. Review-Required Licenses (Adapter & Reference Only)
- **GPL-3.0**, **AGPL-3.0**, **LGPL-3.0**, **MPL-2.0**.
- **Rule**: Do not vendor or statically link copyleft code directly into proprietary service cores. Access via subprocess CLI, separate microservices, or standard API connectors.

## 3. Prohibited Licenses
- Non-commercial only (CC-BY-NC), proprietary restricted, unverified sources without LICENSE file.
