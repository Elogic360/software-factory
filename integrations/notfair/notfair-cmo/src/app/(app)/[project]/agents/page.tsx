import Link from "next/link";
import { Bot, Check, Clock, MessageSquare } from "lucide-react";
import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { TEMPLATES } from "@/server/agent-templates";
import { listProjectAgents } from "@/server/agent-meta";
import { listCronsForProject } from "@/server/scheduler/display";
import { reprovisionAgentsAction } from "@/server/actions/projects";
import { ReprovisionButton } from "@/components/reprovision-button";
import { AgentAvatar } from "@/components/agent-avatar";
import { projectHref } from "@/lib/project-href";

export default async function AgentsPage({
  params,
}: {
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  const cronByAgent = new Map<string, number>();
  try {
    const view = await listCronsForProject(project.slug);
    for (const g of view.groups) cronByAgent.set(g.agent, g.crons.length);
  } catch {}

  const projectAgents = await listProjectAgents(project.slug);
  const reprovision = reprovisionAgentsAction.bind(null, project.slug);

  return (
    <div className="ns-app-wide" style={{ maxWidth: 880 }}>
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Agents</h1>
          <p className="ns-page-sub">
            <b>{projectAgents.length}</b> agent
            {projectAgents.length === 1 ? "" : "s"} · running on{" "}
            <b>
              {project.harness_adapter === "codex-local" ? "Codex" : "Claude Code"}
            </b>
          </p>
        </div>
        <div className="ns-page-actions">
          <ReprovisionButton action={reprovision} />
        </div>
      </header>

      <div className="grid gap-4">
        {projectAgents.map((agent) => {
          const role = agent.template_key
            ? TEMPLATES.find((t) => t.key === agent.template_key)
            : undefined;
          const crons = cronByAgent.get(agent.agent_id) ?? 0;
          return (
            <div key={agent.agent_id} className="ns-card">
              <div className="flex items-start gap-4 p-[18px]">
                {agent.template_key ? (
                  <AgentAvatar role={agent.template_key} size={44} />
                ) : (
                  <span className="ns-glyph" aria-hidden>
                    <Bot className="size-[18px] text-[hsl(var(--notfair-ink-2))]" />
                  </span>
                )}
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
                    <h2 className="m-0 text-[15.5px] font-semibold tracking-tight text-[hsl(var(--notfair-ink))]">
                      {agent.name}
                    </h2>
                    {role && <span className="ns-tag">{role.display_name}</span>}
                    <span className="ns-tag-mono">{agent.agent_id}</span>
                  </div>
                  <p className="mt-1 text-[13px] leading-snug text-[hsl(var(--notfair-ink-3))]">
                    {role?.description ?? agent.description ?? "Custom agent."}
                  </p>
                </div>
                <div className="flex shrink-0 items-center gap-2">
                  {crons > 0 && (
                    <Link
                      href={projectHref(slug, "/crons")}
                      className="inline-flex items-center gap-1 rounded-md px-2 py-1 text-[12px] text-[hsl(var(--notfair-ink-4))] transition-colors hover:bg-[hsl(var(--notfair-surface-2))] hover:text-[hsl(var(--notfair-ink-2))]"
                    >
                      <Clock className="size-3" />
                      {crons}
                    </Link>
                  )}
                  <Link
                    href={projectHref(slug, `/agents/${agent.slug}/chat`)}
                    className="ns-btn ns-btn-primary ns-btn-sm"
                  >
                    <MessageSquare className="size-3.5" />
                    Chat
                  </Link>
                </div>
              </div>
              {role && (
                <div className="border-t border-border/60 px-[18px] py-3">
                  <ul className="grid grid-cols-1 gap-1.5 text-[13px] text-[hsl(var(--notfair-ink-3))] md:grid-cols-2">
                    {role.capabilities.map((c) => (
                      <li key={c} className="flex items-start gap-2">
                        <Check className="mt-0.5 size-3.5 shrink-0 text-[hsl(var(--notfair-accent))]" />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
