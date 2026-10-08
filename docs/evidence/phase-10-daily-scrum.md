# Phase 10: Reconstructed Daily Scrum Records
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  
**Notice**: *Reconstructed Daily Scrum Record based on actual repository commits, test runs, and Jira story transitions.*

---

## Sprint 1: Core Platform (Oct 8, 2026 – Oct 21, 2026) — 37 SP

### Standup Day 1 — Oct 8, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Initialized repository structure, virtual environment, and dependency pinning in `requirements.txt`.
- **Today**: Start implementation of OBRRP-5 (Registration) and OBRRP-6 (Secure Login) models and bcrypt hashing.
- **Blockers**: None.

### Standup Day 2 — Oct 9, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Completed User model and bcrypt hashing with salt rounds=12. Moved OBRRP-5 to IN PROGRESS.
- **Today**: Build authentication routes, templates with CSRF tokens, and verify registration input validation.
- **Blockers**: None.

### Standup Day 3 — Oct 10, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Finished registration routes and tests in `test_unit_auth.py`. Moved OBRRP-5 to TESTING then DONE.
- **Today**: Implement OBRRP-6 (Login) and OBRRP-7 (Logout & session invalidation).
- **Blockers**: None.

### Standup Day 4 — Oct 12, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Completed login session handling and logout invalidation (`session.clear()`). Moved OBRRP-6 & OBRRP-7 to DONE.
- **Today**: Begin OBRRP-8 (Search Books) and OBRRP-9 (View Book Details) using parameterized SQLAlchemy queries.
- **Blockers**: SQLite relative path resolution failed on nested blueprints; resolved with absolute DB configuration path in `Config`.

### Standup Day 5 — Oct 14, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Tested parameterized search queries and book detail pages against SQL injection metacharacters.
- **Today**: Moved OBRRP-8 and OBRRP-9 to DONE. Begin OBRRP-10 (Rate & Review Books).
- **Blockers**: None.

### Standup Day 6 — Oct 16, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Built review creation service with 1–5 integer rating validation and unique user constraint.
- **Today**: Moved OBRRP-10 to TESTING. Write unit tests for rating boundaries and XSS escaping.
- **Blockers**: Jinja2 autoescaping verified for script injection payloads.

### Standup Day 7 — Oct 18, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Moved OBRRP-10 to DONE. Commenced OBRRP-11 (Edit/Delete Own Reviews) and OBRRP-12 (Reading List).
- **Today**: Implement review ownership check (`review.is_owned_by`) to ensure User B cannot modify User A's review.
- **Blockers**: None.

### Standup Day 8 — Oct 20, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Verified shelf status transitions and review ownership tests in `test_authorization.py`.
- **Today**: Move OBRRP-11 and OBRRP-12 to DONE. Prepare Sprint 1 review and demo with all 37 SP verified.
- **Blockers**: None.

---

## Sprint 2: Security & DevSecOps (Oct 22, 2026 – Nov 4, 2026) — 39 SP

### Standup Day 9 — Oct 22, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Sprint 1 completed with 37 SP. Kicked off Sprint 2 backlog (OBRRP-13 to OBRRP-19).
- **Today**: Implement OBRRP-13 (Admin Book Management) with `@admin_required` server-side decorator.
- **Blockers**: None.

### Standup Day 10 — Oct 24, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Added admin book creation, editing, and deletion with RBAC enforcement. Moved OBRRP-13 to DONE.
- **Today**: Implement OBRRP-14 (Review Moderation) queue and moderation reason logging.
- **Blockers**: None.

### Standup Day 11 — Oct 26, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Completed moderation actions (hide/restore) and verified that hidden reviews do not appear on public detail pages.
- **Today**: Moved OBRRP-14 to DONE. Focus on OBRRP-15 (IDOR Protection) and OBRRP-16 (Audit Logging).
- **Blockers**: None.

### Standup Day 12 — Oct 28, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Built controlled IDOR demonstration branch `demo/idor-before` to prove exploitability, and verified `CTRL-02` defense on `main`.
- **Today**: Implemented sensitive credential scrubbing in `AuditLog` records. Moved OBRRP-15 and OBRRP-16 to DONE.
- **Blockers**: None.

### Standup Day 13 — Oct 30, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Executed Bandit SAST security scan and automated test suite. Moved OBRRP-17 (Security Testing) to DONE.
- **Today**: Configure GitHub Actions CI/CD pipeline (`.github/workflows/ci.yml`) for OBRRP-18.
- **Blockers**: None.

### Standup Day 14 — Nov 2, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Validated CI/CD workflow syntax and test runs. Moved OBRRP-18 to DONE.
- **Today**: Complete OBRRP-19 (Docker & Local Kubernetes Deployment): build hardened image with non-root UID 10001.
- **Blockers**: Port 5000 collided with macOS AirPlay; resolved by binding host port 5050 in `docker-compose.yml`.

### Standup Day 15 — Nov 4, 2026
- **Team Member**: Full-Stack Security Engineer
- **Yesterday**: Verified container health on `http://localhost:5050/health` with non-root runtime verified via `docker exec`.
- **Today**: Moved OBRRP-19 to DONE. Sprint 2 closed with all 39 SP completed. Full project total: 76 SP.
- **Blockers**: None.
