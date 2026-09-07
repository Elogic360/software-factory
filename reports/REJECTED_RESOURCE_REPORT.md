# Software Factory — Rejected & Quarantined Resource Report

| Resource / Pattern | Reason for Rejection / Quarantine | Mitigation / Alternative |
| :--- | :--- | :--- |
| **Uncontrolled Brute-Force Passwords** | Offensive high-risk vectors violate safety policy. | Integrated `prowler` and `security-audit` defense scanners. |
| **Hardcoded API Token Samples** | Secret leakage risk. | Enforced environment variable credential resolution (`${TOKEN}`). |
| **Unlicensed Repositories** | Legal ambiguity and copyright risk. | Filtered to Tier-5-Reference only; zero vendored code. |
