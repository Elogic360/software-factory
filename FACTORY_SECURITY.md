# 🛡️ Software Supply-Chain Security & AST Firewall

## Security Posture (`core/security_auditor.py`)
- 4-Tier permission isolation model (`T0_NOOP`, `T1_READ`, `T2_WORKSPACE`, `T3_NETWORK_WRITE`).
- AST static scanning detecting remote shell execution (`curl|bash`), credential exfiltration, and prompt injection.
- Zero committed secrets policy strictly verified.
