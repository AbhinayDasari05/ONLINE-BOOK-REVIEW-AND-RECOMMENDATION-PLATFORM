# Phase 9: Jira Product Backlog Evidence
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  
**Jira Project**: Online Book Review and Recommendation Platform (OBRRP)  
**Total Epics**: Exactly 4  
**Total Stories**: Exactly 15  
**Total Story Points**: Exactly 76 SP  

---

## 1. Epics Definition

| Epic ID | Epic Name | Scope |
|---|---|---|
| **EPIC-01** | Authentication & User Management | User registration, password hashing, session creation, logout, and credential validation. |
| **EPIC-02** | Books, Reviews & Reading List | Catalog search, detail view, rating, review creation, review editing/deletion, and personal reading shelves. |
| **EPIC-03** | Administration & Security | Admin catalog CRUD, review moderation, object-level authorization (IDOR protection), and tamper-evident audit logging. |
| **EPIC-04** | Testing, DevSecOps & Deployment | Automated testing suites, Bandit SAST security scans, CI/CD pipeline, and hardened Docker/Kubernetes containerization. |

---

## 2. Product Backlog (15 Stories, 76 Story Points)

### EPIC-01: Authentication & User Management (11 SP)

#### OBRRP-5: Registration
- **Epic**: EPIC-01
- **Story Points**: 3 SP
- **Priority**: High
- **Description**: As a new visitor, I want to create a secure personal account with unique credentials, so that I can access personalized book reviews and shelves.
- **Acceptance Criteria**:
  - [x] Required registration fields (username, email, password, confirm_password) are validated.
  - [x] Passwords are securely hashed with bcrypt (work factor=12).
  - [x] Duplicate username and email addresses are rejected with safe error messages.
  - [x] Invalid inputs (malformed emails, short usernames, passwords < 8 chars) are rejected.
  - [x] Successful registration creates a standard USER account (`is_admin=False`).
  - [x] User cannot self-register or elevate privilege as ADMIN.
- **Status**: DONE (Verified by `test_unit_auth.py`, `test_integration_auth.py`, `test_e2e_workflow.py`).

#### OBRRP-6: Secure Login
- **Epic**: EPIC-01
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As a registered user, I want to authenticate with my username/email and password, so that I can securely access my private session.
- **Acceptance Criteria**:
  - [x] Valid credentials authenticate successfully and establish a server-side session.
  - [x] Invalid credentials return a generic denial message without user enumeration.
  - [x] Passwords are never stored, logged, or displayed in plaintext.
  - [x] Secure session cookie is issued with `HttpOnly=True` and `SameSite=Lax`.
  - [x] Authentication failures and successes are recorded in the audit log.
- **Status**: DONE (Verified by `test_unit_auth.py`, `test_integration_auth.py`).

#### OBRRP-7: Secure Logout & Sessions
- **Epic**: EPIC-01
- **Story Points**: 3 SP
- **Priority**: Medium
- **Description**: As an authenticated user, I want to terminate my session on logout, so that my account cannot be accessed from a shared or public device.
- **Acceptance Criteria**:
  - [x] Logout invalidates the server-side session completely via `session.clear()`.
  - [x] Protected pages (`/my-shelf`, `/admin/*`) cannot be accessed after logout.
  - [x] Cookie is expired or unlinked upon logout.
  - [x] Logout event is recorded in the audit log.
- **Status**: DONE (Verified by `test_integration_auth.py`, `test_authorization.py`).

---

### EPIC-02: Books, Reviews & Reading List (26 SP)

#### OBRRP-8: Search Books
- **Epic**: EPIC-02
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As a reader, I want to search and filter books by keyword, author, and genre, so that I can discover books matching my interests.
- **Acceptance Criteria**:
  - [x] User can search by title keywords.
  - [x] User can search by author name.
  - [x] User can filter by genre dropdown or genre pill chips.
  - [x] Search input is validated and sanitized against null bytes.
  - [x] Database queries use 100% parameterized SQLAlchemy ORM queries to prevent SQL injection.
- **Status**: DONE (Verified by `test_unit_search.py`, `test_fuzzing.py`).

#### OBRRP-9: View Book Details
- **Epic**: EPIC-02
- **Story Points**: 3 SP
- **Priority**: Medium
- **Description**: As a reader, I want to view full metadata, synopsis, and community reviews for a book, so that I can evaluate whether to read it.
- **Acceptance Criteria**:
  - [x] Book details (title, author, genre, ISBN, publication year, description) are displayed.
  - [x] Star ratings and review count are rendered accurately.
  - [x] Community reviews are displayed with author usernames and timestamps.
  - [x] Average rating is calculated dynamically from approved reviews.
  - [x] Non-existent book IDs return a safe HTTP 404 response without stack trace leakage.
- **Status**: DONE (Verified by `test_fuzzing.py`, `test_e2e_workflow.py`).

#### OBRRP-10: Rate & Review Books
- **Epic**: EPIC-02
- **Story Points**: 8 SP
- **Priority**: High
- **Description**: As an authenticated reader, I want to assign a 1–5 star rating and post a written review, so that I can contribute to the community catalog.
- **Acceptance Criteria**:
  - [x] Rating is restricted strictly to integer values between 1 and 5.
  - [x] User can submit a written review between 5 and 2000 characters.
  - [x] Review input is sanitized and automatically HTML-escaped by Jinja2 to prevent XSS.
  - [x] Unique constraint enforces at most one review per user per book.
  - [x] Review creation is audit-logged with actor, book ID, and timestamp.
- **Status**: DONE (Verified by `test_unit_validation.py`, `test_fuzzing.py`, `test_integration_reviews.py`).

#### OBRRP-11: Edit/Delete Own Reviews
- **Epic**: EPIC-02
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As a review author, I want to update or delete my existing review, so that I can manage my published opinions.
- **Acceptance Criteria**:
  - [x] User can edit rating and text of their own review.
  - [x] User can delete their own review.
  - [x] User cannot edit another user's review (IDOR strictly denied).
  - [x] User cannot delete another user's review (IDOR strictly denied).
  - [x] Unauthorized modification/deletion attempts leave the database completely unchanged.
- **Status**: DONE (Verified by `test_authorization.py`, `test_integration_reviews.py`).

#### OBRRP-12: Reading List
- **Epic**: EPIC-02
- **Story Points**: 5 SP
- **Priority**: Medium
- **Description**: As a reader, I want to maintain a private reading shelf (`want-to-read`, `reading`, `finished`), so that I can track my personal reading journey.
- **Acceptance Criteria**:
  - [x] User can add any book to their reading shelf.
  - [x] User can update the reading status among allowed values.
  - [x] User can remove a book from their reading list.
  - [x] Reading list items are strictly isolated to the authenticated user.
  - [x] Other users cannot view or mutate another user's private reading list.
- **Status**: DONE (Verified by `test_e2e_workflow.py`, `test_authorization.py`).

---

### EPIC-03: Administration & Security (21 SP)

#### OBRRP-13: Admin Book Management
- **Epic**: EPIC-03
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As an administrator, I want to create, update, and delete books in the catalog, so that the platform inventory stays accurate and up-to-date.
- **Acceptance Criteria**:
  - [x] Administrator can create new book entries with validation.
  - [x] Administrator can edit existing book metadata.
  - [x] Administrator can delete obsolete book entries.
  - [x] Normal authenticated users and anonymous visitors cannot access `/admin/books`.
  - [x] Unauthorized access attempts return HTTP 403 Forbidden.
- **Status**: DONE (Verified by `test_authorization.py`).

#### OBRRP-14: Review Moderation
- **Epic**: EPIC-03
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As an administrator, I want to hide or restore abusive reviews with a mandatory reason, so that community safety and decency standards are maintained.
- **Acceptance Criteria**:
  - [x] Administrator can access the moderation queue at `/admin/moderation`.
  - [x] Administrator can hide reviews by providing a required moderation reason.
  - [x] Administrator can restore hidden reviews.
  - [x] Hidden reviews are immediately filtered out of the public book details page.
  - [x] Normal users cannot perform moderation actions.
  - [x] Moderation decisions are logged immutably in the audit log.
- **Status**: DONE (Verified by `test_authorization.py`, `test_integration_reviews.py`).

#### OBRRP-15: Secure Authorization & IDOR Protection
- **Epic**: EPIC-03
- **Story Points**: 8 SP
- **Priority**: Highest
- **Description**: As a security engineer, I want object-level authorization enforced on all mutable resources, so that horizontal privilege escalation (IDOR) attacks are completely blocked.
- **Acceptance Criteria**:
  - [x] User A can modify and delete only their own reviews and reading shelf items.
  - [x] User B's attempts to modify or delete User A's review return an authorization denial.
  - [x] Unauthorized mutation requests return appropriate denial and log a security event.
  - [x] Database records remain intact and unchanged after attack attempts.
  - [x] Authorization logic is enforced server-side inside `ReviewService` and cannot be bypassed client-side.
- **Status**: DONE (Verified by `test_authorization.py`, `test_idor_vulnerability_proof.py` on demo branch).

#### OBRRP-16: Audit Logging
- **Epic**: EPIC-03
- **Story Points**: 3 SP
- **Priority**: High
- **Description**: As a security auditor, I want a tamper-evident audit log of all security and administrative events, so that system activities are traceable and non-repudiable.
- **Acceptance Criteria**:
  - [x] Security-sensitive actions (login, logout, registration) are logged.
  - [x] Administrative catalog modifications and moderation actions are logged.
  - [x] Authorization failures and IDOR attempts are recorded with client IP and target ID.
  - [x] Passwords, secret keys, and session tokens are strictly scrubbed before logging.
- **Status**: DONE (Verified by `app/core/audit.py`, `test_authorization.py`).

---

### EPIC-04: Testing, DevSecOps & Deployment (18 SP)

#### OBRRP-17: Security & Authorization Testing
- **Epic**: EPIC-04
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As a QA/Security tester, I want automated test suites covering unit, integration, authorization, and fuzzing vectors, so that vulnerabilities are detected before release.
- **Acceptance Criteria**:
  - [x] Authentication unit and integration tests exist and pass.
  - [x] Authorization tests verifying RBAC and IDOR prevention exist and pass.
  - [x] Input validation and boundary fuzzing tests exist and pass.
  - [x] Static application security testing (Bandit) executes cleanly (0 High, 0 Medium).
  - [x] Real automated tests produce verifiable output logs in `evidence/`.
- **Status**: DONE (Verified by `pytest tests/ -v`, 23/23 tests passing).

#### OBRRP-18: CI/CD Pipeline
- **Epic**: EPIC-04
- **Story Points**: 5 SP
- **Priority**: High
- **Description**: As a DevSecOps engineer, I want a GitHub Actions pipeline running tests and SAST scans on every push, so that code quality and security policies are automatically enforced.
- **Acceptance Criteria**:
  - [x] Pipeline definition exists in `.github/workflows/ci.yml`.
  - [x] Pipeline installs pinned dependencies from `requirements.txt`.
  - [x] Pipeline executes all Pytest unit and integration tests.
  - [x] Pipeline runs Bandit SAST security analysis.
  - [x] Pipeline validates container Dockerfile and Kubernetes security contexts.
- **Status**: DONE (Verified by `.github/workflows/ci.yml`).

#### OBRRP-19: Docker & Local Kubernetes Deployment
- **Epic**: EPIC-04
- **Story Points**: 8 SP
- **Priority**: High
- **Description**: As a DevOps engineer, I want the platform containerized with non-root security and equipped with Kubernetes manifests, so that the application is production-deployable.
- **Acceptance Criteria**:
  - [x] Multi-stage `docker/Dockerfile` exists and builds cleanly.
  - [x] Container executes under dedicated unprivileged user (`UID 10001:10001`).
  - [x] Secrets are not hardcoded in Docker image layers.
  - [x] Container healthcheck probe `/health` returns HTTP 200 with database status.
  - [x] Kubernetes manifests (`namespace.yaml`, `deployment.yaml`) enforce `runAsNonRoot: true`, resource limits, and health probes.
- **Status**: DONE (Verified by `docker compose up -d`, `curl http://localhost:5050/health`).
