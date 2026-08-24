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
    faq: {
        question: string;
        answer: string;
    }[];
    landingPage: string;
    documentationRef: string;
}
declare const entities: EntityMeta[];
export declare function getEntity(id: string): EntityMeta | undefined;
export declare function getAllEntities(): readonly EntityMeta[];
export declare function getEntitiesByType(type: EntityType): EntityMeta[];
export declare function searchEntities(query: string): EntityMeta[];
export { entities, type EntityMeta, type EntityType };
