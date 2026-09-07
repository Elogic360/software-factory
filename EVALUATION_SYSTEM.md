# Evaluation, Reliability & Benchmarking System

## Metrics Tracked
- **Success@1**: Single-attempt task completion rate.
- **Success@k**: Multi-attempt completion rate (with error recovery).
- **Reliability@k**: Ratio of successful trials over $k$ runs.
- **Token Efficiency**: Mean token expenditure per solved task.
- **Latency**: Mean wall-clock time per task.

## CLI Invocation
```bash
python3 factory.py evals --task "Refactor Auth Middleware" --agent "Antigravity"
```
