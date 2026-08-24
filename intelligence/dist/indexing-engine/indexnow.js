"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateSitemap = generateSitemap;
exports.generateRobotsTxt = generateRobotsTxt;
exports.generateWellKnownMCP = generateWellKnownMCP;
exports.pushToIndexNow = pushToIndexNow;
exports.generateIndexingOutput = generateIndexingOutput;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const https = __importStar(require("https"));
const SITE_URL = 'https://integralmarket.ai';
const ENTITY_URLS = [
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
function generateSitemap() {
    const lines = [];
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
function generateRobotsTxt() {
    const lines = [];
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
function generateWellKnownMCP(host, key) {
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
async function pushToIndexNow(urls, host, key) {
    const payload = {
        host,
        key,
        keyLocation: `https://${host}/${key}.txt`,
        urlList: urls
    };
    const body = JSON.stringify(payload);
    return new Promise((resolve) => {
        const req = https.request({
            hostname: 'api.indexnow.org',
            port: 443,
            path: '/indexnow',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': Buffer.byteLength(body)
            }
        }, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode || 0,
                    message: data || 'No response body',
                    errors: res.statusCode && res.statusCode >= 400 ? [data] : undefined
                });
            });
        });
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
function generateIndexingOutput(outputDir) {
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
        fs.writeFileSync(path.join(wellKnownDir, 'mcp.json'), JSON.stringify(mcpConfig, null, 2), 'utf-8');
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
