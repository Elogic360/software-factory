/**
 * Intelligence Engine — main entry point
 * Generates all AI optimization artifacts: knowledge graph, structured data,
 * MCP manifest, GEO content, sitemaps, metadata, and authority reports.
 */
import { generateSitemap } from './indexing-engine/sitemap-generator';
import { generateStructuredData } from './entity-engine/structured-data';
import { generateGEOContent } from './geo-engine/geo-generator';
import { generateMCPManifestFile } from './mcp-discovery-engine/mcp-manifest';
import { generateMetadata } from './entity-engine/og-metadata';

export function runIntelligenceEngine(): void {
  console.log('🚀 Starting Intelligence Engine...\n');

  console.log('1/5 Generating structured data schemas...');
  generateStructuredData();

  console.log('2/5 Generating GEO content (FAQ, comparisons)...');
  generateGEOContent();

  console.log('3/5 Generating MCP discovery manifest...');
  generateMCPManifestFile();

  console.log('4/5 Generating sitemaps and robots.txt...');
  generateSitemap();

  console.log('5/5 Generating OpenGraph metadata...');
  generateMetadata();

  console.log('\n✅ Intelligence Engine complete. All artifacts in software-factory/intelligence/dist/');
}

if (require.main === module) {
  runIntelligenceEngine();
}
