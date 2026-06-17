import { notFound } from "next/navigation";

import { AgentTaskWorkspace } from "@/components/agent-task-workspace";
import { getProject } from "@/server/db/projects";
import { getMcpCatalog } from "@/server/mcp-catalog";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { listApprovalsForTask } from "@/server/db/approvals";
import { listQuestionsForTask } from "@/server/db/questions";
import { getTask, listTasksByAgent, setTaskThreadIfMissing } from "@/server/db/tasks";
import { buildPendingSessionKey, findSessionBySessionId } from "@/server/sessions/view";
import {
  readTranscriptTail,
  type TranscriptEvent,
} from "@/server/sessions/transcript-tail";
import {
  buildTaskKickoffMessage,
  generateTaskThreadId,
} from "@/server/orchestration/task-kickoff";
import type { Approval, Question, Task } from "@/types";

type Props = {
  params: Promise<{ agent: string; project: string }>;
  searchParams: Promise<{ task?: string }>;
};

type SelectedBundle = {
  task: Task;
  threadId: string;
  sessionKey: string;
  initialEvents: TranscriptEvent[];
  initialByteOffset: number;
  /**
   * Every approval ever requested on this task, newest first. The chat view
   * renders these above the transcript so the user can act on a pending
   * approval without leaving the task. Resolved rows show too — they're
   * the audit trail for "what did I approve here?".
   */
  approvals: Approval[];
  /**
   * Every question ever raised on this task via `ask_user_question`,
   * newest first. The chat view renders the pending one inline so the
   * user can answer without leaving the task; resolved rows stay as the
   * audit trail.
   */
  questions: Question[];
  /**
   * Auto-kickoff payload for tasks that haven't started yet. The page
   * builds the full assignment brief server-side so the client can just
   * hand it to /api/chat — no business logic on the browser. `null` for
   * any task already past `proposed` (kickoff already happened or never
   * will).
   */
  kickoff: { taskId: string; message: string } | null;
};

export default async function AgentTasksPage({ params, searchParams }: Props) {
  const [{ agent: agentSlug, project: projectSlug }, { task: selectedTaskId }] =
    await Promise.all([params, searchParams]);

  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();

  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  const agentFullId = resolved.agent_id;

  // Load the selected task's brief + transcript bundle if `?task=` is set.
  // For tasks still in `proposed`, we hand the client a kickoff payload it
  // fires through /api/chat on mount — the SSE path streams gateway events
  // live (JSONL polling alone misses the run because OpenClaw's codex
  // mode flushes the transcript once per turn). For tasks already past
  // proposed (delegated via MCP, restarted via Start all, or finished),
  // this path is read-only.
  let selected: SelectedBundle | null = null;
  if (selectedTaskId) {
    selected = await loadSelectedBundle(project.slug, agentFullId, selectedTaskId);
    // Guard: drop selection if it's not on this agent (cross-agent links etc).
    if (selected && selected.task.agent_id !== agentFullId) selected = null;
  }

  const tasks = listTasksByAgent(agentFullId);
  const proposedCount = tasks.filter((t) => t.status === "proposed").length;
  // Brand-favicon lookup table for MCP tool calls in the transcript.
  const mcpCatalog = getMcpCatalog(project.slug).map((m) => ({
    key: m.key,
    display_name: m.display_name,
    resource_url: m.resource_url,
  }));

  return (
    <AgentTaskWorkspace
      projectSlug={projectSlug}
      agentSlug={agentSlug}
      agentFullId={agentFullId}
      agentDisplayName={resolved.name}
      tasks={tasks}
      selected={selected}
      proposedCount={proposedCount}
      mcpCatalog={mcpCatalog}
    />
  );
}

async function loadSelectedBundle(
  projectSlug: string,
  agentFullId: string,
  taskId: string,
): Promise<SelectedBundle | null> {
  let task = getTask(taskId);
  if (!task) return null;

  // Lazily mint a per-task chat thread on first open. Stable forever after.
  if (!task.thread_id) {
    const updated = setTaskThreadIfMissing(task.id, generateTaskThreadId());
    if (updated) task = updated;
  }
  if (!task.thread_id) return null;
  const threadId = task.thread_id;

  // Resolve canonical sessionKey for /api/chat composer sends (when task
  // is done and user wants to keep chatting). The pending key is a safe
  // fallback for brand-new threads.
  const session = findSessionBySessionId(projectSlug, agentFullId, threadId);
  const sessionKey =
    session?.sessionKey ?? buildPendingSessionKey(agentFullId, threadId);

  const { events, byteOffset } = readTranscriptTail(projectSlug, agentFullId, threadId, 0);
  const approvals = listApprovalsForTask(task.id);
  const questions = listQuestionsForTask(task.id);

  // Only minted for `proposed` tasks. The client uses this to fire the
  // first turn via /api/chat (which streams gateway events live), and
  // /api/chat atomically claims the task on the server before forwarding
  // — so reloads / concurrent tabs can't double-fire the agent.
  const kickoff =
    task.status === "proposed"
      ? { taskId: task.id, message: buildTaskKickoffMessage(task) }
      : null;

  return {
    task,
    threadId,
    sessionKey,
    initialEvents: events,
    initialByteOffset: byteOffset,
    approvals,
    questions,
    kickoff,
  };
}
