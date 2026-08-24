"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.runIntelligenceEngine = runIntelligenceEngine;
/**
 * Intelligence Engine — main entry point
 * Generates all AI optimization artifacts: knowledge graph, structured data,
 * MCP manifest, GEO content, sitemaps, metadata, and authority reports.
 */
const sitemap_generator_1 = require("./indexing-engine/sitemap-generator");
const structured_data_1 = require("./entity-engine/structured-data");
const geo_generator_1 = require("./geo-engine/geo-generator");
const mcp_manifest_1 = require("./mcp-discovery-engine/mcp-manifest");
const og_metadata_1 = require("./entity-engine/og-metadata");
function runIntelligenceEngine() {
    console.log('🚀 Starting Intelligence Engine...\n');
    console.log('1/5 Generating structured data schemas...');
    (0, structured_data_1.generateStructuredData)();
    console.log('2/5 Generating GEO content (FAQ, comparisons)...');
    (0, geo_generator_1.generateGEOContent)();
    console.log('3/5 Generating MCP discovery manifest...');
    (0, mcp_manifest_1.generateMCPManifestFile)();
    console.log('4/5 Generating sitemaps and robots.txt...');
    (0, sitemap_generator_1.generateSitemap)();
    console.log('5/5 Generating OpenGraph metadata...');
    (0, og_metadata_1.generateMetadata)();
    console.log('\n✅ Intelligence Engine complete. All artifacts in software-factory/intelligence/dist/');
}
if (require.main === module) {
    runIntelligenceEngine();
}
