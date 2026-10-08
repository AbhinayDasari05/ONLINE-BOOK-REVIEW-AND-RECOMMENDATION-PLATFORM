# Project Status Matrix
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  
**Updated**: October 2026

---

## 1. Phase Completion Status

| Phase | Description | Status | Evidence / Key Artifacts |
|---|---|---|---|
| Phase 0 | Environment & Project Skeleton | COMPLETE | Directory layout, `.gitignore`, `.env.example`, `requirements.txt` |
| Phase 1 | Agile Process & XP Security Practices | COMPLETE | `docs/phase-01-agile/agile-approach.md` (5 principles, 2 refactorings) |
| Phase 2 | Requirements Engineering (SRS) | COMPLETE | `docs/phase-02-requirements/srs.md` (REQ-01 to REQ-12) |
| Phase 3 | UML Use Case Diagrams & Specifications | COMPLETE | `docs/phase-03-uml/use-cases.md` (Mermaid diagram, UC-01/02 specs) |
| Phase 4 | ER Diagram, DFDs & Trust Boundaries | COMPLETE | `docs/phase-04-data-flow/er-dfd-trust-boundaries.md` (Level 0/1 DFD, ER) |
| Phase 5 | Architecture & Design | COMPLETE | `docs/phase-05-architecture/architecture.md` (4-layer diagram, COMP-01..08) |
| Phase 6 | UI Design & Connected Screens | COMPLETE | `docs/phase-06-ui/ui-screens.md`, 6 templates in `app/templates/` |
| Phase 7 | Threat Modeling (STRIDE) | COMPLETE | `docs/phase-07-threat-model/stride-analysis.md` (10 assets, 10 threats) |
| Phase 8 | Attack Tree Analysis | COMPLETE | `docs/phase-08-attack-tree/attack-tree.md` (ATK-01 Mermaid AND/OR tree) |
| Phase 9 | Product Backlog & User Stories | COMPLETE | `docs/phase-09-backlog/user-stories.md`, `jira-import.csv` |
| Phase 10 | Sprint Planning & Burndown Metrics | COMPLETE | `docs/phase-10-sprint/sprint-metrics.md` (velocity, Mermaid burndown) |
| Phase 11 | Secure Build & SAST Security Scanning | COMPLETE | `evidence/phase-11/bandit_scan.txt`, `secret_scan_report.txt` |
| Phase 12 | Secure Coding & Controlled IDOR Demo | COMPLETE | `docs/phase-12-secure-coding/idor-demonstration.md`, `evidence/phase-12/` |
| Phase 13 | Containerization (Docker & Compose) | COMPLETE | `docker/Dockerfile`, `docker-compose.yml`, non-root execution UID 10001 |
| Phase 14 | Automated Testing & Verification | COMPLETE | 23/23 passing pytest tests, `evidence/phase-14/pytest_output.txt` |
| Phase 15 | Logging, Monitoring & Audit | COMPLETE | `docs/phase-15-monitoring/monitoring.md`, `app/core/audit.py`, `/health` |
| Phase 16 | Hardening & Security Audit | COMPLETE | `docs/phase-16-hardening/security-review.md`, `SECURITY.md` |

---

## 2. Test & Scan Verification Summary

- **Automated Tests**: 23/23 passed (`pytest tests/`)
- **Bandit SAST Scan**: 0 High, 0 Medium, 1 Low (test configuration mock key)
- **Controlled IDOR Proof**: Verified exploitable on branch `demo/idor-before`, verified strictly prevented on `main`
- **Secret Scan**: Clean; 0 unauthorized secrets committed
