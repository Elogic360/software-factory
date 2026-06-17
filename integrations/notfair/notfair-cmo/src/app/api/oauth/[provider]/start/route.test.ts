import { afterAll, describe, expect, it, vi } from "vitest";

// Set env BEFORE the route is imported. vi.hoisted runs before any ESM
// `import` statement, including the import below — without this the
// OAUTH_CONFIG closure snapshots an empty env and every google_ads test
// hits the 503 "not configured" branch.
const { ORIGINAL_ENV } = vi.hoisted(() => {
  const orig = { ...process.env };
  process.env.GOOGLE_ADS_CLIENT_ID = "my-google-client-id";
  process.env.GOOGLE_ADS_CLIENT_SECRET = "my-secret";
  delete process.env.GSC_CLIENT_ID;
  delete process.env.GSC_CLIENT_SECRET;
  return { ORIGINAL_ENV: orig };
});

import { GET } from "./route";

function makeReq(url: string): Request {
  return new Request(url, { method: "GET" });
}

describe("GET /api/oauth/[provider]/start", () => {
  afterAll(() => {
    process.env = { ...ORIGINAL_ENV };
  });

  it("returns 400 when project query param is missing", async () => {
    const res = await GET(
      makeReq("http://localhost/api/oauth/google_ads/start"),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(400);
    const body = (await res.json()) as { error: string };
    expect(body.error).toContain("project");
  });

  it("returns 404 when provider is unknown", async () => {
    const res = await GET(
      makeReq("http://localhost/api/oauth/unknown_provider/start?project=acme"),
      { params: Promise.resolve({ provider: "unknown_provider" }) },
    );
    expect(res.status).toBe(404);
    const body = (await res.json()) as { error: string };
    expect(body.error).toMatch(/unknown_provider/i);
  });

  it("returns 503 with helpful text for a known-but-unconfigured provider (gsc)", async () => {
    const res = await GET(
      makeReq("http://localhost/api/oauth/gsc/start?project=acme"),
      { params: Promise.resolve({ provider: "gsc" }) },
    );
    expect(res.status).toBe(503);
    expect(res.headers.get("Content-Type")).toContain("text/plain");
    const text = await res.text();
    expect(text).toContain("GSC_CLIENT_ID");
    expect(text).toContain("GSC_CLIENT_SECRET");
  });

  it("redirects to Google's OAuth consent screen for google_ads when configured", async () => {
    const res = await GET(
      makeReq("http://localhost/api/oauth/google_ads/start?project=acme"),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(307);
    const location = res.headers.get("location");
    expect(location).toBeTruthy();
    const redirect = new URL(location!);
    expect(redirect.origin).toBe("https://accounts.google.com");
    expect(redirect.pathname).toBe("/o/oauth2/v2/auth");
    expect(redirect.searchParams.get("client_id")).toBe("my-google-client-id");
    expect(redirect.searchParams.get("redirect_uri")).toBe(
      "http://localhost/api/oauth/google_ads/callback",
    );
    expect(redirect.searchParams.get("response_type")).toBe("code");
    expect(redirect.searchParams.get("scope")).toContain("adwords");
    expect(redirect.searchParams.get("access_type")).toBe("offline");
    expect(redirect.searchParams.get("prompt")).toBe("consent");

    const state = redirect.searchParams.get("state");
    expect(state).toBeTruthy();
    const decoded = JSON.parse(
      Buffer.from(state!, "base64url").toString("utf8"),
    ) as { project: string; ts: number };
    expect(decoded.project).toBe("acme");
    expect(typeof decoded.ts).toBe("number");
  });
});
