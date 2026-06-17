import { NextResponse } from "next/server";
import { getProject } from "@/server/db/projects";
import { ensureProjectAgents } from "@/server/agent-templates";

export const runtime = "nodejs";

/**
 * POST /api/projects/[slug]/provision
 * Idempotently creates OpenClaw agents for this project (CMO + specialists).
 * Called from onboarding flow once after project creation.
 */
export async function POST(
  _request: Request,
  { params }: { params: Promise<{ slug: string }> },
) {
  const { slug } = await params;
  const project = getProject(slug);
  if (!project) {
    return NextResponse.json({ error: "Project not found" }, { status: 404 });
  }
  const result = await ensureProjectAgents(slug);
  return NextResponse.json({ ok: true, ...result });
}
