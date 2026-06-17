import { notFound } from "next/navigation";
import { TEMPLATES } from "@/server/agent-templates";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug, readAgentMeta } from "@/server/agent-meta";
import { AgentDangerZone } from "@/components/agent-danger-zone";

type Params = { agent: string; project: string };

export default async function AgentSettingsPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();
  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  const meta = readAgentMeta(resolved.agent_id);
  const role = resolved.template_key
    ? TEMPLATES.find((t) => t.key === resolved.template_key)
    : undefined;

  return (
    <div className="h-full overflow-y-auto">
      <div className="ns-app-narrow">
        <header className="ns-page-head">
          <div className="ns-page-head-stack">
            <h1 className="ns-page-title">Settings</h1>
            <p className="ns-page-sub">
              <b>{resolved.name}</b>{" "}
              <span className="font-mono text-[12px]">· {resolved.agent_id}</span>
            </p>
          </div>
        </header>

        <section>
          <h2 className="ns-h2">
            <span>Identity</span>
            <span className="ns-h2-meta">Immutable for the life of the project</span>
          </h2>
          <div className="ns-card">
            <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-3 p-[18px]">
              <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                Name
              </dt>
              <dd className="text-[13px] font-medium text-[hsl(var(--notfair-ink-2))]">
                {resolved.name}
              </dd>

              {role && (
                <>
                  <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                    Role
                  </dt>
                  <dd className="text-[13px] text-[hsl(var(--notfair-ink-2))]">
                    {role.display_name}
                  </dd>
                </>
              )}

              <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                URL slug
              </dt>
              <dd>
                <span className="ns-tag-mono">{resolved.slug}</span>
              </dd>

              <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                Agent id
              </dt>
              <dd>
                <span className="ns-tag-mono">{resolved.agent_id}</span>
              </dd>

              {meta?.source_agent_id && (
                <>
                  <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                    Cloned from
                  </dt>
                  <dd>
                    <span className="ns-tag-mono">{meta.source_agent_id}</span>
                  </dd>
                </>
              )}

              {meta?.created_at && (
                <>
                  <dt className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                    Created
                  </dt>
                  <dd className="text-[13px] tabular-nums text-[hsl(var(--notfair-ink-2))]">
                    {new Date(meta.created_at).toLocaleString()}
                  </dd>
                </>
              )}
            </dl>
          </div>
        </section>

        <section>
          <h2 className="ns-h2">
            <span>Danger zone</span>
          </h2>
          <AgentDangerZone
            agentId={resolved.agent_id}
            agentDisplayName={resolved.name}
          />
        </section>
      </div>
    </div>
  );
}
