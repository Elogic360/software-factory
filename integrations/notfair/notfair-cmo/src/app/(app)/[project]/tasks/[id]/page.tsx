import { notFound, redirect } from "next/navigation";

import { readAgentMeta } from "@/server/agent-meta";
import { getProject } from "@/server/db/projects";
import { getTask } from "@/server/db/tasks";
import {
  TEMPLATES,
  agentUrlSlug,
  type AgentTemplateKey,
} from "@/server/agent-templates";
import { projectHref } from "@/lib/project-href";

/**
 * Deep-link destination for task IDs. The canonical view lives in the agent
 * workspace, so we resolve the task's owning agent and redirect there with
 * the task pre-selected.
 */
export default async function TaskDetailPage({
  params,
}: {
  params: Promise<{ id: string; project: string }>;
}) {
  const { id, project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  const task = getTask(id);
  if (!task || task.project_slug !== project.slug) notFound();

  // Resolve the assignee's URL slug. For template agents the slug is
  // `<role>-<personal-name>`; for clones we use the slug stored on the
  // meta sidecar.
  const meta = readAgentMeta(task.agent_id);
  let agentSlug: string;
  if (meta?.template_key) {
    const template = TEMPLATES.find((t) => t.key === meta.template_key);
    const role = (meta.template_key as AgentTemplateKey) ?? "google_ads";
    const name = meta.name ?? template?.default_name ?? "agent";
    agentSlug = agentUrlSlug(role, name);
  } else if (meta?.slug) {
    agentSlug = meta.slug;
  } else {
    // No meta on disk yet — fall back to the agent_id's tail.
    agentSlug = task.agent_id.replace(`${slug}-`, "");
  }

  // Use the human-readable display_id in the canonical URL so the path
  // someone bookmarks reads "?task=demo7-3" not a UUID. getTask in the
  // workspace accepts either form.
  redirect(
    projectHref(slug, `/agents/${agentSlug}/tasks?task=${task.display_id}`),
  );
}
