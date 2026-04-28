# API Compatibility Auto-Fix Pipeline

A multi-agent workflow that automatically migrates broken API calls across multiple microservice repositories after a breaking dependency upgrade.

## Problem

Our team maintains 8 microservices depending on a shared internal `CoreLib`. After an unannounced breaking upgrade (v1 → v2), all callers broke — compilation errors, runtime exceptions, a sea of red. Manual fix would take 3 people × 5 days, with risk of missing edge cases.

## Solution

A 5-agent automated migration pipeline that scans, plans, fixes, verifies, and generates PRs — reducing 15 person-days of work to ~6 hours (~85% time saved).

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Scanner  │───▶ Planner  │───▶ Modifier │───▶ Verifier │───▶  PR Gen  │
│  Agent    │    │  Agent    │    │  Agent    │    │  Agent    │    │  Agent    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
AST Scan     Strategy Plan   Auto Patch     Compile Test    Create PRs
76 calls     Priority +     Per-file       + Auto Rollback  + @Owners
8 services   Confidence     Gradual
```

## Quick Start

```bash
# Run the full pipeline
python pipeline/run_pipeline.py

# Reset all services to v1 state (for fresh re-run)
bash reset_services.sh
```

## Architecture

### 5-Agent Pipeline

| Agent | Responsibility | Key Output |
|-------|---------------|------------|
| **Scanner** | AST-based v1 API discovery across all repos | Hit list with 76 call sites |
| **Planner** | Match migration rules, assign priority & confidence | Fix plan per call site |
| **Modifier** | Apply regex patches file-by-file | 75 auto-fixed, 1 TODO |
| **Verifier** | Syntax check + simulated unit tests | 7/8 services passed |
| **PR Gen** | Generate PRs per repo with code owner notification | 7 PRs created |

### Migration Strategy

The pipeline uses 18 v1→v2 mapping rules across 5 modules:

| Module | Calls | Strategies |
|--------|-------|------------|
| `auth` | 12 | Swap args, keyword params, sub-module move |
| `data` | 18 | Builder pattern, param rename |
| `messaging` | 10 | Struct wrapping, param rename |
| `config` | 18 | Enum key conversion, function rename |
| `logging` | 18 | Object-based logger |

Difficulty distribution: **59 simple**, **16 medium**, **1 complex**

### Gradual Migration Pattern

```python
# Before (v1)
from corelib import auth

user = auth.authenticate(token, secret)

# After (v2) — import preserved for backward compat
from corelib_v2 import auth

user = auth.login(secret, token, scope="default")
```

Complex cases (like raw SQL → query builder) are marked `TODO` instead of blind replacement.

## Project Structure

```
├── core-lib-v1/               # Old CoreLib (pre-breaking-change)
│   └── corelib.py
├── core-lib-v2/               # New CoreLib (breaking upgrade)
│   └── corelib_v2.py
├── migration-guide/           # v1→v2 mapping rules
│   └── mapping.md
├── services/                  # 8 microservice repos
│   ├── analytics-service/
│   ├── gateway-service/
│   ├── message-service/
│   ├── notification-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── search-service/
│   └── user-service/
├── pipeline/
│   ├── run_pipeline.py        # 5-agent orchestration
│   └── patches/               # Generated patch files
└── reset_services.sh          # Reset to v1 for re-run
```

## Results

| Metric | Value |
|--------|-------|
| Repositories scanned | 8 |
| API calls discovered | 76 |
| Auto-fixed | 75 (99%) |
| Manual review needed | 1 |
| Services passed | 7/8 |
| PRs created | 7 |
| Time saved | ~85% |
