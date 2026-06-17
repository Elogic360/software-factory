import Link from "next/link";
import { notFound } from "next/navigation";
import { Bot, MessageSquare } from "lucide-react";
import { getProject } from "@/server/db/projects";
import { listPendingApprovals } from "@/server/db/approvals";
import { listTasks } from "@/server/db/tasks";
import { listAgentActions } from "@/server/db/agent-actions";
import { TEMPLATES } from "@/server/agent-templates";
import { listProjectAgents } from "@/server/agent-meta";
import { colorForRole } from "@/lib/agent-colors";
import { cn } from "@/lib/utils";
import { projectHref } from "@/lib/project-href";
import { AgentAvatar } from "@/components/agent-avatar";

function timeAgo(iso: string) {
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 60) return `${Math.floor(seconds)}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default async function ProjectHomePage({
  params,
}: {
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  const pending = listPendingApprovals(project.slug);
  const tasks = listTasks(project.slug);
  const recent = listAgentActions(project.slug, 8);
  const projectAgents = await listProjectAgents(project.slug);
  const cmoAgent = projectAgents.find((a) => a.template_key === "cmo");
  const cmoChatHref = cmoAgent
    ? projectHref(slug, `/agents/${cmoAgent.slug}/chat`)
    : projectHref(slug, "");

  const running = tasks.filter((t) => t.status === "working").length;
  const nothingHappened = tasks.length === 0 && recent.length === 0;

  return (
    <div className="ns-app-wide">
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">{project.display_name}</h1>
          <p className="ns-page-sub">
            Your local AI marketing team. Hand a goal to the CMO and they&rsquo;ll
            delegate.
          </p>
        </div>
        <div className="ns-page-actions">
          <Link href={cmoChatHref} className="ns-btn ns-btn-primary">
            <MessageSquare className="size-4" />
            Chat with CMO
          </Link>
        </div>
      </header>

      {/* KPI strip. Spend tracking lives elsewhere now; the home tiles
          surface only the counters the user has a direct action on. */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <KpiTile
          label="Active tasks"
          value={String(running)}
          hint={`${tasks.length} total`}
          href={projectHref(slug, "/tasks")}
        />
        <KpiTile
          label="Pending approvals"
          value={String(pending.length)}
          hint={pending.length === 0 ? "all caught up" : "review →"}
          href={projectHref(slug, "/approvals")}
          accent={pending.length > 0}
        />
        <KpiTile
          label="Crons"
          value="·"
          hint="scheduled work"
          href={projectHref(slug, "/crons")}
        />
      </div>

      {/* Two-up: agents on the left, recent activity on the right. */}
      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <section className="lg:col-span-2">
          <div className="ns-h2">
            <span>Your agents</span>
            <Link href={projectHref(slug, "/agents")} className="ns-link ns-h2-meta">
              View all ›
            </Link>
          </div>
          <ol className="ns-group">
            {projectAgents.map((agent) => {
              const role = agent.template_key
                ? TEMPLATES.find((t) => t.key === agent.template_key)
                : undefined;
              const rolePalette = agent.template_key
                ? colorForRole(agent.template_key)
                : null;
              return (
                <li key={agent.agent_id}>
                  <Link
                    href={projectHref(slug, `/agents/${agent.slug}/chat`)}
                    className="ns-row-button"
                  >
                    {agent.template_key ? (
                      <AgentAvatar role={agent.template_key} size={40} />
                    ) : (
                      <span className="ns-glyph" aria-hidden>
                        <Bot className="size-[18px] text-[hsl(var(--notfair-ink-2))]" />
                      </span>
                    )}
                    <span className="ns-row-body">
                      <span className="ns-row-title-row">
                        <span className="ns-row-title">{agent.name}</span>
                        {role && (
                          <span
                            className={cn(
                              "inline-flex items-center rounded-[5px] border px-1.5 py-[2px] text-[10.5px] font-medium uppercase tracking-wide leading-none",
                              rolePalette?.chip ?? "ns-tag",
                            )}
                          >
                            {role.display_name}
                          </span>
                        )}
                      </span>
                      <span className="ns-row-desc block">
                        {role?.description ?? agent.description ?? "Custom agent."}
                      </span>
                    </span>
                    <span className="ns-row-meta">
                      <span className="chev" aria-hidden>
                        ›
                      </span>
                    </span>
                  </Link>
                </li>
              );
            })}
          </ol>
        </section>

        <section>
          <div className="ns-h2">
            <span>Recent activity</span>
            <Link
              href={projectHref(slug, "/activity")}
              className="ns-link ns-h2-meta"
            >
              All ›
            </Link>
          </div>
          {recent.length === 0 ? (
            <div className="ns-empty">
              <p className="ns-empty-title">Nothing yet.</p>
              <p className="ns-empty-sub">
                Autonomous decisions and scheduled work will show up here.
              </p>
            </div>
          ) : (
            <ol className="ns-group">
              {recent.map((a) => (
                <li key={a.id} className="ns-row flex-col items-start gap-1">
                  <div className="flex w-full items-baseline justify-between gap-2">
                    <span className="ns-tag-mono">{a.action_type}</span>
                    <span className="text-[11px] tabular-nums text-[hsl(var(--notfair-ink-4))]">
                      {timeAgo(a.occurred_at)}
                    </span>
                  </div>
                  <p className="m-0 text-[12.5px] leading-snug text-[hsl(var(--notfair-ink-3))] line-clamp-2">
                    {a.summary}
                  </p>
                </li>
              ))}
            </ol>
          )}
        </section>
      </div>

      {nothingHappened && (
        <section className="mt-10">
          <div className="ns-h2">
            <span>Getting started</span>
          </div>
          <ol className="ns-group">
            <GettingStartedStep
              n="1"
              title="Connect your data sources"
              desc="Wire up Google Ads, Meta Ads, or Search Console so agents can do real work."
              href={projectHref(slug, "/connections")}
            />
            <GettingStartedStep
              n="2"
              title="Chat with your CMO"
              desc="Brief them on goals, audience, and constraints. They&rsquo;ll plan from there."
              href={cmoChatHref}
            />
            <GettingStartedStep
              n="3"
              title="Schedule recurring work"
              desc="Daily bid review, weekly SEO audit — whatever cadence you want."
              href={projectHref(slug, "/crons")}
            />
          </ol>
        </section>
      )}
    </div>
  );
}

function KpiTile({
  label,
  value,
  hint,
  href,
  accent,
}: {
  label: string;
  value: string;
  hint: string;
  href?: string;
  accent?: boolean;
}) {
  const body = (
    <>
      <p className="ns-kpi-label">{label}</p>
      <p
        className={`ns-kpi-value ${
          accent ? "text-[hsl(var(--notfair-accent))]" : ""
        }`}
      >
        {value}
      </p>
      <p className="ns-kpi-hint">{hint}</p>
    </>
  );
  if (href)
    return (
      <Link href={href} className="ns-kpi">
        {body}
      </Link>
    );
  return <div className="ns-kpi">{body}</div>;
}

function GettingStartedStep({
  n,
  title,
  desc,
  href,
}: {
  n: string;
  title: string;
  desc: string;
  href: string;
}) {
  return (
    <li>
      <Link href={href} className="ns-row-button">
        <span className="ns-glyph ns-glyph-accent" aria-hidden>
          {n}
        </span>
        <span className="ns-row-body">
          <span className="ns-row-title">{title}</span>
          <span className="ns-row-desc block">{desc}</span>
        </span>
        <span className="ns-row-meta">
          <span className="chev" aria-hidden>
            ›
          </span>
        </span>
      </Link>
    </li>
  );
}
