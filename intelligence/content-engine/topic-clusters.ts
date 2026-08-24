import * as fs from 'fs';
import * as path from 'path';

type ContentType =
  | 'pillar'
  | 'cluster-article'
  | 'comparison'
  | 'howto'
  | 'tutorial'
  | 'case-study'
  | 'guide'
  | 'faq'
  | 'review';

type SchemaType =
  | 'Article'
  | 'BlogPosting'
  | 'TechArticle'
  | 'HowTo'
  | 'FAQ'
  | 'Course'
  | 'ItemList'
  | 'NewsArticle'
  | 'SoftwareApplication';

type Priority = 'critical' | 'high' | 'medium' | 'low';

interface TopicClusterArticle {
  title: string;
  slug: string;
  targetKeyword: string;
  secondaryKeywords: string[];
  contentType: ContentType;
  schemaType: SchemaType;
  wordCountTarget: number;
  priority: Priority;
  internalLinks: string[];
}

interface TopicHub {
  name: string;
  slug: string;
  pillarTitle: string;
  pillarKeyword: string;
  pillarWordCount: number;
  articles: TopicClusterArticle[];
}

interface CountryKeywordCluster {
  country: string;
  countryCode: string;
  keywords: {
    keyword: string;
    searchIntent: 'informational' | 'commercial' | 'transactional' | 'navigational';
    difficulty: 'easy' | 'medium' | 'hard';
    priority: Priority;
  }[];
}

interface TopicClusterMap {
  generatedAt: string;
  hubs: TopicHub[];
  eastAfricaClusters: CountryKeywordCluster[];
  totalArticles: number;
  totalKeywords: number;
}

const TOPIC_HUBS: TopicHub[] = [
  {
    name: 'Academy',
    slug: 'academy',
    pillarTitle: 'Complete Trading Education Hub: From Beginner to Professional',
    pillarKeyword: 'trading education',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'How to Start Trading: Complete Beginner Guide 2026',
        slug: 'how-to-start-trading-beginner-guide',
        targetKeyword: 'how to start trading',
        secondaryKeywords: ['beginner trading guide', 'trading for beginners', 'start trading today'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['academy', 'forex', 'risk-management'],
      },
      {
        title: 'Technical Analysis vs Fundamental Analysis: Which Works Better?',
        slug: 'technical-vs-fundamental-analysis',
        targetKeyword: 'technical vs fundamental analysis',
        secondaryKeywords: ['TA vs FA', 'trading analysis methods', 'price analysis'],
        contentType: 'comparison',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['academy', 'quant-trading'],
      },
      {
        title: 'Price Action Trading: The Complete Strategy Guide',
        slug: 'price-action-trading-guide',
        targetKeyword: 'price action trading',
        secondaryKeywords: ['candlestick patterns', 'support resistance', 'chart patterns'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['academy', 'forex', 'stocks'],
      },
      {
        title: 'Risk Management for Beginners: Protect Your Capital',
        slug: 'risk-management-beginners',
        targetKeyword: 'risk management for beginners',
        secondaryKeywords: ['trading risk', 'capital protection', 'stop loss strategy'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 1800,
        priority: 'critical',
        internalLinks: ['risk-management', 'academy'],
      },
    ],
  },
  {
    name: 'Library',
    slug: 'library',
    pillarTitle: 'Trading Books, Resources & Research Library',
    pillarKeyword: 'trading resources',
    pillarWordCount: 3000,
    articles: [
      {
        title: '10 Best Trading Books Every Trader Must Read',
        slug: 'best-trading-books',
        targetKeyword: 'best trading books',
        secondaryKeywords: ['trading books', 'must read trading', 'trading literature'],
        contentType: 'comparison',
        schemaType: 'ItemList',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['library', 'trading-psychology'],
      },
      {
        title: 'Free Trading Courses Online: Complete Directory',
        slug: 'free-trading-courses-online',
        targetKeyword: 'free trading courses online',
        secondaryKeywords: ['trading course free', 'learn trading online', 'trading education free'],
        contentType: 'comparison',
        schemaType: 'Course',
        wordCountTarget: 1800,
        priority: 'high',
        internalLinks: ['library', 'academy'],
      },
      {
        title: 'Trading Glossary: 200+ Terms Every Trader Should Know',
        slug: 'trading-glossary',
        targetKeyword: 'trading glossary',
        secondaryKeywords: ['trading terms', 'forex terminology', 'stock market terms'],
        contentType: 'faq',
        schemaType: 'FAQ',
        wordCountTarget: 3000,
        priority: 'medium',
        internalLinks: ['library', 'forex', 'stocks', 'crypto'],
      },
    ],
  },
  {
    name: 'HedgeFund',
    slug: 'hedge-fund',
    pillarTitle: 'Hedge Fund Strategies & Institutional Trading Methods',
    pillarKeyword: 'hedge fund strategies',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'How Hedge Funds Trade: Strategies Retail Traders Can Learn',
        slug: 'hedge-fund-trading-strategies',
        targetKeyword: 'hedge fund strategies',
        secondaryKeywords: ['institutional trading', 'hedge fund methods', 'professional trading'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2500,
        priority: 'high',
        internalLinks: ['hedge-fund', 'quant-trading', 'risk-management'],
      },
      {
        title: 'Long-Short Equity Strategy Explained',
        slug: 'long-short-equity-strategy',
        targetKeyword: 'long short equity strategy',
        secondaryKeywords: ['hedge fund equity', 'market neutral', 'pairs trading'],
        contentType: 'tutorial',
        schemaType: 'TechArticle',
        wordCountTarget: 2000,
        priority: 'medium',
        internalLinks: ['hedge-fund', 'stocks', 'risk-management'],
      },
      {
        title: 'Global Macro Trading: How Funds Trade Economic Events',
        slug: 'global-macro-trading',
        targetKeyword: 'global macro trading',
        secondaryKeywords: ['macro trading', 'economic event trading', 'fundamental macro'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'medium',
        internalLinks: ['hedge-fund', 'forex', 'commodities'],
      },
    ],
  },
  {
    name: 'QuantTrading',
    slug: 'quant-trading',
    pillarTitle: 'Quantitative Trading: Algorithms, Models & Systems',
    pillarKeyword: 'quantitative trading',
    pillarWordCount: 4000,
    articles: [
      {
        title: 'Quantitative Trading for Beginners: Getting Started',
        slug: 'quantitative-trading-beginners',
        targetKeyword: 'quantitative trading',
        secondaryKeywords: ['quant trading', 'algorithmic trading', 'systematic trading'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['quant-trading', 'ai-lab'],
      },
      {
        title: 'Building Your First Trading Algorithm in Python',
        slug: 'building-trading-algorithm-python',
        targetKeyword: 'trading algorithm Python',
        secondaryKeywords: ['Python trading bot', 'algorithmic trading Python', 'automated trading'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 3000,
        priority: 'high',
        internalLinks: ['quant-trading', 'developer-center'],
      },
      {
        title: 'Backtesting Strategies: How to Validate Your Trading System',
        slug: 'backtesting-strategies-guide',
        targetKeyword: 'backtesting strategies',
        secondaryKeywords: ['backtest trading', 'strategy validation', 'trading system test'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['quant-trading', 'risk-management'],
      },
      {
        title: 'Mean Reversion vs Momentum: Which Quant Strategy Wins?',
        slug: 'mean-reversion-vs-momentum',
        targetKeyword: 'mean reversion vs momentum',
        secondaryKeywords: ['trading strategies compared', 'quant strategy', 'systematic approach'],
        contentType: 'comparison',
        schemaType: 'TechArticle',
        wordCountTarget: 2000,
        priority: 'medium',
        internalLinks: ['quant-trading', 'risk-management'],
      },
    ],
  },
  {
    name: 'MT5Lab',
    slug: 'mt5-lab',
    pillarTitle: 'MetaTrader 5 Complete Guide: Setup, Strategies & Automation',
    pillarKeyword: 'MetaTrader 5 guide',
    pillarWordCount: 4000,
    articles: [
      {
        title: 'MT5 Setup Guide for Linux: Complete Wine Installation',
        slug: 'mt5-setup-linux-wine',
        targetKeyword: 'MT5 setup Linux',
        secondaryKeywords: ['MetaTrader Linux', 'MT5 Wine', 'trading platform Linux'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['mt5-lab', 'developer-center'],
      },
      {
        title: 'Best MT5 Indicators for Forex Trading',
        slug: 'best-mt5-indicators-forex',
        targetKeyword: 'best MT5 indicators',
        secondaryKeywords: ['MT5 indicators forex', 'trading indicators MT5', 'custom indicators'],
        contentType: 'comparison',
        schemaType: 'ItemList',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['mt5-lab', 'forex'],
      },
      {
        title: 'Building Expert Advisors for MT5: Complete MQL5 Tutorial',
        slug: 'building-expert-advisors-mt5',
        targetKeyword: 'Expert Advisor MT5',
        secondaryKeywords: ['MQL5 tutorial', 'automated trading MT5', 'EA development'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 3000,
        priority: 'high',
        internalLinks: ['mt5-lab', 'developer-center', 'quant-trading'],
      },
    ],
  },
  {
    name: 'AILab',
    slug: 'ai-lab',
    pillarTitle: 'AI Trading Lab: Machine Learning for Financial Markets',
    pillarKeyword: 'AI trading',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'AI in Trading: How Machine Learning Is Changing Markets',
        slug: 'ai-in-trading',
        targetKeyword: 'AI in trading',
        secondaryKeywords: ['machine learning trading', 'AI finance', 'neural networks trading'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['ai-lab', 'quant-trading'],
      },
      {
        title: 'Building an AI Trading Bot: Complete Step-by-Step Guide',
        slug: 'building-ai-trading-bot',
        targetKeyword: 'AI trading bot',
        secondaryKeywords: ['trading bot Python', 'automated AI trading', 'ML trading bot'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 3000,
        priority: 'high',
        internalLinks: ['ai-lab', 'quant-trading', 'developer-center'],
      },
      {
        title: 'Sentiment Analysis for Trading: Using NLP on Market News',
        slug: 'sentiment-analysis-trading',
        targetKeyword: 'sentiment analysis trading',
        secondaryKeywords: ['NLP trading', 'news sentiment', 'market sentiment analysis'],
        contentType: 'tutorial',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'medium',
        internalLinks: ['ai-lab', 'market-intelligence'],
      },
    ],
  },
  {
    name: 'TradingPsychology',
    slug: 'trading-psychology',
    pillarTitle: 'Trading Psychology Masterclass: Master Your Mind',
    pillarKeyword: 'trading psychology',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'The Psychology of Winning: How Top Traders Think',
        slug: 'psychology-of-winning-traders',
        targetKeyword: 'trading psychology',
        secondaryKeywords: ['winning mindset', 'trader psychology', 'mental models trading'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['trading-psychology', 'academy'],
      },
      {
        title: 'Overcoming Fear and Greed in Trading',
        slug: 'overcoming-fear-greed-trading',
        targetKeyword: 'fear and greed trading',
        secondaryKeywords: ['trading emotions', 'emotional discipline', 'trading mindset'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 1800,
        priority: 'high',
        internalLinks: ['trading-psychology', 'risk-management'],
      },
      {
        title: 'Cognitive Biases That Destroy Trading Accounts',
        slug: 'cognitive-biases-trading',
        targetKeyword: 'cognitive biases trading',
        secondaryKeywords: ['confirmation bias', 'anchoring bias', 'trading psychology errors'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2000,
        priority: 'medium',
        internalLinks: ['trading-psychology', 'academy'],
      },
    ],
  },
  {
    name: 'RiskManagement',
    slug: 'risk-management',
    pillarTitle: 'Risk Management Strategies: Protect Your Trading Capital',
    pillarKeyword: 'risk management trading',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'Position Sizing: The Mathematics of Trading Survival',
        slug: 'position-sizing-trading',
        targetKeyword: 'position sizing',
        secondaryKeywords: ['kelly criterion', 'trade sizing', 'money management'],
        contentType: 'tutorial',
        schemaType: 'TechArticle',
        wordCountTarget: 2000,
        priority: 'critical',
        internalLinks: ['risk-management', 'academy'],
      },
      {
        title: 'Stop Loss Strategies: Where to Place Your Exit',
        slug: 'stop-loss-strategies',
        targetKeyword: 'stop loss strategies',
        secondaryKeywords: ['stop loss placement', 'exit strategy', 'risk control'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 1800,
        priority: 'high',
        internalLinks: ['risk-management', 'forex', 'stocks'],
      },
      {
        title: 'Building a Complete Risk Management Framework',
        slug: 'risk-management-framework',
        targetKeyword: 'risk management framework',
        secondaryKeywords: ['risk system', 'portfolio risk', 'trading risk rules'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['risk-management', 'hedge-fund'],
      },
    ],
  },
  {
    name: 'PortfolioManagement',
    slug: 'portfolio-management',
    pillarTitle: 'Portfolio Management: Build and Optimize Your Investments',
    pillarKeyword: 'portfolio management',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'Portfolio Diversification: Why and How to Diversify',
        slug: 'portfolio-diversification-guide',
        targetKeyword: 'portfolio diversification',
        secondaryKeywords: ['asset allocation', 'diversified portfolio', 'investment mix'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['portfolio-management', 'risk-management'],
      },
      {
        title: 'Modern Portfolio Theory Explained for Retail Traders',
        slug: 'modern-portfolio-theory',
        targetKeyword: 'modern portfolio theory',
        secondaryKeywords: ['efficient frontier', 'MPT', 'portfolio optimization'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'medium',
        internalLinks: ['portfolio-management', 'quant-trading'],
      },
    ],
  },
  {
    name: 'Forex',
    slug: 'forex',
    pillarTitle: 'Forex Trading Complete Guide: Currencies, Strategies & Brokers',
    pillarKeyword: 'forex trading',
    pillarWordCount: 4000,
    articles: [
      {
        title: 'What Is Forex Trading? Complete Beginner Guide',
        slug: 'what-is-forex-trading',
        targetKeyword: 'what is forex trading',
        secondaryKeywords: ['forex basics', 'currency trading', 'FX market'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['forex', 'academy'],
      },
      {
        title: 'Best Forex Trading Strategies That Actually Work',
        slug: 'best-forex-strategies',
        targetKeyword: 'forex trading strategies',
        secondaryKeywords: ['forex strategy', 'currency trading strategy', 'FX strategies'],
        contentType: 'comparison',
        schemaType: 'ItemList',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['forex', 'quant-trading'],
      },
      {
        title: 'How to Choose the Best Forex Broker',
        slug: 'best-forex-broker',
        targetKeyword: 'best forex broker',
        secondaryKeywords: ['forex broker comparison', 'top brokers', 'forex broker review'],
        contentType: 'comparison',
        schemaType: 'ItemList',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['forex', 'east-africa'],
      },
      {
        title: 'Forex Trading Sessions: Best Times to Trade',
        slug: 'forex-trading-sessions',
        targetKeyword: 'forex trading sessions',
        secondaryKeywords: ['best time to trade', 'London session', 'Asian session', 'NY session'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 1800,
        priority: 'medium',
        internalLinks: ['forex'],
      },
    ],
  },
  {
    name: 'Crypto',
    slug: 'crypto',
    pillarTitle: 'Cryptocurrency Trading Guide: Bitcoin, DeFi & Beyond',
    pillarKeyword: 'crypto trading',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'How to Trade Cryptocurrency: Complete Guide',
        slug: 'how-to-trade-cryptocurrency',
        targetKeyword: 'crypto trading',
        secondaryKeywords: ['bitcoin trading', 'crypto guide', 'cryptocurrency investment'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['crypto', 'academy'],
      },
      {
        title: 'DeFi Trading Strategies: Yield Farming & Liquidity',
        slug: 'defi-trading-strategies',
        targetKeyword: 'DeFi trading',
        secondaryKeywords: ['yield farming', 'liquidity pool', 'DeFi strategies'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'medium',
        internalLinks: ['crypto', 'risk-management'],
      },
      {
        title: 'Crypto vs Forex: Which Market Should You Trade?',
        slug: 'crypto-vs-forex',
        targetKeyword: 'crypto vs forex',
        secondaryKeywords: ['forex or crypto', 'market comparison', 'trading market choice'],
        contentType: 'comparison',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['crypto', 'forex'],
      },
    ],
  },
  {
    name: 'Stocks',
    slug: 'stocks',
    pillarTitle: 'Stock Market Trading: From Analysis to Execution',
    pillarKeyword: 'stock trading',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'How to Trade Stocks: Beginner to Intermediate Guide',
        slug: 'how-to-trade-stocks',
        targetKeyword: 'how to trade stocks',
        secondaryKeywords: ['stock market trading', 'equities trading', 'shares trading'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['stocks', 'academy'],
      },
      {
        title: 'Nairobi Securities Exchange: Complete Trading Guide',
        slug: 'nairobi-securities-exchange-guide',
        targetKeyword: 'Nairobi Securities Exchange',
        secondaryKeywords: ['NSE trading', 'Kenya stocks', 'Nairobi stock market'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['stocks', 'east-africa'],
      },
      {
        title: 'Dividend Investing Strategy: Build Passive Income',
        slug: 'dividend-investing-strategy',
        targetKeyword: 'dividend investing',
        secondaryKeywords: ['dividend stocks', 'passive income', 'income investing'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'medium',
        internalLinks: ['stocks', 'portfolio-management'],
      },
    ],
  },
  {
    name: 'Commodities',
    slug: 'commodities',
    pillarTitle: 'Commodities Trading: Gold, Oil, Agricultural Futures',
    pillarKeyword: 'commodities trading',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'How to Trade Commodities: Complete Guide',
        slug: 'how-to-trade-commodities',
        targetKeyword: 'commodities trading',
        secondaryKeywords: ['gold trading', 'oil trading', 'commodity futures'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['commodities', 'academy'],
      },
      {
        title: 'Gold Trading Strategies: Safe Haven Investing',
        slug: 'gold-trading-strategies',
        targetKeyword: 'gold trading',
        secondaryKeywords: ['XAUUSD', 'gold investment', 'precious metals trading'],
        contentType: 'guide',
        schemaType: 'TechArticle',
        wordCountTarget: 2000,
        priority: 'high',
        internalLinks: ['commodities', 'forex'],
      },
    ],
  },
  {
    name: 'Futures',
    slug: 'futures',
    pillarTitle: 'Futures Trading: Contracts, Leverage & Strategies',
    pillarKeyword: 'futures trading',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'What Are Futures Contracts? Complete Beginner Guide',
        slug: 'what-are-futures-contracts',
        targetKeyword: 'futures trading',
        secondaryKeywords: ['futures contracts', 'futures explained', 'derivatives trading'],
        contentType: 'guide',
        schemaType: 'Article',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['futures', 'academy'],
      },
      {
        title: 'Futures vs Options: Which Derivative Is Right for You?',
        slug: 'futures-vs-options',
        targetKeyword: 'futures vs options',
        secondaryKeywords: ['derivatives comparison', 'futures or options', 'trading instruments'],
        contentType: 'comparison',
        schemaType: 'Article',
        wordCountTarget: 2000,
        priority: 'medium',
        internalLinks: ['futures', 'options'],
      },
    ],
  },
  {
    name: 'Options',
    slug: 'options',
    pillarTitle: 'Options Trading: Calls, Puts & Advanced Strategies',
    pillarKeyword: 'options trading',
    pillarWordCount: 3500,
    articles: [
      {
        title: 'Options Trading for Beginners: Complete Guide',
        slug: 'options-trading-beginners',
        targetKeyword: 'options trading',
        secondaryKeywords: ['options explained', 'calls and puts', 'options basics'],
        contentType: 'guide',
        schemaType: 'HowTo',
        wordCountTarget: 2500,
        priority: 'critical',
        internalLinks: ['options', 'academy'],
      },
      {
        title: 'Options Greeks Explained: Delta, Gamma, Theta, Vega',
        slug: 'options-greeks-explained',
        targetKeyword: 'options greeks',
        secondaryKeywords: ['delta gamma theta', 'options pricing', 'implied volatility'],
        contentType: 'tutorial',
        schemaType: 'TechArticle',
        wordCountTarget: 2200,
        priority: 'high',
        internalLinks: ['options', 'quant-trading'],
      },
    ],
  },
  {
    name: 'DeveloperCenter',
    slug: 'developer-center',
    pillarTitle: 'Developer Center: APIs, SDKs & Integration Guides',
    pillarKeyword: 'trading API',
    pillarWordCount: 3000,
    articles: [
      {
        title: 'Trading API Integration Guide: Complete Documentation',
        slug: 'trading-api-integration',
        targetKeyword: 'trading API',
        secondaryKeywords: ['broker API', 'trading API documentation', 'API integration guide'],
        contentType: 'tutorial',
        schemaType: 'TechArticle',
        wordCountTarget: 2500,
        priority: 'high',
        internalLinks: ['developer-center', 'mt5-lab'],
      },
      {
        title: 'Building Trading Bots with Python and REST APIs',
        slug: 'building-trading-bots-python',
        targetKeyword: 'trading bot Python',
        secondaryKeywords: ['Python trading API', 'automated trading bot', 'REST API trading'],
        contentType: 'tutorial',
        schemaType: 'HowTo',
        wordCountTarget: 3000,
        priority: 'high',
        internalLinks: ['developer-center', 'quant-trading', 'ai-lab'],
      },
    ],
  },
];

const EAST_AFRICA_CLUSTERS: CountryKeywordCluster[] = [
  {
    country: 'Kenya',
    countryCode: 'KE',
    keywords: [
      { keyword: 'forex trading Kenya', searchIntent: 'informational', difficulty: 'medium', priority: 'critical' },
      { keyword: 'how to trade forex Kenya', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'best forex broker Kenya M-Pesa', searchIntent: 'commercial', difficulty: 'medium', priority: 'critical' },
      { keyword: 'CMA licensed brokers Kenya', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'trading course Kenya', searchIntent: 'commercial', difficulty: 'medium', priority: 'high' },
      { keyword: 'crypto trading Kenya', searchIntent: 'informational', difficulty: 'medium', priority: 'high' },
      { keyword: 'MT5 Kenya setup guide', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'Nairobi Securities Exchange trading', searchIntent: 'informational', difficulty: 'hard', priority: 'medium' },
      { keyword: 'binary options Kenya regulation', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'M-Pesa forex deposit', searchIntent: 'transactional', difficulty: 'easy', priority: 'high' },
      { keyword: 'forex trading app Kenya', searchIntent: 'transactional', difficulty: 'medium', priority: 'medium' },
      { keyword: 'how to make money trading Kenya', searchIntent: 'informational', difficulty: 'medium', priority: 'medium' },
    ],
  },
  {
    country: 'Tanzania',
    countryCode: 'TZ',
    keywords: [
      { keyword: 'forex trading Tanzania', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'how to trade forex Tanzania', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'best forex broker Tanzania', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'trading course Dar es Salaam', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'M-Pesa forex Tanzania', searchIntent: 'transactional', difficulty: 'easy', priority: 'high' },
      { keyword: 'crypto trading Tanzania', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'mobile money forex deposit Tanzania', searchIntent: 'transactional', difficulty: 'easy', priority: 'medium' },
      { keyword: 'Tanzania stock exchange DSE', searchIntent: 'informational', difficulty: 'medium', priority: 'medium' },
      { keyword: 'forex regulation Tanzania BRL', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'Swahili trading education', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'best trading app Tanzania', searchIntent: 'transactional', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex trading Dodoma', searchIntent: 'informational', difficulty: 'easy', priority: 'low' },
    ],
  },
  {
    country: 'Uganda',
    countryCode: 'UG',
    keywords: [
      { keyword: 'forex trading Uganda', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'how to start trading Uganda', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'best forex broker Uganda', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'MT5 Uganda mobile setup', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'crypto Uganda regulation', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'Uganda stock exchange USE', searchIntent: 'informational', difficulty: 'medium', priority: 'medium' },
      { keyword: 'mobile money forex deposit Uganda', searchIntent: 'transactional', difficulty: 'easy', priority: 'high' },
      { keyword: 'forex trading Kampala', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'trading education Uganda', searchIntent: 'commercial', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex broker mobile money Uganda', searchIntent: 'transactional', difficulty: 'easy', priority: 'high' },
      { keyword: 'how to make money trading Uganda', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
    ],
  },
  {
    country: 'Rwanda',
    countryCode: 'RW',
    keywords: [
      { keyword: 'forex trading Rwanda', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'how to trade forex Rwanda', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'best forex broker Rwanda', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'Rwanda stock exchange RSE', searchIntent: 'informational', difficulty: 'medium', priority: 'medium' },
      { keyword: 'crypto trading Kigali', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'trading course Rwanda', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'mobile money forex Rwanda', searchIntent: 'transactional', difficulty: 'easy', priority: 'high' },
      { keyword: 'MT5 Rwanda setup', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex regulation Rwanda BNR', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'investment education Rwanda', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex trading beginner Rwanda', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'best trading platform Rwanda', searchIntent: 'transactional', difficulty: 'easy', priority: 'medium' },
    ],
  },
  {
    country: 'Burundi',
    countryCode: 'BI',
    keywords: [
      { keyword: 'forex trading Burundi', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'how to trade forex Burundi', searchIntent: 'informational', difficulty: 'easy', priority: 'high' },
      { keyword: 'best forex broker Burundi', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'crypto trading Bujumbura', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'mobile money forex Burundi', searchIntent: 'transactional', difficulty: 'easy', priority: 'medium' },
      { keyword: 'Bujumbura stock exchange', searchIntent: 'informational', difficulty: 'easy', priority: 'low' },
      { keyword: 'trading education Burundi', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex regulation Burundi BCB', searchIntent: 'informational', difficulty: 'easy', priority: 'low' },
      { keyword: 'MT5 Burundi setup guide', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex trading beginner Burundi', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'best trading app Burundi', searchIntent: 'transactional', difficulty: 'easy', priority: 'low' },
    ],
  },
  {
    country: 'Ethiopia',
    countryCode: 'ET',
    keywords: [
      { keyword: 'forex trading Ethiopia', searchIntent: 'informational', difficulty: 'medium', priority: 'critical' },
      { keyword: 'how to trade forex Ethiopia', searchIntent: 'informational', difficulty: 'easy', priority: 'critical' },
      { keyword: 'best forex broker Ethiopia', searchIntent: 'commercial', difficulty: 'medium', priority: 'high' },
      { keyword: 'Ethiopia forex regulation NBE', searchIntent: 'informational', difficulty: 'medium', priority: 'high' },
      { keyword: 'crypto trading Addis Ababa', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'Ethiopian stock market', searchIntent: 'informational', difficulty: 'medium', priority: 'medium' },
      { keyword: 'forex trading Addis Ababa', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'mobile money forex Ethiopia', searchIntent: 'transactional', difficulty: 'medium', priority: 'medium' },
      { keyword: 'trading course Ethiopia', searchIntent: 'commercial', difficulty: 'easy', priority: 'high' },
      { keyword: 'MT5 Ethiopia setup guide', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex education Amharic', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
      { keyword: 'forex trading beginner Ethiopia', searchIntent: 'informational', difficulty: 'easy', priority: 'medium' },
    ],
  },
];

function buildTopicClusterMap(): TopicClusterMap {
  const totalArticles = TOPIC_HUBS.reduce(
    (sum, hub) => sum + hub.articles.length + 1,
    0,
  );

  const totalKeywords = TOPIC_HUBS.reduce(
    (sum, hub) =>
      sum +
      hub.articles.reduce(
        (articleSum, article) => articleSum + article.secondaryKeywords.length + 1,
        1,
      ),
    0,
  ) + EAST_AFRICA_CLUSTERS.reduce(
    (sum, cluster) => sum + cluster.keywords.length,
    0,
  );

  return {
    generatedAt: new Date().toISOString(),
    hubs: TOPIC_HUBS,
    eastAfricaClusters: EAST_AFRICA_CLUSTERS,
    totalArticles,
    totalKeywords,
  };
}

function generateHubSummary(): string {
  const lines: string[] = ['## Topic Cluster Hubs Summary\n'];

  for (const hub of TOPIC_HUBS) {
    lines.push(`### ${hub.name}`);
    lines.push(`- Pillar: ${hub.pillarTitle}`);
    lines.push(`- Primary keyword: ${hub.pillarKeyword}`);
    lines.push(`- Articles: ${hub.articles.length}`);
    lines.push(`- Total content: ~${hub.articles.reduce((s, a) => s + a.wordCountTarget, hub.pillarWordCount).toLocaleString()} words\n`);
  }

  return lines.join('\n');
}

function generateEastAfricaSummary(): string {
  const lines: string[] = ['## East Africa Keyword Clusters\n'];

  for (const cluster of EAST_AFRICA_CLUSTERS) {
    const critical = cluster.keywords.filter((k) => k.priority === 'critical').length;
    const high = cluster.keywords.filter((k) => k.priority === 'high').length;
    lines.push(`### ${cluster.country} (${cluster.countryCode})`);
    lines.push(`- Total keywords: ${cluster.keywords.length}`);
    lines.push(`- Critical: ${critical} | High: ${high}`);
    lines.push('- Top keywords:');
    for (const kw of cluster.keywords.filter((k) => k.priority === 'critical').slice(0, 3)) {
      lines.push(`  - ${kw.keyword} [${kw.searchIntent}, ${kw.difficulty}]`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

function writeTopicClusters(outputDir: string): void {
  const map = buildTopicClusterMap();
  const jsonPath = path.join(outputDir, 'topic-cluster-map.json');
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(jsonPath, JSON.stringify(map, null, 2));
  console.log(`Topic cluster map written to ${jsonPath}`);

  const summaryPath = path.join(outputDir, 'topic-cluster-summary.md');
  const summary = [
    '# Integral Market Topic Cluster Map',
    '',
    `Generated: ${map.generatedAt}`,
    `Total hubs: ${TOPIC_HUBS.length}`,
    `Total articles: ${map.totalArticles}`,
    `Total keywords: ${map.totalKeywords}`,
    '',
    generateHubSummary(),
    generateEastAfricaSummary(),
    '## Content Rules',
    '- Minimum 1,500 words per cluster article',
    '- Minimum 3,000 words per pillar page',
    '- Each article must link to its hub pillar',
    '- Each cluster article must link to 2+ sibling articles',
    '- Include FAQ schema on all articles',
    '- Include regional keywords for East Africa content',
    '- Use natural internal linking, not forced keyword mentions',
  ].join('\n');

  fs.writeFileSync(summaryPath, summary);
  console.log(`Topic cluster summary written to ${summaryPath}`);
}

export {
  ContentType,
  SchemaType,
  Priority,
  TopicClusterArticle,
  TopicHub,
  CountryKeywordCluster,
  TopicClusterMap,
  TOPIC_HUBS,
  EAST_AFRICA_CLUSTERS,
  buildTopicClusterMap,
  generateHubSummary,
  generateEastAfricaSummary,
  writeTopicClusters,
};

if (require.main === module) {
  const outputDir = path.join(__dirname, '..', '..', '..', 'output');
  writeTopicClusters(outputDir);
}
