import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import { getMcpCatalog } from "@/server/mcp-catalog";
import { getMcpStatus } from "@/server/mcp/state";
import { summarizeBuiltinTools } from "@/server/mcp-server/tool-summaries";
import { McpCard } from "@/components/mcp-card";
import { BuiltinMcpCard } from "@/components/builtin-mcp-card";
import { McpFlashBanner } from "@/components/mcp-flash-banner";
import { AddMcpServerMenu } from "@/components/add-mcp-server-card";
import { normalizeResourceUrl } from "@/server/mcp/discovery-url";

type Search = { mcp_connected?: string; mcp_error?: string };

export default async function ConnectionsPage({
  searchParams,
  params,
}: {
  searchParams: Promise<Search>;
  params: Promise<{ project: string }>;
}) {
  const { project: slug } = await params;
  const project = getProject(slug);
  const { mcp_connected, mcp_error } = await searchParams;
  if (!project || project.archived_at) notFound();

  const catalog = getMcpCatalog(project.slug);
  const statuses = await Promise.all(
    catalog.map((s) => getMcpStatus(project.slug, s.key)),
  );

  const builtinTools = summarizeBuiltinTools();
  const connectedCount = statuses.filter((s) => s.state === "connected").length;
  const connectedSpecs = catalog.filter(
    (_, i) => statuses[i].state === "connected",
  );
  const connectedKeys = connectedSpecs.map((s) => s.key);
  const connectedResourceUrls = connectedSpecs.map((s) =>
    normalizeResourceUrl(s.resource_url),
  );

  return (
    <div className="ns-app-narrow">
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Connections</h1>
          <p className="ns-page-sub">
            MCP servers are the tools your agents call. Browse the curated list
            or paste any <b>OAuth&nbsp;2.0</b> URL.
          </p>
        </div>
        <div className="ns-page-actions">
          <AddMcpServerMenu
            connectedKeys={connectedKeys}
            connectedResourceUrls={connectedResourceUrls}
          />
        </div>
      </header>

      <McpFlashBanner connected={mcp_connected} error={mcp_error} />

      <section>
        <h2 className="ns-h2">
          <span>Built-in</span>
          <span className="ns-h2-meta">Ships with notfair-cmo</span>
        </h2>
        <div className="ns-group">
          <BuiltinMcpCard
            name="Orchestration"
            description="Built-in tools your agents use to coordinate: assign tasks, request approvals, write PROJECT.md, comment, and report status."
            tools={builtinTools}
          />
        </div>
      </section>

      <section>
        <h2 className="ns-h2">
          <span>Servers</span>
          <span className="ns-h2-meta">
            {catalog.length === 0
              ? "None yet"
              : `${connectedCount} of ${catalog.length} connected`}
          </span>
        </h2>
        {catalog.length === 0 ? (
          <div className="ns-empty">
            <p className="ns-empty-title">No MCP servers yet.</p>
            <p className="ns-empty-sub">
              Use <span className="font-medium text-foreground">Add server</span>{" "}
              above to browse trusted connectors or paste a URL.
            </p>
          </div>
        ) : (
          <ol className="ns-group">
            {catalog.map((spec, i) => (
              <li key={spec.key}>
                <McpCard spec={spec} status={statuses[i]} />
              </li>
            ))}
          </ol>
        )}
      </section>
    </div>
  );
}
