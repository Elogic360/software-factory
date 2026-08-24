# 2026-07-28 — Permanent Business Email Infrastructure Verification

## Architecture & Integration State
- **Stalwart Version**: `v0.16.13` OCI Container on DigitalOcean Droplet (`159.65.177.103`)
- **Outbound Relay**: Brevo SMTP Relay (`smtp-relay.brevo.com:587`)
- **Storage Strategy**: Hybrid — RocksDB for raw message blobs/JMAP indexing + PostgreSQL (`integral_maildb`) for business metadata.
- **Port Mapping**: SMTPS `465`, Submission `587`, IMAPS `993`, JMAP/HTTP `8080`, Mgmt `8081`.

## Verified Permanent Business Mailboxes (15/15 PASS)
- `admin@integralmarket.tech` (Pass: `IntegralAdmin2026!`)
- `noreply@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `security@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `alerts@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `notifications@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `academy@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `info@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `support@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `expert@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `team@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `community@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `webinar@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `imfund@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `certificates@integralmarket.tech` (Pass: `IntegralMail2026!`)
- `postmaster@integralmarket.tech` (Pass: `IntegralMail2026!`)

## Automated Test Matrix Result
- **Report Location**: `audit-evidence/email_account_validation_report.json`
- **Result**: `15 / 15 accounts PASSED` IMAPS Auth, SMTPS Auth, and Outbound Relay Dispatch.
