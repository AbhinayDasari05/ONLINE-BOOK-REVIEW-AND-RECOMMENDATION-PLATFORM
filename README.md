# Online Book Review and Recommendation Platform
**Course Code**: 20CYS401 — Secure Software Engineering  
**Degree**: B.Tech CSE — Cybersecurity  
**Problem Statement**: 5. Online Book Review and Recommendation Platform

---

## 1. Executive Summary

This project implements a secure, modular, containerized web platform enabling users to discover books, view ratings, write and manage reviews, and maintain private reading lists, while giving administrators tools to manage the catalog and moderate reviews.

### Key Capabilities:
- **Authentication & RBAC**: Bcrypt password hashing (rounds=12), HttpOnly cookie session management, server-side session invalidation, and role-based access control.
- **Review Integrity & IDOR Defense**: Strict server-side object-level ownership checks preventing unauthorized modification or deletion of reviews.
- **Defense in Depth**: Zero raw SQL queries (100% SQLAlchemy ORM), CSRF protection via synchronizer tokens, XSS defense via Jinja2 autoescaping, custom error handlers preventing information disclosure, and security headers (CSP, X-Frame-Options, nosniff).
- **Audit Logging**: Comprehensive, tamper-evident audit trail capturing sensitive authentication, catalog mutations, and moderation actions with credential scrubbing.
- **DevSecOps**: Multi-stage non-root Dockerfile, Kubernetes manifests with resource limits and health probes, and automated GitHub Actions CI/CD workflow.

---

## 2. Quick Start Guide (Local Execution)

### Prerequisites:
- Python 3.9+ (Tested on Python 3.14.8)
- Virtual environment (`venv`)

### 1. Set Up Environment & Run
```bash
# Navigate to project directory
cd /Users/abhinaydasari/Documents/sse/secure-book-review-platform

# Activate existing venv or create one
source venv/bin/activate

# Install dependencies (already pinned in requirements.txt)
pip install -r requirements.txt

# Seed the database with sample books and demo accounts (idempotent)
python scripts/seed.py

# Start the application
python wsgi.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 3. Demo Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `AdminPass123!` | Access `/admin/books`, `/admin/moderation`, view audit logs |
| **Regular User** | `alice` | `AlicePass123!` | Author reviews, manage private reading list |
| **Regular User (Attacker)** | `bob` | `BobPass123!` | Used in IDOR security demonstration tests |

---

## 4. Running Tests & Security Scans

### Execute Full Pytest Test Suite
```bash
./venv/bin/pytest -v
```
*Result: 23 passed across unit, integration, authorization, fuzzing, and e2e suites.*

### Run Bandit SAST Security Scan
```bash
./venv/bin/bandit -r app/ -f txt
```

### Reproduce Controlled IDOR Demonstration
```bash
# 1. Switch to vulnerable demo branch
git checkout demo/idor-before

# 2. Run exploit proof (PASSES, proving exploit works when check is missing)
./venv/bin/pytest tests/test_idor_vulnerability_proof.py -v

# 3. Return to main secure branch
git checkout main

# 4. Run authorization tests (PASSES, proving attack is strictly denied)
./venv/bin/pytest tests/test_authorization.py -v
```

---

## 5. Container & Kubernetes Deployment

### Docker Build & Run (Requires Docker Desktop Running)
```bash
docker build -f docker/Dockerfile -t secure-book-review-platform:latest .
docker run -p 5000:5000 secure-book-review-platform:latest
```

### Kubernetes Manifest Deployment
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
```

---

## 6. Project Structure

```
├── app/
│   ├── config.py             # Environment configurations
│   ├── extensions.py         # SQLAlchemy, LoginManager, CSRFProtect
│   ├── core/                 # Security decorators & audit logging
│   ├── models/               # User, Book, Review, ReadingListItem, AuditLog
│   ├── routes/               # Blueprints: auth, catalog, reviews, reading_list, admin, health
│   ├── services/             # Business logic & IDOR authorization rules
│   ├── static/css/           # Responsive CSS styles
│   └── templates/            # Jinja2 templates (6 connected screens + error pages)
├── docker/                   # Hardened multi-stage Dockerfile
├── docs/                     # Full 16-phase examination documentation
│   ├── phase-01-agile/       # Scrum + XP security practices, refactorings
│   ├── phase-02-requirements/# Complete SRS (REQ-01 to REQ-12)
│   ├── phase-03-uml/         # Mermaid use case diagrams and specifications
│   ├── phase-04-data-flow/   # ER diagram, Level 0/1 DFDs, Trust boundaries
│   ├── phase-05-architecture/# Layered architecture design
│   ├── phase-06-ui/          # 6 connected screens walkthrough
│   ├── phase-07-threat-model/# STRIDE threat analysis (10 assets, 10 threats)
│   ├── phase-08-attack-tree/ # ATK-01 Mermaid AND/OR tree
│   ├── phase-09-backlog/     # 10 user stories, Jira import CSV
│   ├── phase-10-sprint/      # Sprint metrics & burndown charts
│   ├── phase-12-secure-coding/# IDOR vulnerability before/after proof
│   ├── phase-15-monitoring/  # Audit logging & health probes
│   └── phase-16-hardening/   # Security hardening & controls verification
├── evidence/                 # Saved test execution and scan logs
├── k8s/                      # Namespace, ConfigMap, Secret, Deployment, Service
├── scripts/                  # Idempotent database seeder (seed.py)
├── tests/                    # Pytest test suite (23 tests)
└── wsgi.py                   # Application entrypoint
```
