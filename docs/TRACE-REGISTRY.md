# Complete Traceability Registry
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  
**Jira Project**: OBRRP (15 Stories, 4 Epics, 76 Story Points)

---

## 1. Master Traceability Matrix

| Requirement | Jira Story | Epic | Implementation Component | Automated Test | Security Control | Verification Evidence |
|---|---|---|---|---|---|---|
| **REQ-01** (User Registration) | **OBRRP-5** (3 SP) | EPIC-01 | `app/routes/auth.py`, `UserService`, `models/user.py` | `test_unit_auth.py`, `test_integration_auth.py` | CTRL-01 (Bcrypt, Validation) | `docs/evidence/phase-09-jira-backlog.md` |
| **REQ-02** (Secure Login) | **OBRRP-6** (5 SP) | EPIC-01 | `app/routes/auth.py`, `UserService` | `test_unit_auth.py`, `test_integration_auth.py` | CTRL-01 (HttpOnly, SameSite) | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-12** (Secure Logout) | **OBRRP-7** (3 SP) | EPIC-01 | `app/routes/auth.py::logout` | `test_integration_auth.py` | CTRL-01 (Session Invalidation) | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-03** (Book Search) | **OBRRP-8** (5 SP) | EPIC-02 | `app/routes/catalog.py`, `SearchService` | `test_unit_search.py`, `test_fuzzing.py` | CTRL-05 (Parameterized ORM) | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-04** (Book Details) | **OBRRP-9** (3 SP) | EPIC-02 | `app/routes/catalog.py::detail` | `test_fuzzing.py`, `test_e2e_workflow.py` | CTRL-04, CTRL-07 | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-05, REQ-06** (Rate & Review) | **OBRRP-10** (8 SP) | EPIC-02 | `app/routes/reviews.py`, `ReviewService` | `test_unit_validation.py`, `test_integration_reviews.py` | CTRL-03 (XSS Escaping), CTRL-04 | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-07, REQ-08** (Edit/Delete Review) | **OBRRP-11** (5 SP) | EPIC-02 | `app/services/review_service.py` | `test_authorization.py` | CTRL-02 (Object Ownership) | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-09** (Reading Shelf) | **OBRRP-12** (5 SP) | EPIC-02 | `app/routes/reading_list.py`, `ReadingListService` | `test_e2e_workflow.py` | CTRL-02, CTRL-06 | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-10** (Admin Catalog) | **OBRRP-13** (5 SP) | EPIC-03 | `app/routes/admin.py`, `BookService` | `test_authorization.py` | CTRL-06 (`@admin_required`) | `docs/evidence/phase-10-board-workflow.md` |
| **REQ-11** (Review Moderation) | **OBRRP-14** (5 SP) | EPIC-03 | `app/routes/admin.py`, `ReviewService` | `test_authorization.py` | CTRL-06 (`@admin_required`), CTRL-08 | `docs/evidence/phase-10-board-workflow.md` |
| **THR-02, VUL-01** (IDOR Defense) | **OBRRP-15** (8 SP) | EPIC-03 | `ReviewService::update_review` | `test_authorization.py`, IDOR demo test | CTRL-02 (Server-Side Ownership) | `docs/phase-12-secure-coding/idor-demonstration.md` |
| **NFR-07** (Audit Logging) | **OBRRP-16** (3 SP) | EPIC-03 | `app/core/audit.py`, `models/audit_log.py` | `test_authorization.py` | CTRL-08 (Tamper-Evident Audit) | `docs/evidence/phase-10-board-workflow.md` |
| **NFR-01..05** (Security Testing) | **OBRRP-17** (5 SP) | EPIC-04 | Full test suite in `tests/` | 23/23 tests passing | Bandit SAST Scan | `evidence/phase-11/bandit_scan.txt` |
| **NFR-09** (CI/CD Pipeline) | **OBRRP-18** (5 SP) | EPIC-04 | `.github/workflows/ci.yml` | Pipeline workflow lint & test | Minimal Permissions Policy | `docs/evidence/phase-10-board-workflow.md` |
| **NFR-10** (Container & K8s) | **OBRRP-19** (8 SP) | EPIC-04 | `docker/Dockerfile`, `docker-compose.yml`, `k8s/` | Container runtime `/health` probe | CTRL-10 (Non-root UID 10001) | `docs/evidence/phase-10-board-workflow.md` |

---

## 2. Requirement ID Definitions

- **REQ-01**: User registration with unique username and email format validation.
- **REQ-02**: User login with bcrypt password hash verification (rounds=12).
- **REQ-03**: Parameterized search across books by title, author, and genre.
- **REQ-04**: Book details display with aggregated rating and review counter.
- **REQ-05**: Strict integer rating bound between 1 and 5.
- **REQ-06**: Review creation with length bounds (5–2000 chars) and autoescaping.
- **REQ-07**: Server-side authorization allowing edit of own review only.
- **REQ-08**: Server-side authorization allowing deletion of own review only.
- **REQ-09**: Private reading list management per authenticated user.
- **REQ-10**: Administrator book catalog CRUD guarded by RBAC.
- **REQ-11**: Administrator review moderation with mandatory reason logging.
- **REQ-12**: Server-side session invalidation on logout.
