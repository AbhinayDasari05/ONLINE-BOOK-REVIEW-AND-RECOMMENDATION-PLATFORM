# Project Status: Online Book Review and Recommendation Platform

**Course Code**: 20CYS401 — Secure Software Engineering  
**Degree/Branch**: B.Tech CSE — Cybersecurity  
**Execution Mode**: Stage Execution Model (Stages 0–3)  
**Current Stage**: STAGE 0 COMPLETED — Ready for Stage 1  

---

## Examination Phase Status Matrix

| Phase | Current Status | Existing Work | Missing Work | Next Action |
|---|---|---|---|---|
| **Phase 1: Agile Process** (6 Marks) | NOT STARTED | Requirements analyzed | Scrum+XP mapping, refactoring records, agile risks | Execute in Stage 2 |
| **Phase 2: Requirements** (7 Marks) | NOT STARTED | Trace registry initialized | SRS, requirements matrix, security requirements, CIA | Execute in Stage 2 |
| **Phase 3: UML & Analysis** (7 Marks) | NOT STARTED | Trace IDs assigned | Use Case diagram, UC-01/02 flows, scenario analysis | Execute in Stage 2 |
| **Phase 4: ER, DFD & Trust Boundaries** (7 Marks) | NOT STARTED | Component boundaries planned | ER diagram, Level-0/1 DFDs, Trust Boundary diagram | Execute in Stage 2 |
| **Phase 5: Architecture & Design** (7 Marks) | NOT STARTED | COMP-01..08 identified | Layered architecture diagram, component map, design patterns | Execute in Stage 2 |
| **Phase 6: UI Implementation & Wireframes** (5 Marks) | NOT STARTED | Screen requirements documented | 6 connected screens with Jinja2/CSS/JS, UI doc | Implement in Stage 1, Doc in Stage 2 |
| **Phase 7: Threat Modeling (STRIDE)** (10 Marks) | NOT STARTED | 10 Assets & 10 Threats mapped | STRIDE sheets, info flow diagram, vulnerability analysis (6 findings) | Execute in Stage 2 |
| **Phase 8: Attack Tree** (6 Marks) | NOT STARTED | ATK-01 root goal identified | AND/OR attack tree Mermaid, control mappings | Execute in Stage 2 |
| **Phase 9: Product Backlog** (7 Marks) | NOT STARTED | 10 User stories planned | Backlog markdown, 2 Sprints, jira-import.csv | Execute in Stage 2 |
| **Phase 10: Sprint Execution & Metrics** (7 Marks) | NOT STARTED | Tasks assigned to sprints | Sprint boards, burndown arithmetic, velocity, retro | Execute in Stage 2 |
| **Phase 11: Secure Build & Code Review** (6 Marks) | NOT STARTED | Tool checks executed | 5 build controls, secret scanning evidence, PR template | Execute in Stage 3 |
| **Phase 12: Secure Coding & Weakness Fix** (7 Marks) | NOT STARTED | VUL-01 IDOR identified | Controlled IDOR branch demo, fix, before/after evidence | Execute in Stage 1 / Stage 3 |
| **Phase 13: Docker & Kubernetes** (7 Marks) | NOT STARTED | Tool checks executed | Secure Dockerfile, k8s manifests, build/run verification | Execute in Stage 3 |
| **Phase 14: CI/CD & Testing** (7 Marks) | NOT STARTED | Test plan in trace registry | Unit/Integration/E2E/Fuzz tests, CI workflow, real output | Implement in Stage 1, Pipeline in Stage 3 |
| **Phase 15: Logging, Monitoring & Hardening** (5 Marks) | NOT STARTED | COMP-08 planned | Audit logs, 5 metric thresholds, hardening checklists | Execute in Stage 3 |
| **Phase 16: Final Security Review & Traceability** (1 Mark) | NOT STARTED | Full trace chain planned | REQ-07 end-to-end trace audit, residual risk analysis | Execute in Stage 3 |

---

## Tool Availability

| Tool | Status | Binary Location / Details | Impact |
|---|---|---|---|
| `git` | Available | `/usr/bin/git` (v2.39.5) | Fully operational for version control and branch demos |
| `python3` | Available | `/usr/bin/python3` (3.9.6) & `/opt/homebrew/bin/python3` (3.14.8) | Available for virtualenv creation and test execution |
| `pip` | Available | `/opt/homebrew/bin/pip3` | Available for package management |
| `docker` | CLI Available, Daemon Offline | `/Users/abhinaydasari/.docker/bin/docker` | Local Docker daemon socket is not running; container builds prepared |
| `docker-compose` | CLI Available | `/Users/abhinaydasari/.docker/bin/docker-compose` | Docker compose manifests created |
| `kubectl` | CLI Available | `/Users/abhinaydasari/.docker/bin/kubectl` | Kubernetes manifests created; local cluster not running |
| `minikube` / `kind`| Not Installed | Not in PATH | Minikube/kind not installed on machine |
| `gh` | Not Installed | Not in PATH | GitHub CLI not available; git and workflow files used directly |
| `semgrep` | Installed | `/opt/homebrew/bin/semgrep` | Local config permissions restricted; can scan code directly |
| `bandit` | Not in global PATH | Python package | Can be run via pip/virtualenv or python AST checks |
| `gitleaks` | Not Installed | Not in PATH | Automated pattern inspection script used for secret scanning |
| `trivy` | Not Installed | Not in PATH | Container scanner not present |
| `terraform` | Installed | `/opt/homebrew/bin/terraform` (v1.16.4) | IaC validation only (Cost protection: NO apply) |
| `jira` | No Cloud Account | N/A | Offline Scrum tracking via `jira-import.csv` & Sprint markdown |

---

## Blocked Items

1. **Local Docker Daemon & Kubernetes Cluster**: Docker Desktop / socket is not active in this environment, and Minikube/kind are not installed.
   - *Impact*: Docker images and Kubernetes manifests will be written, verified, and syntax-checked. If Docker Desktop is started by user, image build and run can proceed.
   - *Action*: Manifests placed in `k8s/` and `docker/`. Full manual commands provided in guide.
2. **Jira Cloud Access**: No live Atlassian Jira credentials or enterprise token provided.
   - *Impact*: Cannot push directly to live Jira Cloud instance.
   - *Action*: Generate standards-compliant `jira-import.csv` and detailed Jira sprint boards reconstructed in markdown.

---

## Existing Security Findings

- *Pre-assessment*: Baseline scaffold contains zero hard-coded credentials.
- Controlled demonstration planned for **VUL-01 (IDOR on review modification)** and **VUL-02 (XSS escaping)**.

---

## Existing Test Status

- 0 tests currently executed (Stage 0 scaffold).
- Test targets planned in TRACE-REGISTRY: TEST-01 through TEST-12.

---

## Existing Deployment Status

- Local SQLite architecture configured for complete offline standalone execution.
- AWS Cost & Credit Protection enforced: Zero AWS resources will be created.
