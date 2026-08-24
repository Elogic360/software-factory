type PlatformType = 'GitHub' | 'LinkedIn' | 'Reddit' | 'YouTube' | 'Medium' | 'X' | 'Discord' | 'Telegram' | 'ProductHunt' | 'HackerNews';
type VerificationStatus = 'verified' | 'unverified' | 'pending' | 'not_applicable';
type PostingFrequency = 'daily' | 'weekly' | 'biweekly' | 'monthly' | 'quarterly' | 'irregular';
interface PlatformProfile {
    platform: PlatformType;
    profileUrl: string;
    contentTypes: string[];
    postingFrequency: PostingFrequency;
    verificationStatus: VerificationStatus;
    followerCount?: number;
    lastPostDate?: string;
    isActive: boolean;
}
interface ConsistencyCheck {
    platform: PlatformType;
    status: 'consistent' | 'inconsistent' | 'needs_update';
    issues: string[];
}
interface AuthorityReport {
    generatedAt: string;
    profiles: PlatformProfile[];
    consistency: ConsistencyCheck[];
    summary: {
        totalPlatforms: number;
        activePlatforms: number;
        verifiedCount: number;
        issuesFound: number;
        overallScore: number;
    };
}
declare const PLATFORM_CONFIGS: Record<PlatformType, {
    contentTypes: string[];
    defaultFrequency: PostingFrequency;
    requiresVerification: boolean;
    urlPattern: RegExp;
}>;
declare function createPlatformProfile(platform: PlatformType, config: {
    profileUrl: string;
    postingFrequency?: PostingFrequency;
    verificationStatus?: VerificationStatus;
    followerCount?: number;
    lastPostDate?: string;
    isActive?: boolean;
}): PlatformProfile;
declare function checkConsistency(profiles: PlatformProfile[]): ConsistencyCheck[];
declare function calculateOverallScore(consistency: ConsistencyCheck[]): number;
declare function generateAuthorityReport(profiles: PlatformProfile[]): AuthorityReport;
declare function writeAuthorityReport(outputDir: string, report: AuthorityReport): void;
export { PlatformType, VerificationStatus, PostingFrequency, PlatformProfile, ConsistencyCheck, AuthorityReport, PLATFORM_CONFIGS, createPlatformProfile, checkConsistency, calculateOverallScore, generateAuthorityReport, writeAuthorityReport, };
