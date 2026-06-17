# Graphify Integration

Graphify is the semantic memory engine for the Software Factory. Use it before cross-domain changes.

Required Usage
- Query Graphify before refactors that affect multiple modules.
- Use Graphify to identify dependencies and call graphs.

Suggested Commands
- graphify watch .
- graphify build .

Recommended Queries
- Components to pages
- API routes to services
- Models to migrations
- Event flow dependencies

Update Cadence
- Run graphify build after major refactors.
- Keep graphify watch running during large implementation phases.

Automated Cadence (self-updating)
- `scripts/update_skills.py` runs automatically via the git `post-commit` hook
  (install once with `bash software-factory/scripts/install_hooks.sh`).
- After every commit it: (1) detects + documents changes via
  `context-engine/change_detector.py` into `memory/`, (2) maps changed domains to
  the owning skills and rewrites the AUTO-SYNC block in `SKILLS_REGISTRY.md`,
  (3) best-effort refreshes the knowledge graph into `software-factory/graphify/`.
- Manual full graph rebuild: `graphify . --update` (or `/graphify .`).
- Run `python3 software-factory/scripts/update_skills.py --seed` to re-seed from scratch.
