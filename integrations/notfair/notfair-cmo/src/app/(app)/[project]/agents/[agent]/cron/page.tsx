import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { listCronsForProject } from "@/server/scheduler/display";
import {
  annotateOccurrencesWithRunStatus,
  expandSchedule,
} from "@/server/scheduler/display";
import {
  CronCalendar,
  type CalendarCron,
  type CalendarOccurrence,
} from "@/components/cron-calendar";
import { ScheduleCronDialog } from "@/components/schedule-cron-dialog";
import type { ScheduleInput } from "@/server/actions/cron-runs";

const NUM_DAYS = 14;

function scheduleForCalendar(s: unknown): ScheduleInput | null {
  if (!s || typeof s !== "object") return null;
  const obj = s as { kind?: string; expr?: unknown; tz?: unknown };
  if (obj.kind === "cron" && typeof obj.expr === "string") {
    return { kind: "cron", expr: obj.expr, ...(typeof obj.tz === "string" ? { tz: obj.tz } : {}) };
  }
  return null;
}

type Params = { agent: string; project: string };

export default async function AgentCronPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();
  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();

  const templateSlug = resolved.slug;

  let error: string | null = null;
  let view: Awaited<ReturnType<typeof listCronsForProject>>;
  try {
    view = await listCronsForProject(project.slug);
  } catch (err) {
    view = { project_slug: project.slug, groups: [] };
    error = err instanceof Error ? err.message : String(err);
  }

  const myGroup = view.groups.find((g) => g.agent === templateSlug);
  const allCrons = myGroup?.crons ?? [];

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const startOfFirstDay = today.getTime();
  const dayMs = 24 * 60 * 60 * 1000;
  const until = startOfFirstDay + NUM_DAYS * dayMs;

  const occurrences: CalendarOccurrence[] = [];
  const schedulesByCronId = new Map<string, ReturnType<typeof scheduleForCalendar>>();
  for (const cron of allCrons) {
    const occs = expandSchedule(
      cron.id,
      cron.schedule_raw,
      { from: startOfFirstDay, until },
      {
        name: cron.name,
        short_name: cron.short_name,
        agent_id: cron.agent_id,
        agent_slug: cron.agent_slug,
        schedule_text: cron.schedule_text,
      },
    );
    for (const o of occs) occurrences.push({ ...o, cron_disabled: cron.disabled });
    schedulesByCronId.set(cron.id, scheduleForCalendar(cron.schedule_raw));
  }
  annotateOccurrencesWithRunStatus(
    occurrences,
    new Map(
      [...schedulesByCronId.entries()].map(([k, v]) => [k, v ?? undefined]),
    ),
  );

  const cronsById: Record<string, CalendarCron> = {};
  for (const cron of allCrons) {
    cronsById[cron.id] = {
      id: cron.id,
      short_name: cron.short_name,
      full_name: cron.name,
      agent_id: cron.agent_id,
      agent_slug: cron.agent_slug,
      schedule_text: cron.schedule_text,
      disabled: cron.disabled,
      status_text: cron.status_text,
      message: cron.message,
      description: cron.description,
      last_run_at_ms: cron.last_run_at_ms,
      last_status: cron.last_status,
      last_error: cron.last_error,
      schedule_raw: scheduleForCalendar(cron.schedule_raw),
    };
  }

  const totalActive = allCrons.filter((c) => !c.disabled).length;
  const totalDisabled = allCrons.length - totalActive;

  return (
    <div className="h-full overflow-y-auto">
      <div className="ns-app-wide">
        <header className="ns-page-head">
          <div className="ns-page-head-stack">
            <h1 className="ns-page-title">{resolved.name}&rsquo;s schedule</h1>
            <p className="ns-page-sub">
              <b>{totalActive}</b> active
              {totalDisabled > 0 ? ` · ${totalDisabled} disabled` : ""}
            </p>
          </div>
          <div className="ns-page-actions">
            <ScheduleCronDialog projectSlug={project.slug} />
          </div>
        </header>

        {error && (
          <div className="ns-card">
            <div className="ns-card-body">
              <p className="text-[14px] font-semibold text-destructive">
                Could not load crons.
              </p>
              <p className="mt-1 text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
                {error}
              </p>
            </div>
          </div>
        )}

        {!error && allCrons.length === 0 && (
          <div className="ns-empty">
            <p className="ns-empty-title">
              No scheduled work for {resolved.name} yet.
            </p>
            <p className="ns-empty-sub">
              Ask the agent in chat (&ldquo;run a daily bid review at 9am&rdquo;)
              or schedule one directly.
            </p>
            <div className="ns-empty-action">
              <ScheduleCronDialog projectSlug={project.slug} />
            </div>
          </div>
        )}

        {!error && allCrons.length > 0 && (
          <CronCalendar
            startOfFirstDay={startOfFirstDay}
            numDays={NUM_DAYS}
            occurrences={occurrences}
            cronsById={cronsById}
            agentSlugs={[templateSlug]}
          />
        )}
      </div>
    </div>
  );
}
