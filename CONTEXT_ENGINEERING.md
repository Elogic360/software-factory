# Context Engineering

Purpose
- Provide a minimal, accurate context window for large-scale changes.
- Prevent stale assumptions by using Graphify and canonical docs.

Context Sources (priority order)
1. specs/<feature>/spec.md, plan.md, tasks.md
2. .specify/memory/constitution.md
3. software-factory/GRAPHIFY.md and graphify outputs
4. module-level READMEs or architecture docs

Compression Rules
- Summarize only the relevant domains for the current task.
- Do not copy entire file trees into prompts.
- Use stable identifiers for requirements and tasks.

Retrieval Checklist
- Identify affected modules and contracts.
- Pull API, data-model, and event-flow facts only.
- Confirm current structure from the repository, not memory.

Outputs
- A short change brief with scope, risks, and validation plan.
- A dependency map limited to the impacted domains.
