import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { listCronsForProject } from "@/server/scheduler/display";
import {
  annotateOccurrencesWithRunStatus,
  expandSchedule,
} from "@/server/scheduler/display";
import { ScheduleCronDialog } from "@/components/schedule-cron-dialog";
import {
  CronCalendar,
  type CalendarCron,
  type CalendarOccurrence,
} from "@/components/cron-calendar";
import type { ScheduleInput } from "@/server/actions/cron-runs";

function scheduleForCalendar(s: unknown): ScheduleInput | null {
  if (!s || typeof s !== "object") return null;
  const obj = s as { kind?: string; expr?: unknown; tz?: unknown };
  if (obj.kind === "cron" && typeof obj.expr === "string") {
    return { kind: "cron", expr: obj.expr, ...(typeof obj.tz === "string" ? { tz: obj.tz } : {}) };
  }
  return null;
}

const NUM_DAYS = 14;

export default async function CronsPage({
  params,
}: {
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  let error: string | null = null;
  let view: Awaited<ReturnType<typeof listCronsForProject>>;
  try {
    view = await listCronsForProject(project.slug);
  } catch (err) {
    view = { project_slug: project.slug, groups: [] };
    error = err instanceof Error ? err.message : String(err);
  }

  const allCrons = view.groups.flatMap((g) => g.crons);
  const agentSlugs = view.groups.map((g) => g.agent);

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
    new Map([...schedulesByCronId.entries()].map(([k, v]) => [k, v ?? undefined])),
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
    <div className="ns-app-wide">
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Crons</h1>
          <p className="ns-page-sub">
            <b>{totalActive}</b> active
            {totalDisabled > 0 ? ` · ${totalDisabled} disabled` : ""} ·
            recurring work scheduled across your agents.
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
            <p className="mt-2 text-[12px] text-[hsl(var(--notfair-ink-4))]">
              Run{" "}
              <code className="rounded bg-[hsl(var(--notfair-surface-2))] px-1.5 py-px font-mono">
                notfair-cmo doctor
              </code>{" "}
              for help.
            </p>
          </div>
        </div>
      )}

      {!error && allCrons.length === 0 && (
        <div className="ns-empty">
          <p className="ns-empty-title">No scheduled work yet.</p>
          <p className="ns-empty-sub">
            Schedule a recurring job for one of this project&rsquo;s agents.
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
          agentSlugs={agentSlugs}
        />
      )}
    </div>
  );
}
