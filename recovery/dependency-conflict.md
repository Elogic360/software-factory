# Recovery Playbook: Dependency Conflict

## Diagnosis Tree

```
Dependency conflict?
  │
  ├── Python pip conflict
  │     ├── "ERROR: Cannot install X because Y requires Z>=A but W requires Z<=B"
  │     │     → pip install pip-tools
  │     │     → pip-compile requirements.in  (generate locked requirements.txt)
  │     │     → OR: relax the conflicting constraint if safe
  │     │
  │     ├── "ImportError: cannot import name X from Y"
  │     │     → Package updated and removed/renamed X
  │     │     → pip show <package> to see installed version
  │     │     → Check changelog of the package for breaking changes
  │     │     → Pin to last working version: package==X.Y.Z in requirements.txt
  │     │
  │     └── Conflict introduced by new package
  │           → pip install <new-package> --dry-run
  │           → Shows what would be installed/changed before committing
  │
  ├── Node.js / pnpm conflict
  │     ├── "WARN Issues with peer dependencies found"
  │     │     → Usually safe to ignore for non-breaking peer deps
  │     │     → pnpm install --strict-peer-dependencies=false if needed
  │     │
  │     ├── "Cannot find module X"
  │     │     → pnpm install (re-install after package.json change)
  │     │     → Check if package is in dependencies vs devDependencies
  │     │
  │     └── Type errors after updating a package
  │           → @types/<package> may need separate update
  │           → pnpm add -D @types/<package>@latest
  │
  └── Version constraint strategy
        → Python: pin ALL versions in requirements.txt (pip freeze)
        → Node: pnpm uses lockfile (pnpm-lock.yaml) — commit it
        → Never commit: venv/, node_modules/, __pycache__/
```

---

## Python Dependency Management

```bash
# Add new dependency correctly:
cd integral-expert-backend && source venv/bin/activate
pip install <package>              # install
pip freeze > requirements.txt      # lock all versions
git add requirements.txt           # commit the lock

# Check what a package depends on:
pip show <package>

# Find what's using a conflicting package:
pip-tree | grep <package>          # install: pip install pipdeptree

# Audit for security vulnerabilities:
pip install safety
safety check -r requirements.txt
```

---

## Node.js Dependency Management

```bash
# Add new dependency:
cd app
pnpm add <package>                  # production dependency
pnpm add -D <package>              # dev dependency
git add package.json pnpm-lock.yaml # commit both

# Update a specific package:
pnpm update <package>

# Audit for vulnerabilities:
pnpm audit

# Check why a package is installed:
pnpm why <package>
```

---

## Version Pinning Strategy

```
Python:
  - Pin ALL packages in requirements.txt (pip freeze output)
  - Use requirements.in for human-readable constraints
  - requirements.txt is the lockfile — never edit manually

Node:
  - pnpm-lock.yaml is the lockfile — always commit it
  - package.json uses ^ for minor updates (e.g., ^18.0.0)
  - Lock exact version for: React, TypeScript, critical UI libraries
  - Renovate/Dependabot for automated update PRs

Rule: "If it works, pin it. If you upgrade, test everything."
```
