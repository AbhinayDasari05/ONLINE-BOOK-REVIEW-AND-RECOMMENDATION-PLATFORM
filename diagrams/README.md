# System Diagrams & Architecture Artifacts
**Course Code**: 20CYS401 — Secure Software Engineering  
**Project**: Online Book Review and Recommendation Platform

All diagrams in this directory are available in both raw Mermaid source format (`.mmd`) and high-resolution rendered graphic images (`.png`).

---

## Diagram Index

| # | Diagram Name | Source File | High-Res PNG | Phase Mapping |
|---|---|---|---|---|
| 01 | **UML Use Case Diagram** | [`01_use_case_diagram.mmd`](01_use_case_diagram.mmd) | [`01_use_case_diagram.png`](01_use_case_diagram.png) | Phase 3 (UML Use Cases) |
| 02 | **Entity-Relationship (ER) Diagram** | [`02_er_diagram.mmd`](02_er_diagram.mmd) | [`02_er_diagram.png`](02_er_diagram.png) | Phase 4 (Data Modeling) |
| 03 | **Data Flow Diagram (Level 0 - Context)** | [`03_dfd_level_0.mmd`](03_dfd_level_0.mmd) | [`03_dfd_level_0.png`](03_dfd_level_0.png) | Phase 4 (DFD Level 0) |
| 04 | **Data Flow Diagram (Level 1 - Process)** | [`04_dfd_level_1.mmd`](04_dfd_level_1.mmd) | [`04_dfd_level_1.png`](04_dfd_level_1.png) | Phase 4 (DFD Level 1) |
| 05 | **Trust Boundary Diagram** | [`05_trust_boundary_diagram.mmd`](05_trust_boundary_diagram.mmd) | [`05_trust_boundary_diagram.png`](05_trust_boundary_diagram.png) | Phase 4 (Trust Boundaries) |
| 06 | **Layered System Architecture** | [`06_system_architecture.mmd`](06_system_architecture.mmd) | [`06_system_architecture.png`](06_system_architecture.png) | Phase 5 (Architecture & Design) |
| 07 | **Attack Tree (ATK-01 Review Tampering)** | [`07_attack_tree_atk01.mmd`](07_attack_tree_atk01.mmd) | [`07_attack_tree_atk01.png`](07_attack_tree_atk01.png) | Phase 8 (Attack Tree Analysis) |
| 08 | **Deployment Architecture (Container & K8s)** | [`08_deployment_architecture.mmd`](08_deployment_architecture.mmd) | [`08_deployment_architecture.png`](08_deployment_architecture.png) | Phase 5 & 13 (Deployment) |

---

## Overview of Key Diagrams

### 1. UML Use Case Diagram (`01_use_case_diagram.png`)
Captures all functional use cases for **USER**, **ADMINISTRATOR**, and **Anonymous Visitor** actors across registration, search, rating/review submission, review editing/deletion (with IDOR prevention), and administrator catalog/moderation management.

### 2. Entity-Relationship Diagram (`02_er_diagram.png`)
Directly maps the SQLAlchemy ORM models:
- `USERS` (Authentication, bcrypt hashes, admin flag)
- `BOOKS` (Catalog metadata, ISBN unique constraint)
- `REVIEWS` (Composite foreign keys, rating constraint 1-5, moderation fields)
- `READING_LIST_ITEMS` (Shelf categories: want-to-read, reading, finished)
- `AUDIT_LOGS` (Immutable tamper-evident security audit trail)

### 3. Data Flow Diagrams (`03_dfd_level_0.png` & `04_dfd_level_1.png`)
Traces data flows across actors, processes (`P1` to `P7`), data stores (`D1` to `D5`), and the system trust boundary. Highlights where inputs are validated and scrubbed.

### 4. Trust Boundary Diagram (`05_trust_boundary_diagram.png`)
Illustrates the transition points from untrusted browser clients through security middleware (CSP, X-Frame-Options, CSRF validation) into authenticated application layers, RBAC decorators, and non-root persistence boundaries.

### 5. Layered System Architecture (`06_system_architecture.png`)
Detailed 4-layer architectural diagram: Presentation (Blueprints & Jinja2) → Security Cross-Cutting Tier → Service Layer (Business rules & IDOR verification) → Data Access & Persistence Tier (ORM & SQLite).

### 6. Attack Tree (`07_attack_tree_atk01.png`)
Mermaid AND/OR attack tree modeling how an adversary might attempt unauthorized modification of book reviews (ATK-01) across IDOR, CSRF, Credential Abuse, and SQLi, demonstrating the specific security controls that block each attack path.
