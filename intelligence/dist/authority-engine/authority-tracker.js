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
exports.PLATFORM_CONFIGS = void 0;
exports.createPlatformProfile = createPlatformProfile;
exports.checkConsistency = checkConsistency;
exports.calculateOverallScore = calculateOverallScore;
exports.generateAuthorityReport = generateAuthorityReport;
exports.writeAuthorityReport = writeAuthorityReport;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const PLATFORM_CONFIGS = {
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
exports.PLATFORM_CONFIGS = PLATFORM_CONFIGS;
function createPlatformProfile(platform, config) {
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
function checkConsistency(profiles) {
    return profiles.map((profile) => {
        const issues = [];
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
        const status = issues.length === 0 ? 'consistent' : issues.length <= 1 ? 'needs_update' : 'inconsistent';
        return {
            platform: profile.platform,
            status,
            issues,
        };
    });
}
function calculateOverallScore(consistency) {
    if (consistency.length === 0)
        return 0;
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
function generateAuthorityReport(profiles) {
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
function writeAuthorityReport(outputDir, report) {
    fs.mkdirSync(outputDir, { recursive: true });
    const outputPath = path.join(outputDir, 'authority-report.json');
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
    console.log(`Authority report written to ${outputPath}`);
}
