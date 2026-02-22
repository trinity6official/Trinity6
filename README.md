# Trinity6 GRC Scanner
### Intelligent Security - Powered by AI

![Trinity6](https://img.shields.io/badge/Trinity6-Intelligent%20Security-00d4ff)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Status](https://img.shields.io/badge/Status-Active%20Development-green)

---

## What is Trinity6?

Trinity6 is an AI powered GRC scanner that automatically discovers devices on your network and verifies compliance against major security frameworks including CIS Benchmarks, NIST CSF, ISO 27001, and SOC 2.

Unlike expensive enterprise tools, Trinity6 uses local AI via Ollama and Mistral to analyze scan results intelligently while keeping all client data private on your own infrastructure.

---

## How It Works

Step 1 - Network Discovery
Trinity6 scans your network and finds every connected device

Step 2 - Compliance Scanning
SSH into Linux servers and run 100+ CIS benchmark checks

Step 3 - AI Analysis
Local Mistral AI interprets results and prioritizes findings

Step 4 - Professional Reports
HTML reports with executive summary and remediation guidance

---

## Architecture

Type 1 - Deterministic - Compliance as Code
YAML files define all controls
Python engine executes checks
Pass/Fail results collected

Type 2 - AI Powered
Local Mistral via Ollama
Interprets scan results
Generates plain English reports
Zero external API calls
All data stays on your server

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama installed with Mistral model
- SSH access to target servers

### Installation

Clone repository
git clone https://github.com/trinity6official/Trinity6.git
cd Trinity6

Install dependencies
pip install -r requirements.txt

Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

Pull Mistral model
ollama pull mistral

### Setup Audit User on Target Servers

Create audit user
useradd -m -s /bin/bash trinity6_audit

Create SSH directory
mkdir -p /home/trinity6_audit/.ssh
chmod 700 /home/trinity6_audit/.ssh

Add Trinity6 public key
echo "YOUR_PUBLIC_KEY_HERE" >> /home/trinity6_audit/.ssh/authorized_keys
chmod 600 /home/trinity6_audit/.ssh/authorized_keys

Grant read only sudo permissions
echo "trinity6_audit ALL=(ALL) NOPASSWD: /usr/bin/cat, /usr/bin/find, /usr/bin/stat, /usr/sbin/sysctl, /usr/bin/systemctl" >> /etc/sudoers.d/trinity6

### Run Your First Scan

Scan entire network
python cli/trinity6.py scan --network 192.168.1.0/24 --username trinity6_audit --key ~/.ssh/trinity6_key

Scan single host
python cli/trinity6.py host --host 192.168.1.100 --username trinity6_audit --key ~/.ssh/trinity6_key

Discover devices only
python cli/trinity6.py discover --network 192.168.1.0/24

Show version
python cli/trinity6.py version

---

## Compliance Frameworks

| Framework | Status | Controls |
|-----------|--------|----------|
| CIS Benchmark Linux | Active | 100+ |
| CIS Benchmark Windows | Coming Phase 3 | - |
| NIST CSF | Coming Phase 4 | - |
| ISO 27001 | Coming Phase 4 | - |
| SOC 2 | Coming Phase 4 | - |

---

## CIS Benchmark Coverage

| Section | Title | Status |
|---------|-------|--------|
| Section 1 | Filesystem Configuration | Complete |
| Section 2 | Services | Complete |
| Section 3 | Network Configuration | Complete |
| Section 4 | Logging and Auditing | Complete |
| Section 5 | Access Control | Complete |
| Section 6 | System Maintenance | Complete |

---

## Project Structure

Trinity6/
├── compliance/
│   └── cis/
│       └── linux/
│           ├── section1_filesystem.yaml
│           ├── section2_services.yaml
│           ├── section3_network.yaml
│           ├── section4_logging.yaml
│           ├── section5_access.yaml
│           └── section6_maintenance.yaml
├── engine/
│   └── compliance_engine.py
├── scanner/
│   ├── discovery.py
│   ├── cis_checks.py
│   ├── ai_analyst.py
│   └── main.py
├── cli/
│   └── trinity6.py
├── reports/
│   └── generator.py
├── results/
└── requirements.txt

---

## Roadmap

- Phase 1 - Foundation - CIS Linux scanning with AI - Complete
- Phase 2 - Complete CIS coverage and PDF reports - Coming
- Phase 3 - Windows server support - Coming
- Phase 4 - NIST ISO 27001 SOC 2 frameworks - Coming
- Phase 5 - Network device scanning - Coming
- Phase 6 - Production ready with client portal - Coming
- Phase 7 - Cloud infrastructure scanning - Coming
- Phase 8 - SaaS platform - Coming

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| SSH | Paramiko |
| AI Model | Mistral via Ollama |
| Compliance | Custom YAML Engine |
| Reports | HTML with Jinja2 |
| CLI | Argparse |

---

## Security and Privacy

- All AI analysis runs locally via Ollama
- Client data never leaves your infrastructure
- Read only SSH access to client servers
- No external API calls for analysis
- All results stored locally

---

## About Trinity6

Trinity6 is an intelligent cybersecurity company building AI powered GRC automation tools for small and medium businesses.

- Website: https://trinity6.com
- LinkedIn: https://linkedin.com/company/trinity6
- GitHub: https://github.com/trinity6official
- Email: contact@trinity6.com

---

2026 Trinity6 - Intelligent Security - trinity6.com
