import { notFound } from "next/navigation";

import { TasksBoard } from "@/components/tasks-board";
import { listProjectAgents } from "@/server/agent-meta";
import { getProject } from "@/server/db/projects";
import { listTasks } from "@/server/db/tasks";

export default async function TasksPage({
  params,
}: {
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  const [tasks, agents] = await Promise.all([
    Promise.resolve(listTasks(project.slug)),
    listProjectAgents(project.slug),
  ]);

  return (
    <div className="ns-app-wide">
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Tasks</h1>
          <p className="ns-page-sub">
            <b>{tasks.length}</b> {tasks.length === 1 ? "task" : "tasks"} ·
            CMO and specialists create work here as they delegate.
          </p>
        </div>
      </header>

      <TasksBoard projectSlug={project.slug} tasks={tasks} agents={agents} />
    </div>
  );
}
