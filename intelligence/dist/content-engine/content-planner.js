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
exports.ARTICLE_TEMPLATES = exports.CONTENT_CATEGORIES = void 0;
exports.generateArticleTemplate = generateArticleTemplate;
exports.generateContentPlan = generateContentPlan;
exports.generateMonthlyTopics = generateMonthlyTopics;
exports.generateContentCalendar = generateContentCalendar;
exports.generateFullPlan = generateFullPlan;
exports.writeContentPlan = writeContentPlan;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const CONTENT_CATEGORIES = {
    'Trading Psychology': {
        keywords: ['trading mindset', 'discipline', 'emotional control', 'cognitive bias', 'behavioral finance'],
        baseWordCount: 1800,
    },
    'Risk Management': {
        keywords: ['risk management', 'position sizing', 'stop loss', 'drawdown', 'portfolio risk'],
        baseWordCount: 2000,
    },
    'AI-Assisted Trading': {
        keywords: ['AI trading', 'machine learning', 'algorithmic trading', 'neural networks', 'backtesting'],
        baseWordCount: 2200,
    },
    'Platform Updates': {
        keywords: ['platform update', 'new features', 'release notes', 'changelog', 'product update'],
        baseWordCount: 800,
    },
    'Tutorials': {
        keywords: ['how to', 'step by step', 'guide', 'tutorial', 'walkthrough'],
        baseWordCount: 1500,
    },
    Research: {
        keywords: ['research paper', 'market analysis', 'quantitative analysis', 'data analysis', 'findings'],
        baseWordCount: 2500,
    },
};
exports.CONTENT_CATEGORIES = CONTENT_CATEGORIES;
const ARTICLE_TEMPLATES = {
    'Trading Psychology': [
        {
            title: 'The Psychology of Winning: How Top Traders Think',
            metaDescription: 'Discover the psychological principles that separate winning traders from the rest. Learn mental frameworks for consistent trading performance.',
            keywords: ['trading psychology', 'winning mindset', 'trader discipline', 'mental models'],
            schemaType: 'Article',
            wordCountTarget: 1800,
        },
        {
            title: 'Overcoming Fear and Greed: The Two Emotions That Destroy Portfolios',
            metaDescription: 'Learn how fear and greed impact your trading decisions and practical strategies to manage emotional responses in volatile markets.',
            keywords: ['fear greed trading', 'emotional trading', 'psychology of money', 'behavioral trading'],
            schemaType: 'BlogPosting',
            wordCountTarget: 1600,
        },
        {
            title: 'Cognitive Biases Every Trader Must Recognize',
            metaDescription: 'A comprehensive guide to cognitive biases affecting trading performance, with actionable techniques to counteract them.',
            keywords: ['cognitive biases', 'confirmation bias', 'anchoring', 'trading errors'],
            schemaType: 'TechArticle',
            wordCountTarget: 2000,
        },
    ],
    'Risk Management': [
        {
            title: 'Position Sizing: The Mathematics of Survival',
            metaDescription: 'Master position sizing techniques including Kelly Criterion, fixed fractional, and volatility-adjusted sizing for long-term trading survival.',
            keywords: ['position sizing', 'kelly criterion', 'money management', 'trade sizing'],
            schemaType: 'TechArticle',
            wordCountTarget: 2000,
        },
        {
            title: 'Building a Risk Management Framework That Works',
            metaDescription: 'Step-by-step guide to creating a comprehensive risk management framework for individual and institutional traders.',
            keywords: ['risk framework', 'portfolio management', 'risk assessment', 'hedging strategies'],
            schemaType: 'HowTo',
            wordCountTarget: 2200,
        },
    ],
    'AI-Assisted Trading': [
        {
            title: 'Machine Learning for Trading: From Theory to Production',
            metaDescription: 'How to implement machine learning models for trading, from data preparation to live deployment and monitoring.',
            keywords: ['ML trading', 'machine learning finance', 'predictive models', 'feature engineering'],
            schemaType: 'TechArticle',
            wordCountTarget: 2500,
        },
        {
            title: 'Building Your First AI Trading Bot: A Complete Guide',
            metaDescription: 'Learn to build an AI-powered trading bot from scratch, covering data pipelines, model training, and live execution.',
            keywords: ['AI trading bot', 'algorithmic trading', 'automated trading', 'Python trading'],
            schemaType: 'HowTo',
            wordCountTarget: 2200,
        },
    ],
    'Platform Updates': [
        {
            title: 'Introducing [Feature Name]: What\'s New in Integral Market',
            metaDescription: 'Get the latest update on Integral Market platform features, improvements, and what they mean for your trading.',
            keywords: ['platform update', 'new features', 'integral market update', 'product release'],
            schemaType: 'NewsArticle',
            wordCountTarget: 800,
        },
    ],
    Tutorials: [
        {
            title: 'How to Set Up Your Trading Journal in 10 Minutes',
            metaDescription: 'Quick guide to setting up your personalized trading journal for tracking performance and improving your edge.',
            keywords: ['trading journal setup', 'performance tracking', 'trade logging', 'journal guide'],
            schemaType: 'HowTo',
            wordCountTarget: 1500,
        },
        {
            title: 'Using AI Analytics to Identify High-Probability Trades',
            metaDescription: 'Step-by-step tutorial on leveraging AI analytics tools to find and validate high-probability trade setups.',
            keywords: ['AI analytics', 'trade analysis', 'probability', 'setup identification'],
            schemaType: 'HowTo',
            wordCountTarget: 1800,
        },
    ],
    Research: [
        {
            title: 'Market Microstructure Analysis: Patterns in Order Flow',
            metaDescription: 'Research findings on order flow patterns and their predictive value for short-term price movements.',
            keywords: ['order flow', 'market microstructure', 'price discovery', 'liquidity analysis'],
            schemaType: 'TechArticle',
            wordCountTarget: 2500,
        },
    ],
};
exports.ARTICLE_TEMPLATES = ARTICLE_TEMPLATES;
function generateArticleTemplate(category) {
    const config = CONTENT_CATEGORIES[category];
    const templates = ARTICLE_TEMPLATES[category] || [];
    return templates.map((tpl) => ({
        ...tpl,
        keywords: [...tpl.keywords, ...config.keywords.slice(0, 2)],
        wordCountTarget: tpl.wordCountTarget || config.baseWordCount,
    }));
}
function generateContentPlan(category) {
    return {
        category,
        articles: generateArticleTemplate(category),
    };
}
function generateMonthlyTopics(year, month) {
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
    ];
    const categories = [
        'Trading Psychology',
        'Risk Management',
        'AI-Assisted Trading',
        'Platform Updates',
        'Tutorials',
        'Research',
    ];
    const topicsPerMonth = 4;
    const topics = [];
    for (let week = 0; week < topicsPerMonth; week++) {
        const categoryIndex = (month + week) % categories.length;
        const category = categories[categoryIndex];
        const templates = ARTICLE_TEMPLATES[category];
        const template = templates[week % templates.length];
        const publishDay = 1 + week * 7;
        const publishDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(publishDay).padStart(2, '0')}`;
        topics.push({
            category,
            title: template.title,
            publishDate,
        });
    }
    return {
        month: monthNames[month],
        year,
        topics,
    };
}
function generateContentCalendar(year) {
    const months = [];
    for (let m = 0; m < 12; m++) {
        months.push(generateMonthlyTopics(year, m));
    }
    return { year, months };
}
function generateFullPlan() {
    const categories = [
        'Trading Psychology',
        'Risk Management',
        'AI-Assisted Trading',
        'Platform Updates',
        'Tutorials',
        'Research',
    ];
    const plans = categories.map(generateContentPlan);
    const calendar = generateContentCalendar(new Date().getFullYear());
    return { plans, calendar };
}
function writeContentPlan(outputDir) {
    const plan = generateFullPlan();
    const outputPath = path.join(outputDir, 'content-plan.json');
    fs.mkdirSync(outputDir, { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(plan, null, 2));
    console.log(`Content plan written to ${outputPath}`);
}
if (require.main === module) {
    const outputDir = path.join(__dirname, '..', '..', '..', 'output');
    writeContentPlan(outputDir);
}
