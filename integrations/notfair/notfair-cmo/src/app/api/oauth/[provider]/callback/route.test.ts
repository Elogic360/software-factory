import { afterAll, afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const storeOAuthTokenMock = vi.fn();
vi.mock("@/server/db/oauth", () => ({
  storeOAuthToken: (...args: unknown[]) => storeOAuthTokenMock(...args),
}));

// vi.hoisted runs before any ESM `import` statement, so TOKEN_CONFIG can
// snapshot a properly-configured process.env at module-load time.
const { ORIGINAL_ENV } = vi.hoisted(() => {
  const orig = { ...process.env };
  process.env.GOOGLE_ADS_CLIENT_ID = "id";
  process.env.GOOGLE_ADS_CLIENT_SECRET = "secret";
  delete process.env.GSC_CLIENT_ID;
  delete process.env.GSC_CLIENT_SECRET;
  return { ORIGINAL_ENV: orig };
});

import { GET } from "./route";

function makeReq(url: string): Request {
  return new Request(url, { method: "GET" });
}

function buildState(project: string): string {
  return Buffer.from(JSON.stringify({ project, ts: Date.now() })).toString(
    "base64url",
  );
}

describe("GET /api/oauth/[provider]/callback", () => {
  const fetchMock = vi.fn();
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.clearAllMocks();
    fetchMock.mockReset();
    globalThis.fetch = fetchMock as unknown as typeof fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  afterAll(() => {
    process.env = { ...ORIGINAL_ENV };
  });

  it("returns 400 HTML when provider sends an error param", async () => {
    const res = await GET(
      makeReq(
        "http://localhost/api/oauth/google_ads/callback?error=access_denied",
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(400);
    expect(res.headers.get("Content-Type")).toContain("text/html");
    const text = await res.text();
    expect(text).toContain("OAuth denied");
    expect(text).toContain("access_denied");
  });

  it("escapes HTML in the error param", async () => {
    const res = await GET(
      makeReq(
        "http://localhost/api/oauth/google_ads/callback?error=" +
          encodeURIComponent("<script>x</script>"),
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    const text = await res.text();
    expect(text).not.toContain("<script>x</script>");
    expect(text).toContain("&lt;script&gt;");
  });

  it("returns 400 when code or state is missing", async () => {
    const res = await GET(
      makeReq("http://localhost/api/oauth/google_ads/callback?code=abc"),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(400);
    const text = await res.text();
    expect(text).toContain("Missing code or state");
  });

  it("returns 400 when state token is malformed base64", async () => {
    const res = await GET(
      makeReq(
        "http://localhost/api/oauth/google_ads/callback?code=abc&state=not-base64-json!!!",
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(400);
    const text = await res.text();
    expect(text).toContain("Invalid state token");
  });

  it("returns 503 when provider is known but client id is not configured (gsc)", async () => {
    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/gsc/callback?code=abc&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "gsc" }) },
    );
    expect(res.status).toBe(503);
    const text = await res.text();
    expect(text).toContain("OAuth not configured");
    expect(text).toContain("GSC_CLIENT_ID");
  });

  it("returns 503 when provider key is entirely unknown (config undefined)", async () => {
    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/whatever/callback?code=abc&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "whatever" }) },
    );
    expect(res.status).toBe(503);
    const text = await res.text();
    expect(text).toContain("OAuth not configured");
  });

  it("returns 502 when token exchange request fails", async () => {
    fetchMock.mockResolvedValueOnce(
      new Response("invalid_grant detail", { status: 400 }),
    );
    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/google_ads/callback?code=abc&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(502);
    const text = await res.text();
    expect(text).toContain("Token exchange failed");
    expect(text).toContain("invalid_grant detail");
  });

  it("returns 400 when token response is missing refresh_token", async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          access_token: "at",
          expires_in: 3600,
          scope: "scope",
          token_type: "Bearer",
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/google_ads/callback?code=abc&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(400);
    const text = await res.text();
    expect(text).toContain("No refresh token");
  });

  it("returns 500 when token storage fails", async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          access_token: "at",
          refresh_token: "rt",
          expires_in: 3600,
          scope: "scope",
          token_type: "Bearer",
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    storeOAuthTokenMock.mockRejectedValueOnce(new Error("keychain failed"));

    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/google_ads/callback?code=abc&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(500);
    const text = await res.text();
    expect(text).toContain("Could not store token");
    expect(text).toContain("keychain failed");
  });

  it("redirects to /<project>/connections on full success", async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          access_token: "at",
          refresh_token: "rt",
          expires_in: 3600,
          scope: "scope1 scope2",
          token_type: "Bearer",
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    storeOAuthTokenMock.mockResolvedValueOnce(undefined);

    const res = await GET(
      makeReq(
        `http://localhost/api/oauth/google_ads/callback?code=mycode&state=${buildState("acme")}`,
      ),
      { params: Promise.resolve({ provider: "google_ads" }) },
    );
    expect(res.status).toBe(307);
    expect(res.headers.get("location")).toBe(
      "http://localhost/acme/connections?connected=google_ads",
    );

    expect(storeOAuthTokenMock).toHaveBeenCalledTimes(1);
    const stored = storeOAuthTokenMock.mock.calls[0]![0] as {
      project_slug: string;
      provider: string;
      access_token: string;
      refresh_token: string;
      scope: string;
    };
    expect(stored.project_slug).toBe("acme");
    expect(stored.provider).toBe("google_ads");
    expect(stored.access_token).toBe("at");
    expect(stored.refresh_token).toBe("rt");
    expect(stored.scope).toBe("scope1 scope2");

    const [tokenUrl, init] = fetchMock.mock.calls[0]!;
    expect(tokenUrl).toBe("https://oauth2.googleapis.com/token");
    expect((init as RequestInit).method).toBe("POST");
    const bodyAsString = ((init as RequestInit).body as URLSearchParams).toString();
    expect(bodyAsString).toContain("code=mycode");
    expect(bodyAsString).toContain("grant_type=authorization_code");
    expect(bodyAsString).toContain(
      "redirect_uri=http%3A%2F%2Flocalhost%2Fapi%2Foauth%2Fgoogle_ads%2Fcallback",
    );
  });
});
