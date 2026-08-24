import * as fs from "fs";
import * as path from "path";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type EntityType = "Platform" | "Product" | "Feature" | "Capability" | "Topic" | "Course" | "Book";

interface EntityMeta {
  id: string;
  name: string;
  type: EntityType;
  description: string;
  url: string;
  canonical: string;
  jsonld: Record<string, unknown>;
  openGraph: {
    title: string;
    description: string;
    url: string;
    type: "website" | "product";
    image: string;
  };
  keywords: string[];
  faq: { question: string; answer: string }[];
  landingPage: string;
  documentationRef: string;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const BASE_URL = "https://integralmarket.com";
const ORG_ID = `${BASE_URL}/#organization`;

// ---------------------------------------------------------------------------
// Entity definitions
// ---------------------------------------------------------------------------

const entities: EntityMeta[] = [
  {
    id: "integral-market",
    name: "Integral Market",
    type: "Platform",
    description:
      "Institutional-grade AI-native fintech ecosystem combining copy trading, journaling, charting, market intelligence, and education.",
    url: BASE_URL,
    canonical: BASE_URL,
    jsonld: {
      "@context": "https://schema.org",
      "@type": ["Organization", "EducationalOrganization"],
      "@id": ORG_ID,
      name: "Integral Market",
      url: BASE_URL,
      sameAs: [
        "https://github.com/integral-market",
        "https://x.com/integralmarket",
        "https://linkedin.com/company/integral-market",
      ],
    },
    openGraph: {
      title: "Integral Market — AI-Native Trading Ecosystem",
      description: "Copy trading, journaling, charting, and market intelligence powered by AI.",
      url: BASE_URL,
      type: "website",
      image: `${BASE_URL}/og/integral-market.png`,
    },
    keywords: [
      "Integral Market",
      "trading platform",
      "AI fintech",
      "copy trading",
      "trading journal",
    ],
    faq: [
      {
        question: "What is Integral Market?",
        answer:
          "Integral Market is an AI-native fintech ecosystem that provides copy trading, trading journals, advanced charting, market intelligence, and structured education.",
      },
      {
        question: "Is Integral Market free to use?",
        answer:
          "Integral Market offers a free tier for core features. Premium plans unlock advanced analytics, AI features, and priority support.",
      },
    ],
    landingPage: "/",
    documentationRef: "/docs/platform-overview",
  },

  {
    id: "im-academy",
    name: "IM Academy",
    type: "Course",
    description:
      "Structured trading education with expert-led courses on forex, stocks, cryptocurrency, and AI-assisted trading strategies.",
    url: `${BASE_URL}/academy`,
    canonical: `${BASE_URL}/academy`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "EducationalOrganization",
      "@id": `${BASE_URL}/academy`,
      name: "IM Academy",
      description:
        "Structured trading education with expert-led courses on forex, stocks, cryptocurrency, and AI-assisted trading strategies.",
      url: `${BASE_URL}/academy`,
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "USD",
      },
    },
    openGraph: {
      title: "IM Academy — Trading Education",
      description: "Expert-led courses on forex, stocks, crypto, and AI-assisted strategies.",
      url: `${BASE_URL}/academy`,
      type: "website",
      image: `${BASE_URL}/og/academy.png`,
    },
    keywords: [
      "trading courses",
      "forex education",
      "stock trading course",
      "crypto trading course",
      "AI trading education",
      "online trading academy",
    ],
    faq: [
      {
        question: "What courses are available in IM Academy?",
        answer:
          "IM Academy offers courses on forex trading, stock market fundamentals, cryptocurrency markets, AI-assisted trading, and trading psychology.",
      },
      {
        question: "Are the courses self-paced?",
        answer:
          "Yes. All courses are self-paced with lifetime access. Each module includes video lessons, quizzes, and practical exercises.",
      },
    ],
    landingPage: "/academy",
    documentationRef: "/docs/academy",
  },

  {
    id: "im-library",
    name: "IM Library",
    type: "Book",
    description:
      "Curated digital library of trading books, research papers, strategy documentation, and market analysis reports.",
    url: `${BASE_URL}/library`,
    canonical: `${BASE_URL}/library`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "DigitalDocument",
      "@id": `${BASE_URL}/library`,
      name: "IM Library",
      description:
        "Curated digital library of trading books, research papers, and strategy documentation.",
      url: `${BASE_URL}/library`,
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "IM Library — Trading Resources",
      description: "Curated books, research papers, and strategy documentation.",
      url: `${BASE_URL}/library`,
      type: "website",
      image: `${BASE_URL}/og/library.png`,
    },
    keywords: [
      "trading books",
      "research papers",
      "trading strategies",
      "digital library",
      "market analysis reports",
    ],
    faq: [
      {
        question: "What type of content is in IM Library?",
        answer:
          "IM Library contains trading books, academic research papers, strategy guides, and market analysis reports organized by topic and difficulty level.",
      },
    ],
    landingPage: "/library",
    documentationRef: "/docs/library",
  },

  {
    id: "ai-journal",
    name: "AI Journal",
    type: "Product",
    description:
      "AI-powered trading journal with automated trade logging, performance analytics, and behavioral insights.",
    url: `${BASE_URL}/journal`,
    canonical: `${BASE_URL}/journal`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/journal`,
      name: "AI Journal",
      description: "AI-powered trading journal with automated trade logging and analytics.",
      url: `${BASE_URL}/journal`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "AI Journal — Intelligent Trade Journaling",
      description: "Automated trade logging, performance analytics, and behavioral insights.",
      url: `${BASE_URL}/journal`,
      type: "product",
      image: `${BASE_URL}/og/ai-journal.png`,
    },
    keywords: [
      "AI trading journal",
      "trade logging",
      "performance analytics",
      "trading psychology",
      "automated journal",
    ],
    faq: [
      {
        question: "How does the AI Journal work?",
        answer:
          "The AI Journal automatically logs trades from your connected broker, analyzes patterns, and provides behavioral insights to improve your trading performance.",
      },
      {
        question: "Which brokers are supported?",
        answer:
          "AI Journal supports MT5, Binance, and cTrader integrations for automated trade sync.",
      },
    ],
    landingPage: "/journal",
    documentationRef: "/docs/ai-journal",
  },

  {
    id: "trading-journal",
    name: "Trading Journal",
    type: "Product",
    description:
      "Manual and MT5-synced trading journal with advanced analytics, risk management metrics, and performance tracking.",
    url: `${BASE_URL}/journal`,
    canonical: `${BASE_URL}/journal`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/trading-journal`,
      name: "Trading Journal",
      description: "Manual and MT5-synced trading journal with advanced analytics.",
      url: `${BASE_URL}/journal`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "Trading Journal — Track Every Trade",
      description: "Manual and MT5-synced journal with risk management metrics.",
      url: `${BASE_URL}/journal`,
      type: "product",
      image: `${BASE_URL}/og/trading-journal.png`,
    },
    keywords: [
      "trading journal",
      "MT5 journal",
      "trade history",
      "risk management",
      "performance tracking",
    ],
    faq: [
      {
        question: "Can I manually add trades?",
        answer:
          "Yes. You can manually log trades or enable automatic sync from MT5 and other supported brokers.",
      },
    ],
    landingPage: "/journal",
    documentationRef: "/docs/trading-journal",
  },

  {
    id: "market-intelligence",
    name: "Market Intelligence",
    type: "Capability",
    description:
      "Real-time AI-powered market analysis combining technical, fundamental, and sentiment data from multiple sources.",
    url: `${BASE_URL}/intelligence`,
    canonical: `${BASE_URL}/intelligence`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/intelligence`,
      name: "Market Intelligence",
      description: "AI-powered market analysis with technical, fundamental, and sentiment data.",
      url: `${BASE_URL}/intelligence`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "Market Intelligence — AI-Powered Analysis",
      description: "Real-time technical, fundamental, and sentiment analysis powered by AI.",
      url: `${BASE_URL}/intelligence`,
      type: "product",
      image: `${BASE_URL}/og/market-intelligence.png`,
    },
    keywords: [
      "market analysis",
      "AI analysis",
      "technical analysis",
      "fundamental analysis",
      "sentiment analysis",
      "news analysis",
    ],
    faq: [
      {
        question: "What data sources does Market Intelligence use?",
        answer:
          "Market Intelligence aggregates data from financial news APIs, social sentiment feeds, on-chain analytics, and technical indicator engines.",
      },
      {
        question: "Is the analysis real-time?",
        answer:
          "Yes. Market Intelligence processes data in real-time and updates analysis continuously during market hours.",
      },
    ],
    landingPage: "/intelligence",
    documentationRef: "/docs/market-intelligence",
  },

  {
    id: "copy-trading",
    name: "Copy Trading",
    type: "Product",
    description:
      "Social copy trading platform connecting signal providers with subscribers for automated trade replication.",
    url: `${BASE_URL}/copy-trading`,
    canonical: `${BASE_URL}/copy-trading`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/copy-trading`,
      name: "Copy Trading",
      description: "Social copy trading with signal providers and automated trade replication.",
      url: `${BASE_URL}/copy-trading`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "Copy Trading — Follow Top Traders",
      description: "Automated trade replication from verified signal providers.",
      url: `${BASE_URL}/copy-trading`,
      type: "product",
      image: `${BASE_URL}/og/copy-trading.png`,
    },
    keywords: [
      "copy trading",
      "signal providers",
      "trade replication",
      "social trading",
      "automated trading",
    ],
    faq: [
      {
        question: "How does copy trading work?",
        answer:
          "Signal providers share their trades in real-time. Subscribers can automatically replicate those trades in their own accounts.",
      },
      {
        question: "How are signal providers verified?",
        answer:
          "Providers undergo performance verification including track record analysis, risk metrics, and consistency scoring.",
      },
    ],
    landingPage: "/copy-trading",
    documentationRef: "/docs/copy-trading",
  },

  {
    id: "imcharts",
    name: "imCharts",
    type: "Feature",
    description:
      "Advanced charting suite with TradingView integration, watchlists, and trade execution directly from charts.",
    url: `${BASE_URL}/charts`,
    canonical: `${BASE_URL}/charts`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/charts`,
      name: "imCharts",
      description: "Advanced charting with TradingView integration and trade execution.",
      url: `${BASE_URL}/charts`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "imCharts — Advanced Trading Charts",
      description: "TradingView-powered charts with watchlists and one-click execution.",
      url: `${BASE_URL}/charts`,
      type: "product",
      image: `${BASE_URL}/og/imcharts.png`,
    },
    keywords: [
      "TradingView charts",
      "interactive charts",
      "watchlists",
      "trade execution",
      "charting platform",
    ],
    faq: [
      {
        question: "What charting technology does imCharts use?",
        answer:
          "imCharts integrates TradingView's charting library with custom indicators, watchlists, and direct trade execution.",
      },
    ],
    landingPage: "/charts",
    documentationRef: "/docs/imcharts",
  },

  {
    id: "forex-trading",
    name: "Forex Trading",
    type: "Topic",
    description:
      "Foreign exchange trading — currency pairs, market hours, broker integration, and MT5 connectivity.",
    url: `${BASE_URL}/learn/forex`,
    canonical: `${BASE_URL}/learn/forex`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "Topic",
      "@id": `${BASE_URL}/learn/forex`,
      name: "Forex Trading",
      description: "Foreign exchange trading — currency pairs, market hours, and MT5 connectivity.",
      url: `${BASE_URL}/learn/forex`,
      isPartOf: { "@id": `${BASE_URL}/academy` },
    },
    openGraph: {
      title: "Forex Trading — IM Academy",
      description: "Learn forex trading with structured courses and live practice.",
      url: `${BASE_URL}/learn/forex`,
      type: "website",
      image: `${BASE_URL}/og/forex-trading.png`,
    },
    keywords: [
      "forex trading",
      "currency pairs",
      "MT5",
      "forex broker",
      "forex strategy",
    ],
    faq: [
      {
        question: "What is forex trading?",
        answer:
          "Forex trading is the buying and selling of currency pairs in the foreign exchange market, the largest and most liquid financial market in the world.",
      },
    ],
    landingPage: "/learn/forex",
    documentationRef: "/docs/forex",
  },

  {
    id: "stock-trading",
    name: "Stock Trading",
    type: "Topic",
    description:
      "Equity market trading — stock analysis, portfolio management, and long/short strategies.",
    url: `${BASE_URL}/learn/stocks`,
    canonical: `${BASE_URL}/learn/stocks`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "Topic",
      "@id": `${BASE_URL}/learn/stocks`,
      name: "Stock Trading",
      description: "Equity market trading — stock analysis, portfolio management, and strategies.",
      url: `${BASE_URL}/learn/stocks`,
      isPartOf: { "@id": `${BASE_URL}/academy` },
    },
    openGraph: {
      title: "Stock Trading — IM Academy",
      description: "Learn stock trading fundamentals and advanced strategies.",
      url: `${BASE_URL}/learn/stocks`,
      type: "website",
      image: `${BASE_URL}/og/stock-trading.png`,
    },
    keywords: [
      "stock trading",
      "equity analysis",
      "portfolio management",
      "stock market",
      "long short strategies",
    ],
    faq: [
      {
        question: "How do I start stock trading?",
        answer:
          "Start with IM Academy's stock trading fundamentals course covering market structure, technical analysis, and risk management.",
      },
    ],
    landingPage: "/learn/stocks",
    documentationRef: "/docs/stocks",
  },

  {
    id: "crypto-trading",
    name: "Cryptocurrency Trading",
    type: "Topic",
    description:
      "Digital asset trading — BTC, ETH, altcoins, DeFi strategies, and exchange integrations.",
    url: `${BASE_URL}/learn/crypto`,
    canonical: `${BASE_URL}/learn/crypto`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "Topic",
      "@id": `${BASE_URL}/learn/crypto`,
      name: "Cryptocurrency Trading",
      description: "Digital asset trading — BTC, ETH, altcoins, and DeFi strategies.",
      url: `${BASE_URL}/learn/crypto`,
      isPartOf: { "@id": `${BASE_URL}/academy` },
    },
    openGraph: {
      title: "Cryptocurrency Trading — IM Academy",
      description: "Learn crypto trading from basics to advanced DeFi strategies.",
      url: `${BASE_URL}/learn/crypto`,
      type: "website",
      image: `${BASE_URL}/og/crypto-trading.png`,
    },
    keywords: [
      "cryptocurrency trading",
      "Bitcoin trading",
      "DeFi",
      "crypto strategies",
      "altcoin trading",
    ],
    faq: [
      {
        question: "Which cryptocurrencies can I trade?",
        answer:
          "Integral Market supports major cryptocurrencies including BTC, ETH, and top altcoins through integrated exchanges like Binance.",
      },
    ],
    landingPage: "/learn/crypto",
    documentationRef: "/docs/crypto",
  },

  {
    id: "ai-trading-assistant",
    name: "AI Trading Assistant",
    type: "Capability",
    description:
      "LLM-powered trading assistant for trade journaling, strategy analysis, and real-time market Q&A.",
    url: `${BASE_URL}/ai-assistant`,
    canonical: `${BASE_URL}/ai-assistant`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/ai-assistant`,
      name: "AI Trading Assistant",
      description: "LLM-powered assistant for trade analysis and market Q&A.",
      url: `${BASE_URL}/ai-assistant`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "AI Trading Assistant — Your Trading Co-Pilot",
      description: "AI-powered trade analysis, journaling assistance, and market Q&A.",
      url: `${BASE_URL}/ai-assistant`,
      type: "product",
      image: `${BASE_URL}/og/ai-assistant.png`,
    },
    keywords: [
      "AI trading assistant",
      "LLM trading",
      "AI analysis",
      "trading insights",
      "trade co-pilot",
    ],
    faq: [
      {
        question: "What can the AI Trading Assistant do?",
        answer:
          "It analyzes your trades, identifies patterns, answers market questions, and helps you maintain a structured trading journal.",
      },
    ],
    landingPage: "/ai-assistant",
    documentationRef: "/docs/ai-assistant",
  },

  {
    id: "trading-psychology",
    name: "Trading Psychology",
    type: "Topic",
    description:
      "Behavioral finance, emotional discipline, and psychological frameworks for consistent trading performance.",
    url: `${BASE_URL}/learn/psychology`,
    canonical: `${BASE_URL}/learn/psychology`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "Topic",
      "@id": `${BASE_URL}/learn/psychology`,
      name: "Trading Psychology",
      description: "Behavioral finance and psychological frameworks for trading.",
      url: `${BASE_URL}/learn/psychology`,
      isPartOf: { "@id": `${BASE_URL}/academy` },
    },
    openGraph: {
      title: "Trading Psychology — Master Your Mind",
      description: "Behavioral finance, discipline, and psychological frameworks for traders.",
      url: `${BASE_URL}/learn/psychology`,
      type: "website",
      image: `${BASE_URL}/og/trading-psychology.png`,
    },
    keywords: [
      "trading psychology",
      "behavioral finance",
      "emotional discipline",
      "trading mindset",
    ],
    faq: [
      {
        question: "Why is trading psychology important?",
        answer:
          "Trading psychology governs decision-making under uncertainty. Mastering it reduces emotional errors and improves consistency.",
      },
    ],
    landingPage: "/learn/psychology",
    documentationRef: "/docs/psychology",
  },

  {
    id: "backtesting",
    name: "Backtesting",
    type: "Capability",
    description:
      "Strategy backtesting engine for validating trading strategies against historical market data.",
    url: `${BASE_URL}/backtesting`,
    canonical: `${BASE_URL}/backtesting`,
    jsonld: {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "@id": `${BASE_URL}/backtesting`,
      name: "Backtesting",
      description: "Strategy backtesting engine for historical data validation.",
      url: `${BASE_URL}/backtesting`,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    },
    openGraph: {
      title: "Backtesting — Validate Your Strategies",
      description: "Test trading strategies against historical market data.",
      url: `${BASE_URL}/backtesting`,
      type: "product",
      image: `${BASE_URL}/og/backtesting.png`,
    },
    keywords: [
      "backtesting",
      "strategy validation",
      "historical data",
      "quantitative analysis",
      "strategy testing",
    ],
    faq: [
      {
        question: "What data is available for backtesting?",
        answer:
          "Backtesting supports historical OHLCV data across forex, stocks, and cryptocurrency markets with configurable timeframes.",
      },
    ],
    landingPage: "/backtesting",
    documentationRef: "/docs/backtesting",
  },
];

// ---------------------------------------------------------------------------
// Registry API
// ---------------------------------------------------------------------------

const registryById = new Map<string, EntityMeta>();
for (const e of entities) {
  registryById.set(e.id, e);
}

export function getEntity(id: string): EntityMeta | undefined {
  return registryById.get(id);
}

export function getAllEntities(): readonly EntityMeta[] {
  return entities;
}

export function getEntitiesByType(type: EntityType): EntityMeta[] {
  return entities.filter((e) => e.type === type);
}

export function searchEntities(query: string): EntityMeta[] {
  const q = query.toLowerCase();
  return entities.filter(
    (e) =>
      e.name.toLowerCase().includes(q) ||
      e.description.toLowerCase().includes(q) ||
      e.keywords.some((k) => k.toLowerCase().includes(q)),
  );
}

// ---------------------------------------------------------------------------
// Per-entity JSON-LD snippet generator
// ---------------------------------------------------------------------------

function generateEntityJsonLd(entity: EntityMeta): string {
  return JSON.stringify(entity.jsonld, null, 2);
}

// ---------------------------------------------------------------------------
// Write individual JSON-LD snippets to dist/
// ---------------------------------------------------------------------------

function writeEntitySnippets(): void {
  const outDir = path.resolve(__dirname, "dist", "entities");
  fs.mkdirSync(outDir, { recursive: true });

  for (const entity of entities) {
    const filePath = path.join(outDir, `${entity.id}.jsonld`);
    fs.writeFileSync(filePath, generateEntityJsonLd(entity), "utf-8");
  }

  // Write a combined registry index
  const index = entities.map((e) => ({
    id: e.id,
    name: e.name,
    type: e.type,
    url: e.url,
    canonical: e.canonical,
    keywords: e.keywords,
    faqCount: e.faq.length,
  }));

  fs.writeFileSync(
    path.join(outDir, "_index.json"),
    JSON.stringify(index, null, 2),
    "utf-8",
  );

  console.log(`[entity-registry] wrote ${entities.length} entity snippets to ${outDir}`);
}

// ---------------------------------------------------------------------------
// Main (when run directly)
// ---------------------------------------------------------------------------

if (require.main === module) {
  writeEntitySnippets();
}

export { entities, type EntityMeta, type EntityType };
