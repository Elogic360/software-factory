import { NextResponse } from "next/server";
import { getActiveProject } from "@/server/active-project";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { readTranscriptTail } from "@/server/sessions/transcript-tail";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * Generic transcript tail endpoint — agent + thread, no task lookup.
 *
 * Both surfaces (the task workspace and the free-form /chat/[thread] view)
 * poll this with the byte offset they last saw; we return any events
 * written since. Threads have no terminal state, so callers manage their
 * own "stop polling" signal (the task workspace gates on task.status).
 *
 * Project resolution: prefer the explicit `project` query param (the page
 * knows its URL slug and passes it through), fall back to the
 * active-project cookie. The cookie can lag the URL on first paint after a
 * project switch or direct deep-link, so the explicit param is the source
 * of truth when present.
 */
export async function GET(
  request: Request,
  context: { params: Promise<{ agent: string; thread: string }> },
) {
  const { agent: agentSlug, thread: threadId } = await context.params;

  const url = new URL(request.url);
  const projectParam = url.searchParams.get("project");
  const project = projectParam
    ? getProject(projectParam)
    : await getActiveProject();
  if (!project) {
    return NextResponse.json({ error: "no active project" }, { status: 400 });
  }

  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) {
    return NextResponse.json({ error: "unknown agent" }, { status: 404 });
  }

  const offsetParam = url.searchParams.get("offset");
  const byteOffset = offsetParam ? Number(offsetParam) : 0;
  const validOffset = Number.isFinite(byteOffset) && byteOffset >= 0 ? byteOffset : 0;

  const { events, byteOffset: newOffset, fileSize } = readTranscriptTail(
    project.slug,
    resolved.agent_id,
    threadId,
    validOffset,
  );

  return NextResponse.json({
    events,
    byteOffset: newOffset,
    file_size: fileSize,
  });
}
