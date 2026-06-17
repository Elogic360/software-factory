import { NextResponse } from "next/server";
import { getActiveProject } from "@/server/active-project";
import { resolveAgentBySlug } from "@/server/agent-meta";
import { getProject } from "@/server/db/projects";
import {
  readTranscriptTail,
  resolveSessionForThread,
} from "@/server/sessions/transcript-tail";
import { subscribeSessionEvents } from "@/server/live-events/emitter";
import type { TranscriptEvent as RawTranscriptEvent } from "@/server/sessions";
import { readTranscriptTail as tailFromCursor } from "@/server/sessions/transcript-tail";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

const DEBUG = process.env.NOTFAIR_LIVE_BRIDGE_DEBUG !== "0";
function log(...args: unknown[]): void {
  if (DEBUG) console.log("[live-bridge]", ...args);
}

/**
 * SSE bridge that streams a session's transcript live.
 *
 * Mechanism (paperclip-style pub/sub):
 *   1. Resolve the session row from (project_slug, agent_id, label).
 *   2. Backfill events the client hasn't seen yet by reading
 *      `transcript_events` from `?cursor=` (default 0) forward.
 *   3. Subscribe to the in-process emitter for this session_id. From this
 *      point, every `appendTranscriptEvent` call fires this listener and
 *      we forward the event to the client in milliseconds — no polling.
 *
 * Reattach safety: the backfill + subscribe pair brackets the gap between
 * page render and SSE connect. Any event written during that window lands
 * in the backfill or in the live stream; the client filters by `seq` so
 * an event that crosses the boundary is deduped.
 */
export async function GET(
  request: Request,
  { params }: { params: Promise<{ agent: string; thread: string }> },
): Promise<Response> {
  const { agent: agentSlug, thread: threadId } = await params;

  const url = new URL(request.url);
  const projectSlug = url.searchParams.get("project");
  const projectRow = projectSlug ? getProject(projectSlug) : await getActiveProject();
  if (!projectRow || projectRow.archived_at) {
    return NextResponse.json({ error: "Unknown project" }, { status: 404 });
  }
  const resolved = await resolveAgentBySlug(projectRow.slug, agentSlug);
  if (!resolved) {
    return NextResponse.json({ error: "Unknown agent" }, { status: 404 });
  }
  const agentFullId = resolved.agent_id;
  const cursorParam = url.searchParams.get("cursor");
  const startCursor = cursorParam ? Math.max(0, Number(cursorParam)) : 0;

  // Resolve the underlying notfair-cmo session row so we can subscribe on
  // its id (the EventEmitter key). A pending thread that hasn't received
  // any turn yet has no row — we still hold the SSE open and rely on the
  // subscribe-on-create branch below (the first turn creates the row and
  // pushes the first event, which we'd miss). To handle that case, we
  // also poll-fallback for the row every 1s while it's missing.
  let session = resolveSessionForThread(projectRow.slug, agentFullId, threadId);

  const encoder = new TextEncoder();

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      let closed = false;
      let unsubscribe: (() => void) | null = null;
      let bufferedDuringBackfill: RawTranscriptEvent[] | null = [];
      let lastSeqEmitted = startCursor;
      let pendingProbe: ReturnType<typeof setInterval> | null = null;

      function send(event: string, data: unknown): void {
        if (closed) return;
        try {
          controller.enqueue(
            encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`),
          );
        } catch {
          // torn down
        }
      }

      function teardown(): void {
        if (closed) return;
        closed = true;
        if (pendingProbe) clearInterval(pendingProbe);
        if (unsubscribe) {
          unsubscribe();
          unsubscribe = null;
        }
        try {
          controller.close();
        } catch {
          // already closed
        }
      }

      request.signal.addEventListener("abort", teardown);

      /**
       * Convert a single transcript_events row into the UI event shape and
       * forward over SSE. Dedupes by seq so events delivered both via
       * backfill and live stream don't render twice.
       */
      function forwardRow(row: RawTranscriptEvent): void {
        if (row.seq <= lastSeqEmitted) return;
        lastSeqEmitted = row.seq;
        // Reuse readTranscriptTail's mapping to keep the UI shape in one
        // place; it accepts a cursor strictly less than the row's seq.
        const { events } = tailFromCursor(
          projectRow!.slug,
          agentFullId,
          threadId,
          row.seq - 1,
        );
        if (events.length > 0) {
          send("transcript", { events });
        }
      }

      function liveListener(row: RawTranscriptEvent): void {
        if (closed) return;
        if (bufferedDuringBackfill) {
          // Backfill is still draining — queue and replay after it finishes
          // to preserve order and let dedup-by-seq do its job.
          bufferedDuringBackfill.push(row);
          return;
        }
        forwardRow(row);
      }

      function attachSubscription(sessionId: string): void {
        unsubscribe = subscribeSessionEvents(sessionId, liveListener);
      }

      function backfill(): void {
        if (closed) return;
        const { events, byteOffset } = readTranscriptTail(
          projectRow!.slug,
          agentFullId,
          threadId,
          lastSeqEmitted,
        );
        if (events.length > 0) {
          lastSeqEmitted = byteOffset;
          send("transcript", { events });
        }
        // Drain anything that arrived while we were reading the DB.
        const buf = bufferedDuringBackfill ?? [];
        bufferedDuringBackfill = null;
        for (const row of buf) forwardRow(row);
      }

      send("ready", { thread: threadId, cursor: startCursor });

      if (session) {
        // Standard path: row exists. Subscribe FIRST so events written
        // during the backfill land in the buffer, then read the DB.
        attachSubscription(session.id);
        backfill();
      } else {
        // Pending thread with no first turn yet. Poll-fallback for the row
        // every 1s. When it appears, attach and backfill. Keep the SSE
        // open meanwhile so the client doesn't reconnect uselessly.
        log("waiting for session row", { threadId });
        pendingProbe = setInterval(() => {
          if (closed) return;
          session = resolveSessionForThread(projectRow!.slug, agentFullId, threadId);
          if (session) {
            clearInterval(pendingProbe!);
            pendingProbe = null;
            attachSubscription(session.id);
            backfill();
          }
        }, 1000);
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
    },
  });
}
