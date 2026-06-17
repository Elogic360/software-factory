import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { ProjectCookieSync } from "@/components/project-cookie-sync";

/**
 * Validates that the URL's project slug actually exists. Live-syncing the
 * cookie used by `getActiveProject()` (which the sidebar + API routes still
 * read) is handled by a thin client component so we can stay inside server
 * render. The actual sidebar / chrome is mounted by the parent `(app)/layout`.
 */
export default async function ProjectScopedLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  if (!project || project.archived_at) {
    notFound();
  }
  return (
    <>
      <ProjectCookieSync slug={slug} />
      {children}
    </>
  );
}
