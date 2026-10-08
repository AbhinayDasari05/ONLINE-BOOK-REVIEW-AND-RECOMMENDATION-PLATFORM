# Phase 10: Defect Tracking & Resolution Evidence
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  

---

## 1. Actual Defect Log

| Defect ID | Associated Story | Severity | Defect Description | Root Cause | Status | Resolution |
|---|---|---|---|---|---|---|
| **DEF-01** | OBRRP-6 | High | SQLite relative path failed on blueprint execution | SQLite relative path evaluated relative to CWD, causing database locked/not found errors | **RESOLVED** | Converted DB path in `app/config.py` to use `os.path.abspath` anchored to project root directory. |
| **DEF-02** | OBRRP-11 | Critical | Ambiguous foreign key mapping between User and Review | Both `user_id` and `moderated_by` in `Review` referenced `User.id` | **RESOLVED** | Disambiguated relationships in `User` and `Review` models with explicit `foreign_keys=[moderated_by]`. |
| **DEF-03** | OBRRP-10 | Medium | Flash message quote assertion mismatch in E2E tests | Jinja2 auto-escaped single quotes into `&#39;` in HTML response | **RESOLVED** | Updated test assertions in `test_e2e_workflow.py` to match escaped text substrings. |
| **DEF-04** | OBRRP-19 | Medium | Docker host port conflict with macOS AirPlay Receiver | Port 5000 is occupied by macOS `ControlCenter` listening for AirPlay | **RESOLVED** | Updated `docker-compose.yml` to bind host port `5050` to container port `5000`. |
| **DEF-05** | OBRRP-19 | Low | Container SQLite database was unseeded on first spin-up | Docker volume initialization started with empty database | **RESOLVED** | Executed idempotent seeder `scripts/seed.py` inside container via `docker exec`. |

---

## 2. Defects Carried Over

- **Defects Carried Over from Sprint 1 to Sprint 2**: **0**
- **Defects Carried Over from Sprint 2 to Release**: **0**
- **Current Open Defects**: **0** (All 5 encountered defects were diagnosed, fixed, and verified via test suites).
