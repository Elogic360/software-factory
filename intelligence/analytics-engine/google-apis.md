# Google APIs Integration — Integral Market

## API Key

```
AIzaSyBE7b25zdrafAJXXJC1Z_rEMlHHab4gmMc
```

**Created:** July 6, 2026  
**Project:** integralmarket  
**Restrictions:** None (recommend restricting to domain before production)

---

## Enabled APIs (26 total)

### SEO & Search
| API | Purpose | Endpoint |
|-----|---------|----------|
| **Google Search Console API** | Submit sitemaps, request indexing, monitor search performance | `searchconsole.googleapis.com` |
| **Knowledge Graph Search API** | Query Google's knowledge graph for entity data | `kgsearch.googleapis.com` |
| **PageSpeed Insights API** | Measure Core Web Vitals performance | `www.googleapis.com/pagespeedonline/v5` |

### Analytics & Data
| API | Purpose | Endpoint |
|-----|---------|----------|
| **Google Analytics Data API** | Query GA4 properties for traffic data | `analyticsdata.googleapis.com` |
| **BigQuery API** | Large-scale data analysis | `bigquery.googleapis.com` |
| **Cloud Logging API** | Application logging | `logging.googleapis.com` |
| **Cloud Monitoring API** | Uptime and performance monitoring | `monitoring.googleapis.com` |

### Storage & Infrastructure
| API | Purpose | Endpoint |
|-----|---------|----------|
| **Cloud Storage** | Object storage (R2 alternative) | `storage.googleapis.com` |
| **Cloud SQL** | Managed PostgreSQL | `sqladmin.googleapis.com` |
| **Cloud Trace API** | Distributed tracing | `trace.googleapis.com` |

---

## Environment Variables

Add to `integral-market-backend/.env`:

```env
# Google APIs
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_CONSOLE_API_KEY=your_google_search_console_api_key
GOOGLE_KNOWLEDGE_GRAPH_API_KEY=your_google_knowledge_graph_api_key
GOOGLE_PAGESPEED_API_KEY=your_google_pagespeed_api_key
GOOGLE_ANALYTICS_API_KEY=your_google_analytics_api_key

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=https://integralmarket.tech/auth/oauth/callback
```

Add to `app/.env` (frontend):

```env
VITE_GOOGLE_API_KEY=your_vite_google_api_key
```

---

## API Usage Examples

### Google Search Console — Submit Sitemap
```bash
curl -X POST \
  'https://searchconsole.googleapis.com/webmasters/v3/sites/https%3A%2F%2Fintegralmarket.tech/sitemaps' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"feedpath": "https://integralmarket.tech/sitemap.xml"}'
```

### Knowledge Graph Search
```bash
curl "https://kgsearch.googleapis.com/v1/entities:search?query=Integral+Market&key=AIzaSyBE7b25zdrafAJXXJC1Z_rEMlHHab4gmMc&limit=5"
```

### PageSpeed Insights
```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://integralmarket.tech&key=AIzaSyBE7b25zdrafAJXXJC1Z_rEMlHHab4gmMc&category=performance&category=seo"
```

### IndexNow (Instant Indexing)
```bash
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "integralmarket.tech",
    "key": "your-indexnow-key",
    "urlList": ["https://integralmarket.tech/", "https://integralmarket.tech/academy"]
  }'
```

---

## Security Notes

- API key has no restrictions yet — restrict to `*.integralmarket.tech` before production
- Never commit API key to git (add `.env` to `.gitignore`)
- Use `x-goog-api-key` header instead of query parameter when possible
- Rotate keys periodically per Google best practices
