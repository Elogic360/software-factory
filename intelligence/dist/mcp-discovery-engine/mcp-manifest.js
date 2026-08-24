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
exports.generateMCPManifestFile = generateMCPManifestFile;
/**
 * MCP Discovery Engine — generates the Model Context Protocol manifest
 * for AI agent discoverability of Integral Market tools.
 */
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const OUTPUT_DIR = path.join(__dirname, '../dist/mcp');
function generateMCPManifest() {
    const tools = [
        {
            name: 'analyze_trade_psychology',
            description: 'Analyzes historical trade data to detect cognitive biases (FOMO, over-trading, revenge trading) and psychological patterns.',
            inputSchema: {
                type: 'object',
                properties: {
                    trades: { type: 'array', items: { type: 'object' }, description: 'Array of trade objects with entry/exit prices, timestamps, and sizes' },
                    timeframe: { type: 'string', enum: ['7d', '30d', '90d', '1y'], description: 'Analysis timeframe' },
                },
                required: ['trades'],
            },
        },
        {
            name: 'fetch_backtest_strategy',
            description: 'Retrieves institutional strategy indicators and historical win-rates from the IM Library.',
            inputSchema: {
                type: 'object',
                properties: {
                    assetClass: { type: 'string', enum: ['forex', 'crypto', 'equity', 'futures', 'options'] },
                    strategy: { type: 'string', description: 'Strategy name or category' },
                },
                required: ['assetClass'],
            },
        },
        {
            name: 'get_market_data',
            description: 'Fetches real-time or historical market data for specified instruments.',
            inputSchema: {
                type: 'object',
                properties: {
                    symbols: { type: 'array', items: { type: 'string' }, description: 'Trading symbols (e.g., EURUSD, BTCUSDT)' },
                    timeframe: { type: 'string', enum: ['1m', '5m', '15m', '1h', '4h', '1d'] },
                    limit: { type: 'number', description: 'Number of candles', default: 100 },
                },
                required: ['symbols'],
            },
        },
        {
            name: 'calculate_risk_metrics',
            description: 'Calculates portfolio risk metrics including Sharpe ratio, max drawdown, VaR, and position sizing.',
            inputSchema: {
                type: 'object',
                properties: {
                    portfolio: { type: 'array', items: { type: 'object' }, description: 'Portfolio positions' },
                    riskFreeRate: { type: 'number', description: 'Annual risk-free rate', default: 0.05 },
                },
                required: ['portfolio'],
            },
        },
        {
            name: 'get_economic_calendar',
            description: 'Fetches upcoming economic events and their expected impact on markets.',
            inputSchema: {
                type: 'object',
                properties: {
                    dateRange: { type: 'string', enum: ['today', 'week', 'month'] },
                    impact: { type: 'string', enum: ['low', 'medium', 'high', 'all'] },
                },
            },
        },
    ];
    return {
        '$schema': 'https://modelcontextprotocol.io/schema/mcp.json',
        mcpServerManifest: {
            name: 'Integral Market Analytics Server',
            version: '1.0.0',
            description: 'Provides programmatic access to trading analytics, journal data, risk metrics, and market intelligence from Integral Market.',
            homepage: 'https://integralmarket.tech',
            endpoints: {
                openapi: 'https://integralmarket.tech/docs/api',
            },
            capabilities: { tools },
        },
    };
}
function generateMCPManifestFile() {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    const manifest = generateMCPManifest();
    fs.writeFileSync(path.join(OUTPUT_DIR, 'mcp.json'), JSON.stringify(manifest, null, 2));
    console.log('✅ Generated MCP manifest at dist/mcp/mcp.json');
}
if (require.main === module) {
    generateMCPManifestFile();
}
