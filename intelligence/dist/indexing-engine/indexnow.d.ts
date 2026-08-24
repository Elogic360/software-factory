interface IndexNowResponse {
    statusCode: number;
    message: string;
    errors?: string[];
}
export declare function generateSitemap(): string;
export declare function generateRobotsTxt(): string;
export declare function generateWellKnownMCP(host: string, key: string): Record<string, unknown>;
export declare function pushToIndexNow(urls: string[], host: string, key: string): Promise<IndexNowResponse>;
export declare function generateIndexingOutput(outputDir?: string): {
    sitemap: string;
    robots: string;
    urls: string[];
};
export {};
