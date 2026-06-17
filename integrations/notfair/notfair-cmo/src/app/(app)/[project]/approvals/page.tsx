import Link from "next/link";
import { notFound } from "next/navigation";
import { getProject } from "@/server/db/projects";
import {
  listActionableApprovals,
  listPolicies,
  listResolvedApprovals,
} from "@/server/db/approvals";
import { ApprovalCard } from "@/components/approval-card";
import { PolicyList } from "@/components/policy-list";
import { projectHref } from "@/lib/project-href";

type TabKey = "pending" | "resolved" | "policies";

function parseTab(raw: string | string[] | undefined): TabKey {
  const value = Array.isArray(raw) ? raw[0] : raw;
  if (value === "resolved" || value === "policies") return value;
  return "pending";
}

export default async function ApprovalsPage({
  params,
  searchParams,
}: {
  params: Promise<{ project: string }>;
  searchParams: Promise<{ tab?: string | string[] }>;
}) {
  const { project: slug } = await params;
  const { tab } = await searchParams;
  const activeTab = parseTab(tab);

  const project = getProject(slug);
  if (!project || project.archived_at) notFound();

  const actionable = listActionableApprovals(project.slug);
  const resolved =
    activeTab === "resolved" ? listResolvedApprovals(project.slug, 50) : [];
  const policies = activeTab === "policies" ? listPolicies(project.slug) : [];

  const counts = {
    pending: actionable.length,
    resolved: resolved.length,
    policies: policies.length,
  };

  return (
    <div className="ns-app-narrow">
      <header className="ns-page-head">
        <div className="ns-page-head-stack">
          <h1 className="ns-page-title">Approvals</h1>
          <p className="ns-page-sub">
            Your inbox for agent decisions. Anything not already covered by an
            <b> auto-approve rule</b> lands here for a quick yes or no.
          </p>
        </div>
      </header>

      <nav
        className="ns-tabs mb-6"
        role="tablist"
        aria-label="Approval tabs"
      >
        <TabLink
          slug={slug}
          tab="pending"
          active={activeTab}
          label="Inbox"
          count={counts.pending}
        />
        <TabLink
          slug={slug}
          tab="resolved"
          active={activeTab}
          label="Resolved"
        />
        <TabLink
          slug={slug}
          tab="policies"
          active={activeTab}
          label="Auto-approve rules"
        />
      </nav>

      {activeTab === "pending" &&
        (actionable.length === 0 ? (
          <div className="ns-empty">
            <p className="ns-empty-title">All caught up.</p>
            <p className="ns-empty-sub">
              When an agent needs your go-ahead, it&rsquo;ll show up here.
              Manage rules in{" "}
              <Link
                href={`${projectHref(slug, "/approvals")}?tab=policies`}
                className="ns-link"
              >
                Auto-approve rules
              </Link>
              .
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {actionable.map((a) => (
              <ApprovalCard key={a.id} approval={a} />
            ))}
          </div>
        ))}

      {activeTab === "resolved" &&
        (resolved.length === 0 ? (
          <div className="ns-empty">
            <p className="ns-empty-title">No resolved approvals yet.</p>
            <p className="ns-empty-sub">
              Decisions show up here after they&rsquo;re approved, rejected, or
              auto-handled.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {resolved.map((a) => (
              <ApprovalCard key={a.id} approval={a} />
            ))}
          </div>
        ))}

      {activeTab === "policies" && (
        <PolicyList projectSlug={project.slug} policies={policies} />
      )}
    </div>
  );
}

function TabLink({
  slug,
  tab,
  active,
  label,
  count,
}: {
  slug: string;
  tab: TabKey;
  active: TabKey;
  label: string;
  count?: number;
}) {
  const isActive = active === tab;
  const href =
    tab === "pending"
      ? projectHref(slug, "/approvals")
      : `${projectHref(slug, "/approvals")}?tab=${tab}`;
  return (
    <Link
      href={href}
      role="tab"
      aria-selected={isActive}
      className="ns-tab"
      data-active={isActive}
    >
      {label}
      {count !== undefined && count > 0 && (
        <span
          className={`ml-1 inline-flex h-[16px] min-w-[16px] items-center justify-center rounded-full px-1 text-[10px] font-semibold tabular-nums leading-none ${
            isActive
              ? "bg-[hsl(var(--notfair-ink))] text-white"
              : "bg-[hsl(var(--notfair-surface-2))] text-[hsl(var(--notfair-ink-3))]"
          }`}
        >
          {count}
        </span>
      )}
    </Link>
  );
}
