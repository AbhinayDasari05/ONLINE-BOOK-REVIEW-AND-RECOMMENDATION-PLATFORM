# Phase 9: Product Backlog and User Stories
**Course Code**: 20CYS401 | **Project**: Online Book Review and Recommendation Platform

---

## 9.1 Product Backlog (10 User Stories across 2 Sprints)

| Story ID | User Story Title | As a / I want / So that | Priority | Story Points | Sprint | Status |
|---|---|---|---|---|---|---|
| US-01 | User Registration & Login | As a reader, I want to securely register and log in, so that my account and personal data remain protected. | High | 5 | Sprint 1 | DONE |
| US-02 | Book Discovery & Search | As a reader, I want to search books by title, author, and genre, so that I can quickly discover new reading material. | High | 5 | Sprint 1 | DONE |
| US-03 | Book Details & Ratings Display | As a reader, I want to view detailed book information and aggregated community ratings, so that I can decide whether to read it. | High | 3 | Sprint 1 | DONE |
| US-04 | Submit Rating & Review | As a reader, I want to rate (1-5 stars) and write a review for a book, so that I can share my opinion with others. | High | 5 | Sprint 1 | DONE |
| US-05 | Edit & Delete Own Reviews | As an author of a review, I want to modify or remove my review, while preventing other users from altering it. | Critical | 8 | Sprint 2 | DONE |
| US-06 | Personal Reading List Shelf | As a reader, I want to maintain a private reading list (want-to-read, reading, finished), so that I can track my personal progress. | Medium | 5 | Sprint 2 | DONE |
| US-07 | Admin Catalog Management | As an administrator, I want to add, edit, and delete books in the catalog, so that the collection stays accurate and up-to-date. | High | 5 | Sprint 2 | DONE |
| US-08 | Review Moderation | As an administrator, I want to moderate and hide inappropriate reviews with documented reasons, so that the platform stays safe. | High | 5 | Sprint 2 | DONE |
| US-09 | Security Audit Logging | As a security officer, I want all sensitive authentication and moderation events logged immutably, so that actions are traceable. | High | 5 | Sprint 2 | DONE |
| US-10 | Secure Containerization & Health Probes | As a DevSecOps engineer, I want the application packaged in a hardened Docker container with health probes, so that it runs securely. | Medium | 3 | Sprint 2 | DONE |

---

## 9.2 Acceptance Criteria per User Story

### US-05: Edit & Delete Own Reviews (Security Focus)
- **Given** an authenticated user who authored Review X,
- **When** the user sends a valid update or delete request for Review X,
- **Then** the system successfully applies the changes and updates the database.
- **Given** an authenticated user who did NOT author Review X (or an unauthenticated user),
- **When** the user attempts an update or delete request targeting Review X,
- **Then** the request is rejected with access denied, an audit event is logged, and the database record remains intact.
