import { NextResponse } from "next/server";
import { storeOAuthToken } from "@/server/db/oauth";
import type { OAuthProvider } from "@/types";

export const runtime = "nodejs";

/**
 * GET /api/oauth/[provider]/callback?code=...&state=...
 *
 * Provider redirects here after the user grants consent. We exchange the code
 * for tokens, encrypt with the master key, and persist to SQLite.
 */
export async function GET(
  request: Request,
  { params }: { params: Promise<{ provider: string }> },
) {
  const { provider } = await params;
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const errorParam = url.searchParams.get("error");

  if (errorParam) {
    return htmlResponse(
      `<h1>OAuth denied</h1><p>The provider returned: <code>${escapeHtml(errorParam)}</code></p><p><a href="/">Back to app</a></p>`,
      400,
    );
  }
  if (!code || !state) {
    return htmlResponse(`<h1>OAuth error</h1><p>Missing code or state.</p>`, 400);
  }

  let project: string;
  try {
    const decoded = JSON.parse(Buffer.from(state, "base64url").toString("utf8")) as {
      project: string;
    };
    project = decoded.project;
  } catch {
    return htmlResponse(`<h1>OAuth error</h1><p>Invalid state token.</p>`, 400);
  }

  const config = TOKEN_CONFIG[provider];
  if (!config || !config.clientId || !config.clientSecret) {
    return htmlResponse(
      `<h1>OAuth not configured</h1><p>Set ${config?.envClientId ?? "(client id env var)"} + secret in your environment.</p>`,
      503,
    );
  }

  const callbackBase = url.origin;
  const tokenRes = await fetch(config.tokenEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: config.clientId,
      client_secret: config.clientSecret,
      redirect_uri: `${callbackBase}/api/oauth/${provider}/callback`,
      grant_type: "authorization_code",
    }),
  });

  if (!tokenRes.ok) {
    const detail = await tokenRes.text();
    return htmlResponse(
      `<h1>Token exchange failed</h1><pre>${escapeHtml(detail)}</pre>`,
      502,
    );
  }

  const tokenData = (await tokenRes.json()) as {
    access_token: string;
    refresh_token?: string;
    expires_in: number;
    scope: string;
    token_type: string;
  };

  if (!tokenData.refresh_token) {
    return htmlResponse(
      `<h1>No refresh token</h1><p>Re-authorize and ensure the consent screen prompts for offline access.</p><p><a href="/${encodeURIComponent(project)}/connections">Back</a></p>`,
      400,
    );
  }

  try {
    await storeOAuthToken({
      project_slug: project,
      provider: provider as OAuthProvider,
      account_label: "default",
      access_token: tokenData.access_token,
      refresh_token: tokenData.refresh_token,
      expires_at: new Date(Date.now() + tokenData.expires_in * 1000).toISOString(),
      scope: tokenData.scope ?? config.scopes.join(" "),
    });
  } catch (err) {
    return htmlResponse(
      `<h1>Could not store token</h1><pre>${escapeHtml(err instanceof Error ? err.message : String(err))}</pre><p>This usually means OS keychain is unavailable.</p>`,
      500,
    );
  }

  return NextResponse.redirect(
    `${callbackBase}/${encodeURIComponent(project)}/connections?connected=${provider}`,
  );
}

type TokenConfig = {
  clientId: string | undefined;
  clientSecret: string | undefined;
  envClientId: string;
  tokenEndpoint: string;
  scopes: string[];
};

const TOKEN_CONFIG: Record<string, TokenConfig> = {
  google_ads: {
    clientId: process.env.GOOGLE_ADS_CLIENT_ID,
    clientSecret: process.env.GOOGLE_ADS_CLIENT_SECRET,
    envClientId: "GOOGLE_ADS_CLIENT_ID",
    tokenEndpoint: "https://oauth2.googleapis.com/token",
    scopes: ["https://www.googleapis.com/auth/adwords"],
  },
  gsc: {
    clientId: process.env.GSC_CLIENT_ID,
    clientSecret: process.env.GSC_CLIENT_SECRET,
    envClientId: "GSC_CLIENT_ID",
    tokenEndpoint: "https://oauth2.googleapis.com/token",
    scopes: ["https://www.googleapis.com/auth/webmasters.readonly"],
  },
};

function htmlResponse(html: string, status = 200): Response {
  return new Response(
    `<!doctype html><meta charset="utf-8"><style>body{font-family:system-ui;max-width:32rem;margin:4rem auto;padding:0 1rem;color:#18181b}h1{font-size:1.2rem}a{color:#2563eb}pre{background:#f4f4f5;padding:.75rem;border-radius:.5rem;overflow:auto}</style>${html}`,
    { status, headers: { "Content-Type": "text/html; charset=utf-8" } },
  );
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
