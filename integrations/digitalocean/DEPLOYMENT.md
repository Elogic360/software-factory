# DigitalOcean Deployment Configuration — Integral Market

## Architecture Overview

```
DigitalOcean Cloud
├── Managed PostgreSQL
│   ├── integral_market_db (schemas: iam, core, academy, library, journal, copy_trading, notifications, audit)
│   └── integral_journal_db (schemas: journal, copy_trading)
├── Managed Redis
│   ├── DB 0: Market Backend cache
│   ├── DB 1: Expert Backend cache
│   ├── DB 2: Celery broker
│   ├── DB 3: Celery results
│   └── DB 4: Intelligence cache
├── Droplet (4vCPU, 8GB RAM)
│   ├── integral-market-backend (:8000)
│   ├── integral-expert-backend (:8001)
│   ├── integral-market-intelligence (:8002)
│   ├── integral-mail-backend (:8011)
│   └── Nginx reverse proxy (:80/:443)
└── Stalwart Mail Server (separate Droplet or same server)
    ├── SMTP (:465/:587)
    ├── IMAP (:993)
    └── Web UI (:8080)
```

## Prerequisites

1. DigitalOcean API token with scopes: `read`, `write`
2. Domain `integralmarket.tech` configured in Cloudflare
3. SSH key added to DigitalOcean account

## Step 1: Create Managed Databases

### PostgreSQL Database Cluster
```bash
# Create cluster
doctl databases create integral-market-pg \
  --engine pg \
  --version 16 \
  --size db-s-2vcpu-4gb \
  --region nyc1 \
  --num-nodes 1

# Note the cluster ID from output
CLUSTER_ID=$(doctl databases list --format ID | tail -1)

# Create databases
doctl databases db create $CLUSTER_ID --name integral_market_db
doctl databases db create $CLUSTER_ID --name integral_journal_db

# Create user
doctl databases user create $CLUSTER_ID --name integralmarket
# Note the generated password from output

# Get connection string
doctl databases connection $CLUSTER_ID --format Host,Port,User,Password,Database
```

### Redis Database
```bash
# Create Redis cluster
doctl databases create integral-market-redis \
  --engine redis \
  --version 7 \
  --size db-s-1vcpu-1gb \
  --region nyc1

# Get connection details
REDIS_ID=$(doctl databases list --format ID | tail -1)
doctl databases connection $REDIS_ID
```

## Step 2: Create Droplet

```bash
# Create Droplet
doctl compute droplet create integral-platform \
  --size s-4vcpu-8gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <YOUR_KEY_ID> \
  --tag-names production,integral-market

# Wait for Droplet to be ready
DROPLET_ID=$(doctl compute droplet list --format ID --no-header | head -1)
doctl compute droplet get $DROPLET_ID --format PublicIPv4

# SSH into Droplet
doctl compute ssh integral-platform
```

## Step 3: Deploy on Droplet

```bash
# On the Droplet:

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone the project
git clone https://github.com/Elogic360/Integral-Market.git
cd Integral-Market

# Create .env files for each service
# (copy from .env.example and fill in DigitalOcean database connection strings)

# Start services
docker compose -f docker-compose.prod.yml up -d
```

## Step 4: Configure DNS

In Cloudflare, add these records:

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| A | @ | YOUR_DROPLET_IP | DNS only |
| A | mail | YOUR_STALWART_IP | DNS only |
| MX | @ | mail.integralmarket.tech (10) | DNS only |
| TXT | @ | v=spf1 mx a ~all | DNS only |
| TXT | _dmarc | v=DMARC1; p=quarantine | DNS only |
| TXT | default._domainkey | (DKIM key from Stalwart) | DNS only |

## Step 5: Environment Variables

### integral-market-backend/.env
```env
DATABASE_URL=postgresql+asyncpg://integralmarket:PASSWORD@HOST:25060/integral_market_db
DATABASE_URL_SYNC=postgresql://integralmarket:PASSWORD@HOST:25060/integral_market_db
REDIS_URL=redis://default:PASSWORD@HOST:25061
SECRET_KEY=<generated>
INTERNAL_SERVICE_TOKEN=<generated>
CORS_ORIGINS=https://integralmarket.tech
MAIL_SERVICE_URL=http://localhost:8011
```

### integral-expert-backend/.env
```env
DATABASE_URL=postgresql+asyncpg://integralmarket:PASSWORD@HOST:25060/integral_journal_db
DATABASE_URL_SYNC=postgresql://integralmarket:PASSWORD@HOST:25060/integral_journal_db
REDIS_URL=redis://default:PASSWORD@HOST:25061
SECRET_KEY=<same as market backend>
ENCRYPTION_KEY=<generated>
CORS_ORIGINS=https://integralmarket.tech
```

## Estimated Costs (DigitalOcean)

| Resource | Size | Monthly Cost |
|----------|------|-------------|
| Managed PostgreSQL | db-s-2vcpu-4gb | ~$60 |
| Managed Redis | db-s-1vcpu-1gb | ~$15 |
| Droplet | s-4vcpu-8gb | ~$48 |
| **Total** | | **~$123/mo** |

For the Stalwart Mail Server, add a separate Droplet:
| Resource | Size | Monthly Cost |
|----------|------|-------------|
| Droplet (Stalwart) | s-2vcpu-4gb | ~$24 |
| **Total with Mail** | | **~$147/mo** |
