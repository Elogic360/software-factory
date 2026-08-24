# DigitalOcean Integration — Setup & Deployment Guide

## Overview

This guide covers installing and configuring DigitalOcean tools for deploying Integral Market backends and databases.

## Prerequisites

- Node.js v18+ and npm v8+
- DigitalOcean account with API token
- doctl CLI (for Droplet/database management)

---

## 1. Install DigitalOcean MCP

```bash
# Install globally via npm
npm install -g @digitalocean/mcp

# Verify installation
npx @digitalocean/mcp --help
```

### Configure MCP in Claude Code

```bash
# Set your API token
export DIGITALOCEAN_API_TOKEN="dop_v1_your_token_here"

# Add to Claude Code
claude mcp add digitalocean \
  --env DIGITALOCEAN_API_TOKEN=${DIGITALOCEAN_API_TOKEN} \
  -- npx -y "@digitalocean/mcp"
```

### Configure MCP in mcp.json (for other clients)

```json
{
  "mcpServers": {
    "digitalocean": {
      "command": "npx",
      "args": ["-y", "@digitalocean/mcp", "--services", "apps,droplets,databases"],
      "env": {
        "DIGITALOCEAN_API_TOKEN": "dop_v1_your_token_here"
      }
    }
  }
}
```

### Available Services

| Service | Flag | Description |
|---------|------|-------------|
| App Platform | `--services apps` | Deploy and manage apps |
| Droplets | `--services droplets` | Manage virtual machines |
| Databases | `--services databases` | Managed PostgreSQL, Redis, MongoDB |
| Kubernetes | `--services kubernetes` | Manage K8s clusters |
| Spaces | `--services spaces` | Object storage (S3-compatible) |
| Domains | `--services domains` | DNS management |
| Firewalls | `--services firewalls` | Network security |
| Load Balancers | `--services loadbalancers` | Traffic distribution |

---

## 2. Install doctl CLI

```bash
# Linux
curl -sL https://github.com/digitalocean/doctl/releases/latest/download/doctl-linux-amd64.tar.gz | tar -xz -C /usr/local/bin/

# macOS
brew install doctl

# Verify
doctl version
```

### Authenticate

```bash
doctl auth init
# Enter your DigitalOcean API token when prompted
```

### Useful Commands

```bash
# List Droplets
doctl compute droplet list

# Create a Droplet
doctl compute droplet create integral-mail \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <key_id>

# List managed databases
doctl databases list

# Create a managed PostgreSQL database
doctl databases create integral-mail-db \
  --engine pg \
  --version 16 \
  --size db-s-1vcpu-1gb \
  --region nyc1

# Create a managed Redis database
doctl databases create integral-mail-redis \
  --engine redis \
  --version 7 \
  --size db-s-1vcpu-1gb \
  --region nyc1
```

---

## 3. Deploy Backends to DigitalOcean

### Option A: App Platform (Recommended for simplicity)

```bash
# Deploy from source
doctl apps create --spec ./app-spec.yaml

# Or via MCP
# "Deploy the integral-mail-backend from /path/to/integral-mail-backend"
```

### Option B: Droplet (Recommended for Stalwart + full control)

```bash
# 1. Create Droplet
doctl compute droplet create integral-platform \
  --size s-4vcpu-8gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <your_key_id>

# 2. SSH into Droplet
doctl compute ssh integral-platform

# 3. Install Docker + deploy
curl -fsSL https://get.docker.com | sh
docker compose up -d

# 4. Install Stalwart Mail Server
curl -sSf https://stalw.art/latest/install | bash
```

### Option C: Docker Compose (Local/VM)

```bash
# Deploy all services together
docker compose -f docker-compose.prod.yml up -d

# Or individual services
docker compose up -d postgres redis
docker compose up -d integral-market integral-expert integral-intelligence
docker compose up -d stalwart-mail
```

---

## 4. Database Setup

### Managed PostgreSQL (DigitalOcean)

```bash
# Create database
doctl databases create integral-market-db \
  --engine pg \
  --version 16 \
  --size db-s-2vcpu-4gb \
  --region nyc1

# Create database
doctl databases db create <cluster-id> --name integral_market_db

# Create user
doctl databases user create <cluster-id> --name integralmarket

# Get connection string
doctl databases connection <cluster-id> --format Host,Port,User,Password,Database
```

### Docker PostgreSQL (local)

```yaml
# docker-compose.yml
services:
  postgres:
    image: timescaledb:latest-pg16
    environment:
      POSTGRES_USER: integralmarket
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: integral_market_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

### Database Migrations

```bash
# Market Backend
cd integral-market-backend
alembic upgrade head

# Expert Backend
cd integral-expert-backend
alembic upgrade head

# Intelligence Backend
cd integral-market-intelligence
alembic upgrade head

# Mail Backend
cd integral-mail-backend
alembic upgrade head
```

---

## 5. Environment Configuration

### Production .env Template

```env
# ── Database ─────────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DATABASE_URL_SYNC=postgresql://user:pass@host:5432/db

# ── Redis ────────────────────────────────────────────────
REDIS_URL=redis://host:6379/0

# ── Security ─────────────────────────────────────────────
SECRET_KEY=<generate-random-64-char-hex>
INTERNAL_SERVICE_TOKEN=<generate-random-32-char>

# ── Email ────────────────────────────────────────────────
SENDGRID_API_KEY=SG.your_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@integralmarket.tech
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@integralmarket.tech

# ── Stalwart Mail ────────────────────────────────────────
STALWART_API_URL=https://mail.integralmarket.tech/api
STALWART_API_KEY=your-stalwart-admin-key

# ── Mail Service ─────────────────────────────────────────
MAIL_SERVICE_URL=http://localhost:8011

# ── CORS ─────────────────────────────────────────────────
CORS_ORIGINS=https://integralmarket.tech,https://www.integralmarket.tech

# ── Domain ───────────────────────────────────────────────
PRIMARY_DOMAIN=integralmarket.tech
```

### Generate Secrets

```bash
# JWT Secret (64 chars)
python3 -c "import secrets; print(secrets.token_hex(32))"

# Internal Service Token (32 chars)
python3 -c "import secrets; print(secrets.token_hex(16))"

# Fernet Encryption Key
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 6. DNS Configuration

See `stalwart-mail/DNS_CONFIGURATION.md` for complete DNS records.

Quick summary for `integralmarket.tech`:
- MX → mail.integralmarket.tech
- SPF → `v=spf1 mx a ~all`
- DKIM → generate with Stalwart
- DMARC → `v=DMARC1; p=quarantine`
- A → mail → YOUR_SERVER_IP

---

## 7. Deployment Checklist

### Local Development
- [ ] Docker + Docker Compose installed
- [ ] All .env files created from .env.example
- [ ] Secrets generated
- [ ] `docker compose up -d` — all services running
- [ ] Verify: `curl http://localhost:8000/health`
- [ ] Run: `bash stalwart-mail/test-flow.sh`

### Staging
- [ ] DigitalOcean Droplet created
- [ ] Docker installed on Droplet
- [ ] DNS configured for staging subdomain
- [ ] SSL certificates provisioned
- [ ] All env vars set in production
- [ ] Database migrations run
- [ ] Stalwart configured and tested
- [ ] SendGrid verified

### Production
- [ ] All env vars set (no defaults)
- [ ] Secrets generated and stored securely
- [ / [ ] DNS records verified (MX, SPF, DKIM, DMARC)
- [ ] PTR record configured with VPS provider
- [ ] IP reputation checked (mxtoolbox.com)
- [ ] Stalwart admin account created
- [ ] DKIM key generated and DNS updated
- [ ] Test email sent and delivered
- [ ] All health checks passing
- [ ] Monitoring alerts configured
