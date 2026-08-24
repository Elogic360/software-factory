import * as fs from "fs";
import * as path from "path";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface JsonLdNode {
  "@context": string;
  "@type": string | string[];
  "@id": string;
  name: string;
  description: string;
  url: string;
  sameAs?: string[];
  [key: string]: unknown;
}

interface GraphEdge {
  source: string;
  relation: string;
  target: string;
}

interface KnowledgeGraph {
  nodes: JsonLdNode[];
  edges: GraphEdge[];
}

// ---------------------------------------------------------------------------
// Platform configuration
// ---------------------------------------------------------------------------

const BASE_URL = "https://integralmarket.com";
const ORG_ID = `${BASE_URL}/#organization`;

const socialLinks = {
  github: "https://github.com/integral-market",
  twitter: "https://x.com/integralmarket",
  linkedin: "https://linkedin.com/company/integral-market",
};

// ---------------------------------------------------------------------------
// Core entity definitions
// ---------------------------------------------------------------------------

const organizationNode: JsonLdNode = {
  "@context": "https://schema.org",
  "@type": ["Organization", "EducationalOrganization"],
  "@id": ORG_ID,
  name: "Integral Market",
  description:
    "Institutional-grade AI-native fintech ecosystem — copy trading, journaling, charting, market intelligence, and education.",
  url: BASE_URL,
  sameAs: [socialLinks.github, socialLinks.twitter, socialLinks.linkedin],
  logo: `${BASE_URL}/logo.png`,
  foundingDate: "2025",
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "customer service",
    availableLanguage: ["English"],
  },
};

// Platform product / feature nodes

interface EntityDef {
  id: string;
  name: string;
  type: string | string[];
  description: string;
  path: string;
  keywords: string[];
}

const entities: EntityDef[] = [
  {
    id: "im-academy",
    name: "IM Academy",
    type: ["EducationalOrganization", "Course"],
    description:
      "Structured trading education with courses on forex, stocks, crypto, and AI-assisted trading strategies.",
    path: "/academy",
    keywords: [
      "trading courses",
      "forex education",
      "stock trading course",
      "crypto trading course",
      "AI trading education",
    ],
  },
  {
    id: "im-library",
    name: "IM Library",
    type: "DigitalDocument",
    description:
      "Curated digital library of trading books, research papers, and strategy documentation.",
    path: "/library",
    keywords: [
      "trading books",
      "research papers",
      "trading strategies",
      "digital library",
    ],
  },
  {
    id: "ai-journal",
    name: "AI Journal",
    type: ["SoftwareApplication", "Product"],
    description:
      "AI-powered trading journal with automated trade logging, performance analytics, and behavioral insights.",
    path: "/journal",
    keywords: [
      "AI trading journal",
      "trade logging",
      "performance analytics",
      "trading psychology",
    ],
  },
  {
    id: "trading-journal",
    name: "Trading Journal",
    type: ["SoftwareApplication", "Product"],
    description:
      "Manual and MT5-synced trading journal with advanced analytics and risk management metrics.",
    path: "/journal",
    keywords: [
      "trading journal",
      "MT5 journal",
      "trade history",
      "risk management",
    ],
  },
  {
    id: "market-intelligence",
    name: "Market Intelligence",
    type: ["SoftwareApplication", "Product"],
    description:
      "Real-time AI-powered market analysis combining technical, fundamental, and sentiment data.",
    path: "/intelligence",
    keywords: [
      "market analysis",
      "AI analysis",
      "technical analysis",
      "fundamental analysis",
      "sentiment analysis",
    ],
  },
  {
    id: "copy-trading",
    name: "Copy Trading",
    type: ["SoftwareApplication", "Product"],
    description:
      "Social copy trading platform connecting signal providers with subscribers for automated trade replication.",
    path: "/copy-trading",
    keywords: [
      "copy trading",
      "signal providers",
      "trade replication",
      "social trading",
    ],
  },
  {
    id: "imcharts",
    name: "imCharts",
    type: ["SoftwareApplication", "Feature"],
    description:
      "Advanced charting suite with TradingView integration, watchlists, and trade execution directly from charts.",
    path: "/charts",
    keywords: [
      "TradingView charts",
      "interactive charts",
      "watchlists",
      "trade execution",
      "charting platform",
    ],
  },
  {
    id: "forex-trading",
    name: "Forex Trading",
    type: "Topic",
    description:
      "Foreign exchange trading — currency pairs, market hours, broker integration, and MT5 connectivity.",
    path: "/learn/forex",
    keywords: [
      "forex trading",
      "currency pairs",
      "MT5",
      "forex broker",
      "forex strategy",
    ],
  },
  {
    id: "stock-trading",
    name: "Stock Trading",
    type: "Topic",
    description:
      "Equity market trading — stock analysis, portfolio management, and long/short strategies.",
    path: "/learn/stocks",
    keywords: [
      "stock trading",
      "equity analysis",
      "portfolio management",
      "stock market",
    ],
  },
  {
    id: "crypto-trading",
    name: "Cryptocurrency Trading",
    type: "Topic",
    description:
      "Digital asset trading — BTC, ETH, altcoins, DeFi strategies, and exchange integrations.",
    path: "/learn/crypto",
    keywords: [
      "cryptocurrency trading",
      "Bitcoin trading",
      "DeFi",
      "crypto strategies",
    ],
  },
  {
    id: "ai-trading-assistant",
    name: "AI Trading Assistant",
    type: "SoftwareApplication",
    description:
      "LLM-powered trading assistant for trade journaling, strategy analysis, and real-time market Q&A.",
    path: "/ai-assistant",
    keywords: [
      "AI trading assistant",
      "LLM trading",
      "AI analysis",
      "trading insights",
    ],
  },
  {
    id: "trading-psychology",
    name: "Trading Psychology",
    type: "Topic",
    description:
      "Behavioral finance, emotional discipline, and psychological frameworks for consistent trading performance.",
    path: "/learn/psychology",
    keywords: [
      "trading psychology",
      "behavioral finance",
      "emotional discipline",
      "trading mindset",
    ],
  },
  {
    id: "backtesting",
    name: "Backtesting",
    type: "SoftwareApplication",
    description:
      "Strategy backtesting engine for validating trading strategies against historical market data.",
    path: "/backtesting",
    keywords: [
      "backtesting",
      "strategy validation",
      "historical data",
      "quantitative analysis",
    ],
  },
];

// ---------------------------------------------------------------------------
// Relationship edges
// ---------------------------------------------------------------------------

const edges: GraphEdge[] = [
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/academy` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/library` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/journal` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/intelligence` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/copy-trading` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/charts` },
  { source: ORG_ID, relation: "hasPart", target: `${BASE_URL}/ai-assistant` },

  { source: `${BASE_URL}/academy`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/library`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/journal`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/intelligence`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/copy-trading`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/charts`, relation: "isPartOf", target: ORG_ID },
  { source: `${BASE_URL}/ai-assistant`, relation: "isPartOf", target: ORG_ID },

  { source: `${BASE_URL}/journal`, relation: "uses", target: `${BASE_URL}/ai-assistant` },
  { source: `${BASE_URL}/journal`, relation: "uses", target: `${BASE_URL}/intelligence` },
  { source: `${BASE_URL}/charts`, relation: "uses", target: `${BASE_URL}/intelligence` },
  { source: `${BASE_URL}/copy-trading`, relation: "uses", target: `${BASE_URL}/charts` },
  { source: `${BASE_URL}/copy-trading`, relation: "uses", target: `${BASE_URL}/journal` },

  { source: `${BASE_URL}/academy`, relation: "teaches", target: `${BASE_URL}/learn/forex` },
  { source: `${BASE_URL}/academy`, relation: "teaches", target: `${BASE_URL}/learn/stocks` },
  { source: `${BASE_URL}/academy`, relation: "teaches", target: `${BASE_URL}/learn/crypto` },
  { source: `${BASE_URL}/academy`, relation: "teaches", target: `${BASE_URL}/learn/psychology` },
  { source: `${BASE_URL}/backtesting`, relation: "isFeatureOf", target: `${BASE_URL}/charts` },
];

// ---------------------------------------------------------------------------
// Build JSON-LD graph
// ---------------------------------------------------------------------------

function buildGraph(): KnowledgeGraph {
  const nodes: JsonLdNode[] = [organizationNode];

  for (const e of entities) {
    nodes.push({
      "@context": "https://schema.org",
      "@type": e.type,
      "@id": `${BASE_URL}${e.path}`,
      name: e.name,
      description: e.description,
      url: `${BASE_URL}${e.path}`,
      keywords: e.keywords.join(", "),
      isPartOf: { "@id": ORG_ID },
      provider: { "@id": ORG_ID },
    });
  }

  return { nodes, edges };
}

// ---------------------------------------------------------------------------
// Serialise to JSON-LD
// ---------------------------------------------------------------------------

function serialiseJsonLd(graph: KnowledgeGraph): string {
  const context = {
    "@vocab": "https://schema.org/",
    hasPart: "https://schema.org/hasPart",
    isPartOf: "https://schema.org/isPartOf",
    uses: { "@id": "https://schema.org/uses", "@type": "@id" },
    teaches: { "@id": "https://schema.org/teaches", "@type": "@id" },
    isFeatureOf: { "@id": "https://schema.org/isBasedOn", "@type": "@id" },
  };

  const payload = {
    "@context": context,
    "@graph": graph.nodes,
    _edges: graph.edges,
  };

  return JSON.stringify(payload, null, 2);
}

// ---------------------------------------------------------------------------
// Serialise to Turtle
// ---------------------------------------------------------------------------

function esc(s: string): string {
  return s.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function serialiseTurtle(graph: KnowledgeGraph): string {
  const lines: string[] = [
    "@prefix schema: <https://schema.org/> .",
    "@prefix kg:     <https://integralmarket.com/graph/> .",
    "",
  ];

  for (const node of graph.nodes) {
    const id = node["@id"]!;
    const types = Array.isArray(node["@type"]) ? node["@type"] : [node["@type"]];
    const typesStr = types.map((t) => `schema:${t}`).join(", ");

    lines.push(`<${id}> a ${typesStr} ;`);
    lines.push(`  schema:name "${esc(node.name)}" ;`);
    lines.push(`  schema:description "${esc(node.description)}" ;`);
    lines.push(`  schema:url <${node.url}> ;`);

    if (node.sameAs) {
      for (const s of node.sameAs) {
        lines.push(`  schema:sameAs <${s}> ;`);
      }
    }
    if (node.keywords) {
      lines.push(`  schema:keyword "${esc(node.keywords as string)}" ;`);
    }

    lines.push("  .");
    lines.push("");
  }

  for (const edge of graph.edges) {
    lines.push(`<${edge.source}> kg:${edge.relation} <${edge.target}> .`);
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Write outputs
// ---------------------------------------------------------------------------

function writeOutputs(graph: KnowledgeGraph): void {
  const outDir = path.resolve(__dirname, "dist");
  fs.mkdirSync(outDir, { recursive: true });

  const jsonLd = serialiseJsonLd(graph);
  fs.writeFileSync(path.join(outDir, "graph.jsonld"), jsonLd, "utf-8");

  const turtle = serialiseTurtle(graph);
  fs.writeFileSync(path.join(outDir, "graph.ttl"), turtle, "utf-8");

  console.log(`[graph-builder] wrote ${graph.nodes.length} nodes, ${graph.edges.length} edges`);
  console.log(`  → ${path.join(outDir, "graph.jsonld")}`);
  console.log(`  → ${path.join(outDir, "graph.ttl")}`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main(): void {
  const graph = buildGraph();
  writeOutputs(graph);
}

main();
