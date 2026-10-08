# Phase 10: Sprint Retrospective Evidence
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform  

---

## 1. Sprint 1 Retrospective (Core Platform)

### What Went Well:
- **Layered Service Architecture**: Separating business logic into `UserService`, `BookService`, and `ReviewService` enabled clean, isolated testing without relying on HTTP contexts.
- **SQLAlchemy Parameterization**: Prevented SQL injection vulnerabilities from Day 1 across all search and detail queries.
- **Strict Password Security**: Bcrypt with work factor 12 was implemented and verified early in the sprint.

### What Did Not Go Well:
- **Database Path Resolution (DEF-01)**: Using relative paths for the SQLite database caused file locking and lookup issues during testing; required switching to absolute paths in `Config`.
- **Foreign Key Ambiguity (DEF-02)**: Having dual relationships between `User` and `Review` (`user_id` and `moderated_by`) caused SQLAlchemy mapping warnings until explicitly disambiguated.

### Concrete Improvement Actions (Sprint 1):
1. **Improve test coverage before moving stories to TESTING**: Mandate that authorization test files (`test_authorization.py`) must be executed and passing before advancing issues out of IN PROGRESS.
2. **Move security verification earlier in the implementation workflow**: Perform threat modeling and define object-level ownership checks during story design rather than retrofitting after UI creation.

---

## 2. Sprint 2 Retrospective (Security & DevSecOps)

### What Went Well:
- **Isolated IDOR Demonstration**: Using a dedicated Git branch (`demo/idor-before`) allowed us to prove the vulnerability without compromising the security of the `main` branch.
- **Automated Verification**: Running automated Pytest suites and Bandit SAST scans as part of the Definition of Done gave high confidence in release security.
- **Container Hardening**: Multi-stage build achieved a compact, secure image running as unprivileged user `UID 10001:10001`.

### What Did Not Go Well:
- **Port Conflict on macOS (DEF-04)**: Port 5000 collided with the native macOS AirPlay Receiver (`ControlCenter`), producing an empty white page; resolved by rebinding to port 5050 in `docker-compose.yml`.
- **Initial Unseeded Container Volume (DEF-05)**: The fresh Docker volume needed manual execution of `seed.py` inside the container to populate catalog items.

### Concrete Improvement Actions (Sprint 2):
1. **Integrate automated DB migration/seeding in Docker entrypoint**: Ensure container startup automatically runs an idempotent database seed check if the database is unpopulated.
2. **Standardize non-standard ports across all development manifests**: Use port 5050 across local configs, Docker compose, and Kubernetes development overlays to avoid macOS system port conflicts.
