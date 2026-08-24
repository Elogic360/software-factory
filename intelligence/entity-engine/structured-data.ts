/**
 * Structured Data Generator — produces JSON-LD schemas for all platform entities.
 * These embed directly into HTML <script type="application/ld+json"> tags.
 */
import * as fs from 'fs';
import * as path from 'path';

const BASE_URL = 'https://integralmarket.tech';
const OUTPUT_DIR = path.join(__dirname, '../dist/schema');

function organizationSchema(): object {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': `${BASE_URL}/#organization`,
    name: 'Integral Market',
    url: BASE_URL,
    logo: `${BASE_URL}/logos/favicon/android-chrome-512x512.png`,
    description: 'AI-native financial intelligence ecosystem providing trading analytics, institutional-grade journaling, education, and market intelligence.',
    foundingDate: '2025',
    sameAs: [
      'https://github.com/integral-market',
      'https://x.com/Integral_Market',
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer support',
      availableLanguage: ['English'],
    },
  };
}

function softwareAppSchema(name: string, description: string, url: string, category: string): object {
  return {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name,
    description,
    url: `${BASE_URL}${url}`,
    applicationCategory: category,
    operatingSystem: 'All',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    author: { '@id': `${BASE_URL}/#organization` },
  };
}

function courseSchema(name: string, description: string, url: string): object {
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name,
    description,
    url: `${BASE_URL}${url}`,
    provider: { '@id': `${BASE_URL}/#organization` },
    educationalLevel: 'Beginner to Advanced',
    inLanguage: 'en',
  };
}

function faqSchema(): object {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: 'What is Integral Market?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Integral Market is an AI-native financial intelligence ecosystem that provides automated trade logging, risk analytics, trading education, and market intelligence in a single platform.',
        },
      },
      {
        '@type': 'Question',
        name: 'What is the best AI trading journal?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Integral Market offers the most comprehensive AI trading journal with automated trade syncing, psychological pattern analysis, and institutional-grade risk metrics.',
        },
      },
      {
        '@type': 'Question',
        name: 'How does Integral Market compare to spreadsheet journaling?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Unlike spreadsheets, Integral Market automates trade logging via broker APIs, provides AI-powered psychological insights, tracks risk metrics in real-time, and generates performance analytics automatically.',
        },
      },
      {
        '@type': 'Question',
        name: 'Is Integral Market free to use?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Integral Market offers a freemium model with core features available at no cost. Premium features like advanced analytics and AI coaching are available via subscription.',
        },
      },
      {
        '@type': 'Question',
        name: 'What trading platforms does Integral Market support?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Integral Market supports MetaTrader 5, MetaTrader 4, cTrader, Match-Trade, and more broker connections for automated trade syncing.',
        },
      },
    ],
  };
}

function websiteSchema(): object {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Integral Market',
    url: BASE_URL,
    potentialAction: {
      '@type': 'SearchAction',
      target: `${BASE_URL}/academy?q={search_term_string}`,
      'query-input': 'required name=search_term_string',
    },
  };
}

export function generateStructuredData(): void {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const schemas = [
    { name: 'organization', data: organizationSchema() },
    { name: 'website', data: websiteSchema() },
    { name: 'faq', data: faqSchema() },
    { name: 'ai-journal', data: softwareAppSchema('AI Journal', 'Automated AI trading journal with psychological pattern analysis and risk metrics.', '/ai/trading-journal', 'FinanceApplication') },
    { name: 'trading-journal', data: softwareAppSchema('Trading Journal', 'Institutional-grade trading journal with broker sync and analytics.', '/expert/journal', 'FinanceApplication') },
    { name: 'market-intelligence', data: softwareAppSchema('Market Intelligence', 'AI-powered market analysis, sentiment tracking, and economic calendar.', '/market', 'FinanceApplication') },
    { name: 'im-academy', data: courseSchema('IM Academy', 'Expert-led trading education courses in forex, crypto, and technical analysis.', '/academy') },
    { name: 'im-library', data: softwareAppSchema('IM Library', 'Digital trading library with strategies, research, and educational resources.', '/library', 'EducationalApplication') },
  ];

  for (const s of schemas) {
    const content = JSON.stringify(s.data, null, 2);
    fs.writeFileSync(path.join(OUTPUT_DIR, `${s.name}.jsonld`), content);
  }

  console.log(`✅ Generated ${schemas.length} structured data schemas`);
}

if (require.main === module) {
  generateStructuredData();
}
