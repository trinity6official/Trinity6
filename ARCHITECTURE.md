# Trinity6 — Architecture & Roadmap
> Last updated: February 2026

---

## Repository Structure

### Trinity6 Repo (Private — Your Core IP)
This is your engine. The actual scanning intelligence.
Nobody sees this code. This is what you own.

```
Trinity6/
  compliance/
    cis/
      linux/       - Linux CIS check definitions (exists)
      windows/     - Windows CIS checks (Phase 3)
      docker/      - Docker CIS checks (Phase 2)
      aws/         - AWS CIS checks (Phase 3)
  engine/          - Scanner engine core (exists)
  scanner/         - Main scanner logic (exists)
  reports/         - PDF and HTML generation (exists)
  dashboard/       - Internal admin dashboard (exists)
  cli/             - Command line interface (exists)
  agent/           - Agent wrapper (build Phase 1)
```

### trinity6-platform Repo (Private — Your Product)
This is your delivery layer. What clients interact with.

```
trinity6-platform/
  backend/
    api.py              - Central Flask API (done)
  dashboard/
    index.html          - Client web dashboard (done)
  agents/
    linux_agent.py      - Linux thin wrapper (Phase 1)
    windows_agent.ps1   - Windows thin wrapper (Phase 3)
  scanners/
    docker_scanner.py   - Docker thin wrapper (Phase 2)
    database_scanner.py - Database thin wrapper (Phase 2)
    network_scanner.py  - Network thin wrapper (Phase 4)
    k8s_scanner.py      - Kubernetes thin wrapper (Phase 4)
  connectors/
    aws_connector.py    - AWS thin wrapper (Phase 3)
    azure_connector.py  - Azure thin wrapper (Phase 4)
    gcp_connector.py    - GCP thin wrapper (Phase 4)
```

---

## How Everything Works Together

```
┌─────────────────────────────────┐
│ Trinity6 repo (YOUR IP)         │
│                                 │
│  Engine + Checks + Reports      │
│  The intelligence               │
│  Nobody sees this               │
└───────────────┬─────────────────┘
                │ imported by
┌───────────────▼─────────────────┐
│ trinity6-platform repo          │
│                                 │
│  Agents (thin wrappers)         │
│  Scanners (thin wrappers)       │
│  API (receives results)         │
│  Dashboard (shows results)      │
└───────────────┬─────────────────┘
                │ posts results to
┌───────────────▼─────────────────┐
│ trinity6-platform.onrender.com  │
│                                 │
│  Client logs in                 │
│  Sees their compliance data     │
│  Downloads reports              │
└─────────────────────────────────┘
```

### What Agents and Scanners Actually Do
Agents and scanners in trinity6-platform are THIN WRAPPERS only.
They do NOT contain scanning logic. They just:

1. Call Trinity6 engine
2. Collect results
3. Post results to API

All actual intelligence stays in Trinity6 repo.

### Example — How linux_agent.py Works
```python
# Step 1: Import Trinity6 engine
from trinity6.engine import Scanner
from trinity6.compliance.cis.linux import checks

# Step 2: Run scan locally on client server
results = Scanner.run(checks)

# Step 3: Post to platform API
requests.post(API_URL, json=results)
```
Three steps. That is all. The engine does the work.

---

## What The Two Dashboards Are For

| Dashboard | Location | Who Uses It | Purpose |
|-----------|----------|-------------|---------|
| Trinity6/dashboard/ | Local machine | You only | Internal development and testing |
| trinity6-platform/dashboard/ | Hosted on internet | Clients | Production client facing dashboard |

The local dashboard can eventually become your admin view.
Clients always use the platform dashboard.

---

## Scan Types and Where They Live

| Scanner | Scans | Lives In | Phase |
|---------|-------|----------|-------|
| linux_agent.py | Linux servers | trinity6-platform/agents/ | 1 |
| windows_agent.ps1 | Windows servers | trinity6-platform/agents/ | 3 |
| docker_scanner.py | Docker containers | trinity6-platform/scanners/ | 2 |
| database_scanner.py | MySQL Postgres MongoDB | trinity6-platform/scanners/ | 2 |
| network_scanner.py | Routers switches | trinity6-platform/scanners/ | 4 |
| k8s_scanner.py | Kubernetes clusters | trinity6-platform/scanners/ | 4 |
| aws_connector.py | AWS infrastructure | trinity6-platform/connectors/ | 3 |
| azure_connector.py | Azure infrastructure | trinity6-platform/connectors/ | 4 |
| gcp_connector.py | GCP infrastructure | trinity6-platform/connectors/ | 4 |

All CIS check definitions for every scanner live in Trinity6/compliance/

---

## Enterprise GRC View — What This Becomes

A GRC Head opens the dashboard and sees:

```
Company Compliance Score: 67%

Linux Servers:      82%  ✓ good
Windows Servers:    71%  ⚠ warning
Docker Containers:  45%  ✗ critical
Databases:          58%  ✗ critical
AWS Infrastructure: 79%  ✓ good
Network Devices:    88%  ✓ good
```

Drills into Docker 45%:
- 47 containers failing CIS checks
- Root running as container user
- No resource limits set
- Privileged containers running
- Outdated base images

Clicks one container:
- Exact failures listed
- Fix command shown
- One click remediation
- Compliance certificate after fix

---

## 5 Year Product Roadmap

### Phase 1 — SMB Linux Focus (Now to Month 3)
**Goal: First paying client. 999 INR per month.**

- agent/trinity6_agent.py wrapping existing engine
- trinity6-platform/agents/linux_agent.py thin wrapper
- Dashboard showing Linux scan results
- Systemd service for auto weekly scans
- Drift detection comparing to previous scan

Target clients: IT managers with 5 to 20 Linux servers
in Chennai healthcare finance and IT services companies.

Milestone: One paying client by end of Month 1.

---

### Phase 2 — Docker and Databases (Month 3 to 6)
**Goal: 10 clients. 30000 INR MRR.**

- trinity6-platform/scanners/docker_scanner.py
- trinity6-platform/scanners/database_scanner.py
- Trinity6/compliance/cis/docker/ check definitions
- Dashboard showing Docker and DB results
- Email alerts for critical failures

Most SMBs run Docker now. Adding Docker scanning
doubles the value of Trinity6 immediately.

---

### Phase 3 — Windows and Cloud (Month 6 to 12)
**Goal: 50 clients. 150000 INR MRR.**

- trinity6-platform/agents/windows_agent.ps1
- trinity6-platform/connectors/aws_connector.py
- Trinity6/compliance/cis/windows/ check definitions
- Multi server dashboard view
- PDF compliance certificates
- Auto remediation suggestions

Start SOC 2 Type 1 audit for Trinity6 itself.
Cannot sell compliance without being compliant.

---

### Phase 4 — Enterprise Ready (Year 2)
**Goal: 100 clients. 500000 INR MRR.**

- Kubernetes and network scanners
- Azure and GCP connectors
- Role based access control
- Full audit log export
- Multi tenant MSP support
- Jira and Slack integrations
- Pan India expansion

---

### Phase 5 — Full GRC Platform (Year 3 to 5)
**Goal: 500 clients. Compete with enterprise tools.**

- Visual workflow builder for compliance automation
- Risk scoring engine
- All major frameworks SOC 2 ISO 27001 PCI DSS NIST
- Automated evidence collection for audits
- White label for MSP partners
- Marketplace for third party integrations
- Southeast Asia Middle East UK expansion

---

## Current Infrastructure Status

| Component | Location | Status |
|-----------|----------|--------|
| Scanner Engine | Trinity6 repo | Live |
| CIS Linux Checks | Trinity6/compliance/cis/linux/ | Live |
| Platform API | trinity6-platform.onrender.com | Live |
| Client Dashboard | trinity6-platform.onrender.com/dashboard | Live |
| Trinity AI | GitHub Actions | Live |
| Trinity AI Hardware | Mac Mini M5 | Waiting |

---

## The Single Most Important Thing Right Now

Everything in this roadmap depends on one thing.
Getting the first paying client.

Not building more scanners.
Not adding more connectors.
Not improving the dashboard.

The first paying client.
Even 500 INR per month.
Even a friend's company.
Even with a massive discount.

One real human paying real money for Trinity6 Scanner.
That validates everything. That proves the market exists.

Do that this week. Everything else is secondary.

---

*Trinity6 — Intelligent Security for the Real World*
*Built in Chennai. Built to go global.*
