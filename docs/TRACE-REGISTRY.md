# Traceability Registry — Single Source of Truth

**Project**: Online Book Review and Recommendation Platform  
**Course Code**: 20CYS401 — Secure Software Engineering  
**Degree / Branch**: B.Tech CSE — Cybersecurity  
**Document Status**: Baseline Created (Stage 0)  

---

## 1. Requirements (REQ)
| ID | Title / Summary | CIA Category | Target Component |
|---|---|---|---|
| REQ-01 | User Registration & Login with Unique Username/Email & Strict Validation | C, I | COMP-01, COMP-02 |
| REQ-02 | Secure Server-Side Authentication & Session Management (Bcrypt, HttpOnly, Expiry) | C, I | COMP-01 |
| REQ-03 | Parameterized Book Search by Title, Author, Genre | I, A | COMP-04 |
| REQ-04 | View Book Details with Aggregated Rating & Moderated Reviews | I, A | COMP-03, COMP-05 |
| REQ-05 | Submit Book Rating (Integer 1–5, 1 per user per book) | I | COMP-05 |
| REQ-06 | Write Review with Strict Validation & Safe Output Encoding | I | COMP-05 |
| REQ-07 | Edit Own Review (Enforced Server-Side Object-Level Authorization) | I | COMP-05 |
| REQ-08 | Delete Own Review (Enforced Server-Side Object-Level Authorization) | I | COMP-05 |
| REQ-09 | Maintain Private Reading List with Status (want-to-read, reading, finished) | C, I | COMP-06 |
| REQ-10 | Administrator Book Management (Create, Update, Delete) | I, A | COMP-03, COMP-07 |
| REQ-11 | Administrator Review Moderation (Hide/Remove with Audit Reason) | I | COMP-05, COMP-07, COMP-08 |
| REQ-12 | Secure Logout with Complete Server-Side Session Invalidation | C, I | COMP-01 |

---

## 2. Use Cases (UC)
| ID | Title | Primary Actor | Traces To |
|---|---|---|---|
| UC-01 | Register & Authenticate User | User | REQ-01, REQ-02, REQ-12 |
| UC-02 | Discover & Search Books | User, Admin | REQ-03 |
| UC-03 | View Book Details & Ratings | User, Admin | REQ-04 |
| UC-04 | Submit Rating & Review | User | REQ-05, REQ-06 |
| UC-05 | Edit/Delete Own Review | User | REQ-07, REQ-08 |
| UC-06 | Maintain Personal Reading List | User | REQ-09 |
| UC-07 | Administrator Manage Book Catalog | Administrator | REQ-10 |
| UC-08 | Administrator Moderate Inappropriate Reviews | Administrator | REQ-11 |
| UC-09 | Inspect System Audit Logs | Administrator | REQ-11, COMP-08 |

---

## 3. Architecture Components (COMP)
| ID | Name | Subsystem / Layer | Source Location |
|---|---|---|---|
| COMP-01 | Authentication Subsystem | Auth / Controller | `app/auth/` |
| COMP-02 | User Management Subsystem | Service / Repository | `app/services/user_service.py` |
| COMP-03 | Book Catalog Subsystem | Catalog / Repository | `app/catalog/` |
| COMP-04 | Search Subsystem | Search Service | `app/services/search_service.py` |
| COMP-05 | Review & Rating Service | Review Service | `app/reviews/` |
| COMP-06 | Reading List Subsystem | Reading List Service | `app/reading_list/` |
| COMP-07 | Admin & Moderation Subsystem | Admin Controller | `app/admin/` |
| COMP-08 | Security Audit Logging Subsystem | Cross-cutting Core | `app/core/audit.py` |

---

## 4. DFD Processes (DFD-P) & Data Stores (DATA)
| ID | Name | Boundary / Type |
|---|---|---|
| DFD-P01 | Authenticate & Manage Session | Trust Boundary Ingress |
| DFD-P02 | Search Book Catalog | Application Core |
| DFD-P03 | Retrieve Book Details & Aggregates | Application Core |
| DFD-P04 | Submit / Edit / Delete Review & Rating | Object Authorization Boundary |
| DFD-P05 | Manage Private Reading List | Authorization Boundary |
| DFD-P06 | Moderate Content & Manage Catalog | Admin Boundary |
| DFD-P07 | Record Security Audit Event | Secure Core |
| DATA-01 | D01: User Credential & Profile Store | Internal Data Store |
| DATA-02 | D02: Book Catalog Store | Internal Data Store |
| DATA-03 | D03: Review & Rating Store | Internal Data Store |
| DATA-04 | D04: Reading List Store | Internal Data Store |
| DATA-05 | D05: Tamper-Evident Audit Log Store | Internal Data Store |

---

## 5. Assets (ASSET)
| ID | Asset Description | Sensitivity | Traces To |
|---|---|---|---|
| ASSET-01 | User Authentication Credentials (Hashes, Salts) | High (Confidentiality) | DATA-01 |
| ASSET-02 | User Profile & Email Information | Medium (Privacy) | DATA-01 |
| ASSET-03 | Book Catalog Records | Medium (Integrity) | DATA-02 |
| ASSET-04 | User Review Content | Medium (Integrity) | DATA-03 |
| ASSET-05 | Book Rating Values (1–5) | Medium (Integrity) | DATA-03 |
| ASSET-06 | Personal Reading Lists | Medium (Privacy) | DATA-04 |
| ASSET-07 | Administrator Privilege Flags & Tokens | Critical (Integrity) | COMP-01, COMP-07 |
| ASSET-08 | Security Audit Trail & Event Logs | Critical (Non-repudiation) | DATA-05 |
| ASSET-09 | Server-Side Session Identifiers & Cookies | High (Confidentiality) | COMP-01 |
| ASSET-10 | Primary Application SQLite Database File | Critical (All) | DATA-01..05 |

---

## 6. Threats (THR) & Attack Nodes (ATK)
| ID | Threat Title | STRIDE Category | Traces To |
|---|---|---|---|
| THR-01 | Credential Stuffing & Brute Force on Login | Spoofing | COMP-01, ASSET-01 |
| THR-02 | Unauthorized Review Alteration / Deletion (IDOR) | Tampering | COMP-05, ASSET-04 |
| THR-03 | Review Reputation Manipulation via Multiple Ratings | Tampering | COMP-05, ASSET-05 |
| THR-04 | Cross-Site Scripting (XSS) in Review Body | Tampering | COMP-05, ASSET-04 |
| THR-05 | SQL Injection in Search Parameters | Information Disclosure | COMP-04, DATA-02 |
| THR-06 | Session Hijacking via Insecure Cookie Flags | Spoofing | COMP-01, ASSET-09 |
| THR-07 | Cross-Site Request Forgery (CSRF) on Review Delete | Tampering | COMP-05, REQ-08 |
| THR-08 | Privilege Escalation to Admin Routes | Elevation of Privilege | COMP-07, ASSET-07 |
| THR-09 | Denial of Service via Massive Review Payload | Denial of Service | COMP-05, REQ-06 |
| THR-10 | Repudiation of Admin Moderation Action | Repudiation | COMP-07, ASSET-08 |
| ATK-01 | Modify or Delete Another User's Review Without Authorization | Root Goal | THR-02, REQ-07, REQ-08 |

---

## 7. Vulnerabilities (VUL) & Defects (DEF)
| ID | Vulnerability / Defect Title | Source Type | Mitigated By |
|---|---|---|---|
| VUL-01 | Insecure Direct Object Reference (IDOR) on Review Mutation | Controlled Demo & Fix | CTRL-02, REQ-07 |
| VUL-02 | Cross-Site Scripting (XSS) via Unsanitized Review Content | Controlled Demo & Fix | CTRL-04, REQ-06 |
| VUL-03 | Missing CSRF Token on State-Changing Review Endpoints | Security Scan / Fix | CTRL-03, REQ-08 |
| VUL-04 | Information Exposure via Verbose Stack Traces in 500 Responses | Tool Scan / Hardening | CTRL-07, REQ-02 |
| VUL-05 | Insecure Cookie Missing HttpOnly and SameSite Attributes | Security Finding | CTRL-01, REQ-02 |
| VUL-06 | SQL Injection Risk from Dynamic Query Concatenation | Tool Finding / Fix | CTRL-05, REQ-03 |
| DEF-01 | Review Ownership Bypass on Direct HTTP POST to Edit Route | Development Defect | CTRL-02, TEST-05 |

---

## 8. User Stories (US), Sprints & Tasks (TASK)
| ID | User Story Title | Sprint | Task IDs |
|---|---|---|---|
| US-01 | User Registration and Secure Login | SPRINT-01 | TASK-01, TASK-02 |
| US-02 | Book Catalog Browsing & Search | SPRINT-01 | TASK-03, TASK-04 |
| US-03 | Book Details and Rating Aggregation | SPRINT-01 | TASK-05 |
| US-04 | User Rating Submission | SPRINT-02 | TASK-06 |
| US-05 | User Review Creation | SPRINT-02 | TASK-07 |
| US-06 | User Edit Own Review | SPRINT-02 | TASK-08 |
| US-07 | User Delete Own Review | SPRINT-02 | TASK-09 |
| US-08 | Private Reading List Management | SPRINT-02 | TASK-10 |
| US-09 | Administrator Book CRUD Operations | SPRINT-02 | TASK-11 |
| US-10 | Administrator Review Moderation & Audit | SPRINT-02 | TASK-12, TASK-13 |

---

## 9. Security Controls (CTRL) & Deployment Controls (DEP)
| ID | Control Name | Type | Description |
|---|---|---|---|
| CTRL-01 | Secure Session & Cookie Configuration | Preventive | HttpOnly, SameSite=Lax, Expire, Server Invalidation |
| CTRL-02 | Server-Side Object-Level Authorization | Preventive | Review owner check prior to edit/delete (`review.user_id == current_user.id`) |
| CTRL-03 | CSRF Protection on All Mutation Forms | Preventive | Anti-CSRF token verification on all POST/PUT/DELETE forms |
| CTRL-04 | Strict Input Validation & Context-Aware Escaping | Preventive | Length bounds, whitelist rating (1–5), Jinja autoescaping |
| CTRL-05 | Parameterized ORM Queries | Preventive | SQLAlchemy ORM parameterized statements, no string interpolation |
| CTRL-06 | Role-Based Access Control (RBAC) | Preventive | `@admin_required` decorator verifying `is_admin` boolean |
| CTRL-07 | Hardened Error Handling | Preventive | Custom 400/403/404/500 handlers without stack traces |
| CTRL-08 | Security Audit Logging | Detective | Structured audit logs for auth failures, review changes, admin actions |
| CTRL-09 | Security HTTP Response Headers | Preventive | CSP, X-Frame-Options, X-Content-Type-Options |
| DEP-01 | Docker Non-Root User | Deployment | Container runs as non-privileged user `appuser` (UID 10001) |
| DEP-02 | Minimal Container Base Image | Deployment | `python:3.11-slim` image with build tools discarded |
| DEP-03 | Container Healthcheck Probe | Operational | HEALTHCHECK instruction verifying `/health` endpoint |
| DEP-04 | Kubernetes Resource Quotas & Limits | Deployment | Pod CPU/Memory requests and limits enforced |
| DEP-05 | Kubernetes Security Context & Non-Root | Deployment | `runAsNonRoot: true`, `allowPrivilegeEscalation: false` |
| DEP-06 | Kubernetes Secret Decoupling | Deployment | Application secrets injected via Kubernetes Secret manifest |

---

## 10. Tests (TEST)
| ID | Title / Purpose | Category | Target |
|---|---|---|---|
| TEST-01 | Password Hashing & Argon2/Bcrypt Verification | Unit | COMP-01 |
| TEST-02 | Book Rating Input Validation (1–5, Types) | Unit | COMP-05 |
| TEST-03 | Search Parameter Sanitization & ORM Querying | Unit | COMP-04 |
| TEST-04 | Complete User Login & Session Verification | Integration | COMP-01 |
| TEST-05 | Review Ownership Authorization (User B cannot edit User A) | Authorization | COMP-05 |
| TEST-06 | Review Ownership Authorization (User B cannot delete User A) | Authorization | COMP-05 |
| TEST-07 | RBAC Enforcement (Normal User Rejected on Admin Routes) | Authorization | COMP-07 |
| TEST-08 | Anonymous User Redirected from Protected Routes | Authorization | COMP-01, COMP-05 |
| TEST-09 | Full Review Lifecycle Integration (Create -> DB -> Retrieve) | Integration | COMP-05 |
| TEST-10 | End-to-End User Journey (Register -> Search -> Rate -> Review -> List) | System / E2E | COMP-01..06 |
| TEST-11 | Input Validation Boundary & Payload Fuzzing | Security / Fuzz | COMP-04, COMP-05 |
| TEST-12 | Controlled IDOR Vulnerability Demonstration Test | Security Demo | VUL-01, CTRL-02 |
