import * as fs from 'fs';
import * as path from 'path';
import * as https from 'https';
import * as http from 'http';

interface SitemapURL {
  loc: string;
  lastmod: string;
  changefreq: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never';
  priority: number;
}

interface IndexNowPayload {
  host: string;
  key: string;
  keyLocation: string;
  urlList: string[];
}

interface IndexNowResponse {
  statusCode: number;
  message: string;
  errors?: string[];
}

const SITE_URL = 'https://integralmarket.ai';

const ENTITY_URLS: SitemapURL[] = [
  { loc: `${SITE_URL}/`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'daily', priority: 1.0 },
  { loc: `${SITE_URL}/journal`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.9 },
  { loc: `${SITE_URL}/academy`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.8 },
  { loc: `${SITE_URL}/copy-trading`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.8 },
  { loc: `${SITE_URL}/backtesting`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.7 },
  { loc: `${SITE_URL}/analytics`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.7 },
  { loc: `${SITE_URL}/risk-management`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.7 },
  { loc: `${SITE_URL}/pricing`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.8 },
  { loc: `${SITE_URL}/about`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.5 },
  { loc: `${SITE_URL}/contact`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.5 },
  { loc: `${SITE_URL}/faq`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.6 },
  { loc: `${SITE_URL}/docs/api`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'weekly', priority: 0.6 },
  { loc: `${SITE_URL}/docs/mt5-setup`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.6 },
  { loc: `${SITE_URL}/docs/psychology-tracking`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.6 },
  { loc: `${SITE_URL}/blog`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'daily', priority: 0.7 },
  { loc: `${SITE_URL}/blog/forex-journaling-guide`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.5 },
  { loc: `${SITE_URL}/blog/ai-trading-psychology`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.5 },
  { loc: `${SITE_URL}/blog/mt5-setup-guide`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'monthly', priority: 0.5 },
  { loc: `${SITE_URL}/terms`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'yearly', priority: 0.3 },
  { loc: `${SITE_URL}/privacy`, lastmod: new Date().toISOString().split('T')[0], changefreq: 'yearly', priority: 0.3 }
];

export function generateSitemap(): string {
  const lines: string[] = [];
  lines.push('<?xml version="1.0" encoding="UTF-8"?>');
  lines.push('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">');
  for (const entry of ENTITY_URLS) {
    lines.push('  <url>');
    lines.push(`    <loc>${entry.loc}</loc>`);
    lines.push(`    <lastmod>${entry.lastmod}</lastmod>`);
    lines.push(`    <changefreq>${entry.changefreq}</changefreq>`);
    lines.push(`    <priority>${entry.priority}</priority>`);
    lines.push('  </url>');
  }
  lines.push('</urlset>');
  return lines.join('\n');
}

export function generateRobotsTxt(): string {
  const lines: string[] = [];
  lines.push('# Integral Market — robots.txt');
  lines.push('# https://integralmarket.ai');
  lines.push('');
  lines.push('User-agent: *');
  lines.push('Allow: /');
  lines.push('Disallow: /api/');
  lines.push('Disallow: /admin/');
  lines.push('Disallow: /dashboard/');
  lines.push('Disallow: /settings/');
  lines.push('Disallow: /auth/');
  lines.push('');
  lines.push('User-agent: GPTBot');
  lines.push('Allow: /faq');
  lines.push('Allow: /docs/');
  lines.push('Allow: /blog/');
  lines.push('');
  lines.push('User-agent: Google-Extended');
  lines.push('Allow: /faq');
  lines.push('Allow: /docs/');
  lines.push('Allow: /blog/');
  lines.push('');
  lines.push('Sitemap: https://integralmarket.ai/sitemap.xml');
  lines.push('');
  return lines.join('\n');
}

export function generateWellKnownMCP(host: string, key: string): Record<string, unknown> {
  return {
    mcpVersion: '2025-06-18',
    server: {
      name: 'integral-market',
      url: `https://${host}/mcp`,
      capabilities: ['tools'],
      auth: { type: 'bearer', key }
    }
  };
}

export async function pushToIndexNow(
  urls: string[],
  host: string,
  key: string
): Promise<IndexNowResponse> {
  const payload: IndexNowPayload = {
    host,
    key,
    keyLocation: `https://${host}/${key}.txt`,
    urlList: urls
  };

  const body = JSON.stringify(payload);

  return new Promise((resolve) => {
    const req = https.request(
      {
        hostname: 'api.indexnow.org',
        port: 443,
        path: '/indexnow',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Length': Buffer.byteLength(body)
        }
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode || 0,
            message: data || 'No response body',
            errors: res.statusCode && res.statusCode >= 400 ? [data] : undefined
          });
        });
      }
    );

    req.on('error', (err) => {
      resolve({
        statusCode: 0,
        message: err.message,
        errors: [err.message]
      });
    });

    req.write(body);
    req.end();
  });
}

export function generateIndexingOutput(outputDir?: string): {
  sitemap: string;
  robots: string;
  urls: string[];
} {
  const sitemap = generateSitemap();
  const robots = generateRobotsTxt();
  const urls = ENTITY_URLS.map(u => u.loc);

  if (outputDir) {
    fs.mkdirSync(outputDir, { recursive: true });

    fs.writeFileSync(path.join(outputDir, 'sitemap.xml'), sitemap, 'utf-8');
    fs.writeFileSync(path.join(outputDir, 'robots.txt'), robots, 'utf-8');
    fs.writeFileSync(path.join(outputDir, 'urls.json'), JSON.stringify(urls, null, 2), 'utf-8');

    const wellKnownDir = path.join(outputDir, '.well-known');
    fs.mkdirSync(wellKnownDir, { recursive: true });
    const mcpConfig = generateWellKnownMCP('integralmarket.ai', 'YOUR_INDEXNOW_KEY');
    fs.writeFileSync(
      path.join(wellKnownDir, 'mcp.json'),
      JSON.stringify(mcpConfig, null, 2),
      'utf-8'
    );
  }

  return { sitemap, robots, urls };
}

if (require.main === module) {
  const outDir = path.join(__dirname, 'output');
  const { sitemap, robots, urls } = generateIndexingOutput(outDir);

  console.log(`Sitemap generated: ${urls.length} URLs`);
  console.log(`Robots.txt generated`);
  console.log(`Output written to: ${outDir}`);
}
