import * as fs from 'fs';
import * as path from 'path';

type PlatformType =
  | 'GitHub'
  | 'LinkedIn'
  | 'Reddit'
  | 'YouTube'
  | 'Medium'
  | 'X'
  | 'Discord'
  | 'Telegram'
  | 'ProductHunt'
  | 'HackerNews';

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

const PLATFORM_CONFIGS: Record<PlatformType, {
  contentTypes: string[];
  defaultFrequency: PostingFrequency;
  requiresVerification: boolean;
  urlPattern: RegExp;
}> = {
  GitHub: {
    contentTypes: ['repositories', 'gists', 'contributions', 'discussions'],
    defaultFrequency: 'weekly',
    requiresVerification: false,
    urlPattern: /^https:\/\/github\.com\/[\w-]+$/,
  },
  LinkedIn: {
    contentTypes: ['posts', 'articles', 'company_page', 'newsletter'],
    defaultFrequency: 'daily',
    requiresVerification: true,
    urlPattern: /^https:\/\/linkedin\.com\/(in|company)\/[\w-]+$/,
  },
  Reddit: {
    contentTypes: ['posts', 'comments', 'wiki_contributions'],
    defaultFrequency: 'daily',
    requiresVerification: false,
    urlPattern: /^https:\/\/reddit\.com\/u\/[\w-]+$/,
  },
  YouTube: {
    contentTypes: ['videos', 'shorts', 'live_streams', 'community_posts'],
    defaultFrequency: 'weekly',
    requiresVerification: true,
    urlPattern: /^https:\/\/youtube\.com\/@[\w-]+$/,
  },
  Medium: {
    contentTypes: ['articles', 'stories', 'series'],
    defaultFrequency: 'weekly',
    requiresVerification: false,
    urlPattern: /^https:\/\/medium\.com\/@[\w-]+$/,
  },
  X: {
    contentTypes: ['tweets', 'threads', 'spaces', 'community'],
    defaultFrequency: 'daily',
    requiresVerification: true,
    urlPattern: /^https:\/\/x\.com\/[\w]+$/,
  },
  Discord: {
    contentTypes: ['server', 'forums', 'events', 'announcements'],
    defaultFrequency: 'daily',
    requiresVerification: false,
    urlPattern: /^https:\/\/discord\.(gg|com\/invite)\/[\w]+$/,
  },
  Telegram: {
    contentTypes: ['channel', 'group', 'announcements'],
    defaultFrequency: 'daily',
    requiresVerification: false,
    urlPattern: /^https:\/\/t\.me\/[\w]+$/,
  },
  ProductHunt: {
    contentTypes: ['launches', 'upvotes', 'comments', 'collections'],
    defaultFrequency: 'monthly',
    requiresVerification: true,
    urlPattern: /^https:\/\/producthunt\.com\/posts\/[\w-]+$/,
  },
  HackerNews: {
    contentTypes: ['posts', 'comments', 'show_hn'],
    defaultFrequency: 'irregular',
    requiresVerification: false,
    urlPattern: /^https:\/\/news\.ycombinator\.com\/user\?id=[\w]+$/,
  },
};

function createPlatformProfile(
  platform: PlatformType,
  config: {
    profileUrl: string;
    postingFrequency?: PostingFrequency;
    verificationStatus?: VerificationStatus;
    followerCount?: number;
    lastPostDate?: string;
    isActive?: boolean;
  }
): PlatformProfile {
  const platformConfig = PLATFORM_CONFIGS[platform];

  return {
    platform,
    profileUrl: config.profileUrl,
    contentTypes: platformConfig.contentTypes,
    postingFrequency: config.postingFrequency || platformConfig.defaultFrequency,
    verificationStatus: config.verificationStatus || (platformConfig.requiresVerification ? 'pending' : 'not_applicable'),
    followerCount: config.followerCount,
    lastPostDate: config.lastPostDate,
    isActive: config.isActive ?? true,
  };
}

function checkConsistency(profiles: PlatformProfile[]): ConsistencyCheck[] {
  return profiles.map((profile) => {
    const issues: string[] = [];
    const platformConfig = PLATFORM_CONFIGS[profile.platform];

    if (!platformConfig.urlPattern.test(profile.profileUrl)) {
      issues.push('Profile URL does not match expected format');
    }

    if (profile.isActive && !profile.lastPostDate) {
      issues.push('Active profile missing last post date');
    }

    if (platformConfig.requiresVerification && profile.verificationStatus === 'unverified') {
      issues.push('Platform supports verification but profile is unverified');
    }

    if (profile.isActive && profile.postingFrequency === 'irregular' && profile.platform !== 'HackerNews') {
      issues.push('Active profile has irregular posting frequency');
    }

    if (profile.followerCount !== undefined && profile.followerCount < 0) {
      issues.push('Follower count is negative');
    }

    const status: ConsistencyCheck['status'] =
      issues.length === 0 ? 'consistent' : issues.length <= 1 ? 'needs_update' : 'inconsistent';

    return {
      platform: profile.platform,
      status,
      issues,
    };
  });
}

function calculateOverallScore(consistency: ConsistencyCheck[]): number {
  if (consistency.length === 0) return 0;

  const scores = consistency.map((c) => {
    switch (c.status) {
      case 'consistent':
        return 100;
      case 'needs_update':
        return 60;
      case 'inconsistent':
        return 20;
    }
  });

  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
}

function generateAuthorityReport(profiles: PlatformProfile[]): AuthorityReport {
  const consistency = checkConsistency(profiles);
  const verifiedCount = profiles.filter((p) => p.verificationStatus === 'verified').length;
  const activePlatforms = profiles.filter((p) => p.isActive).length;
  const issuesFound = consistency.reduce((sum, c) => sum + c.issues.length, 0);

  return {
    generatedAt: new Date().toISOString(),
    profiles,
    consistency,
    summary: {
      totalPlatforms: profiles.length,
      activePlatforms,
      verifiedCount,
      issuesFound,
      overallScore: calculateOverallScore(consistency),
    },
  };
}

function writeAuthorityReport(outputDir: string, report: AuthorityReport): void {
  fs.mkdirSync(outputDir, { recursive: true });
  const outputPath = path.join(outputDir, 'authority-report.json');
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.log(`Authority report written to ${outputPath}`);
}

export {
  PlatformType,
  VerificationStatus,
  PostingFrequency,
  PlatformProfile,
  ConsistencyCheck,
  AuthorityReport,
  PLATFORM_CONFIGS,
  createPlatformProfile,
  checkConsistency,
  calculateOverallScore,
  generateAuthorityReport,
  writeAuthorityReport,
};
