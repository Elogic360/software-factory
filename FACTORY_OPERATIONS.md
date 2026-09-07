# ⚙️ Software Factory Operations Manual

## CLI Operational Commands
```bash
# Bootstrap any new software project
python3 factory.py init /path/to/project

# Run 15-subsystem health diagnostics
python3 factory.py doctor

# Inspect factory status & capability counts
python3 factory.py status

# Search and inspect warehouse capabilities
python3 factory.py warehouse --search "FastAPI"

# Context & Token optimization
python3 factory.py context --query "PostgreSQL connection pool" --budget 2000

# Central Memory operations
python3 factory.py memory remember --neuron Decision --topic "Auth" --content "Used OAuth2/JWT"
python3 factory.py memory route --query "How does auth work?"

# SDD & Quality Gates
python3 factory.py spec compile --title "TradingGateway"
python3 factory.py manufacture gates
python3 factory.py manufacture eval-gate --gate G7

# Observability & Reversible Deployment
python3 factory.py deploy health
python3 factory.py deploy rollback

# Continuous Self-Learning
python3 factory.py learn mine-failures
python3 factory.py learn mine-components
```
