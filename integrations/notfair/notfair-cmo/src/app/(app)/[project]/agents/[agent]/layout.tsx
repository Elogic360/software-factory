import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { resolveAgentMcpBlocker } from "@/server/onboarding/agent-mcp-blocker";
import { AgentTabs } from "@/components/agent-tabs";
import { AgentMcpBlockerCard } from "@/components/agent-mcp-blocker-card";

type Params = { agent: string; project: string };

export default async function AgentLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<Params>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();
  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  // Specialists whose required MCP isn't connected for this project
  // render a "Connect <platform>" blocker in place of the chat/tasks UI.
  // The tab strip is suppressed too — there's nothing actionable inside
  // any of the tabs until the MCP is wired.
  const blocker = resolveAgentMcpBlocker(project.slug, resolved.template_key);
  if (blocker) {
    return (
      <div className="absolute inset-0 flex flex-col">
        <AgentMcpBlockerCard projectSlug={projectSlug} blocker={blocker} />
      </div>
    );
  }

  return (
    // Escape parent main's p-6 so the tab strip + content area can own the
    // full viewport region. Children pick their own scroll/padding strategy.
    <div className="absolute inset-0 flex flex-col">
      <AgentTabs projectSlug={projectSlug} agentSlug={agentSlug} />
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  );
}
