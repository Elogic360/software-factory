type ContentCategory = 'Trading Psychology' | 'Risk Management' | 'AI-Assisted Trading' | 'Platform Updates' | 'Tutorials' | 'Research';
type SchemaType = 'Article' | 'BlogPosting' | 'TechArticle' | 'HowTo' | 'NewsArticle';
interface ArticleTemplate {
    title: string;
    metaDescription: string;
    keywords: string[];
    schemaType: SchemaType;
    wordCountTarget: number;
}
interface ContentPlan {
    category: ContentCategory;
    articles: ArticleTemplate[];
}
interface MonthlyTopic {
    month: string;
    year: number;
    topics: {
        category: ContentCategory;
        title: string;
        publishDate: string;
    }[];
}
interface ContentCalendar {
    year: number;
    months: MonthlyTopic[];
}
declare const CONTENT_CATEGORIES: Record<ContentCategory, {
    keywords: string[];
    baseWordCount: number;
}>;
declare const ARTICLE_TEMPLATES: Record<ContentCategory, ArticleTemplate[]>;
declare function generateArticleTemplate(category: ContentCategory): ArticleTemplate[];
declare function generateContentPlan(category: ContentCategory): ContentPlan;
declare function generateMonthlyTopics(year: number, month: number): MonthlyTopic;
declare function generateContentCalendar(year: number): ContentCalendar;
declare function generateFullPlan(): {
    plans: ContentPlan[];
    calendar: ContentCalendar;
};
declare function writeContentPlan(outputDir: string): void;
export { ContentCategory, SchemaType, ArticleTemplate, ContentPlan, MonthlyTopic, ContentCalendar, generateArticleTemplate, generateContentPlan, generateMonthlyTopics, generateContentCalendar, generateFullPlan, writeContentPlan, CONTENT_CATEGORIES, ARTICLE_TEMPLATES, };
