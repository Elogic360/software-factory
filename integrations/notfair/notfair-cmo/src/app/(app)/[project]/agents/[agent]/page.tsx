import { redirect } from "next/navigation";
import { projectHref } from "@/lib/project-href";

export default async function AgentIndexPage({
  params,
}: {
  params: Promise<{ agent: string; project: string }>;
}) {
  const { agent, project } = await params;
  redirect(projectHref(project, `/agents/${agent}/chat`));
}
