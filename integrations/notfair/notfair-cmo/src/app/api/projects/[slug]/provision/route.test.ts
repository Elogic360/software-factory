import { beforeEach, describe, expect, it, vi } from "vitest";

import type { Project } from "@/types";

const getProjectMock = vi.fn();
vi.mock("@/server/db/projects", () => ({
  getProject: (...args: unknown[]) => getProjectMock(...args),
}));

const ensureProjectAgentsMock = vi.fn();
vi.mock("@/server/agent-templates", () => ({
  ensureProjectAgents: (...args: unknown[]) => ensureProjectAgentsMock(...args),
}));

import { POST } from "./route";

function makeProject(overrides: Partial<Project> = {}): Project {
  return {
    id: "uuid",
    slug: "acme",
    display_name: "Acme",
    created_at: "now",
    archived_at: null,
    google_ads_account_id: null,
    website_url: null,
    codebase_path: null,
    ...overrides,
  };
}

function makeReq(): Request {
  return new Request("http://localhost/api/projects/acme/provision", {
    method: "POST",
  });
}

describe("POST /api/projects/[slug]/provision", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns 404 when project not found", async () => {
    getProjectMock.mockReturnValueOnce(null);
    const res = await POST(makeReq(), { params: Promise.resolve({ slug: "ghost" }) });
    expect(res.status).toBe(404);
    const body = (await res.json()) as { error: string };
    expect(body.error).toBe("Project not found");
    expect(ensureProjectAgentsMock).not.toHaveBeenCalled();
  });

  it("returns ok with ensureProjectAgents result on success", async () => {
    getProjectMock.mockReturnValueOnce(makeProject({ slug: "acme" }));
    ensureProjectAgentsMock.mockResolvedValueOnce({
      created: ["acme-cmo"],
      existed: [],
      failed: [],
    });
    const res = await POST(makeReq(), { params: Promise.resolve({ slug: "acme" }) });
    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      ok: boolean;
      created: string[];
      existed: string[];
      failed: unknown[];
    };
    expect(body).toEqual({
      ok: true,
      created: ["acme-cmo"],
      existed: [],
      failed: [],
    });
    expect(ensureProjectAgentsMock).toHaveBeenCalledWith("acme");
  });

  it("returns ok even when ensureProjectAgents reports partial failures", async () => {
    getProjectMock.mockReturnValueOnce(makeProject({ slug: "acme" }));
    ensureProjectAgentsMock.mockResolvedValueOnce({
      created: [],
      existed: ["acme-cmo"],
      failed: [{ name: "acme-google-ads", error: "boom" }],
    });
    const res = await POST(makeReq(), { params: Promise.resolve({ slug: "acme" }) });
    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      ok: boolean;
      failed: Array<{ name: string; error: string }>;
    };
    expect(body.ok).toBe(true);
    expect(body.failed).toHaveLength(1);
  });

  it("propagates the slug from params to getProject + ensureProjectAgents", async () => {
    getProjectMock.mockReturnValueOnce(makeProject({ slug: "other" }));
    ensureProjectAgentsMock.mockResolvedValueOnce({ created: [], existed: [], failed: [] });
    await POST(makeReq(), { params: Promise.resolve({ slug: "other" }) });
    expect(getProjectMock).toHaveBeenCalledWith("other");
    expect(ensureProjectAgentsMock).toHaveBeenCalledWith("other");
  });
});
