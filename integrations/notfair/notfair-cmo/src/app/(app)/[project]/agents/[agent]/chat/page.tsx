import { redirect, notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import {
  listSessionsForAgent,
  newSessionId,
} from "@/server/sessions/view";
import { pickLatestChatSession } from "@/server/sessions/view";
import { listTasksByAgent } from "@/server/db/tasks";
import { projectHref } from "@/lib/project-href";

/**
 * Default landing for /<project>/agents/[agent]/chat — pick a free-form
 * chat thread (NOT a task workspace or cron run) and redirect into the
 * per-thread URL so refresh/share/back-button all keep the thread context.
 * Task and cron threads have their own entry points (kanban card, cron
 * calendar) and shouldn't hijack the agent's "chat" landing.
 */
export default async function ChatIndexPage({
  params,
}: {
  params: Promise<{ agent: string; project: string }>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();
  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  // Build a set of every thread_id that belongs to a task so we can
  // exclude those sessions. Cron sessions self-identify via OpenClaw's
  // `cron:<jobId>:run:<id>` label prefix.
  const taskThreadIds = new Set<string>();
  for (const t of listTasksByAgent(resolved.agent_id)) {
    if (t.thread_id) taskThreadIds.add(t.thread_id);
  }

  const sessions = listSessionsForAgent(project.slug, resolved.agent_id);
  const latestChat = pickLatestChatSession(sessions, taskThreadIds);
  const target = latestChat?.sessionId ?? newSessionId();
  redirect(projectHref(projectSlug, `/agents/${agentSlug}/chat/${target}`));
}
