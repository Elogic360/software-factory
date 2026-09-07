#!/usr/bin/env bash
# scripts/install_crontab.sh — Provisions local user crontab for Software Factory automated cycles.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SF_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Installing Software Factory automated scheduler into user crontab..."

CRON_CMD_DAILY="0 3 * * * cd \"$SF_ROOT\" && python3 factory.py radar --period daily >> logs/daily_radar.log 2>&1"
CRON_CMD_SECURITY="30 3 * * * cd \"$SF_ROOT\" && python3 factory.py security >> logs/daily_security.log 2>&1"
CRON_CMD_WEEKLY="0 4 * * 1 cd \"$SF_ROOT\" && python3 factory.py learn mine-failures >> logs/weekly_learning.log 2>&1"
CRON_CMD_MONTHLY="0 5 1 * * cd \"$SF_ROOT\" && python3 factory.py audit >> logs/monthly_audit.log 2>&1"

mkdir -p "${SF_ROOT}/logs"

(crontab -l 2>/dev/null | grep -v "factory.py" ; echo "$CRON_CMD_DAILY" ; echo "$CRON_CMD_SECURITY" ; echo "$CRON_CMD_WEEKLY" ; echo "$CRON_CMD_MONTHLY") | crontab -

echo "✅ Installed 4 scheduled jobs in user crontab:"
crontab -l | grep "factory.py"
