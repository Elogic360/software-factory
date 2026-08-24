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
exports.generateMetadata = generateMetadata;
/**
 * OpenGraph & Twitter Card Metadata Generator
 * Generates per-page metadata for social sharing and AI crawlers.
 */
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const BASE_URL = 'https://integralmarket.tech';
const OUTPUT_DIR = path.join(__dirname, '../dist/metadata');
const PAGES = [
    {
        path: '/',
        title: 'Integral Market — AI-Native Financial Intelligence Platform',
        description: 'Institutional-grade AI trading journal, analytics, academy, and market intelligence. Automate trade logging, track psychology, and master markets.',
        image: `${BASE_URL}/og/home.png`,
        type: 'website',
        keywords: ['AI trading journal', 'trading platform', 'financial intelligence', 'trading analytics'],
    },
    {
        path: '/academy',
        title: 'IM Academy — Trading Education Platform',
        description: 'Expert-led courses in forex, crypto, technical analysis, and trading psychology. Learn from professionals with structured curriculum.',
        image: `${BASE_URL}/og/academy.png`,
        type: 'website',
        keywords: ['trading academy', 'forex courses', 'crypto education', 'trading psychology'],
    },
    {
        path: '/library',
        title: 'IM Library — Trading Research & Strategy Database',
        description: 'Comprehensive digital library of trading strategies, research papers, and educational resources.',
        image: `${BASE_URL}/og/library.png`,
        type: 'website',
        keywords: ['trading library', 'strategy database', 'research papers', 'trading guides'],
    },
    {
        path: '/ai/trading-journal',
        title: 'AI Trading Journal — Automated Trade Logging & Analytics',
        description: 'The best AI trading journal. Automate trade logging, track psychological patterns, and analyze execution quality with AI.',
        image: `${BASE_URL}/og/ai-journal.png`,
        type: 'product',
        keywords: ['AI trading journal', 'trade logging', 'trading analytics', 'best trading journal'],
    },
    {
        path: '/ai/faq',
        title: 'Frequently Asked Questions — Integral Market',
        description: 'Answers to common questions about Integral Market, AI trading journals, and our financial intelligence platform.',
        image: `${BASE_URL}/og/faq.png`,
        type: 'website',
        keywords: ['Integral Market FAQ', 'AI trading journal FAQ', 'trading platform questions'],
    },
    {
        path: '/docs/api',
        title: 'Integral Market API Documentation',
        description: 'Complete API reference for integrating with Integral Market. REST endpoints, WebSocket streams, and SDK documentation.',
        image: `${BASE_URL}/og/api-docs.png`,
        type: 'website',
        keywords: ['trading API', 'REST API', 'WebSocket API', 'financial API'],
    },
];
function generateOGMeta(page) {
    return `<!-- OpenGraph -->
<meta property="og:type" content="${page.type}" />
<meta property="og:title" content="${page.title}" />
<meta property="og:description" content="${page.description}" />
<meta property="og:image" content="${page.image}" />
<meta property="og:url" content="${BASE_URL}${page.path}" />
<meta property="og:site_name" content="Integral Market" />
<meta property="og:locale" content="en_US" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@Integral_Market" />
<meta name="twitter:title" content="${page.title}" />
<meta name="twitter:description" content="${page.description}" />
<meta name="twitter:image" content="${page.image}" />

<!-- SEO -->
<meta name="description" content="${page.description}" />
<meta name="keywords" content="${page.keywords.join(', ')}" />
<link rel="canonical" href="${BASE_URL}${page.path}" />
`;
}
function generateMetadata() {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    for (const page of PAGES) {
        const filename = page.path === '/' ? 'home' : page.path.replace(/\//g, '_').slice(1);
        const content = generateOGMeta(page);
        fs.writeFileSync(path.join(OUTPUT_DIR, `${filename}.html`), content);
    }
    console.log(`✅ Generated ${PAGES.length} OpenGraph metadata files`);
}
if (require.main === module) {
    generateMetadata();
}
