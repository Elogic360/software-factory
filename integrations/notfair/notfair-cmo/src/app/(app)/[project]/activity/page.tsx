import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { listAgentActions } from "@/server/db/agent-actions";

function timeAgo(iso: string) {
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 60) return `${Math.floor(seconds)}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default async function ActivityPage({
  params,
}: {
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();
  const actions = listAgentActions(project.slug, 200);

  return (
    <div className="ns-app-wide" style={{ maxWidth: 900 }}>
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Activity</h1>
          <p className="ns-page-sub">
            <b>{actions.length}</b> {actions.length === 1 ? "action" : "actions"}
            {" "}· append-only audit log of every autonomous decision and
            scheduled run.
          </p>
        </div>
      </header>

      {actions.length === 0 ? (
        <div className="ns-empty">
          <p className="ns-empty-title">No activity yet.</p>
          <p className="ns-empty-sub">
            Every autonomous decision and scheduled job lands here for auditing.
            When you provision agents or schedule crons, the events show up.
          </p>
        </div>
      ) : (
        <ol className="ns-group">
          {actions.map((a) => (
            <li key={a.id} className="ns-row flex-col items-start gap-2">
              <div className="flex w-full flex-wrap items-baseline gap-2">
                <span className="ns-tag-mono">{a.action_type}</span>
                <span className="font-mono text-[11px] text-[hsl(var(--notfair-ink-4))]">
                  {a.agent_id}
                </span>
                <span className="ml-auto text-[11.5px] tabular-nums text-[hsl(var(--notfair-ink-4))]">
                  {timeAgo(a.occurred_at)} ·{" "}
                  {new Date(a.occurred_at).toLocaleString()}
                </span>
              </div>
              <p className="m-0 text-[13px] leading-snug text-[hsl(var(--notfair-ink-2))]">
                {a.summary}
              </p>
              {a.reasoning && (
                <p className="m-0 w-full whitespace-pre-wrap rounded-lg bg-[hsl(var(--notfair-surface-2))] px-3 py-2 text-[12.5px] leading-snug text-[hsl(var(--notfair-ink-3))]">
                  {a.reasoning}
                </p>
              )}
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export const dynamic = "force-dynamic";
