# Architecture Discovery Quick Start

**Time:** 15 minutes  
**Goal:** Understand your repository structure and generate first architecture map

---

## Step 1: Prerequisites (2 min)

```bash
# Check you have git
git --version
cd /path/to/your/project

# Install diagram tools (one-time)
# macOS
brew install plantuml graphviz mermaid-cli

# Linux (Ubuntu/Debian)
sudo apt install plantuml graphviz npm
npm install -g @mermaid-js/cli

# Windows (PowerShell)
choco install plantuml graphviz nodejs
npm install -g @mermaid-js/cli
```

---

## Step 2: Load Architecture Discovery (1 min)

### For Claude Code Users

```bash
cd /path/to/project
claude --load software-factory/ARCHITECTURE_DISCOVERY.md
```

### For All Other Agents

1. Navigate to `software-factory/`
2. Open `ARCHITECTURE_DISCOVERY.md`
3. Copy/paste into your agent
4. Activate the `architect-discovery` skill

---

## Step 3: Run Quick Discovery (5 min)

### Option A: Full Discovery (Recommended First Time)

```bash
claude /architect-discovery --full
```

**What happens:**
- Scans all source files
- Detects architecture patterns
- Generates C4 diagrams
- Creates documentation
- Outputs to `docs/architecture/`

**Expected output:**
```
✓ PHASE 1:  Repository scan → REPOSITORY_MAP.md
✓ PHASE 2:  Pattern detection → ARCHITECTURE_ANALYSIS.md
✓ PHASE 3:  DDD analysis → DDD_MODEL.md
✓ PHASE 4:  C4 diagrams → C4_CONTEXT.md, C4_CONTAINER.md, ...
✓ PHASE 5:  Dependency analysis → DEPENDENCY_ANALYSIS.md
✓ PHASE 6:  Data flows → DATA_FLOW.md
✓ PHASE 7:  Infrastructure → DEPLOYMENT.md
✓ PHASE 8:  Test coverage → TEST_COVERAGE.md
✓ PHASE 9:  Security → SECURITY.md
✓ PHASE 10: Performance → PERFORMANCE.md
✓ PHASE 11: ADRs → adr/ADR-*.md
✓ PHASE 12: Documentation created
✓ PHASE 13: Living mode ready

Documentation created in: docs/architecture/
```

### Option B: Quick Scan Only (5 minutes)

```bash
claude /architect-discovery --quick
```

**Generates:**
- `REPOSITORY_MAP.md` - Directory tree
- `ARCHITECTURE_ANALYSIS.md` - Detected patterns

---

## Step 4: Review Generated Documentation (5 min)

```bash
# Open directory
open docs/architecture/

# Or command-line browse
ls -la docs/architecture/
head -50 docs/architecture/REPOSITORY_MAP.md
head -50 docs/architecture/ARCHITECTURE_ANALYSIS.md
```

**Key files to review first:**

1. **REPOSITORY_MAP.md** → Understand folder structure
2. **ARCHITECTURE_ANALYSIS.md** → See detected patterns
3. **C4_CONTAINER.md** → Visualize your services
4. **DEPENDENCY_ANALYSIS.md** → Find violations

---

## Step 5: Set Up Living Architecture (2 min)

Enable automatic updates when code changes:

```bash
claude /architect-discovery --watch . --interval 60
```

**This will:**
- Watch for file changes
- Re-scan changed areas every 60 seconds
- Update diagrams automatically
- Flag new violations

Or set it up permanently in your CI/CD:

```yaml
# .github/workflows/architecture.yml
name: Architecture Discovery

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Architecture Discovery
        run: |
          claude /architect-discovery --full --output docs/architecture/
      - name: Commit documentation
        run: |
          git add docs/architecture/
          git commit -m "chore: update architecture documentation"
          git push
```

---

## Step 6: Integrate with Your Team

```bash
# 1. Commit generated docs
git add docs/architecture/
git commit -m "docs: initial architecture discovery"
git push

# 2. Share with team
# Send link to docs/architecture/ARCHITECTURE_ANALYSIS.md
# Share C4 diagrams in Confluence/Notion

# 3. Use in onboarding
# New team members read docs/architecture/REPOSITORY_MAP.md first
```

---

## Common Commands

```bash
# Full discovery
claude /architect-discovery --full

# Quick scan only
claude /architect-discovery --quick

# Generate only C4 diagrams
claude /architect-discovery --generate-c4

# Generate only UML
claude /architect-discovery --generate-uml

# Generate only ADRs
claude /architect-discovery --generate-adr

# Watch mode (continuous updates)
claude /architect-discovery --watch . --interval 60

# Dry run (no file creation)
claude /architect-discovery --dry-run

# Verbose output
claude /architect-discovery --full --verbose

# Focus on specific areas
claude /architect-discovery --focus ddd      # DDD analysis only
claude /architect-discovery --focus security # Security review
claude /architect-discovery --focus perf     # Performance analysis

# Validate existing docs
claude /architect-discovery --validate
```

---

## Expected Output Structure

After running discovery, you'll have:

```
docs/architecture/
├── REPOSITORY_MAP.md              ← Start here: full directory tree
├── ARCHITECTURE_ANALYSIS.md       ← Detected patterns & confidence
├── DDD_MODEL.md                   ← Bounded contexts & aggregates
├── C4_CONTEXT.md                  ← Level 1: System boundaries
├── C4_CONTAINER.md                ← Level 2: Services & databases
├── C4_COMPONENT.md                ← Level 3: Internal structure
├── C4_CODE.md                      ← Level 4: UML class diagrams
├── DEPENDENCY_ANALYSIS.md         ← Coupling, violations, cycles
├── DATA_FLOW.md                   ← Request sequences
├── DEPLOYMENT.md                  ← Infrastructure & K8s
├── TEST_COVERAGE.md               ← Coverage gaps
├── SECURITY.md                    ← Auth, encryption, RBAC
├── PERFORMANCE.md                 ← Hotspots, optimization
├── VIOLATIONS.md                  ← Critical issues to fix
├── adr/
│   ├── ADR-001-architecture-choice.md
│   ├── ADR-002-technology-stack.md
│   └── ...
└── diagrams/
    ├── c4-context.puml            ← PlantUML (edit in IDE)
    ├── c4-context.mmd             ← Mermaid (render in markdown)
    ├── c4-container.puml
    ├── c4-component.puml
    ├── uml-order.puml
    ├── sequence-order.puml
    └── dependency-graph.mmd
```

---

## Integration with Different Agents

### Using Claude Code

```bash
# 1. Open project folder in terminal
cd /path/to/project

# 2. Load architecture prompt
claude --load software-factory/ARCHITECTURE_DISCOVERY.md

# 3. Run discovery
claude /architect-discovery --full

# 4. Watch mode
claude /architect-discovery --watch .
```

### Using Copilot (VSCode)

```
1. Open command palette: Cmd+Shift+P
2. Type: "Copilot: Chat" or #copilot
3. Paste: /architecture-discovery --full
4. Or: #copilot analyze this project structure
```

### Using Cursor

```
1. Open project in Cursor
2. Create file: .cursor/discover.md
3. Paste: software-factory/ARCHITECTURE_DISCOVERY.md
4. Run: /architect-discovery --full
```

### Using Gemini (Colab)

```python
# In Colab notebook
import sys
sys.path.append('/path/to/software-factory/scripts')
from discovery import ArchitectureDiscovery

arch = ArchitectureDiscovery('/path/to/project')
arch.scan()
arch.generate_c4()
arch.generate_reports()
```

---

## Troubleshooting

### "Module not found" or "Command not found"

**Fix:** Ensure you're in the project root and have .git directory

```bash
cd /path/to/project
ls -la .git
```

### "PlantUML not installed"

**Fix:** Install it

```bash
# macOS
brew install plantuml

# Ubuntu
sudo apt install plantuml

# Or use online renderer: plantuml.com
```

### "No architecture detected"

**Fix:** Ensure project has recognizable structure (src/, app/, lib/, etc.)

```bash
ls -la
# Should see: src/, app/, lib/, or similar
```

### "Memory not persisting"

**Fix:** Make sure `.specify/memory/` is not in `.gitignore`

```bash
cat .gitignore | grep specify
# Should be empty or commented out

# Or commit to git
git add .specify/
git commit -m "chore: architecture memory"
```

### "Agent can't find ARCHITECTURE_DISCOVERY.md"

**Fix:** Use absolute path or ensure you're in repo root

```bash
# Absolute path
claude --load /full/path/to/software-factory/ARCHITECTURE_DISCOVERY.md

# Or relative
cd /path/to/software-factory
claude --load ARCHITECTURE_DISCOVERY.md
```

---

## Next Steps

1. ✓ **Day 1:** Run quick scan, review REPOSITORY_MAP.md
2. ✓ **Day 2:** Run full discovery, share C4 diagrams with team
3. ✓ **Day 3:** Set up living mode, integrate into CI/CD
4. ✓ **Week 1:** Use discovery for onboarding new team members
5. ✓ **Ongoing:** Keep architecture docs in sync with code

---

## Tips for Success

✅ **Do:** Run discovery after major changes  
✅ **Do:** Commit `docs/architecture/` to git  
✅ **Do:** Review diagrams with your team  
✅ **Do:** Update ADRs when you make decisions  

❌ **Don't:** Ignore violations without creating ADRs  
❌ **Don't:** Let documentation get stale (> 1 sprint)  
❌ **Don't:** Skip Phase 13 (living mode setup)  

---

## Need Help?

- **Full documentation:** `ARCHITECTURE_DISCOVERY.md`
- **Multi-agent setup:** `AGENT_INTEGRATION.md`
- **Memory system:** `MEMORY_ARCHITECTURE.md`
- **Examples:** `software-factory/skills/architect-discovery/examples/`
- **Troubleshooting:** Search ARCHITECTURE_DISCOVERY.md for your issue

---

**Ready to discover your architecture?**

```bash
cd /path/to/project
claude /architect-discovery --full
```

This will generate a complete architectural map of your system in 10-15 minutes. ✨

