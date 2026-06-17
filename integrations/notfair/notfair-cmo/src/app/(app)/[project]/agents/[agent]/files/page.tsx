import Link from "next/link";
import { notFound } from "next/navigation";
import { FileText, FileX } from "lucide-react";
import { getProject } from "@/server/db/projects";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { listAgentFiles, getAgentFile } from "@/server/agents/files";
import { cn } from "@/lib/utils";
import { projectHref } from "@/lib/project-href";

type AugmentedFile = Awaited<ReturnType<typeof listAgentFiles>>["files"][number];

type Params = { agent: string; project: string };
type Search = { file?: string };

export default async function AgentFilesPage({
  params,
  searchParams,
}: {
  params: Promise<Params>;
  searchParams: Promise<Search>;
}) {
  const { agent: agentSlug, project: projectSlug } = await params;
  const { file: requestedFile } = await searchParams;

  const project = getProject(projectSlug);
  if (!project || project.archived_at) notFound();

  const resolved = await resolveAgentBySlug(project.slug, agentSlug);
  if (!resolved) notFound();
  const agentFullId = resolved.agent_id;

  let error: string | null = null;
  let files: AugmentedFile[] = [];
  let workspace = "";
  try {
    const list = await listAgentFiles(agentFullId);
    files = list.files;
    workspace = list.workspace;
  } catch (err) {
    error = err instanceof Error ? err.message : String(err);
  }

  const identityIdx = files.findIndex((f) => f.name === "IDENTITY.md");
  const projectIdx = files.findIndex((f) => f.name === "PROJECT.md");
  if (identityIdx >= 0 && projectIdx >= 0 && projectIdx !== identityIdx + 1) {
    const projectFile = files[projectIdx]!;
    const without = files.filter((_, i) => i !== projectIdx);
    const insertAt = without.findIndex((f) => f.name === "IDENTITY.md") + 1;
    files = [...without.slice(0, insertAt), projectFile, ...without.slice(insertAt)];
  }

  const selectedName =
    (requestedFile && files.find((f) => f.name === requestedFile)?.name) ||
    files.find((f) => !f.missing)?.name ||
    files[0]?.name;

  let selectedContent: string | null = null;
  let selectedSize: number | undefined;
  let selectedUpdatedAtMs: number | undefined;
  let selectedMissing = false;
  let selectedError: string | null = null;
  if (selectedName) {
    const entry = files.find((f) => f.name === selectedName);
    selectedMissing = entry?.missing ?? true;
    if (!selectedMissing) {
      try {
        const got = await getAgentFile(agentFullId, selectedName);
        selectedContent = got.file.content;
        selectedSize = got.file.size;
        selectedUpdatedAtMs = got.file.updatedAtMs;
      } catch (err) {
        selectedError = err instanceof Error ? err.message : String(err);
      }
    }
  }

  return (
    <div className="grid h-full grid-cols-[260px_minmax(0,1fr)] divide-x divide-border bg-background">
      {/* Left rail — file list */}
      <aside className="flex min-h-0 flex-col bg-[hsl(0_0%_99%)]">
        <div className="border-b border-border/60 px-4 py-3">
          <div className="text-[11px] font-semibold uppercase tracking-wide text-[hsl(var(--notfair-ink-4))]">
            Workspace files
          </div>
          {workspace && (
            <div className="mt-1 truncate font-mono text-[10px] text-[hsl(var(--notfair-ink-4))]">
              {workspace}
            </div>
          )}
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto py-2">
          {error && (
            <div className="px-4 py-3 text-xs text-destructive">{error}</div>
          )}
          {!error && files.length === 0 && (
            <div className="px-4 py-3 text-xs text-[hsl(var(--notfair-ink-4))]">
              No files yet.
            </div>
          )}
          {files.map((f) => {
            const isActive = f.name === selectedName;
            return (
              <Link
                key={f.name}
                href={projectHref(
                  projectSlug,
                  `/agents/${agentSlug}/files?file=${encodeURIComponent(f.name)}`,
                )}
                className={cn(
                  "mx-2 flex items-center gap-2 rounded-md px-2 py-1.5 text-[13px] transition-colors",
                  isActive
                    ? "bg-[hsl(var(--notfair-accent-soft))] text-[hsl(var(--notfair-accent))]"
                    : "text-[hsl(var(--notfair-ink-3))] hover:bg-[hsl(var(--notfair-surface-2))] hover:text-[hsl(var(--notfair-ink))]",
                  f.missing && !isActive && "opacity-60",
                )}
              >
                {f.missing ? (
                  <FileX className="size-3.5 shrink-0 opacity-70" />
                ) : (
                  <FileText className="size-3.5 shrink-0" />
                )}
                <span className="truncate font-mono">{f.name}</span>
                {f.missing && (
                  <span className="ml-auto rounded-[4px] bg-[hsl(var(--notfair-surface-2))] px-1 py-px text-[9px] font-medium uppercase tracking-wide text-[hsl(var(--notfair-ink-4))]">
                    empty
                  </span>
                )}
              </Link>
            );
          })}
        </div>
      </aside>

      {/* Right pane — file viewer */}
      <section className="flex min-h-0 flex-col bg-background">
        {!selectedName ? (
          <div className="flex h-full items-center justify-center p-6 text-sm text-[hsl(var(--notfair-ink-4))]">
            Select a file to view its contents.
          </div>
        ) : selectedMissing ? (
          <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
            <FileX className="size-7 text-[hsl(var(--notfair-ink-4))] opacity-60" />
            <div className="text-[14px] font-medium text-[hsl(var(--notfair-ink-2))]">
              <span className="font-mono">{selectedName}</span> doesn&rsquo;t exist
              yet.
            </div>
            <div className="text-[12.5px] text-[hsl(var(--notfair-ink-4))]">
              The agent may create it during onboarding or when first invoked.
            </div>
          </div>
        ) : selectedError ? (
          <div className="p-6 text-sm text-destructive">{selectedError}</div>
        ) : (
          <>
            <header className="flex items-center justify-between border-b border-border/60 px-6 py-3">
              <div className="min-w-0">
                <div className="truncate font-mono text-[13.5px] text-[hsl(var(--notfair-ink))]">
                  {selectedName}
                </div>
                <div className="mt-0.5 text-[11px] text-[hsl(var(--notfair-ink-4))]">
                  {selectedSize !== undefined && `${formatBytes(selectedSize)}`}
                  {selectedSize !== undefined && selectedUpdatedAtMs && " · "}
                  {selectedUpdatedAtMs &&
                    `updated ${new Date(selectedUpdatedAtMs).toLocaleString()}`}
                </div>
              </div>
            </header>
            <div className="min-h-0 flex-1 overflow-y-auto">
              <pre className="whitespace-pre-wrap break-words p-6 font-mono text-[13px] leading-relaxed text-[hsl(var(--notfair-ink-2))]">
                {selectedContent}
              </pre>
            </div>
          </>
        )}
      </section>
    </div>
  );
}

function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(2)} MB`;
}
