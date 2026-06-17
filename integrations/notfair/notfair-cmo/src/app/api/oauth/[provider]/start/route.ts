import { NextResponse } from "next/server";

export const runtime = "nodejs";

/**
 * GET /api/oauth/[provider]/start?project=<slug>
 *
 * V1 scaffold: redirects to the provider's OAuth consent screen with our
 * localhost callback URL. The actual provider client IDs + scopes are
 * env-driven so users can register their own OAuth app.
 *
 * Required env vars (per provider):
 *   GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET
 *   GSC_CLIENT_ID, GSC_CLIENT_SECRET
 *
 * If not set, this returns a helpful 503 explaining setup steps instead of
 * silently sending the user to a broken page.
 */
export async function GET(
  request: Request,
  { params }: { params: Promise<{ provider: string }> },
) {
  const { provider } = await params;
  const url = new URL(request.url);
  const project = url.searchParams.get("project");
  if (!project) {
    return NextResponse.json({ error: "project query param required" }, { status: 400 });
  }

  const config = OAUTH_CONFIG[provider];
  if (!config) {
    return NextResponse.json({ error: `Unknown provider: ${provider}` }, { status: 404 });
  }

  if (!config.clientId) {
    return new Response(
      `OAuth not configured for '${provider}'. Set ${config.envClientId} and ${config.envClientSecret} in your environment, then restart notfair-cmo.\n\nSee: README#oauth-setup`,
      { status: 503, headers: { "Content-Type": "text/plain" } },
    );
  }

  const callbackBase = url.origin;
  const callback = `${callbackBase}/api/oauth/${provider}/callback`;
  const state = encodeStateToken(project);

  const authUrl = new URL(config.authEndpoint);
  authUrl.searchParams.set("client_id", config.clientId);
  authUrl.searchParams.set("redirect_uri", callback);
  authUrl.searchParams.set("response_type", "code");
  authUrl.searchParams.set("scope", config.scopes.join(" "));
  authUrl.searchParams.set("access_type", "offline");
  authUrl.searchParams.set("prompt", "consent");
  authUrl.searchParams.set("state", state);

  return NextResponse.redirect(authUrl.toString());
}

type ProviderConfig = {
  clientId: string | undefined;
  envClientId: string;
  envClientSecret: string;
  authEndpoint: string;
  scopes: string[];
};

const OAUTH_CONFIG: Record<string, ProviderConfig> = {
  google_ads: {
    clientId: process.env.GOOGLE_ADS_CLIENT_ID,
    envClientId: "GOOGLE_ADS_CLIENT_ID",
    envClientSecret: "GOOGLE_ADS_CLIENT_SECRET",
    authEndpoint: "https://accounts.google.com/o/oauth2/v2/auth",
    scopes: ["https://www.googleapis.com/auth/adwords"],
  },
  gsc: {
    clientId: process.env.GSC_CLIENT_ID,
    envClientId: "GSC_CLIENT_ID",
    envClientSecret: "GSC_CLIENT_SECRET",
    authEndpoint: "https://accounts.google.com/o/oauth2/v2/auth",
    scopes: ["https://www.googleapis.com/auth/webmasters.readonly"],
  },
};

function encodeStateToken(project: string): string {
  // Simple state encoding; in production add CSRF nonce verification.
  return Buffer.from(JSON.stringify({ project, ts: Date.now() })).toString("base64url");
}
