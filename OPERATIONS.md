# Operations

Execution Loop
1. Load the spec, plan, and tasks for the feature.
2. Validate scope against the constitution.
3. Execute tasks in order, validating after each user story.
4. Update docs and Graphify index after large changes.

Validation
- Unit and integration tests where required.
- API contract verification for public endpoints.
- UI checks for frontend changes.

Recovery
- Use playbooks in .claude/recovery/.
- Log failures, apply fixes, and re-run validation.
