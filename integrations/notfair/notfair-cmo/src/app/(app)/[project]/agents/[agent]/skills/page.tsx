import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { getSkillStatus } from "@/server/agents/skills";
import { SkillsList } from "@/components/skills-list";

type Params = { agent: string; project: string };

export default async function AgentSkillsPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();
  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  const agentFullId = resolved.agent_id;
  let report: Awaited<ReturnType<typeof getSkillStatus>> | null = null;
  let error: string | null = null;
  try {
    report = await getSkillStatus(agentFullId);
  } catch (err) {
    error = err instanceof Error ? err.message : String(err);
  }

  const skills = report?.skills ?? [];

  return (
    <div className="h-full overflow-y-auto">
      <div className="ns-app-wide" style={{ maxWidth: 880 }}>
        <header className="ns-page-head">
          <div className="ns-page-head-stack">
            <h1 className="ns-page-title">Skills</h1>
            <p className="ns-page-sub">
              Capabilities available to <b>{resolved.name}</b> from this
              workspace.
            </p>
          </div>
        </header>

        {error && (
          <div className="ns-card">
            <div className="ns-card-body">
              <p className="text-[14px] font-semibold text-destructive">
                Could not load skills.
              </p>
              <p className="mt-1 text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                {error}
              </p>
            </div>
          </div>
        )}

        {!error && <SkillsList skills={skills} />}
      </div>
    </div>
  );
}
