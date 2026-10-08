# Phase 10: Sprint Review Evidence
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  

---

## 1. Sprint 1 Review: Core Platform

- **Sprint Goal**: *"Build the core Online Book Review and Recommendation Platform with secure authentication, book discovery, reviews, ratings and reading-list functionality."*
- **Iteration Dates**: Oct 8, 2026 – Oct 21, 2026
- **Planned Story Points**: 37 SP
- **Completed Story Points**: 37 SP
- **Completed Stories**:
  - `OBRRP-5` — Registration (3 SP)
  - `OBRRP-6` — Secure Login (5 SP)
  - `OBRRP-7` — Secure Logout & Sessions (3 SP)
  - `OBRRP-8` — Search Books (5 SP)
  - `OBRRP-9` — View Book Details (3 SP)
  - `OBRRP-10` — Rate & Review Books (8 SP)
  - `OBRRP-11` — Edit/Delete Own Reviews (5 SP)
  - `OBRRP-12` — Reading List (5 SP)
- **Incomplete / Carry-Over Stories**: None (0 SP)

### Demonstrated Features & Security Controls:
1. **User Authentication (CTRL-01)**: Bcrypt hashing (rounds=12), HttpOnly and SameSite=Lax cookie issuance, full session invalidation on logout.
2. **Catalog Discovery & Search (CTRL-05)**: Parameterized SQLAlchemy ORM queries filtering by title, author, and genre.
3. **Rating & Review System (CTRL-03, CTRL-04)**: 1–5 integer rating enforcement, unique constraint per user/book, Jinja2 autoescaping preventing XSS.
4. **Ownership Verification (CTRL-02)**: Object-level authorization check `review.is_owned_by(user_id)` preventing cross-user review edits.
5. **Private Reading List (CTRL-02)**: Multi-status shelves isolated per authenticated user.

---

## 2. Sprint 2 Review: Security & DevSecOps

- **Sprint Goal**: *"Complete administrator functionality, security controls, testing and DevSecOps capabilities for the platform."*
- **Iteration Dates**: Oct 22, 2026 – Nov 4, 2026
- **Planned Story Points**: 39 SP
- **Completed Story Points**: 39 SP
- **Completed Stories**:
  - `OBRRP-13` — Admin Book Management (5 SP)
  - `OBRRP-14` — Review Moderation (5 SP)
  - `OBRRP-15` — Secure Authorization & IDOR Protection (8 SP)
  - `OBRRP-16` — Audit Logging (3 SP)
  - `OBRRP-17` — Security & Authorization Testing (5 SP)
  - `OBRRP-18` — CI/CD Pipeline (5 SP)
  - `OBRRP-19` — Docker & Local Kubernetes Deployment (8 SP)
- **Incomplete / Carry-Over Stories**: None (0 SP)

### Demonstrated Features & Security Controls:
1. **Role-Based Access Control (CTRL-06)**: `@admin_required` server-side decorator strictly denying regular users access to `/admin/*` routes with HTTP 403.
2. **Review Moderation (CTRL-06, CTRL-08)**: Admin moderation queue with mandatory reason tracking; hidden reviews excluded from public views.
3. **IDOR Demonstration & Fix (CTRL-02)**: Exploitable on demo branch `demo/idor-before`, mitigated on `main` branch with automated test proof (`test_authorization.py`).
4. **Audit Logging (CTRL-08)**: Dedicated `AuditLog` table with automatic scrubbing of passwords and sensitive tokens.
5. **Automated Testing & SAST (CTRL-07)**: 23/23 Pytest tests passing; Bandit scan with 0 High, 0 Medium vulnerabilities.
6. **Hardened Containerization (CTRL-10)**: Multi-stage Dockerfile running as unprivileged user (`UID 10001:10001`), healthy `/health` probe endpoint on port 5050.
7. **CI/CD Automation**: GitHub Actions pipeline checking tests, SAST scans, and Docker policies.
