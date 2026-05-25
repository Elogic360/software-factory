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
