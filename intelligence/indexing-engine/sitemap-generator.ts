/**
 * Sitemap Generator — generates XML sitemaps for Integral Market
 * Covers all entity URLs for search engine and AI crawler indexing.
 */
import * as fs from 'fs';
import * as path from 'path';

const BASE_URL = 'https://integralmarket.tech';
const OUTPUT_DIR = path.join(__dirname, '../dist/sitemap');

interface SitemapUrl {
  loc: string;
  lastmod: string;
  changefreq: string;
  priority: number;
}

function generateSitemapUrls(): SitemapUrl[] {
  const now = new Date().toISOString().split('T')[0];
  const urls: SitemapUrl[] = [];

  // Core pages
  const corePages = [
    { path: '/', priority: 1.0, freq: 'daily' },
    { path: '/academy', priority: 0.9, freq: 'daily' },
    { path: '/library', priority: 0.9, freq: 'daily' },
    { path: '/market', priority: 0.9, freq: 'daily' },
    { path: '/expert', priority: 0.9, freq: 'daily' },
    { path: '/community', priority: 0.7, freq: 'weekly' },
    { path: '/auth/login', priority: 0.3, freq: 'monthly' },
    { path: '/auth/register', priority: 0.3, freq: 'monthly' },
  ];

  for (const p of corePages) {
    urls.push({ loc: `${BASE_URL}${p.path}`, lastmod: now, changefreq: p.freq, priority: p.priority });
  }

  // AI-focused landing pages
  const aiPages = [
    { path: '/ai/trading-journal', priority: 0.9, freq: 'weekly' },
    { path: '/ai/trading-analytics', priority: 0.9, freq: 'weekly' },
    { path: '/ai/market-intelligence', priority: 0.9, freq: 'weekly' },
    { path: '/ai/copy-trading', priority: 0.8, freq: 'weekly' },
    { path: '/ai/risk-management', priority: 0.8, freq: 'weekly' },
    { path: '/ai/trading-psychology', priority: 0.8, freq: 'weekly' },
    { path: '/ai/backtesting', priority: 0.8, freq: 'weekly' },
    { path: '/ai/portfolio-tracking', priority: 0.8, freq: 'weekly' },
  ];

  for (const p of aiPages) {
    urls.push({ loc: `${BASE_URL}${p.path}`, lastmod: now, changefreq: p.freq, priority: p.priority });
  }

  // GEO pages (LLM-optimized)
  const geoPages = [
    { path: '/ai/faq', priority: 0.9, freq: 'monthly' },
    { path: '/ai/glossary', priority: 0.8, freq: 'monthly' },
    { path: '/ai/comparison', priority: 0.8, freq: 'monthly' },
    { path: '/ai/specifications', priority: 0.7, freq: 'monthly' },
    { path: '/docs/api', priority: 0.9, freq: 'weekly' },
    { path: '/docs/mcp', priority: 0.8, freq: 'weekly' },
    { path: '/docs/sdk', priority: 0.8, freq: 'weekly' },
  ];

  for (const p of geoPages) {
    urls.push({ loc: `${BASE_URL}${p.path}`, lastmod: now, changefreq: p.freq, priority: p.priority });
  }

  return urls;
}

function buildXmlSitemap(urls: SitemapUrl[]): string {
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ];

  for (const u of urls) {
    lines.push('  <url>');
    lines.push(`    <loc>${u.loc}</loc>`);
    lines.push(`    <lastmod>${u.lastmod}</lastmod>`);
    lines.push(`    <changefreq>${u.changefreq}</changefreq>`);
    lines.push(`    <priority>${u.priority}</priority>`);
    lines.push('  </url>');
  }

  lines.push('</urlset>');
  return lines.join('\n');
}

function buildRobotsTxt(): string {
  return `User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /auth/

Sitemap: ${BASE_URL}/sitemap.xml

# AI crawlers — welcome
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: CCBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /
`;
}

export function generateSitemap(): void {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const urls = generateSitemapUrls();
  const xml = buildXmlSitemap(urls);
  fs.writeFileSync(path.join(OUTPUT_DIR, 'sitemap.xml'), xml);

  const robots = buildRobotsTxt();
  fs.writeFileSync(path.join(OUTPUT_DIR, 'robots.txt'), robots);

  console.log(`✅ Generated sitemap.xml (${urls.length} URLs) and robots.txt`);
}

if (require.main === module) {
  generateSitemap();
}
